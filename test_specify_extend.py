#!/usr/bin/env python3
"""
Tests for specify_extend.py

Tests the core functionality of downloading and installing spec-kit-extensions.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import subprocess
import sys

# Add the current directory to path so we can import specify_extend
sys.path.insert(0, str(Path(__file__).parent))

import specify_extend


def test_download_latest_template_tag():
    """Test that download_latest_release fetches the latest templates-v* tag"""

    # Mock response data from GitHub API
    mock_tags_response = [
        {"name": "templates-v2.4.1", "zipball_url": "https://api.github.com/repos/pradeepmouli/spec-kit-extensions/zipball/templates-v2.4.1"},
        {"name": "templates-v2.4.0", "zipball_url": "https://api.github.com/repos/pradeepmouli/spec-kit-extensions/zipball/templates-v2.4.0"},
        {"name": "v1.3.8", "zipball_url": "https://api.github.com/repos/pradeepmouli/spec-kit-extensions/zipball/v1.3.8"},
        {"name": "templates-v2.3.1", "zipball_url": "https://api.github.com/repos/pradeepmouli/spec-kit-extensions/zipball/templates-v2.3.1"},
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        with patch.object(specify_extend.client, 'get') as mock_get:
            # Mock the tags API call
            mock_tags_resp = Mock()
            mock_tags_resp.status_code = 200
            mock_tags_resp.json.return_value = mock_tags_response

            # Mock the zipball download call
            mock_zip_resp = Mock()
            mock_zip_resp.status_code = 200
            mock_zip_resp.content = b"PK\x03\x04"  # Minimal ZIP file header

            # Configure mock to return different responses based on URL
            def get_side_effect(url, **kwargs):
                if "tags" in url:
                    return mock_tags_resp
                elif "archive" in url:
                    # Verify the correct tag is being used in the URL
                    assert "templates-v2.4.1" in url, f"Expected templates-v2.4.1 in URL, got: {url}"
                    return mock_zip_resp
                return Mock(status_code=404)

            mock_get.side_effect = get_side_effect

            # Call the function
            result = specify_extend.download_latest_release(temp_path)

            # Verify the correct API calls were made
            calls = mock_get.call_args_list

            # First call should be to /tags endpoint
            assert "tags" in calls[0][0][0], f"First call should be to /tags, got: {calls[0][0][0]}"

            # Second call should be to download the zipball with templates-v2.4.1
            assert "templates-v2.4.1" in calls[1][0][0], f"Second call should include templates-v2.4.1, got: {calls[1][0][0]}"

            print("✓ Test passed: download_latest_release correctly fetches templates-v2.4.1")


def test_filters_template_tags_only():
    """Test that only templates-v* tags are considered"""

    mock_tags_response = [
        {"name": "v1.5.0", "zipball_url": "..."},
        {"name": "cli-v1.4.0", "zipball_url": "..."},
        {"name": "templates-v2.4.1", "zipball_url": "..."},
        {"name": "v1.3.8", "zipball_url": "..."},
        {"name": "templates-v2.4.0", "zipball_url": "..."},
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        with patch.object(specify_extend.client, 'get') as mock_get:
            mock_tags_resp = Mock()
            mock_tags_resp.status_code = 200
            mock_tags_resp.json.return_value = mock_tags_response

            mock_zip_resp = Mock()
            mock_zip_resp.status_code = 200
            mock_zip_resp.content = b"PK\x03\x04"

            def get_side_effect(url, **kwargs):
                if "tags" in url:
                    return mock_tags_resp
                elif "archive" in url:
                    # Should only download templates-v tags, not v* or cli-v* tags
                    assert "templates-v" in url, f"Should only download templates-v tags, got: {url}"
                    assert "templates-v2.4.1" in url, f"Should download latest templates-v2.4.1, got: {url}"
                    return mock_zip_resp
                return Mock(status_code=404)

            mock_get.side_effect = get_side_effect

            result = specify_extend.download_latest_release(temp_path)

            print("✓ Test passed: Only templates-v* tags are considered")


def test_no_template_tags_found():
    """Test behavior when no templates-v* tags exist"""

    mock_tags_response = [
        {"name": "v1.5.0", "zipball_url": "..."},
        {"name": "v1.3.8", "zipball_url": "..."},
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        with patch.object(specify_extend.client, 'get') as mock_get:
            mock_tags_resp = Mock()
            mock_tags_resp.status_code = 200
            mock_tags_resp.json.return_value = mock_tags_response
            mock_get.return_value = mock_tags_resp

            # Should return None when no template tags found
            result = specify_extend.download_latest_release(temp_path)

            assert result is None, "Should return None when no template tags found"

            print("✓ Test passed: Returns None when no template tags found")


def test_get_repo_root_windows_git_bash_path():
    """Test that Windows Git Bash paths are correctly converted"""
    
    with patch('subprocess.run') as mock_run:
        # Mock git command returning a Git Bash path
        mock_result = Mock()
        mock_result.stdout = "/c/Users/test/project"
        mock_run.return_value = mock_result
        
        with patch('sys.platform', 'win32'):
            result = specify_extend.get_repo_root()
            
            # Should convert /c/Users/test/project to C:/Users/test/project
            assert str(result) == "C:/Users/test/project", f"Expected C:/Users/test/project, got {result}"
            
            print("✓ Test passed: Windows Git Bash path converted correctly")


def test_get_repo_root_windows_drive_root():
    """Test that Windows Git Bash drive root paths are correctly converted"""
    
    with patch('subprocess.run') as mock_run:
        # Mock git command returning a Git Bash drive root path
        mock_result = Mock()
        mock_result.stdout = "/d"
        mock_run.return_value = mock_result
        
        with patch('sys.platform', 'win32'):
            result = specify_extend.get_repo_root()
            
            # Should convert /d to D:/ (Path normalizes to D:)
            # Path() on Windows normalizes D:/ to D:
            assert str(result) in ["D:/", "D:"], f"Expected D:/ or D:, got {result}"
            
            print("✓ Test passed: Windows Git Bash drive root converted correctly")


def test_get_repo_root_unix_no_conversion():
    """Test that Unix paths are not modified on non-Windows platforms"""
    
    with patch('subprocess.run') as mock_run:
        # Mock git command returning a Unix path
        mock_result = Mock()
        mock_result.stdout = "/home/user/project"
        mock_run.return_value = mock_result
        
        with patch('sys.platform', 'linux'):
            result = specify_extend.get_repo_root()
            
            # Should remain unchanged on Linux
            assert str(result) == "/home/user/project", f"Expected /home/user/project, got {result}"
            
            print("✓ Test passed: Unix paths unchanged on non-Windows platforms")


def test_get_repo_root_windows_native_path():
    """Test that native Windows paths are left unchanged"""
    
    with patch('subprocess.run') as mock_run:
        # Mock git command returning a native Windows path
        mock_result = Mock()
        mock_result.stdout = "C:/Users/test/project"
        mock_run.return_value = mock_result
        
        with patch('sys.platform', 'win32'):
            result = specify_extend.get_repo_root()
            
            # Should remain unchanged
            assert str(result) == "C:/Users/test/project", f"Expected C:/Users/test/project, got {result}"
            
            print("✓ Test passed: Native Windows paths unchanged")


def test_get_repo_root_windows_native_path_with_backslashes():
    """Test that native Windows paths with backslashes are normalized to use forward slashes"""
    
    with patch('subprocess.run') as mock_run:
        # Mock git command returning a native Windows path with backslashes
        mock_result = Mock()
        mock_result.stdout = "C:\\Users\\test\\project"
        mock_run.return_value = mock_result
        
        with patch('sys.platform', 'win32'):
            result = specify_extend.get_repo_root()
            
            # Should normalize backslashes and remain as C:/Users/test/project
            assert str(result) == "C:/Users/test/project", f"Expected C:/Users/test/project, got {result}"
            
            print("✓ Test passed: Native Windows paths with backslashes normalized")


def test_get_repo_root_error_handling():
    """Test that get_repo_root falls back to cwd on error"""
    
    with patch('subprocess.run') as mock_run:
        # Mock git command failing
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git')
        
        result = specify_extend.get_repo_root()
        
        # Should fall back to current working directory
        assert result == Path.cwd(), f"Expected current directory, got {result}"
        
        print("✓ Test passed: Falls back to cwd on git error")


def test_get_repo_root_multiple_drive_letters():
    """Test conversion works for different drive letters"""
    
    drive_letters = ['a', 'b', 'c', 'd', 'e', 'z']
    
    for drive in drive_letters:
        with patch('subprocess.run') as mock_run:
            # Mock git command returning a Git Bash path with different drive letters
            mock_result = Mock()
            mock_result.stdout = f"/{drive}/test/path"
            mock_run.return_value = mock_result
            
            with patch('sys.platform', 'win32'):
                result = specify_extend.get_repo_root()
                expected = f"{drive.upper()}:/test/path"
                
                assert str(result) == expected, f"Expected {expected}, got {result}"
    
    print("✓ Test passed: All drive letters convert correctly")


def test_parse_workflow_package_selection_recommended():
    """Test recommended workflow package selection"""

    result = specify_extend.parse_workflow_package_selection("recommended")

    assert result == specify_extend.RECOMMENDED_WORKFLOW_PACKAGES, (
        f"Expected {specify_extend.RECOMMENDED_WORKFLOW_PACKAGES}, got {result}"
    )

    print("✓ Test passed: recommended workflow package selection")


def test_parse_workflow_package_selection_csv():
    """Test comma-separated workflow package selection"""

    result = specify_extend.parse_workflow_package_selection("bugfix-lifecycle,refactor-lifecycle")

    assert result == ["bugfix-lifecycle", "refactor-lifecycle"], (
        f"Expected selected workflow keys, got {result}"
    )

    print("✓ Test passed: comma-separated workflow package selection")


def test_parse_workflow_package_selection_all_includes_new_lifecycle_workflows():
    """Test all workflow package selection includes enhance and hotfix lifecycle workflows"""

    result = specify_extend.parse_workflow_package_selection("all")

    assert "enhance-lifecycle" in result, f"Expected enhance-lifecycle in {result}"
    assert "hotfix-lifecycle" in result, f"Expected hotfix-lifecycle in {result}"

    print("✓ Test passed: all workflow package selection includes enhance and hotfix")


def test_parse_workflow_package_selection_invalid():
    """Test invalid workflow package selection raises ValueError"""

    try:
        specify_extend.parse_workflow_package_selection("not-a-workflow")
        raise AssertionError("Expected ValueError for invalid workflow key")
    except ValueError as exc:
        assert "Invalid workflow package key(s)" in str(exc), (
            f"Unexpected error message: {exc}"
        )

    print("✓ Test passed: invalid workflow package selection rejected")


def test_install_workflow_packages_invokes_specify_workflow_add():
    """Test workflow package installation uses native specify workflow add"""

    repo_root = Path("/tmp/spec-kit-extensions-test")

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = Mock(returncode=0)

        specify_extend.install_workflow_packages(
            repo_root,
            ["bugfix-lifecycle", "refactor-lifecycle"],
            dry_run=False,
        )

        assert mock_run.call_count == 2, f"Expected 2 install calls, got {mock_run.call_count}"

        first_call = mock_run.call_args_list[0]
        second_call = mock_run.call_args_list[1]

        assert first_call.args[0][:3] == ["specify", "workflow", "add"], (
            f"Unexpected first command: {first_call.args[0]}"
        )
        assert second_call.args[0][:3] == ["specify", "workflow", "add"], (
            f"Unexpected second command: {second_call.args[0]}"
        )
        assert "bugfix-lifecycle" in first_call.args[0][3], (
            f"Expected bugfix workflow URL, got {first_call.args[0][3]}"
        )
        assert "refactor-lifecycle" in second_call.args[0][3], (
            f"Expected refactor workflow URL, got {second_call.args[0][3]}"
        )
        assert first_call.kwargs["cwd"] == str(repo_root), "Expected repo_root as cwd string"
        assert second_call.kwargs["cwd"] == str(repo_root), "Expected repo_root as cwd string"

    print("✓ Test passed: workflow packages installed via specify workflow add")


def test_install_workflow_packages_uses_local_workflow_source_when_provided():
    """Test workflow package installation can use local workflow.yml files."""

    repo_root = Path("/tmp/spec-kit-extensions-test")

    with tempfile.TemporaryDirectory() as temp_dir:
        source_root = Path(temp_dir)
        workflow_file = source_root / "workflows" / "enhance-lifecycle" / "workflow.yml"
        workflow_file.parent.mkdir(parents=True, exist_ok=True)
        workflow_file.write_text("schema_version: '1.0'\n")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = Mock(returncode=0)

            specify_extend.install_workflow_packages(
                repo_root,
                ["enhance-lifecycle"],
                dry_run=False,
                workflow_source_root=source_root,
            )

            assert mock_run.call_count == 1, f"Expected 1 install call, got {mock_run.call_count}"
            first_call = mock_run.call_args_list[0]
            assert first_call.args[0][:3] == ["specify", "workflow", "add"], (
                f"Unexpected command: {first_call.args[0]}"
            )
            assert first_call.args[0][3] == str(workflow_file), (
                f"Expected local workflow file, got {first_call.args[0][3]}"
            )

    print("✓ Test passed: local workflow package source is used when provided")


def test_build_integration_install_command():
    """Test upstream integration install command construction."""

    result = specify_extend.build_integration_install_command("copilot")
    assert result == ["specify", "integration", "install", "copilot"], result

    dry_run_result = specify_extend.build_integration_install_command("claude", dry_run=True)
    assert dry_run_result == ["specify", "integration", "install", "claude", "--dry-run"], dry_run_result

    print("✓ Test passed: integration install command built correctly")


def test_should_reconcile_integrations_only_for_explicit_agent_selection():
    """Test integration reconciliation is only enabled for explicit --ai/--agents usage."""

    assert specify_extend.should_reconcile_integrations(None, None) is False
    assert specify_extend.should_reconcile_integrations("claude", None) is True
    assert specify_extend.should_reconcile_integrations(None, "claude,copilot") is True

    print("✓ Test passed: integration reconciliation gating matches explicit agent selection")


def test_install_agent_integrations_invokes_specify_integration_install():
    """Test upstream integration reconciliation uses specify integration install."""

    repo_root = Path("/tmp/spec-kit-extensions-test")

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = Mock(returncode=0)

        specify_extend.install_agent_integrations(
            repo_root,
            ["claude", "copilot"],
            dry_run=False,
        )

        assert mock_run.call_count == 2, f"Expected 2 install calls, got {mock_run.call_count}"

        first_call = mock_run.call_args_list[0]
        second_call = mock_run.call_args_list[1]

        assert first_call.args[0] == ["specify", "integration", "install", "claude"], first_call.args[0]
        assert second_call.args[0] == ["specify", "integration", "install", "copilot"], second_call.args[0]
        assert first_call.kwargs["cwd"] == str(repo_root), "Expected repo_root as cwd string"
        assert second_call.kwargs["cwd"] == str(repo_root), "Expected repo_root as cwd string"

    print("✓ Test passed: agent integrations installed via specify integration install")


def test_install_agent_integrations_dry_run_skips_subprocess():
    """Test dry run integration reconciliation does not invoke subprocess."""

    repo_root = Path("/tmp/spec-kit-extensions-test")

    with patch("subprocess.run") as mock_run:
        specify_extend.install_agent_integrations(
            repo_root,
            ["claude", "copilot"],
            dry_run=True,
        )

        mock_run.assert_not_called()

    print("✓ Test passed: dry run skips integration install subprocess")


def test_stage_local_extension_source_excludes_generated_state():
    """Test local dev staging excludes recursive generated state such as .specify."""

    with tempfile.TemporaryDirectory() as temp_dir:
        source_root = Path(temp_dir) / "extension-source"
        source_root.mkdir()
        (source_root / "extension.yml").write_text("name: workflows\n")
        (source_root / "README.md").write_text("hello\n")
        generated = source_root / ".specify" / "extensions" / "workflows"
        generated.mkdir(parents=True)
        (generated / "extension.yml").write_text("name: nested\n")

        staged_temp, staged_root = specify_extend.stage_local_extension_source(source_root)
        try:
            assert (staged_root / "extension.yml").exists(), "Expected extension.yml in staged source"
            assert (staged_root / "README.md").exists(), "Expected README.md in staged source"
            assert not (staged_root / ".specify").exists(), "Did not expect .specify in staged source"
        finally:
            staged_temp.cleanup()

    print("✓ Test passed: local dev staging excludes generated state")


def test_is_workflows_extension_installed_detects_existing_install():
    """Test detection of an already-installed workflows extension."""

    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = Path(temp_dir)
        assert specify_extend.is_workflows_extension_installed(repo_root) is False

        extension_file = repo_root / ".specify" / "extensions" / "workflows" / "extension.yml"
        extension_file.parent.mkdir(parents=True, exist_ok=True)
        extension_file.write_text('id: "workflows"\n')

        assert specify_extend.is_workflows_extension_installed(repo_root) is True

    print("✓ Test passed: existing workflows install is detected")


def test_install_extension_bundle_compat_copies_current_bundle_layout():
    """Test compatibility install copies the bundled extension layout into .specify/extensions/workflows."""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        repo_root = temp_root / "repo"
        source_root = temp_root / "source"
        repo_root.mkdir()
        source_root.mkdir()

        (source_root / "extension.yml").write_text('id: "workflows"\n')
        (source_root / "commands").mkdir()
        (source_root / "commands" / "bugfix.md").write_text("bugfix\n")
        (source_root / "config").mkdir()
        (source_root / "config" / "workflows-config.template.yml").write_text("config\n")
        (source_root / "scripts").mkdir()
        (source_root / "scripts" / "bash").mkdir()
        (source_root / "scripts" / "bash" / "create-bugfix.sh").write_text("#!/bin/bash\n")
        (source_root / "templates").mkdir()
        (source_root / "templates" / "bugfix").mkdir()
        (source_root / "templates" / "bugfix" / "README.md").write_text("template\n")

        specify_extend.install_extension_bundle_compat(
            repo_root,
            source_root,
            {"bugfix", "review"},
            dry_run=False,
        )

        destination_root = repo_root / ".specify" / "extensions" / "workflows"
        assert (destination_root / "extension.yml").exists()
        assert (destination_root / "commands" / "bugfix.md").exists()
        assert (destination_root / "config" / "workflows-config.template.yml").exists()
        assert (destination_root / "scripts" / "bash" / "create-bugfix.sh").exists()
        assert (destination_root / "templates" / "bugfix" / "README.md").exists()

        enabled_conf = repo_root / ".specify" / "extensions" / "enabled.conf"
        enabled_text = enabled_conf.read_text()
        assert "bugfix" in enabled_text
        assert "review" in enabled_text

    print("✓ Test passed: compatibility bundle installer copies current layout")


def test_patch_common_sh_wraps_upstream_function_instead_of_replacing_it():
    """Test common.sh patching preserves the upstream function and delegates to it."""

    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = Path(temp_dir)
        common_sh = repo_root / ".specify" / "scripts" / "bash" / "common.sh"
        common_sh.parent.mkdir(parents=True, exist_ok=True)
        common_sh.write_text(
            """#!/bin/bash
check_feature_branch() {
    local branch=\"$1\"
    local has_git_repo=\"$2\" 
    if [[ \"$has_git_repo\" != \"true\" ]]; then
        return 0
    fi
    if [[ ! \"$branch\" =~ ^[0-9]{3}- ]]; then
        return 1
    fi
    return 0
}
"""
        )

        specify_extend.patch_common_sh(repo_root, dry_run=False)

        patched = common_sh.read_text()
        assert "check_feature_branch_old()" in patched, "Expected upstream function to be renamed"
        assert 'check_feature_branch_old "$branch" "$has_git_repo"' in patched, (
            "Expected wrapper to delegate back to upstream logic"
        )
        assert "# Extended branch validation supporting spec-kit-extensions" in patched

    print("✓ Test passed: common.sh patch wraps upstream logic instead of replacing it")


if __name__ == "__main__":
    print("Running specify_extend tests...\n")

    try:
        test_download_latest_template_tag()
        test_filters_template_tags_only()
        test_no_template_tags_found()
        test_get_repo_root_windows_git_bash_path()
        test_get_repo_root_windows_drive_root()
        test_get_repo_root_unix_no_conversion()
        test_get_repo_root_windows_native_path()
        test_get_repo_root_windows_native_path_with_backslashes()
        test_get_repo_root_error_handling()
        test_get_repo_root_multiple_drive_letters()
        test_parse_workflow_package_selection_recommended()
        test_parse_workflow_package_selection_csv()
        test_parse_workflow_package_selection_all_includes_new_lifecycle_workflows()
        test_parse_workflow_package_selection_invalid()
        test_install_workflow_packages_invokes_specify_workflow_add()
        test_install_workflow_packages_uses_local_workflow_source_when_provided()
        test_build_integration_install_command()
        test_should_reconcile_integrations_only_for_explicit_agent_selection()
        test_install_agent_integrations_invokes_specify_integration_install()
        test_install_agent_integrations_dry_run_skips_subprocess()
        test_stage_local_extension_source_excludes_generated_state()
        test_is_workflows_extension_installed_detects_existing_install()
        test_install_extension_bundle_compat_copies_current_bundle_layout()
        test_patch_common_sh_wraps_upstream_function_instead_of_replacing_it()

        print("\n✅ All tests passed!")
        sys.exit(0)

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

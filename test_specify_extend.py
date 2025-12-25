#!/usr/bin/env python3
"""
Tests for specify_extend.py

Tests the core functionality of downloading and installing spec-kit-extensions.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
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


if __name__ == "__main__":
    print("Running specify_extend tests...\n")

    try:
        test_download_latest_template_tag()
        test_filters_template_tags_only()
        test_no_template_tags_found()

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

---
name: github-actions
description: Use when creating or maintaining GitHub Actions workflows, CI/CD pipelines, automated testing, releases, or deployments
user-invocable: true
---

# GitHub Actions CI/CD

## Workflow Basics

### File Location
```
.github/workflows/
├── ci.yml          # Main CI pipeline
├── release.yml     # Release automation
├── deploy.yml      # Deployment workflows
└── pr-check.yml    # PR-specific checks
```

### Workflow Structure
```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:  # Manual trigger

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
```

## Triggers

### Common Triggers
```yaml
on:
  # Branch events
  push:
    branches: [main, 'release/*']
    paths-ignore: ['**.md', 'docs/**']

  pull_request:
    types: [opened, synchronize, reopened]

  # Scheduled
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC

  # Manual
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy environment'
        required: true
        default: 'staging'
        type: choice
        options: [staging, production]

  # On release
  release:
    types: [published]

  # From other workflows
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '20'
```

## Caching

### Node.js with pnpm
```yaml
- uses: pnpm/action-setup@v3
  with:
    version: 9

- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'pnpm'

- run: pnpm install --frozen-lockfile
```

### Node.js with npm
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'

- run: npm ci
```

### Custom Caching
```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache
      node_modules/.vite
    key: ${{ runner.os }}-custom-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-custom-
```

### Turborepo Caching
```yaml
- uses: actions/cache@v4
  with:
    path: .turbo
    key: ${{ runner.os }}-turbo-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-turbo-
```

## Matrix Builds

### Multi-Version Testing
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        node-version: [18, 20, 22]
        os: [ubuntu-latest, macos-latest]
        exclude:
          - os: macos-latest
            node-version: 18
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

### Dynamic Matrix
```yaml
jobs:
  prepare:
    runs-on: ubuntu-latest
    outputs:
      packages: ${{ steps.find.outputs.packages }}
    steps:
      - uses: actions/checkout@v4
      - id: find
        run: |
          packages=$(ls packages | jq -R -s -c 'split("\n")[:-1]')
          echo "packages=$packages" >> $GITHUB_OUTPUT

  build:
    needs: prepare
    runs-on: ubuntu-latest
    strategy:
      matrix:
        package: ${{ fromJson(needs.prepare.outputs.packages) }}
    steps:
      - run: echo "Building ${{ matrix.package }}"
```

## Common Patterns

### TypeScript/Node.js CI
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm format:check

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm typecheck

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm test
      - uses: codecov/codecov-action@v4
        if: always()
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  build:
    runs-on: ubuntu-latest
    needs: [lint, typecheck, test]
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm build
```

### Reusable Workflow
```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test

on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '20'
    secrets:
      npm-token:
        required: false

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci
      - run: npm test
```

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '20'
    secrets:
      npm-token: ${{ secrets.NPM_TOKEN }}
```

## Secrets and Environments

### Using Secrets
```yaml
env:
  NPM_TOKEN: ${{ secrets.NPM_TOKEN }}

steps:
  - run: echo "//registry.npmjs.org/:_authToken=$NPM_TOKEN" >> .npmrc
```

### Environment Protection
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    steps:
      - run: ./deploy.sh
```

### GITHUB_TOKEN Permissions
```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write

jobs:
  comment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: 'Build succeeded!'
            })
```

## Artifacts and Outputs

### Upload/Download Artifacts
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
          retention-days: 7

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - run: ./deploy.sh
```

### Job Outputs
```yaml
jobs:
  version:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.pkg.outputs.version }}
    steps:
      - uses: actions/checkout@v4
      - id: pkg
        run: echo "version=$(node -p "require('./package.json').version")" >> $GITHUB_OUTPUT

  publish:
    needs: version
    runs-on: ubuntu-latest
    steps:
      - run: echo "Publishing version ${{ needs.version.outputs.version }}"
```

## Release Automation

### npm Trusted Publishers (OIDC - No Secrets!)

Trusted Publishers use OpenID Connect to authenticate with npm without storing tokens. This is the **recommended approach** for publishing.

#### Step 1: Configure npm Trusted Publisher
1. Go to npmjs.com → Package Settings → Publishing access
2. Add trusted publisher:
   - Provider: GitHub Actions
   - Repository: `owner/repo`
   - Workflow: `release.yml`
   - Environment: `npm` (optional but recommended)

#### Step 2: Workflow with Trusted Publisher
```yaml
name: Publish

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    environment: npm  # Optional: for environment protection rules
    permissions:
      contents: read
      id-token: write  # Required for OIDC token
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'

      - run: npm ci
      - run: npm run build

      # No NODE_AUTH_TOKEN needed - uses OIDC!
      - run: npm publish --provenance --access public
```

#### Trusted Publisher Benefits
- **No secrets to rotate** - OIDC tokens are short-lived
- **Provenance attestation** - Verifiable build origin
- **Environment protection** - Optional approval workflows
- **Audit trail** - Clear link between package and source

### npm Publish with Token (Legacy)
For registries that don't support OIDC:
```yaml
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write  # For provenance
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Changesets with Trusted Publishers
```yaml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    environment: npm
    permissions:
      contents: write
      pull-requests: write
      id-token: write  # For OIDC
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v3
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
          registry-url: 'https://registry.npmjs.org'

      - run: pnpm install --frozen-lockfile

      - name: Create Release PR or Publish
        uses: changesets/action@v1
        with:
          publish: pnpm changeset publish
          version: pnpm changeset version
          title: 'chore: version packages'
          commit: 'chore: version packages'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          # No NPM_TOKEN needed with trusted publishers!
```

### PyPI Trusted Publishers
Python packages also support OIDC:
```yaml
jobs:
  publish:
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install build
      - run: python -m build
      - uses: pypa/gh-action-pypi-publish@release/v1
        # No password needed - uses OIDC!
```

Configure at: pypi.org → Project → Publishing → Add a new publisher

### Automatic Release Tagging

Create GitHub releases automatically based on package.json versions:

```yaml
name: Release

on:
  push:
    branches: [main]
    paths:
      - 'package.json'
      - 'packages/*/package.json'

jobs:
  tag-release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get version from package.json
        id: version
        run: |
          VERSION=$(node -p "require('./package.json').version")
          echo "version=$VERSION" >> $GITHUB_OUTPUT

          # Check if pre-release
          if [[ "$VERSION" == *"-"* ]]; then
            echo "prerelease=true" >> $GITHUB_OUTPUT
          else
            echo "prerelease=false" >> $GITHUB_OUTPUT
          fi

      - name: Check if tag exists
        id: check
        run: |
          if git rev-parse "v${{ steps.version.outputs.version }}" >/dev/null 2>&1; then
            echo "exists=true" >> $GITHUB_OUTPUT
          else
            echo "exists=false" >> $GITHUB_OUTPUT
          fi

      - name: Create Release
        if: steps.check.outputs.exists == 'false'
        uses: actions/github-script@v7
        with:
          script: |
            const version = '${{ steps.version.outputs.version }}';
            const isPrerelease = ${{ steps.version.outputs.prerelease }};

            await github.rest.repos.createRelease({
              owner: context.repo.owner,
              repo: context.repo.repo,
              tag_name: `v${version}`,
              name: `v${version}`,
              prerelease: isPrerelease,
              generate_release_notes: true
            });
```

### Monorepo Multi-Package Tagging

For monorepos with multiple packages, use `<package-name>-v<version>` format:

```yaml
name: Release Packages

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Find changed packages and create releases
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const path = require('path');

            const packagesDir = './packages';
            const packages = fs.readdirSync(packagesDir);

            for (const pkg of packages) {
              const pkgJsonPath = path.join(packagesDir, pkg, 'package.json');
              if (!fs.existsSync(pkgJsonPath)) continue;

              const pkgJson = JSON.parse(fs.readFileSync(pkgJsonPath, 'utf8'));
              const version = pkgJson.version;
              const tagName = `${pkg}-v${version}`;
              const isPrerelease = version.includes('-');

              // Check if tag exists
              try {
                await github.rest.git.getRef({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  ref: `tags/${tagName}`
                });
                console.log(`Tag ${tagName} already exists, skipping`);
                continue;
              } catch (e) {
                // Tag doesn't exist, create release
              }

              await github.rest.repos.createRelease({
                owner: context.repo.owner,
                repo: context.repo.repo,
                tag_name: tagName,
                name: `${pkg} v${version}`,
                prerelease: isPrerelease,
                generate_release_notes: true
              });

              console.log(`Created release: ${tagName}`);
            }
```

### Provenance Attestation
Provenance links published packages to their source:
```yaml
- run: npm publish --provenance --access public
```

Users can verify with:
```bash
npm audit signatures
```

Shows:
```
@myorg/package@1.0.0 has a valid Sigstore attestation
  - Signed by: https://github.com/owner/repo/.github/workflows/release.yml@refs/tags/v1.0.0
```

## Conditional Execution

### Path Filters
```yaml
on:
  push:
    paths:
      - 'packages/core/**'
      - '!packages/core/**/*.md'
```

### Job Conditions
```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh

  notify:
    if: failure()
    needs: [build, test]
    runs-on: ubuntu-latest
    steps:
      - run: ./notify-failure.sh
```

### Step Conditions
```yaml
steps:
  - run: npm test
    id: test

  - run: npm run coverage
    if: steps.test.outcome == 'success'

  - run: echo "Tests failed"
    if: failure()

  - run: echo "Always runs"
    if: always()
```

## Monorepo Patterns

### Affected Packages Only
```yaml
jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      packages: ${{ steps.filter.outputs.changes }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            core:
              - 'packages/core/**'
            cli:
              - 'packages/cli/**'
            docs:
              - 'docs/**'

  test:
    needs: changes
    if: needs.changes.outputs.packages != '[]'
    strategy:
      matrix:
        package: ${{ fromJson(needs.changes.outputs.packages) }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm --filter ${{ matrix.package }} test
```

### Turborepo with Remote Cache
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
      TURBO_TEAM: ${{ vars.TURBO_TEAM }}
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm turbo build test lint
```

## Debugging

### Debug Logging
```yaml
steps:
  - run: echo "Event: ${{ github.event_name }}"
  - run: echo "Ref: ${{ github.ref }}"
  - run: echo "SHA: ${{ github.sha }}"
  - run: |
      echo "Context:"
      echo '${{ toJson(github) }}'
```

### SSH Debug Session
```yaml
steps:
  - uses: mxschmitt/action-tmate@v3
    if: failure()
    timeout-minutes: 15
```

### Re-run with Debug
Enable debug logging by setting secrets:
- `ACTIONS_RUNNER_DEBUG: true`
- `ACTIONS_STEP_DEBUG: true`

## Best Practices

1. **Pin action versions** - Use `@v4` not `@main`
2. **Use `--frozen-lockfile`** - Ensure reproducible builds
3. **Set concurrency** - Cancel redundant runs
4. **Minimize secrets exposure** - Use environments for production
5. **Cache aggressively** - Speed up workflows
6. **Fail fast in matrices** - Unless testing compatibility
7. **Use job dependencies** - Parallelize where possible
8. **Keep workflows DRY** - Use reusable workflows and composite actions

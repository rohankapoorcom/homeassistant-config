# Local Home Assistant Configuration Testing

This directory contains a script to run local testing of your Home Assistant configuration using Docker, replicating the checks performed by the GitHub Actions workflow in `.github/workflows/check-config.yml`.

## Quick Start

**Prerequisites:**
- Docker installed and running
- yamllint installed (required for YAML linting)

**Run tests:**
```bash
./tests/test-config.sh
```

**Run documentation link check only:**
```bash
./tests/check-docs-links.sh
```

## Script Overview

### `test-config.sh`
Runs configuration checks using Docker containers:
- ✅ yamllint validation (if installed locally)
- ✅ Home Assistant configuration validation using Docker
- ✅ Tests multiple versions (current, stable, beta, dev)
- ✅ Documentation link validation
- ✅ Isolated environment (no local dependencies)
- ✅ Replicates GitHub Actions workflow exactly

### `check-docs-links.sh`
Validates internal documentation links:
- ✅ Checks main README.md existence
- ✅ Verifies package documentation links
- ✅ Validates automation documentation links
- ✅ Tests blueprint documentation links
- ✅ Ensures proper relative path resolution
- ✅ Can be run independently or as part of test suite

## What the Tests Check

The script replicates the GitHub Actions workflow by:

1. **yamllint**: Validates YAML syntax and formatting across all YAML files
2. **Home Assistant Configuration Check**: Validates your configuration against different Home Assistant versions using Docker containers
3. **Version Testing**: Tests against your current version (from `.HA_VERSION`) plus stable, beta, and dev versions

## Manual Testing

You can also run individual checks manually:

```bash
# YAML linting (requires yamllint installed)
yamllint .

# Home Assistant configuration check using Docker
docker run --rm \
  -v "$(pwd):/config" \
  -v "$(pwd)/tests/travis_secrets.yaml:/config/secrets.yaml:ro" \
  "ghcr.io/home-assistant/home-assistant:stable" \
  python -m homeassistant --config /config --script check_config
```

## Troubleshooting

### Docker Issues
- Ensure Docker is installed and running
- Check that you have sufficient disk space for Docker images
- Verify Docker has permission to access your configuration directory

### Configuration Errors
The script bind mounts your `tests/travis_secrets.yaml` file as `/config/secrets.yaml` in the Docker container. If you get configuration errors, check that this file exists and contains valid test values.

### Permission Issues
Make sure the script is executable:
```bash
chmod +x tests/test-config.sh
```

## Integration with Git Hooks

You can integrate this test into your Git workflow by creating a pre-commit hook:

```bash
# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
./tests/test-config.sh
EOF

chmod +x .git/hooks/pre-commit
```

This will run the tests automatically before each commit, ensuring your configuration is valid before pushing to GitHub.

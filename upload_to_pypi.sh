#!/bin/bash
set -e

echo "Building and uploading py-kabusapi to PyPI..."

# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
echo "Building package..."
uv run python -m build

# Upload to PyPI using .pypirc config
echo "Uploading to PyPI..."
uv run twine upload dist/*

echo "Successfully uploaded to PyPI!"
echo "View at: https://pypi.org/project/py-kabusapi/"
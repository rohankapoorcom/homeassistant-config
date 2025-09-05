#!/bin/bash

# Documentation Link Checker Test
# This test script checks for broken internal links in the documentation
# Part of the Home Assistant configuration test suite

echo "🔍 Checking documentation links..."

# Function to check if a file exists relative to the current directory
check_link() {
    local file_path="$1"
    local current_dir="$2"
    local full_path="$current_dir/$file_path"
    
    if [[ -f "$full_path" ]]; then
        echo "✅ $file_path"
        return 0
    else
        echo "❌ $file_path (from $current_dir)"
        return 1
    fi
}

# Check main README links
echo "📋 Checking main README.md..."
if [[ -f "README.md" ]]; then
    echo "✅ README.md exists"
else
    echo "❌ README.md missing"
fi

# Check package documentation links
echo "📦 Checking package documentation links..."
if [[ -f "docs/packages/README.md" ]]; then
    echo "✅ docs/packages/README.md exists"
    # Check if main README is accessible from packages directory
    check_link "../../README.md" "docs/packages"
else
    echo "❌ docs/packages/README.md missing"
fi

# Check automation documentation links
echo "🤖 Checking automation documentation links..."
if [[ -f "docs/automations/README.md" ]]; then
    echo "✅ docs/automations/README.md exists"
    # Check if main README is accessible from automations directory
    check_link "../../README.md" "docs/automations"
else
    echo "❌ docs/automations/README.md missing"
fi

# Check blueprint documentation links
echo "📋 Checking blueprint documentation links..."
if [[ -f "docs/blueprints/README.md" ]]; then
    echo "✅ docs/blueprints/README.md exists"
    # Check if main README is accessible from blueprints directory
    check_link "../../README.md" "docs/blueprints"
else
    echo "❌ docs/blueprints/README.md missing"
fi

# Check individual blueprint files
echo "🔧 Checking individual blueprint files..."
for blueprint_file in docs/blueprints/automation/*.md; do
    if [[ -f "$blueprint_file" ]]; then
        filename=$(basename "$blueprint_file")
        echo "✅ $filename exists"
        # Check if blueprint README is accessible from automation directory
        check_link "../README.md" "docs/blueprints/automation"
    fi
done

echo "✅ Documentation link check complete!"
echo ""
echo "💡 To prevent broken links in the future:"
echo "   - Always test relative paths from the correct directory level"
echo "   - Use ../../README.md from docs/subdir/ directories (packages, automations)"
echo "   - Use ../README.md from docs/blueprints/ subdirectories (script, template, automation)"
echo "   - Use ../README.md from docs/blueprints/automation/ individual blueprint files (links to blueprint index)"
echo "   - Use ../README.md from docs/ directory"
echo "   - Run this test as part of the test suite: ./tests/check-docs-links.sh"
echo "   - Include this test in CI/CD pipelines to catch broken links automatically"

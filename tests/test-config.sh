#!/bin/bash

# Local Home Assistant Configuration Testing Script
# This script replicates the checks from .github/workflows/check-config.yml
# Based on frenck/action-home-assistant implementation

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    # Check for yamllint
    if ! command -v yamllint &> /dev/null; then
        print_error "yamllint is not installed. Please install it first:"
        echo "  pip install yamllint"
        echo "  or"
        echo "  sudo apt install yamllint"
        exit 1
    fi
    
    # Check for Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    print_success "All dependencies are installed"
}

# Run yamllint
run_yamllint() {
    print_status "Running yamllint..."
    
    if yamllint .; then
        print_success "yamllint passed"
    else
        print_error "yamllint failed"
        exit 1
    fi
}

# Determine Home Assistant versions to test
get_ha_versions() {
    print_status "Determining Home Assistant versions to test..."
    
    if [[ -f "./.HA_VERSION" ]]; then
        CURRENT_VERSION=$(cat ./.HA_VERSION | tr -d '[:space:]')
        VERSIONS=("$CURRENT_VERSION" "stable" "beta" "dev")
        print_status "Found .HA_VERSION file with version: $CURRENT_VERSION"
    else
        print_warning "No .HA_VERSION file found; using default versions"
        VERSIONS=("stable" "beta" "dev")
    fi
    
    echo "Versions to test: ${VERSIONS[*]}"
}

# Run Home Assistant configuration check
run_ha_check() {
    local version=$1
    print_status "Running Home Assistant configuration check for version: $version"
    
    # Run Home Assistant check using Docker (based on frenck action)
    if docker run --rm \
        -v "$(pwd):/config" \
        -v "$(pwd)/tests/travis_secrets.yaml:/config/secrets.yaml:ro" \
        "ghcr.io/home-assistant/home-assistant:$version" \
        python -m homeassistant --config /config --script check_config; then
        
        print_success "Home Assistant configuration check passed for version: $version"
    else
        print_error "Home Assistant configuration check failed for version: $version"
        exit 1
    fi
}

# Main execution
main() {
    echo "=========================================="
    echo "Home Assistant Configuration Test Runner"
    echo "=========================================="
    echo ""
    
    # Check dependencies
    check_dependencies
    
    # Run yamllint
    run_yamllint
    
    # Get versions to test
    get_ha_versions
    
    # Run Home Assistant checks for each version
    for version in "${VERSIONS[@]}"; do
        echo ""
        echo "------------------------------------------"
        echo "Testing Home Assistant version: $version"
        echo "------------------------------------------"
        run_ha_check "$version"
    done
    
    echo ""
    echo "=========================================="
    print_success "All tests completed successfully!"
    echo "=========================================="
}

# Run main function
main "$@"

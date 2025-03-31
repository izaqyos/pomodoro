#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BLUE='\033[0;34m'
YELLOW='\033[1;33m'

# Function to run tests with coverage
run_tests() {
    echo -e "${BLUE}🧪 Running tests with coverage...${NC}"
    pytest --cov=src tests/ -v
}

# Function to run linting
run_lint() {
    echo -e "${BLUE}🔍 Running code quality checks...${NC}"
    
    echo -e "${YELLOW}Running black...${NC}"
    black --check src/ tests/
    
    echo -e "${YELLOW}Running isort...${NC}"
    isort --check-only src/ tests/
    
    echo -e "${YELLOW}Running flake8...${NC}"
    flake8 src/ tests/
}

# Main execution
echo -e "${BLUE}🚀 Starting test suite...${NC}"

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo -e "${RED}❌ Conda is not installed. Please install Conda first.${NC}"
    exit 1
fi

# Source the conda activation script
if [ -f "activate_env.sh" ]; then
    echo -e "${GREEN}✓ Activating conda environment...${NC}"
    source activate_env.sh
else
    echo -e "${RED}❌ activate_env.sh not found. Please ensure it exists in the project root.${NC}"
    exit 1
fi

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --no-lint)
            NO_LINT=true
            shift
            ;;
        --coverage-only)
            COVERAGE_ONLY=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Run the tests
if [ "$COVERAGE_ONLY" = true ]; then
    run_tests
else
    run_tests
    if [ "$NO_LINT" != true ]; then
        run_lint
    fi
fi

# Check exit status
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
else
    echo -e "${RED}❌ Tests failed!${NC}"
    exit 1
fi 
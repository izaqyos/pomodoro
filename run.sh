#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BLUE='\033[0;34m'
YELLOW='\033[1;33m'

# Function to show usage
show_usage() {
    echo -e "Usage: ./run.sh [OPTIONS]"
    echo -e "Options:"
    echo -e "  -w, --watch    Run in watch mode (auto-reload on file changes)"
    echo -e "  -h, --help     Show this help message"
}

# Default values
WATCH_MODE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -w|--watch)
            WATCH_MODE=true
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_usage
            exit 1
            ;;
    esac
done

# Check if we're already in the pomodoro environment
if [[ "$CONDA_DEFAULT_ENV" == "pomodoro" ]]; then
    echo -e "${GREEN}✓ Already in pomodoro environment${NC}"
    
    if [ "$WATCH_MODE" = true ]; then
        echo -e "${YELLOW}Starting in watch mode...${NC}"
        echo -e "${BLUE}ℹ️  App will automatically reload on file changes${NC}"
        streamlit run src/main.py --server.runOnSave=true
    else
        echo -e "${GREEN}✓ Launching Pomodoro Timer...${NC}"
        streamlit run src/main.py
    fi
    exit 0
fi

# If not in pomodoro environment, run the full setup
echo -e "${BLUE}🍅 Starting Pomodoro Timer...${NC}"

# Initialize conda
eval "$(conda shell.bash hook)"

# Activate the conda environment if it exists, otherwise create it
if conda env list | grep -q "pomodoro"; then
    echo -e "${GREEN}✓ Activating existing conda environment...${NC}"
    conda activate pomodoro || {
        echo -e "${RED}Failed to activate environment. Trying to initialize conda...${NC}"
        conda init bash
        source ~/.bashrc
        conda activate pomodoro
    }
else
    echo -e "${YELLOW}Creating new conda environment...${NC}"
    conda create -n pomodoro python=3.10 -y
    conda activate pomodoro
    pip install -r requirements/dev.txt
fi

# Add the current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the application
if [ "$WATCH_MODE" = true ]; then
    echo -e "${YELLOW}Starting in watch mode...${NC}"
    echo -e "${BLUE}ℹ️  App will automatically reload on file changes${NC}"
    streamlit run src/main.py --server.runOnSave=true
else
    echo -e "${GREEN}✓ Launching Pomodoro Timer...${NC}"
    streamlit run src/main.py 
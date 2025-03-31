#!/bin/bash

# Default values
WATCH_MODE=false
APP_FILE="app.py"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --watch|-w)
            WATCH_MODE=true
            shift # Remove --watch or -w from processing
            ;;
        --*|-*)
            echo "Unknown option $1"
            exit 1
            ;;
        *)
            # First non-flag argument is assumed to be the app file
            APP_FILE="$1"
            shift
            ;;
    esac
done

# Change to the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Conda is not installed. Please install Miniconda or Anaconda first."
    echo "Visit https://docs.conda.io/en/latest/miniconda.html for installation instructions."
    exit 1
fi

# Check if the conda environment exists
if ! conda env list | grep -q "^pomodoro "; then
    echo "Creating pomodoro conda environment..."
    conda env create -f environment.yml
    if [ $? -ne 0 ]; then
        echo "Failed to create conda environment. Please check environment.yml file."
        exit 1
    fi
fi

# Run the streamlit app with the pomodoro environment
echo "Starting Pomodoro Timer App..."

# Use eval to properly activate the conda environment in the current shell
eval "$(conda shell.bash hook)"
conda activate pomodoro

# Now run the app - with watch mode if requested
if [ "$WATCH_MODE" = true ]; then
    echo "Running in watch mode. App will reload automatically when code changes."
    conda run -n pomodoro streamlit run "$APP_FILE" --server.runOnSave=true
else
    conda run -n pomodoro streamlit run "$APP_FILE"
fi 
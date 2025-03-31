#!/bin/bash

# This script should be sourced, not executed
# Usage: source activate_env.sh

# Check if conda is installed
if ! command -v conda &> /dev/null
then
    echo "Conda is not installed. Please install Miniconda or Anaconda first."
    echo "Visit https://docs.conda.io/en/latest/miniconda.html for installation instructions."
    return 1
fi

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Create conda environment if it doesn't exist
if ! conda env list | grep -q "pomodoro"; then
    echo "Creating new conda environment: pomodoro"
    conda create -n pomodoro python=3.10 -y
fi

# Activate the conda environment
conda activate pomodoro

# Install pytest and other testing requirements
conda install -y pytest pytest-cov

# Install other requirements
pip install -r requirements/dev.txt

# Install the package in development mode
pip install -e .

echo "Conda environment 'pomodoro' is now active and requirements are installed"

echo "Environment activated! You can now run the app with: streamlit run app.py" 
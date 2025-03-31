#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BLUE='\033[0;34m'

echo -e "${BLUE}🍅 Activating Pomodoro environment...${NC}"

# Initialize conda for shell script
source ~/miniconda3/etc/profile.d/conda.sh

# Check if pomodoro environment exists
if conda env list | grep -q "pomodoro"; then
    echo -e "${GREEN}✓ Activating existing pomodoro environment${NC}"
    conda activate pomodoro
else
    echo -e "${BLUE}Creating new pomodoro environment...${NC}"
    conda create -n pomodoro python=3.10 -y
    conda activate pomodoro
    echo -e "${BLUE}Installing requirements...${NC}"
    pip install -r requirements/dev.txt
fi

echo -e "${GREEN}✓ Pomodoro environment is ready!${NC}"

# Keep the shell running with the activated environment
exec $SHELL 
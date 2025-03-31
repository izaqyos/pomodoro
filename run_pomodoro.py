#!/usr/bin/env python3
"""
Cross-platform script to run the Pomodoro application with optional watch mode.
This script handles environment activation and running the application on any platform.
"""

import os
import sys
import argparse
import subprocess
import platform

def main():
    """Main function to run the Pomodoro timer app."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the Pomodoro Timer Application")
    parser.add_argument('--watch', '-w', action='store_true', 
                        help='Run in watch mode - automatically reload when code changes')
    parser.add_argument('--debug', '-d', action='store_true',
                        help='Run with debug mode enabled to see Streamlit logs')
    parser.add_argument('app_filepath', nargs='?', default='app.py',
                        help='Streamlit app file to run (default: app.py)')
    args = parser.parse_args()
    
    # Change to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check if conda is installed
    conda_command = "conda.bat" if platform.system() == "Windows" else "conda"
    try:
        subprocess.run([conda_command, "--version"], 
                       stdout=subprocess.PIPE, 
                       stderr=subprocess.PIPE, 
                       check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Conda is not installed. Please install Miniconda or Anaconda first.")
        print("Visit https://docs.conda.io/en/latest/miniconda.html for installation instructions.")
        sys.exit(1)
    
    # Check if the conda environment exists
    env_exists = False
    result = subprocess.run([conda_command, "env", "list"], 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    
    for line in result.stdout.splitlines():
        if line.startswith("pomodoro "):
            env_exists = True
            break
    
    # Create the environment if it doesn't exist
    if not env_exists:
        print("Creating pomodoro conda environment...")
        try:
            subprocess.run([conda_command, "env", "create", "-f", "environment.yml"], 
                          check=True)
        except subprocess.SubprocessError:
            print("Failed to create conda environment. Please check environment.yml file.")
            sys.exit(1)
    
    # Activate the environment and run the application
    print("Starting Pomodoro Timer App...")
    
    # Construct the Streamlit run command with appropriate flags
    streamlit_cmd = ["streamlit", "run", args.app_filepath]
    
    if args.watch:
        print("Running in watch mode. App will reload automatically when code changes.")
        streamlit_cmd.append("--server.runOnSave=true")
    
    if args.debug:
        print("Running in debug mode. Streamlit logs will be displayed.")
        streamlit_cmd.append("--logger.level=debug")
    
    # Different environment activation approaches for different platforms
    if platform.system() == "Windows":
        # For Windows, we need to activate and then run the command
        activate_cmd = f"conda activate pomodoro && {' '.join(streamlit_cmd)}"
        subprocess.run(activate_cmd, shell=True)
    else:
        # For Unix-like systems (macOS, Linux), we can use conda run
        subprocess.run([conda_command, "run", "-n", "pomodoro"] + streamlit_cmd)

if __name__ == "__main__":
    main() 
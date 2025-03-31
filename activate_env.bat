@echo off
setlocal

:: This script should be called, not executed directly
:: Usage: call activate_env.bat

:: Check if conda is installed
where conda >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Conda is not installed. Please install Miniconda or Anaconda first.
    echo Visit https://docs.conda.io/en/latest/miniconda.html for installation instructions.
    goto :EOF
)

:: Navigate to the script directory
cd /d "%~dp0"

:: Check if the conda environment exists
conda env list | findstr /C:"pomodoro " >nul
if %ERRORLEVEL% neq 0 (
    echo Creating pomodoro conda environment...
    conda env create -f environment.yml
    if %ERRORLEVEL% neq 0 (
        echo Failed to create conda environment. Please check environment.yml file.
        goto :EOF
    )
)

:: Activate the conda environment
echo Activating pomodoro conda environment...
call conda activate pomodoro

echo Environment activated! You can now run the app with: streamlit run app.py 
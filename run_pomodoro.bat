@echo off
setlocal enabledelayedexpansion

:: Default values
set WATCH_MODE=false
set APP_FILE=app.py

:: Parse command line arguments
:parse_args
if "%~1"=="" goto :end_parse
if "%~1"=="--watch" (
    set WATCH_MODE=true
    shift
    goto :parse_args
)
if "%~1"=="-w" (
    set WATCH_MODE=true
    shift
    goto :parse_args
)
if "%~1:~0,1%"=="-" (
    echo Unknown option: %~1
    exit /b 1
)
:: First non-flag argument is assumed to be the app file
set APP_FILE=%~1
shift
goto :parse_args
:end_parse

:: Change to the script's directory
cd /d "%~dp0"

:: Check if conda is installed
where conda >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Conda is not installed. Please install Miniconda or Anaconda first.
    echo Visit https://docs.conda.io/en/latest/miniconda.html for installation instructions.
    exit /b 1
)

:: Check if the conda environment exists
conda env list | findstr /C:"pomodoro " >nul
if %ERRORLEVEL% neq 0 (
    echo Creating pomodoro conda environment...
    conda env create -f environment.yml
    if %ERRORLEVEL% neq 0 (
        echo Failed to create conda environment. Please check environment.yml file.
        exit /b 1
    )
)

:: Run the streamlit app with the pomodoro environment
echo Starting Pomodoro Timer App...

:: First activate the environment, then run the app
call conda activate pomodoro
if %ERRORLEVEL% neq 0 (
    echo Failed to activate conda environment.
    exit /b 1
)

if "%WATCH_MODE%"=="true" (
    echo Running in watch mode. App will reload automatically when code changes.
    streamlit run "%APP_FILE%" --server.runOnSave=true
) else (
    streamlit run "%APP_FILE%"
)

:: Deactivate the environment
call conda deactivate 
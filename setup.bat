@echo off
REM Documentation Pipeline - Quick Setup Script for Windows
REM This script sets up the Docker environment for the documentation pipeline

echo.
echo ================================
echo Documentation Pipeline Setup
echo ================================
echo.

REM Check if Docker is installed
echo Checking for Docker...
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker is not installed.
    echo Please install Docker Desktop from:
    echo https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)
echo [OK] Docker found

REM Check if Docker is running
echo Checking if Docker is running...
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker is not running.
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo [OK] Docker is running

REM Create output directories
echo Creating output directories...
if not exist "output\markdown" mkdir output\markdown
if not exist "output\pdf" mkdir output\pdf
if not exist "output\temp" mkdir output\temp
echo [OK] Directories created

REM Ask to build image
echo.
set /p BUILD="Build Docker image now? (y/n): "
if /i "%BUILD%" NEQ "y" goto :skip_build

echo.
echo Building Docker image...
echo This may take 10-20 minutes on first run (downloading packages)
echo.
docker build -t docs-pipeline .
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Docker build failed
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Docker image built successfully!

REM Ask to run test
echo.
set /p TEST="Run test with README.md? (y/n): "
if /i "%TEST%" NEQ "y" goto :skip_test

echo.
echo Testing with README.md...
echo.
docker run --rm -v "%CD%:/app/input:ro" -v "%CD%/output:/app/output" docs-pipeline python3 main.py /app/input/README.md
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Test failed
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Test successful!
echo Check output\pdf\README.pdf
goto :show_usage

:skip_build
echo.
echo Skipped build. Run 'docker build -t docs-pipeline .' when ready.
goto :show_usage

:skip_test
echo.
echo Skipped test.

:show_usage
echo.
echo ================================================
echo           Setup Complete!
echo ================================================
echo.
echo Quick Start Commands:
echo.
echo Using Makefile (if Make is available):
echo   make run FILE=README.md
echo   make run-custom PATH=C:\\path\\to\\folder FILE=file.md
echo   make run-custom-all PATH=C:\\path\\to\\folder
echo.
echo Using Docker directly (Current directory):
echo   docker run --rm ^
echo     -v "%CD%:/app/input:ro" ^
echo     -v "%CD%/output:/app/output" ^
echo     docs-pipeline python3 main.py /app/input/README.md
echo.
echo Using Docker directly (Custom directory):
echo   docker run --rm ^
echo     -v "C:\\path\\to\\folder:/app/input:ro" ^
echo     -v "%CD%/output:/app/output" ^
echo     docs-pipeline python3 main.py /app/input
echo.
echo Using Docker Compose:
echo   docker-compose run docs-pipeline python3 main.py /app/input/README.md
echo   For custom paths, create docker-compose.override.yml
echo.
echo Documentation:
echo   README.md     - Main documentation
echo   DOCKER.md     - Detailed Docker guide
echo.
echo ================================================
echo.
pause

@echo off
REM Hammer Windows Installer (Batch Version)
REM Run as Administrator

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo               HAMMER - Windows Installer
echo ============================================================
echo.

REM Check for admin rights
openfiles >nul 2>&1
if errorlevel 1 (
    echo [-] This script requires administrator privileges!
    echo [*] Please run as Administrator ^(right-click cmd.exe ^> Run as administrator^)
    echo.
    pause
    exit /b 1
)

REM Check for Python
echo [*] Checking for Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [-] Python not found in PATH
    echo [*] Please install Python from https://www.python.org/
    echo [*] Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do (
    echo [+] Found Python: %%i
)

REM Get current directory
set PROJECT_DIR=%~dp0
if not exist "%PROJECT_DIR%hammer.py" (
    echo [-] hammer.py not found in %PROJECT_DIR%
    pause
    exit /b 1
)

echo [*] Project directory: %PROJECT_DIR%
echo.

REM Install pip dependencies
echo [*] Installing Python dependencies...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [-] Failed to upgrade pip
    pause
    exit /b 1
)

python -m pip install -r "%PROJECT_DIR%requirements.txt"
if errorlevel 1 (
    echo [-] Failed to install dependencies
    pause
    exit /b 1
)

REM Install the package
echo [*] Installing Hammer package...
cd /d "%PROJECT_DIR%"
python -m pip install -e .
if errorlevel 1 (
    echo [-] Failed to install Hammer
    pause
    exit /b 1
)

echo.
echo ============================================================
echo               Installation Complete!
echo ============================================================
echo.
echo [+] Hammer has been successfully installed!
echo [*] You can now run 'hammer' from any terminal
echo [*] Note: You may need to restart your terminal for changes to take effect
echo.
pause

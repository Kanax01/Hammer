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
python -m pip install --upgrade pip >nul 2>&1
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

REM Create installation directory
set INSTALL_DIR=%PROGRAMFILES%\Hammer
if not exist "%INSTALL_DIR%" (
    echo [*] Creating installation directory...
    mkdir "%INSTALL_DIR%"
)

REM Copy project files to installation directory
echo [*] Copying Hammer files to %INSTALL_DIR%...
xcopy "%PROJECT_DIR%*.py" "%INSTALL_DIR%\" /Y /Q >nul
xcopy "%PROJECT_DIR%requirements.txt" "%INSTALL_DIR%\" /Y /Q >nul

if not exist "%INSTALL_DIR%hammer.py" (
    echo [-] Failed to copy files
    pause
    exit /b 1
)

REM Create batch wrapper
set BATCH_WRAPPER=%INSTALL_DIR%\hammer.bat
echo [*] Creating batch wrapper...
(
    echo @echo off
    echo cd /d "%INSTALL_DIR%"
    echo python hammer.py %%*
) > "%BATCH_WRAPPER%"

if not exist "%BATCH_WRAPPER%" (
    echo [-] Failed to create wrapper
    pause
    exit /b 1
)

REM Add to PATH
echo [*] Adding Hammer to system PATH...
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH >nul 2>&1
if errorlevel 1 (
    echo [-] Failed to access registry
    pause
    exit /b 1
)

for /f "tokens=2*" %%A in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH ^| find /i "PATH"') do (
    set CURRENT_PATH=%%B
)

if not "!CURRENT_PATH!"=="" (
    echo !CURRENT_PATH! | find /i "%INSTALL_DIR%" >nul 2>&1
    if errorlevel 1 (
        setx /M PATH "!CURRENT_PATH!;%INSTALL_DIR%"
        set "PATH=!PATH!;%INSTALL_DIR%"
        echo [+] Added to system PATH
    ) else (
        echo [+] Already in PATH
    )
)

echo.
echo ============================================================
echo               Installation Complete!
echo ============================================================
echo.
echo [+] Hammer has been successfully installed to: %INSTALL_DIR%
echo [*] You can now run 'hammer' from any terminal
echo [*] Note: You may need to restart your terminal for changes to take effect
echo.
pause

# Hammer Windows Installer
# This script installs Hammer and adds it to your Windows PATH

param(
    [switch]$Uninstall = $false
)

function Write-Title {
    param([string]$Text)
    Write-Host "`n" -ForegroundColor Yellow
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host ""
}

function Test-AdminRights {
    $isAdmin = [bool]([System.Security.Principal.WindowsIdentity]::GetCurrent().Groups -match 'S-1-5-32-544')
    return $isAdmin
}

function Find-Python {
    Write-Host "[*] Checking for Python installation..." -ForegroundColor Yellow
    
    try {
        $python = Get-Command python -ErrorAction Stop
        $version = & $python.Source --version 2>&1
        Write-Host "[+] Found Python: $version" -ForegroundColor Green
        return $python.Source
    }
    catch {
        Write-Host "[-] Python not found in PATH" -ForegroundColor Red
        Write-Host "[*] Please install Python from https://www.python.org/" -ForegroundColor Yellow
        return $null
    }
}

function Install-Hammer {
    Write-Title "Installing Hammer"
    
    # Check admin rights
    if (-not (Test-AdminRights)) {
        Write-Host "[!] This script requires administrator privileges!" -ForegroundColor Red
        Write-Host "[*] Please run as Administrator (right-click PowerShell > Run as administrator)" -ForegroundColor Yellow
        exit 1
    }
    
    # Find Python
    $pythonPath = Find-Python
    if ($null -eq $pythonPath) {
        exit 1
    }
    
    # Get the directory where this script is located
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
    $projectDir = if (Test-Path (Join-Path $scriptDir "hammer.py")) { $scriptDir } else { Get-Location }
    
    if (-not (Test-Path (Join-Path $projectDir "hammer.py"))) {
        Write-Host "[-] hammer.py not found in $projectDir" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "[*] Project directory: $projectDir" -ForegroundColor Cyan
    
    # Install dependencies
    Write-Host "[*] Installing Python dependencies..." -ForegroundColor Yellow
    & $pythonPath -m pip install --upgrade pip 2>&1 | Out-Null
    & $pythonPath -m pip install -r (Join-Path $projectDir "requirements.txt")
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[-] Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
    
    # Copy files to Program Files
    $installDir = "C:\Program Files\Hammer"
    Write-Host "[*] Creating installation directory: $installDir" -ForegroundColor Yellow
    
    if (-not (Test-Path $installDir)) {
        New-Item -ItemType Directory -Force -Path $installDir | Out-Null
    }
    
    Write-Host "[*] Copying Hammer files..." -ForegroundColor Yellow
    Copy-Item -Path (Join-Path $projectDir "hammer.py") -Destination $installDir -Force
    Copy-Item -Path (Join-Path $projectDir "referers.py") -Destination $installDir -Force
    Copy-Item -Path (Join-Path $projectDir "useragents.py") -Destination $installDir -Force
    Copy-Item -Path (Join-Path $projectDir "requirements.txt") -Destination $installDir -Force
    
    # Create batch wrapper
    $batchFile = Join-Path $installDir "hammer.bat"
    $wrapperContent = "@echo off`r`npython `"$installDir\hammer.py`" %*"
    Set-Content -Path $batchFile -Value $wrapperContent -Encoding ASCII
    Write-Host "[+] Created wrapper: $batchFile" -ForegroundColor Green
    
    # Add to PATH if needed
    $envPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
    
    if (-not $envPath.Contains($installDir)) {
        Write-Host "[*] Adding Hammer to system PATH..." -ForegroundColor Yellow
        [Environment]::SetEnvironmentVariable("PATH", "$envPath;$installDir", "Machine")
        $env:PATH = "$env:PATH;$installDir"
        Write-Host "[+] Added to PATH: $installDir" -ForegroundColor Green
    } else {
        Write-Host "[+] Already in PATH" -ForegroundColor Green
    }
    
    Write-Title "Installation Complete!"
    Write-Host "[+] Hammer has been successfully installed to: $installDir" -ForegroundColor Green
    Write-Host "[*] You can now run 'hammer' from any terminal" -ForegroundColor Cyan
    Write-Host "[*] Note: You may need to restart your terminal for changes to take effect" -ForegroundColor Yellow
}

function Uninstall-Hammer {
    Write-Title "Uninstalling Hammer"
    
    # Check admin rights
    if (-not (Test-AdminRights)) {
        Write-Host "[!] This script requires administrator privileges!" -ForegroundColor Red
        Write-Host "[*] Please run as Administrator" -ForegroundColor Yellow
        exit 1
    }
    
    $installDir = "C:\Program Files\Hammer"
    
    if (Test-Path $installDir) {
        Write-Host "[*] Removing Hammer from: $installDir" -ForegroundColor Yellow
        Remove-Item -Path $installDir -Recurse -Force
        Write-Host "[+] Hammer files removed" -ForegroundColor Green
    }
    
    # Remove from PATH
    $envPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
    if ($envPath.Contains($installDir)) {
        Write-Host "[*] Removing from PATH..." -ForegroundColor Yellow
        $newPath = $envPath -replace [regex]::Escape("$installDir;"), "" -replace [regex]::Escape(";$installDir"), ""
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "Machine")
        Write-Host "[+] Removed from PATH" -ForegroundColor Green
    }
    
    Write-Host "[+] Hammer has been uninstalled" -ForegroundColor Green
}

# Main execution
try {
    if ($Uninstall) {
        Uninstall-Hammer
    }
    else {
        Install-Hammer
    }
}
catch {
    Write-Host "[-] An error occurred: $_" -ForegroundColor Red
    exit 1
}

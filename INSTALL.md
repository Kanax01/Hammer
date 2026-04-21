# Hammer Installation Guide (Windows)

This guide explains how to install Hammer on Windows so you can run it from anywhere by typing `hammer` in your terminal.

## Prerequisites

- **Python 3.6+** - Download from https://www.python.org/
  - **IMPORTANT**: During installation, check the box "Add Python to PATH"
- **Administrator Access** - Required to install the program system-wide

## Installation Methods

### Method 1: PowerShell Installer (Recommended)

1. **Open PowerShell as Administrator**
   - Right-click on PowerShell and select "Run as Administrator"
   - Or search for "PowerShell" in Windows Start menu, right-click, and choose "Run as Administrator"

2. **Navigate to the Hammer folder**
   ```powershell
   cd "C:\path\to\Hammer"
   ```

3. **Run the installer**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser -Force
   .\install.ps1
   ```

4. **Verify installation**
   - Restart your terminal (or open a new PowerShell window)
   - Type: `hammer`
   - The Hammer banner should appear

### Method 2: Batch Installer

1. **Open Command Prompt as Administrator**
   - Right-click on Command Prompt (cmd.exe) and select "Run as Administrator"

2. **Navigate to the Hammer folder**
   ```cmd
   cd C:\path\to\Hammer
   ```

3. **Run the installer**
   ```cmd
   install.bat
   ```

4. **Verify installation**
   - Restart your terminal
   - Type: `hammer`

### Method 3: Manual Installation

If the automated installers don't work, follow these steps:

1. **Open Command Prompt or PowerShell as Administrator**

2. **Navigate to the Hammer folder**
   ```cmd
   cd C:\path\to\Hammer
   ```

3. **Install dependencies**
   ```cmd
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. **Copy files to Program Files**
   ```cmd
   mkdir "C:\Program Files\Hammer"
   copy *.py "C:\Program Files\Hammer\"
   ```

5. **Create batch wrapper** (save as `C:\Program Files\Hammer\hammer.bat`)
   ```batch
   @echo off
   python "C:\Program Files\Hammer\hammer.py" %*
   ```

6. **Add to PATH**
   - Right-click "This PC" or "My Computer" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find and select "Path"
   - Click "Edit"
   - Click "New" and add: `C:\Program Files\Hammer`
   - Click OK on all dialogs

7. **Test installation**
   - Open a new Command Prompt or PowerShell
   - Type: `hammer`

## Usage

Once installed, you can run Hammer from anywhere by simply typing:

```cmd
hammer
```

Then follow the prompts to:
- Enter the target URL or IP address
- Specify the number of requests
- Set the number of concurrent threads
- Choose whether to use Tor (optional)

## Where Hammer is Installed

The installer copies Hammer to: `C:\Program Files\Hammer\`

You can also run it directly from the source directory:
```cmd
cd C:\path\to\Hammer
python hammer.py
```

## Uninstalling

### Using PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser -Force
.\install.ps1 -Uninstall
```

### Manual Uninstall:
1. Delete the folder: `C:\Program Files\Hammer\`
2. Remove from PATH:
   - Right-click "This PC" → Properties
   - Advanced system settings → Environment Variables
   - Find "Path" under System variables → Edit
   - Find and delete the line containing `C:\Program Files\Hammer`
   - Click OK

## Troubleshooting

### "Python not found"
- Install Python from https://www.python.org/
- **Make sure to check "Add Python to PATH"** during installation
- Restart your computer after installing Python

### "Permission denied" or "Access is denied"
- The script requires administrator privileges
- Right-click on PowerShell/Command Prompt and select "Run as Administrator"

### "hammer" command not found
- The command might not be available in your current terminal
- Try restarting your terminal or opening a new one
- If still not working, run the installer again as Administrator

### Dependency installation fails
- Make sure Python pip is up to date: `python -m pip install --upgrade pip`
- Try installing dependencies manually:
  ```cmd
  python -m pip install requests colorama PySocks
  ```

### Tor installation (optional)
- If you want to use Tor anonymity features, you'll need Tor installed
- Install Tor from: https://www.torproject.org/download/
- Or use Chocolatey (if installed): `choco install tor`

## Support

For issues or questions, visit the GitHub repository:
https://github.com/Kanax01/Hammer

---

**⚠️ DISCLAIMER**: Unauthorized use of this tool is illegal. Only use this tool on networks you own or have explicit permission to test.

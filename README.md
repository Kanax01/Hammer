<div align="center">

# Hammer
### A network stress testing tool
### Made by, Kanax01

</div>


## Disclaimer

- **UNAUTHORIZED USE OF THIS TOOL ON A NETWORK THAT YOU DO NOT OWN OR HAVE PREMMISION TO TEST IS HIGHLY ILLEGAL**

## Installation

### Quick Install (Windows)

Run one of the installers as Administrator to install Hammer globally:

**PowerShell (Recommended):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser -Force
.\install.ps1
```

**Command Prompt/Batch:**
```cmd
install.bat
```

Then you can use `hammer` from anywhere in the terminal!

For detailed installation instructions, see [INSTALL.md](INSTALL.md)

### Manual Installation

1. Install Python 3.6+ from https://www.python.org/
2. Clone or download this repository
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run Hammer:
   ```
   python hammer.py
   ```

## Optional: Tor Support

- **Chocolatey** (for easy installation): Install Tor via `choco install tor`
- **Or download directly** from https://www.torproject.org/download/

# Troubleshooting Guide

Common issues and solutions when setting up the Market Microstructure Analysis backend.

## Table of Contents
- [Installation Issues](#installation-issues)
- [Runtime Issues](#runtime-issues)
- [Platform-Specific Issues](#platform-specific-issues)

---

## Installation Issues

### Issue: "Failed to build installable wheels for pydantic-core"

**Symptoms:**
```
× Failed to build installable wheels for some pyproject.toml based projects
╰─> pydantic-core
```

**Solutions:**

1. **Upgrade pip, setuptools, and wheel:**
   ```bash
   python -m pip install --upgrade pip setuptools wheel
   ```

2. **Install build dependencies (macOS/Linux):**
   ```bash
   # macOS
   xcode-select --install

   # Ubuntu/Debian
   sudo apt-get install python3-dev build-essential

   # Fedora/RHEL
   sudo dnf install python3-devel gcc
   ```

3. **Use pre-built wheels:**
   ```bash
   pip install --only-binary :all: pydantic pydantic-core
   ```

4. **Use minimal installation (skip pydantic/FastAPI):**
   ```bash
   pip install -r requirements-minimal.txt
   ```
   Note: This installs only what's needed for the WebSocket client. FastAPI features will be unavailable.

### Issue: "ModuleNotFoundError: No module named 'websockets'"

**Symptoms:**
```
ModuleNotFoundError: No module named 'websockets'
```

**Solutions:**

1. **Ensure virtual environment is activated:**
   ```bash
   # macOS/Linux
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python -c "import websockets; print(websockets.__version__)"
   ```

### Issue: Python version too old

**Symptoms:**
```
Python 3.9 is not supported
```

**Solutions:**

1. **Check your Python version:**
   ```bash
   python3 --version
   ```

2. **Install Python 3.11 or higher:**
   - **macOS:** `brew install python@3.11`
   - **Ubuntu:** `sudo apt-get install python3.11`
   - **Windows:** Download from [python.org](https://www.python.org/downloads/)

3. **Create virtual environment with specific Python version:**
   ```bash
   python3.11 -m venv venv
   ```

---

## Runtime Issues

### Issue: "Temporary failure in name resolution" or "Connection refused"

**Symptoms:**
```
socket.gaierror: [Errno -3] Temporary failure in name resolution
```

**Possible Causes:**

1. **No internet connection** - Binance WebSocket requires internet access
2. **Firewall blocking WebSocket connections** - Check firewall settings
3. **VPN issues** - Some VPNs block WebSocket connections
4. **DNS issues** - Try using Google DNS (8.8.8.8)

**Solutions:**

1. **Check internet connection:**
   ```bash
   ping binance.com
   ```

2. **Test WebSocket connectivity:**
   ```bash
   curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" \
        https://stream.binance.com:9443/ws/btcusdt@depth@100ms
   ```

3. **Try different network** - Connect to different WiFi or disable VPN

4. **Check firewall settings** - Ensure outbound WebSocket connections are allowed

### Issue: Application crashes or freezes

**Solutions:**

1. **Check logs** - Look for error messages in console output

2. **Reduce update frequency** - Edit `backend/src/config.py`:
   ```python
   UPDATE_SPEED: Final[str] = "1000ms"  # Changed from 100ms
   ```

3. **Increase timeout values** - Edit `backend/src/config.py`:
   ```python
   PING_TIMEOUT: Final[int] = 30  # Increased from 10
   ```

---

## Platform-Specific Issues

### macOS Issues

#### Issue: "Command line tools are not installed"

**Solution:**
```bash
xcode-select --install
```

#### Issue: M1/M2 Mac compatibility issues with compiled packages

**Solution:**
```bash
# Use Rosetta Python
arch -x86_64 python3 -m venv venv
arch -x86_64 venv/bin/pip install -r requirements.txt

# Or install ARM-native Python from Homebrew
brew install python@3.11
/opt/homebrew/bin/python3.11 -m venv venv
```

### Windows Issues

#### Issue: "Execution of scripts is disabled on this system"

**Solution:**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Issue: "'python' is not recognized as internal or external command"

**Solution:**
1. Add Python to PATH during installation
2. Or use `py` command instead of `python`:
   ```cmd
   py -m venv venv
   ```

### Linux Issues

#### Issue: "python3-venv is not installed"

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-venv python3-dev

# Fedora/RHEL
sudo dnf install python3-virtualenv python3-devel
```

---

## Getting Help

If none of these solutions work:

1. **Check Python version:** Must be 3.11 or higher
   ```bash
   python3 --version
   ```

2. **Check pip version:** Should be recent
   ```bash
   pip --version
   ```

3. **Try clean installation:**
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip setuptools wheel
   pip install -r requirements-minimal.txt
   ```

4. **Create an issue** on GitHub with:
   - Your operating system and version
   - Python version (`python3 --version`)
   - Pip version (`pip --version`)
   - Full error message
   - Output of `pip list`

---

## Quick Fixes Summary

```bash
# Clean installation
rm -rf venv
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# If that fails, use minimal installation
pip install -r requirements-minimal.txt

# Test the installation
python -c "import websockets; print('Success!')"

# Run the application
python run.py
```

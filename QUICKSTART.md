# Quick Start Guide

Get up and running with the Market Microstructure Analysis tool in 5 minutes.

## Prerequisites

- Python 3.11 or higher ([Download](https://www.python.org/downloads/))
- Internet connection
- Terminal/Command Prompt

## Installation Steps

### 1. Clone the Repository

```bash
git clone <https://github.com/jxdai2007/market-microstructure>
cd market-microstructure/backend
```

### 2. Run Setup Script

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

The script will:
- ✅ Verify Python version
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Handle errors automatically

### 3. Run the Application

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Run the application
python run.py
```

### 4. Watch the Magic ✨

You should see real-time order book data streaming:

```
================================================================================
ORDER BOOK UPDATE #1 - BTCUSDT
Timestamp: 14:32:18.456
================================================================================

📊 MARKET METRICS
--------------------------------------------------------------------------------
Midpoint Price:      $94,532.50
Spread:              $0.01 (0.11 bps)
Liquidity Imbalance: +2.34% (BID pressure)
...
```

Press `Ctrl+C` to stop.

## Alternative: Manual Installation

If the setup script doesn't work:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 3. Upgrade pip
pip install --upgrade pip setuptools wheel

# 4. Install dependencies
pip install -r requirements.txt
```

## Troubleshooting

### "Failed to build pydantic-core"

```bash
# Try minimal installation instead
pip install -r requirements-minimal.txt
```

### "ModuleNotFoundError: No module named 'websockets'"

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Then install
pip install websockets
```

### "Python version too old"

```bash
# Check your Python version
python3 --version

# Must be 3.11 or higher
# Download from: https://www.python.org/downloads/
```

### SSL Certificate Verification Errors

If you encounter SSL certificate verification errors:

**Symptoms:**
- `SSLCertVerificationError: certificate verify failed`
- Connection fails when starting the backend

**Quick Fix (Development Only):**
1. Open `backend/.env`
2. Add or update: `BINANCE_VERIFY_SSL=false`
3. Restart the backend

**⚠️ Security Warning:** Disabling SSL verification removes protection against man-in-the-middle attacks. Only use this setting for local development/testing.

**Proper Fix (Recommended for Production):**
1. Update your system's CA certificates
2. Ensure Python's `certifi` package is up to date: `pip install --upgrade certifi`
3. Keep `BINANCE_VERIFY_SSL=true` (or remove the setting to use the secure default)

### Still Having Issues?

See **[TROUBLESHOOTING.md](backend/TROUBLESHOOTING.md)** for comprehensive solutions.

## What You Get

Running `python run.py` displays:

- **Real-time order book** (top 10 bid/ask levels)
- **Market metrics:**
  - Bid-ask spread (absolute & basis points)
  - Midpoint price
  - Volume-weighted average price (VWAP)
  - Liquidity imbalance (market pressure indicator)
- **Live updates** every 100ms
- **Automatic reconnection** if connection drops

## Configuration

Edit `backend/src/config.py` to customize:

```python
# Change trading pair
SYMBOL: Final[str] = "ethusdt"  # Changed from "btcusdt"

# Change update frequency
UPDATE_SPEED: Final[str] = "1000ms"  # Changed from "100ms"

# Change order book depth
TOP_LEVELS: Final[int] = 20  # Changed from 10
```

## Next Steps

1. **Explore the code** - Clean architecture with comprehensive docstrings
2. **Modify metrics** - Add your own calculations in `src/metrics/calculator.py`
3. **Add new features** - The codebase is designed to be extensible
4. **Build frontend** - Phase 2 will add React visualization

## Getting Help

- **Installation issues:** See [TROUBLESHOOTING.md](backend/TROUBLESHOOTING.md)
- **Understanding the code:** Check docstrings and inline comments
- **Feature requests:** Open an issue on GitHub

---

**Happy trading! 📈**

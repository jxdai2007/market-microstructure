# Market Microstructure Analysis Tool

Real-time market microstructure analysis and visualization platform for cryptocurrency markets. Built to demonstrate production-quality software engineering for quantitative trading applications.

## Overview

This tool ingests real-time order book data from Binance, calculates key microstructure metrics, and provides live visualizations through a modern web interface. Designed for low-latency processing and clean, maintainable code.

## Features

### Current (Phase 1 - MVP)
- ✅ Real-time order book data ingestion from Binance WebSocket API
- ✅ Automatic reconnection with exponential backoff
- ✅ Market microstructure metrics calculation:
  - Bid-ask spread (absolute and basis points)
  - Midpoint price
  - Volume-weighted average price (VWAP)
  - Liquidity imbalance
  - Order book depth visualization
- ✅ Production-quality code with type hints and comprehensive docstrings
- ✅ Robust error handling and logging

### Roadmap (Future Phases)
- [ ] FastAPI WebSocket server for frontend streaming
- [ ] React frontend with real-time charts
- [ ] PostgreSQL/TimescaleDB integration for historical data
- [ ] Additional metrics (effective spread, order flow toxicity, market impact)
- [ ] Multi-symbol support
- [ ] Trade flow analysis
- [ ] Docker deployment configuration

## Tech Stack

**Backend:**
- Python 3.11+
- FastAPI
- WebSockets
- asyncio for concurrent processing

**Frontend (Coming Soon):**
- React 18+
- Chart.js / Recharts
- WebSocket client

**Database (Future):**
- PostgreSQL with TimescaleDB extension

## Quick Start

**Want to get started immediately?** See **[QUICKSTART.md](QUICKSTART.md)** for a 5-minute setup guide.

### Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd market-microstructure/backend

# 2. Run setup script
./setup.sh              # macOS/Linux
# OR
setup.bat               # Windows

# 3. Run the application
python run.py
```

You should see real-time order book updates with metrics streaming to your console.

**Encountering errors?** See [backend/TROUBLESHOOTING.md](backend/TROUBLESHOOTING.md)

### Manual Installation

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python run.py
```

## Project Structure

```
market-microstructure/
├── backend/
│   ├── src/
│   │   ├── binance/           # Binance WebSocket client
│   │   ├── metrics/           # Metrics calculation
│   │   ├── utils/             # Logging and utilities
│   │   ├── config.py          # Configuration
│   │   └── main.py            # Entry point (demo)
│   ├── requirements.txt
│   └── README.md
├── frontend/                  # Coming soon
└── README.md
```

## Architecture

The application follows clean architecture principles:

1. **Data Ingestion Layer** (`binance/websocket_client.py`)
   - Manages WebSocket connection to Binance
   - Handles reconnection and error recovery
   - Parses raw messages into structured data

2. **Domain Models** (`binance/models.py`)
   - Immutable data structures for order books
   - Built-in business logic (spread, midpoint calculations)
   - Type-safe with comprehensive validation

3. **Metrics Layer** (`metrics/calculator.py`)
   - Stateless calculators for microstructure metrics
   - VWAP, liquidity imbalance, spreads
   - Extensible for additional metrics

4. **Presentation Layer** (`main.py`)
   - Formatted console output (demo)
   - Future: FastAPI WebSocket server for frontend

## Configuration

Edit `backend/src/config.py` to customize:

- Trading pair (default: BTC/USDT)
- Update frequency (100ms or 1000ms)
- Order book depth
- Reconnection parameters
- Metrics calculation options

## Development Principles

This project demonstrates:

- **Type Safety**: Full type hints throughout
- **Clean Code**: Clear naming, single responsibility, DRY principles
- **Documentation**: Comprehensive docstrings for all public APIs
- **Error Handling**: Graceful degradation and informative logging
- **Async/Await**: Efficient concurrent programming
- **Separation of Concerns**: Clear architectural layers

## Use Cases

- Learning market microstructure concepts
- Algorithmic trading strategy research
- Market quality analysis
- Portfolio for quantitative developer interviews
- Foundation for building trading systems

## Contributing

This is a personal learning/portfolio project, but feedback and suggestions are welcome!

## License

MIT License - see LICENSE file for details

## Contact

Built as a portfolio project demonstrating software engineering skills for quantitative finance roles.

---

**Note**: This tool is for educational and research purposes. Always test thoroughly before using any trading-related software with real funds.

# Market Microstructure Analysis - Backend

Real-time market microstructure analysis tool for cryptocurrency markets. This backend connects to Binance WebSocket API to ingest order book data, calculate key microstructure metrics, and serve data to frontend clients.

## Features

- ✅ Real-time order book data ingestion from Binance WebSocket API
- ✅ Automatic reconnection with exponential backoff
- ✅ Calculation of key microstructure metrics:
  - Bid-ask spread (absolute and basis points)
  - Midpoint price
  - Volume-weighted average price (VWAP)
  - Liquidity imbalance
  - Total bid/ask volume
- ✅ Clean, production-quality code with type hints and docstrings
- ✅ Comprehensive error handling and logging

## Project Structure

```
backend/
├── src/
│   ├── binance/
│   │   ├── models.py              # Data models for order book
│   │   └── websocket_client.py    # WebSocket client implementation
│   ├── metrics/
│   │   └── calculator.py          # Metrics calculation
│   ├── utils/
│   │   └── logger.py              # Logging configuration
│   ├── config.py                  # Configuration settings
│   └── main.py                    # Entry point (demo)
├── requirements.txt
└── README.md
```

## Setup

### Prerequisites

- Python 3.11 or higher
- pip or poetry for package management

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Demo

The demo application connects to Binance WebSocket and displays real-time order book updates with calculated metrics:

```bash
# From the backend directory
python run.py

# Or activate the virtual environment first
source venv/bin/activate  # On Windows: venv\Scripts\activate
python run.py
```

You should see formatted output showing:
- Current order book (top 10 bid/ask levels)
- Market metrics (spread, midpoint, liquidity imbalance)
- VWAP calculations
- Real-time volume data

Press `Ctrl+C` to gracefully stop the application.

**See SAMPLE_OUTPUT.md for an example of what the output looks like with real data.**

### Configuration

Edit `src/config.py` to customize:

- **Symbol**: Change trading pair (default: `btcusdt`)
- **Update Speed**: Choose between `100ms` or `1000ms` updates
- **Order Book Depth**: Number of levels to display
- **Reconnection Settings**: Max attempts, delays, etc.

## Architecture

### BinanceOrderBookClient

The WebSocket client handles:
- Connection management with automatic reconnection
- Message parsing and validation
- Callback-based event handling
- Graceful shutdown

### OrderBook Model

Immutable data structure representing the order book state with:
- Sorted bid/ask levels
- Convenient access to best bid/ask
- Built-in spread and midpoint calculations

### MetricsCalculator

Stateless calculator for microstructure metrics:
- VWAP (Volume-Weighted Average Price)
- Liquidity imbalance ratio
- Spread in basis points
- Cumulative volume calculations

## Next Steps

- [ ] Implement FastAPI WebSocket server for frontend streaming
- [ ] Add data persistence (PostgreSQL/TimescaleDB)
- [ ] Implement additional metrics (effective spread, order flow toxicity)
- [ ] Add unit and integration tests
- [ ] Create Docker configuration
- [ ] Add frontend visualization

## Development

### Code Quality

This project follows best practices:
- Type hints throughout
- Comprehensive docstrings
- Clean architecture with separation of concerns
- Proper error handling and logging

### Future Enhancements

- Historical data storage and replay
- Multiple symbol support
- Order flow analysis
- Market impact estimation
- Integration with other exchanges

## License

MIT License - see LICENSE file for details

"""Configuration settings for the market microstructure analysis tool."""

import os
from pathlib import Path
from typing import Final
from dotenv import load_dotenv

# Load environment variables from .env file
# Look for .env in the backend directory (parent of src)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class BinanceConfig:
    """Binance WebSocket API configuration."""

    # WebSocket endpoints
    WS_BASE_URL: Final[str] = "wss://stream.binance.com:9443/ws"

    # Order book stream parameters
    SYMBOL: Final[str] = "btcusdt"
    STREAM_TYPE: Final[str] = "depth"  # Full order book updates
    UPDATE_SPEED: Final[str] = "100ms"  # Options: 1000ms (1s) or 100ms (or None for 1s default)

    # Connection settings
    RECONNECT_DELAY: Final[int] = 5  # seconds
    MAX_RECONNECT_ATTEMPTS: Final[int] = 10
    PING_INTERVAL: Final[int] = 20  # seconds
    PING_TIMEOUT: Final[int] = 10  # seconds

    # SSL/TLS Configuration
    VERIFY_SSL: Final[bool] = os.getenv('BINANCE_VERIFY_SSL', 'true').lower() != 'false'

    @classmethod
    def get_stream_url(cls) -> str:
        """Construct the WebSocket stream URL.

        Returns:
            str: Full WebSocket URL for the order book stream
        """
        # Format: wss://stream.binance.com:9443/ws/btcusdt@depth@100ms
        # OR: wss://stream.binance.com:9443/ws/btcusdt@depth for default (1s) updates
        if cls.UPDATE_SPEED:
            return f"{cls.WS_BASE_URL}/{cls.SYMBOL}@{cls.STREAM_TYPE}@{cls.UPDATE_SPEED}"
        else:
            return f"{cls.WS_BASE_URL}/{cls.SYMBOL}@{cls.STREAM_TYPE}"

    @classmethod
    def validate_ssl_config(cls) -> None:
        """Log warning if SSL verification is disabled."""
        if not cls.VERIFY_SSL:
            import logging
            logging.warning(
                "⚠️  SSL certificate verification is DISABLED. "
                "This should only be used for development/testing. "
                "DO NOT use in production!"
            )


class MetricsConfig:
    """Metrics calculation configuration."""

    # Order book depth to display
    TOP_LEVELS: Final[int] = 10

    # Metrics calculation settings
    CALCULATE_VWAP: Final[bool] = True
    CALCULATE_LIQUIDITY_IMBALANCE: Final[bool] = True


class LogConfig:
    """Logging configuration."""

    LEVEL: Final[str] = "INFO"
    FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"

"""Configuration settings for the market microstructure analysis tool."""

from typing import Final


class BinanceConfig:
    """Binance WebSocket API configuration."""

    # WebSocket endpoints
    WS_BASE_URL: Final[str] = "wss://stream.binance.com:9443/ws"

    # Order book stream parameters
    SYMBOL: Final[str] = "btcusdt"
    STREAM_TYPE: Final[str] = "depth"  # depth@100ms for 100ms updates
    UPDATE_SPEED: Final[str] = "100ms"  # Options: 1000ms (1s) or 100ms

    # Connection settings
    RECONNECT_DELAY: Final[int] = 5  # seconds
    MAX_RECONNECT_ATTEMPTS: Final[int] = 10
    PING_INTERVAL: Final[int] = 20  # seconds
    PING_TIMEOUT: Final[int] = 10  # seconds

    @classmethod
    def get_stream_url(cls) -> str:
        """Construct the WebSocket stream URL.

        Returns:
            str: Full WebSocket URL for the order book stream
        """
        return f"{cls.WS_BASE_URL}/{cls.SYMBOL}@{cls.STREAM_TYPE}@{cls.UPDATE_SPEED}"


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

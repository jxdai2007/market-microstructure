"""Binance WebSocket client for real-time order book data."""

import asyncio
import json
from typing import Callable, Optional, Any, Dict
import websockets
from websockets.client import WebSocketClientProtocol
from websockets.exceptions import ConnectionClosed, WebSocketException

from binance.models import OrderBook, OrderBookLevel
from config import BinanceConfig
from utils.logger import setup_logger


class BinanceOrderBookClient:
    """WebSocket client for Binance order book stream.

    Handles connection, reconnection, and parsing of order book data.
    Implements exponential backoff for reconnection attempts.
    """

    def __init__(
        self,
        on_orderbook_update: Optional[Callable[[OrderBook], None]] = None,
        symbol: str = BinanceConfig.SYMBOL
    ):
        """Initialize the Binance WebSocket client.

        Args:
            on_orderbook_update: Callback function for order book updates
            symbol: Trading pair symbol (default: btcusdt)
        """
        self.symbol = symbol
        self.url = BinanceConfig.get_stream_url()
        self.on_orderbook_update = on_orderbook_update

        self._websocket: Optional[WebSocketClientProtocol] = None
        self._running = False
        self._reconnect_attempts = 0

        self.logger = setup_logger(f"binance.{symbol}")

    async def connect(self) -> None:
        """Establish WebSocket connection and start receiving data.

        Implements automatic reconnection with exponential backoff.
        """
        self._running = True

        while self._running:
            try:
                self.logger.info(f"Connecting to Binance WebSocket: {self.url}")
                async with websockets.connect(
                    self.url,
                    ping_interval=BinanceConfig.PING_INTERVAL,
                    ping_timeout=BinanceConfig.PING_TIMEOUT
                ) as websocket:
                    self._websocket = websocket
                    self._reconnect_attempts = 0
                    self.logger.info("✓ Connected successfully")

                    await self._handle_messages()

            except ConnectionClosed as e:
                self.logger.warning(f"Connection closed: {e}")
                await self._handle_reconnect()

            except WebSocketException as e:
                self.logger.error(f"WebSocket error: {e}")
                await self._handle_reconnect()

            except Exception as e:
                self.logger.error(f"Unexpected error: {e}", exc_info=True)
                await self._handle_reconnect()

        self.logger.info("WebSocket client stopped")

    async def _handle_messages(self) -> None:
        """Process incoming WebSocket messages."""
        if not self._websocket:
            return

        async for message in self._websocket:
            try:
                await self._process_message(message)
            except Exception as e:
                self.logger.error(f"Error processing message: {e}", exc_info=True)

    async def _process_message(self, message: str) -> None:
        """Parse and process a single WebSocket message.

        Args:
            message: Raw JSON message from WebSocket
        """
        try:
            data = json.loads(message)

            # Binance depth stream format
            if 'e' in data and data['e'] == 'depthUpdate':
                order_book = self._parse_order_book(data)
                if order_book and self.on_orderbook_update:
                    self.on_orderbook_update(order_book)
            else:
                self.logger.debug(f"Received non-depth message: {data.get('e', 'unknown')}")

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON: {e}")
        except Exception as e:
            self.logger.error(f"Error parsing message: {e}", exc_info=True)

    def _parse_order_book(self, data: Dict[str, Any]) -> Optional[OrderBook]:
        """Parse raw Binance order book data into OrderBook model.

        Args:
            data: Raw order book data from WebSocket

        Returns:
            OrderBook instance or None if parsing fails
        """
        try:
            bids = [OrderBookLevel.from_list(bid) for bid in data.get('b', [])]
            asks = [OrderBookLevel.from_list(ask) for ask in data.get('a', [])]

            # Sort bids descending (highest first), asks ascending (lowest first)
            bids.sort(key=lambda x: x.price, reverse=True)
            asks.sort(key=lambda x: x.price)

            return OrderBook(
                symbol=data.get('s', self.symbol),
                bids=bids,
                asks=asks,
                last_update_id=data.get('u', 0),
                timestamp=data.get('E', 0)
            )

        except (KeyError, ValueError, IndexError) as e:
            self.logger.error(f"Failed to parse order book: {e}")
            return None

    async def _handle_reconnect(self) -> None:
        """Handle reconnection with exponential backoff."""
        if not self._running:
            return

        self._reconnect_attempts += 1

        if self._reconnect_attempts > BinanceConfig.MAX_RECONNECT_ATTEMPTS:
            self.logger.error(
                f"Max reconnection attempts ({BinanceConfig.MAX_RECONNECT_ATTEMPTS}) reached. Stopping."
            )
            self._running = False
            return

        # Exponential backoff: 5s, 10s, 20s, 40s, etc.
        delay = min(
            BinanceConfig.RECONNECT_DELAY * (2 ** (self._reconnect_attempts - 1)),
            60  # Cap at 60 seconds
        )

        self.logger.info(
            f"Reconnecting in {delay}s (attempt {self._reconnect_attempts}/"
            f"{BinanceConfig.MAX_RECONNECT_ATTEMPTS})"
        )
        await asyncio.sleep(delay)

    async def disconnect(self) -> None:
        """Gracefully disconnect from WebSocket."""
        self.logger.info("Disconnecting...")
        self._running = False

        if self._websocket:
            await self._websocket.close()
            self._websocket = None

    @property
    def is_connected(self) -> bool:
        """Check if WebSocket is currently connected.

        Returns:
            True if connected, False otherwise
        """
        return self._websocket is not None and not self._websocket.closed

"""Main entry point for the market microstructure analysis backend.

This module provides a simple demo that connects to Binance WebSocket,
receives order book updates, calculates metrics, and displays them in the console.
"""

import asyncio
import signal
from datetime import datetime
from typing import Optional

from binance.websocket_client import BinanceOrderBookClient
from binance.models import OrderBook
from metrics.calculator import MetricsCalculator
from config import MetricsConfig
from utils.logger import setup_logger


logger = setup_logger("main")


class OrderBookPrinter:
    """Handles formatted console output of order book data and metrics."""

    def __init__(self, top_levels: int = MetricsConfig.TOP_LEVELS):
        """Initialize the printer.

        Args:
            top_levels: Number of order book levels to display
        """
        self.top_levels = top_levels
        self.update_count = 0

    def print_order_book(self, order_book: OrderBook) -> None:
        """Print formatted order book with metrics.

        Args:
            order_book: Order book to display
        """
        self.update_count += 1

        # Calculate metrics
        metrics = MetricsCalculator.calculate_all(order_book)

        # Clear previous output (optional, comment out if you want history)
        print("\n" + "=" * 80)
        print(f"ORDER BOOK UPDATE #{self.update_count} - {metrics.symbol.upper()}")
        print(f"Timestamp: {datetime.fromtimestamp(metrics.timestamp / 1000).strftime('%H:%M:%S.%f')[:-3]}")
        print("=" * 80)

        # Print metrics
        print("\n📊 MARKET METRICS")
        print("-" * 80)
        if metrics.midpoint:
            print(f"Midpoint Price:      ${metrics.midpoint:,.2f}")
        if metrics.spread:
            print(f"Spread:              ${metrics.spread:.2f} ({metrics.spread_bps:.2f} bps)")
        if metrics.liquidity_imbalance:
            imbalance_pct = float(metrics.liquidity_imbalance) * 100
            side = "BID" if imbalance_pct > 0 else "ASK"
            print(f"Liquidity Imbalance: {imbalance_pct:+.2f}% ({side} pressure)")

        print(f"\nBid Volume (top {self.top_levels}): {metrics.total_bid_volume:,.4f} BTC")
        print(f"Ask Volume (top {self.top_levels}): {metrics.total_ask_volume:,.4f} BTC")

        if metrics.vwap_bid and metrics.vwap_ask:
            print(f"\nVWAP Bid:            ${metrics.vwap_bid:,.2f}")
            print(f"VWAP Ask:            ${metrics.vwap_ask:,.2f}")

        # Print order book levels
        bids, asks = order_book.get_top_levels(self.top_levels)

        print(f"\n📖 ORDER BOOK (Top {self.top_levels} Levels)")
        print("-" * 80)
        print(f"{'BIDS':<40} | {'ASKS':<40}")
        print(f"{'Price':<15} {'Quantity':<15} {'Total':<10} | {'Price':<15} {'Quantity':<15} {'Total':<10}")
        print("-" * 80)

        # Calculate cumulative volumes
        bid_cumulative = 0
        ask_cumulative = 0

        max_levels = max(len(bids), len(asks))
        for i in range(max_levels):
            # Bid side
            if i < len(bids):
                bid = bids[i]
                bid_cumulative += float(bid.quantity)
                bid_str = f"${bid.price:<13,.2f} {bid.quantity:<13,.4f} {bid_cumulative:<10,.2f}"
            else:
                bid_str = " " * 40

            # Ask side
            if i < len(asks):
                ask = asks[i]
                ask_cumulative += float(ask.quantity)
                ask_str = f"${ask.price:<13,.2f} {ask.quantity:<13,.4f} {ask_cumulative:<10,.2f}"
            else:
                ask_str = " " * 40

            print(f"{bid_str} | {ask_str}")

        print("=" * 80 + "\n")


async def main() -> None:
    """Main application entry point."""
    logger.info("🚀 Starting Market Microstructure Analysis Tool")
    logger.info(f"Connecting to Binance WebSocket for {BinanceOrderBookClient.__name__}")

    # Create order book printer
    printer = OrderBookPrinter()

    # Create WebSocket client with callback
    client = BinanceOrderBookClient(
        on_orderbook_update=printer.print_order_book
    )

    # Set up graceful shutdown
    shutdown_event = asyncio.Event()

    def signal_handler(signum, frame):
        logger.info("Shutdown signal received")
        shutdown_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start WebSocket client
    client_task = asyncio.create_task(client.connect())

    try:
        # Wait for shutdown signal
        await shutdown_event.wait()
    finally:
        logger.info("Shutting down...")
        await client.disconnect()
        await asyncio.wait_for(client_task, timeout=5.0)
        logger.info("Shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)

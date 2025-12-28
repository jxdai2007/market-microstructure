"""Market microstructure metrics calculator."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from binance.models import OrderBook, OrderBookLevel
from config import MetricsConfig


@dataclass
class MicrostructureMetrics:
    """Container for calculated market microstructure metrics.

    Attributes:
        symbol: Trading pair symbol
        timestamp: Event timestamp
        bid_price: Best bid price
        ask_price: Best ask price
        midpoint: Midpoint price
        spread: Bid-ask spread (absolute)
        spread_bps: Bid-ask spread in basis points
        total_bid_volume: Total volume on bid side (top N levels)
        total_ask_volume: Total volume on ask side (top N levels)
        liquidity_imbalance: Ratio of bid to ask volume
        vwap_bid: Volume-weighted average price (bid side)
        vwap_ask: Volume-weighted average price (ask side)
    """
    symbol: str
    timestamp: int
    bid_price: Optional[Decimal]
    ask_price: Optional[Decimal]
    midpoint: Optional[Decimal]
    spread: Optional[Decimal]
    spread_bps: Optional[Decimal]
    total_bid_volume: Decimal
    total_ask_volume: Decimal
    liquidity_imbalance: Optional[Decimal]
    vwap_bid: Optional[Decimal]
    vwap_ask: Optional[Decimal]

    def to_dict(self) -> dict:
        """Convert metrics to dictionary for JSON serialization."""
        return {
            'symbol': self.symbol,
            'timestamp': self.timestamp,
            'bid_price': str(self.bid_price) if self.bid_price else None,
            'ask_price': str(self.ask_price) if self.ask_price else None,
            'midpoint': str(self.midpoint) if self.midpoint else None,
            'spread': str(self.spread) if self.spread else None,
            'spread_bps': str(self.spread_bps) if self.spread_bps else None,
            'total_bid_volume': str(self.total_bid_volume),
            'total_ask_volume': str(self.total_ask_volume),
            'liquidity_imbalance': str(self.liquidity_imbalance) if self.liquidity_imbalance else None,
            'vwap_bid': str(self.vwap_bid) if self.vwap_bid else None,
            'vwap_ask': str(self.vwap_ask) if self.vwap_ask else None,
        }


class MetricsCalculator:
    """Calculate market microstructure metrics from order book data."""

    @staticmethod
    def calculate_vwap(levels: list[OrderBookLevel], depth: int = 10) -> Optional[Decimal]:
        """Calculate Volume-Weighted Average Price.

        Args:
            levels: List of order book levels
            depth: Number of levels to include

        Returns:
            VWAP as Decimal, or None if no volume
        """
        if not levels:
            return None

        total_value = Decimal('0')
        total_volume = Decimal('0')

        for level in levels[:depth]:
            total_value += level.price * level.quantity
            total_volume += level.quantity

        if total_volume == 0:
            return None

        return total_value / total_volume

    @staticmethod
    def calculate_liquidity_imbalance(
        bid_volume: Decimal,
        ask_volume: Decimal
    ) -> Optional[Decimal]:
        """Calculate liquidity imbalance ratio.

        Imbalance = (bid_volume - ask_volume) / (bid_volume + ask_volume)

        Args:
            bid_volume: Total bid side volume
            ask_volume: Total ask side volume

        Returns:
            Imbalance ratio between -1 and 1, or None if total volume is zero
            Positive values indicate more bid pressure, negative more ask pressure
        """
        total_volume = bid_volume + ask_volume

        if total_volume == 0:
            return None

        return (bid_volume - ask_volume) / total_volume

    @staticmethod
    def calculate_all(order_book: OrderBook) -> MicrostructureMetrics:
        """Calculate all microstructure metrics from order book.

        Args:
            order_book: Current order book state

        Returns:
            MicrostructureMetrics instance with all calculated metrics
        """
        # Basic metrics
        best_bid = order_book.best_bid
        best_ask = order_book.best_ask

        # Volume metrics
        total_bid_volume = order_book.total_volume('bid', MetricsConfig.TOP_LEVELS)
        total_ask_volume = order_book.total_volume('ask', MetricsConfig.TOP_LEVELS)

        # VWAP calculations
        vwap_bid = None
        vwap_ask = None
        if MetricsConfig.CALCULATE_VWAP:
            vwap_bid = MetricsCalculator.calculate_vwap(
                order_book.bids,
                MetricsConfig.TOP_LEVELS
            )
            vwap_ask = MetricsCalculator.calculate_vwap(
                order_book.asks,
                MetricsConfig.TOP_LEVELS
            )

        # Liquidity imbalance
        liquidity_imbalance = None
        if MetricsConfig.CALCULATE_LIQUIDITY_IMBALANCE:
            liquidity_imbalance = MetricsCalculator.calculate_liquidity_imbalance(
                total_bid_volume,
                total_ask_volume
            )

        return MicrostructureMetrics(
            symbol=order_book.symbol,
            timestamp=order_book.timestamp,
            bid_price=best_bid.price if best_bid else None,
            ask_price=best_ask.price if best_ask else None,
            midpoint=order_book.midpoint,
            spread=order_book.spread,
            spread_bps=order_book.spread_bps,
            total_bid_volume=total_bid_volume,
            total_ask_volume=total_ask_volume,
            liquidity_imbalance=liquidity_imbalance,
            vwap_bid=vwap_bid,
            vwap_ask=vwap_ask
        )

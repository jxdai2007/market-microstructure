"""Data models for Binance order book data."""

from dataclasses import dataclass
from decimal import Decimal
from typing import List, Tuple


@dataclass
class OrderBookLevel:
    """Represents a single price level in the order book.

    Attributes:
        price: Price level
        quantity: Total quantity at this price level
    """
    price: Decimal
    quantity: Decimal

    @classmethod
    def from_list(cls, data: List[str]) -> "OrderBookLevel":
        """Create OrderBookLevel from Binance API list format.

        Args:
            data: List containing [price, quantity] as strings

        Returns:
            OrderBookLevel instance
        """
        return cls(
            price=Decimal(data[0]),
            quantity=Decimal(data[1])
        )

    def __repr__(self) -> str:
        return f"OrderBookLevel(price={self.price}, qty={self.quantity})"


@dataclass
class OrderBook:
    """Represents the current state of the order book.

    Attributes:
        symbol: Trading pair symbol
        bids: List of bid levels (price, quantity) sorted by price descending
        asks: List of ask levels (price, quantity) sorted by price ascending
        last_update_id: Last update ID from exchange
        timestamp: Event timestamp from exchange
    """
    symbol: str
    bids: List[OrderBookLevel]
    asks: List[OrderBookLevel]
    last_update_id: int
    timestamp: int

    @property
    def best_bid(self) -> OrderBookLevel | None:
        """Get the best (highest) bid price level."""
        return self.bids[0] if self.bids else None

    @property
    def best_ask(self) -> OrderBookLevel | None:
        """Get the best (lowest) ask price level."""
        return self.asks[0] if self.asks else None

    @property
    def spread(self) -> Decimal | None:
        """Calculate the bid-ask spread.

        Returns:
            Spread as Decimal, or None if order book is incomplete
        """
        if not self.best_bid or not self.best_ask:
            return None
        return self.best_ask.price - self.best_bid.price

    @property
    def midpoint(self) -> Decimal | None:
        """Calculate the midpoint price.

        Returns:
            Midpoint as Decimal, or None if order book is incomplete
        """
        if not self.best_bid or not self.best_ask:
            return None
        return (self.best_bid.price + self.best_ask.price) / Decimal('2')

    @property
    def spread_bps(self) -> Decimal | None:
        """Calculate spread in basis points (bps).

        Returns:
            Spread in basis points, or None if order book is incomplete
        """
        if not self.spread or not self.midpoint or self.midpoint == 0:
            return None
        return (self.spread / self.midpoint) * Decimal('10000')

    def total_volume(self, side: str, levels: int = 10) -> Decimal:
        """Calculate total volume for a given side.

        Args:
            side: 'bid' or 'ask'
            levels: Number of levels to include

        Returns:
            Total volume as Decimal
        """
        levels_list = self.bids if side == 'bid' else self.asks
        return sum(level.quantity for level in levels_list[:levels])

    def get_top_levels(self, n: int = 10) -> Tuple[List[OrderBookLevel], List[OrderBookLevel]]:
        """Get top N levels from both sides.

        Args:
            n: Number of levels to return

        Returns:
            Tuple of (top_bids, top_asks)
        """
        return self.bids[:n], self.asks[:n]

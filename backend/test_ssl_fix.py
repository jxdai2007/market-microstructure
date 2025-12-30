#!/usr/bin/env python3
"""Quick test script to verify SSL fix works."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from binance.websocket_client import BinanceOrderBookClient
from config import BinanceConfig

async def test_connection():
    """Test WebSocket connection with SSL settings."""
    print(f"SSL Verification: {'ENABLED' if BinanceConfig.VERIFY_SSL else 'DISABLED'}")
    print(f"Connecting to: {BinanceConfig.get_stream_url()}")
    print("-" * 60)

    received_data = False

    def on_update(orderbook):
        nonlocal received_data
        if not received_data:
            print(f"✓ Successfully received data!")
            print(f"  Symbol: {orderbook.symbol}")
            print(f"  Bids: {len(orderbook.bids)}, Asks: {len(orderbook.asks)}")
            received_data = True

    client = BinanceOrderBookClient(on_orderbook_update=on_update)

    # Start connection
    task = asyncio.create_task(client.connect())

    # Wait up to 10 seconds for data
    for i in range(10):
        await asyncio.sleep(1)
        if received_data:
            print(f"\n✓ Connection test PASSED!")
            break
    else:
        print(f"\n✗ No data received after 10 seconds")

    # Cleanup
    await client.disconnect()
    try:
        await asyncio.wait_for(task, timeout=2)
    except asyncio.TimeoutError:
        pass

if __name__ == "__main__":
    try:
        asyncio.run(test_connection())
    except KeyboardInterrupt:
        print("\nTest interrupted")
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

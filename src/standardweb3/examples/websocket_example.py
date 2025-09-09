"""WebSocket connection example for Standard Protocol.

This example demonstrates how to connect to the Standard Protocol WebSocket
to receive real-time trading data including trades, orders, and market updates.
"""

import asyncio
import json
import websockets
from typing import Dict, Any
from standardweb3 import StandardClient
from standardweb3.types import (
    SpotTradeEvent,
    SpotOrderEvent,
    SpotOrderHistoryEvent,
    SpotBarEvent,
    stream_to_spot_trade_event,
    stream_to_spot_order_event,
    stream_to_spot_order_history_event,
    stream_to_spot_bar_event,
)


class StandardWebSocketClient:
    """Enhanced WebSocket client for Standard Protocol with stream type parsing."""

    def __init__(self, websocket_url: str):
        """Initialize the WebSocket client.

        Args:
            websocket_url: WebSocket server URL
        """
        self.websocket_url = websocket_url
        self.websocket = None
        self.is_connected = False
        self.subscriptions = set()

    async def connect(self):
        """Connect to the WebSocket server."""
        try:
            print(f"Connecting to WebSocket: {self.websocket_url}")
            self.websocket = await websockets.connect(self.websocket_url)
            self.is_connected = True
            print("✅ Connected to Standard Protocol WebSocket")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            self.is_connected = False
            return False

    async def disconnect(self):
        """Disconnect from the WebSocket server."""
        if self.websocket and self.is_connected:
            await self.websocket.close()
            self.is_connected = False
            print("🔌 Disconnected from WebSocket")

    async def send_message(self, message: Dict[str, Any]):
        """Send a message to the WebSocket server.

        Args:
            message: Message dictionary to send
        """
        if not self.is_connected:
            print("❌ Not connected to WebSocket")
            return

        try:
            message_str = json.dumps(message)
            await self.websocket.send(message_str)
            print(f"📤 Sent: {message_str}")
        except Exception as e:
            print(f"❌ Failed to send message: {e}")

    async def subscribe_to_trades(self, pair: str = None):
        """Subscribe to trade updates.

        Args:
            pair: Trading pair (e.g., "ETH/USDC"). If None, subscribes to all pairs.
        """
        subscription = {
            "type": "subscribe",
            "channel": "trades",
        }
        if pair:
            subscription["pair"] = pair

        await self.send_message(subscription)
        self.subscriptions.add(f"trades:{pair or 'all'}")
        print(f"📊 Subscribed to trades for {pair or 'all pairs'}")

    async def subscribe_to_orders(self, account: str = None):
        """Subscribe to order updates.

        Args:
            account: Account address. If None, subscribes to all orders.
        """
        subscription = {
            "type": "subscribe",
            "channel": "orders",
        }
        if account:
            subscription["account"] = account

        await self.send_message(subscription)
        self.subscriptions.add(f"orders:{account or 'all'}")
        print(f"📋 Subscribed to orders for {account or 'all accounts'}")

    async def subscribe_to_orderbook(self, pair: str):
        """Subscribe to orderbook updates.

        Args:
            pair: Trading pair (e.g., "ETH/USDC")
        """
        subscription = {"type": "subscribe", "channel": "orderbook", "pair": pair}
        await self.send_message(subscription)
        self.subscriptions.add(f"orderbook:{pair}")
        print(f"📖 Subscribed to orderbook for {pair}")

    async def subscribe_to_bars(self, pair: str, interval: str = "1m"):
        """Subscribe to price bar updates.

        Args:
            pair: Trading pair (e.g., "ETH/USDC")
            interval: Time interval (1m, 5m, 15m, 1h, 1d)
        """
        subscription = {
            "type": "subscribe",
            "channel": "bars",
            "pair": pair,
            "interval": interval,
        }
        await self.send_message(subscription)
        self.subscriptions.add(f"bars:{pair}:{interval}")
        print(f"📈 Subscribed to {interval} bars for {pair}")

    def parse_stream_data(self, data: Dict[str, Any]):
        """Parse incoming stream data into typed objects.

        Args:
            data: Raw stream data from WebSocket

        Returns:
            Parsed event object or None if parsing fails
        """
        try:
            channel = data.get("channel")
            stream_data = data.get("data")

            if not stream_data:
                return None

            # Convert list/tuple data to appropriate event types
            if channel == "trades" and isinstance(stream_data, (list, tuple)):
                return stream_to_spot_trade_event(tuple(stream_data))
            elif channel == "orders" and isinstance(stream_data, (list, tuple)):
                return stream_to_spot_order_event(tuple(stream_data))
            elif channel == "orderHistory" and isinstance(stream_data, (list, tuple)):
                return stream_to_spot_order_history_event(tuple(stream_data))
            elif channel == "bars" and isinstance(stream_data, (list, tuple)):
                return stream_to_spot_bar_event(tuple(stream_data))
            else:
                # Return raw data if no specific parser available
                return stream_data

        except Exception as e:
            print(f"⚠️ Failed to parse stream data: {e}")
            return None

    async def handle_message(self, message: str):
        """Handle incoming WebSocket messages.

        Args:
            message: Raw message string from WebSocket
        """
        try:
            data = json.loads(message)
            channel = data.get("channel")

            # Parse the stream data
            parsed_data = self.parse_stream_data(data)

            if channel == "trades" and isinstance(parsed_data, SpotTradeEvent):
                await self.handle_trade_update(parsed_data)
            elif channel == "orders" and isinstance(parsed_data, SpotOrderEvent):
                await self.handle_order_update(parsed_data)
            elif channel == "orderHistory" and isinstance(
                parsed_data, SpotOrderHistoryEvent
            ):
                await self.handle_order_history_update(parsed_data)
            elif channel == "bars" and isinstance(parsed_data, SpotBarEvent):
                await self.handle_bar_update(parsed_data)
            elif channel == "orderbook":
                await self.handle_orderbook_update(data.get("data", {}))
            else:
                print(f"📨 Received message: {data}")

        except json.JSONDecodeError:
            print(f"⚠️ Invalid JSON received: {message}")
        except Exception as e:
            print(f"❌ Error handling message: {e}")

    async def handle_trade_update(self, trade: SpotTradeEvent):
        """Handle trade update events.

        Args:
            trade: Parsed trade event
        """
        print(f"💰 TRADE: {trade.base_symbol}/{trade.quote_symbol}")
        print(f"    Price: ${trade.price}")
        print(f"    Amount: {trade.amount} {trade.base_symbol}")
        print(f"    Value: ${trade.value_usd}")
        print(f"    Side: {'BUY' if trade.is_bid else 'SELL'}")
        print(f"    Time: {trade.timestamp}")

    async def handle_order_update(self, order: SpotOrderEvent):
        """Handle order update events.

        Args:
            order: Parsed order event
        """
        print(f"📋 ORDER: {order.base_symbol}/{order.quote_symbol}")
        print(f"    Order ID: {order.order_id}")
        print(f"    Price: ${order.price}")
        print(f"    Amount: {order.amount}")
        print(f"    Side: {'BUY' if order.is_bid else 'SELL'}")

    async def handle_order_history_update(self, order_history: SpotOrderHistoryEvent):
        """Handle order history update events.

        Args:
            order_history: Parsed order history event
        """
        print(
            f"📚 ORDER HISTORY: {order_history.base_symbol}/{order_history.quote_symbol}"
        )
        print(f"    Order ID: {order_history.order_id}")
        print(f"    Status: {order_history.status}")
        print(f"    Executed: {order_history.executed}")
        print(f"    Price: ${order_history.price}")

    async def handle_bar_update(self, bar: SpotBarEvent):
        """Handle price bar update events.

        Args:
            bar: Parsed bar event
        """
        print(f"📈 BAR: {bar.id}")
        print(f"    Price: ${bar.price}")
        print(f"    Base Volume: {bar.base_volume}")
        print(f"    Quote Volume: {bar.quote_volume}")
        print(f"    USD Volume: ${bar.volume_usd}")

    async def handle_orderbook_update(self, orderbook_data: Dict[str, Any]):
        """Handle orderbook update events.

        Args:
            orderbook_data: Raw orderbook data
        """
        print("📖 ORDERBOOK UPDATE:")
        if "bids" in orderbook_data:
            print(
                "    Best Bid: "
                f"{orderbook_data['bids'][0] if orderbook_data['bids'] else 'N/A'}"
            )
        if "asks" in orderbook_data:
            print(
                "    Best Ask: "
                f"{orderbook_data['asks'][0] if orderbook_data['asks'] else 'N/A'}"
            )

    async def listen(self):
        """Listen for incoming messages."""
        if not self.is_connected:
            print("❌ Not connected to WebSocket")
            return

        try:
            print("👂 Listening for messages...")
            async for message in self.websocket:
                await self.handle_message(message)
        except websockets.exceptions.ConnectionClosed:
            print("🔌 WebSocket connection closed")
            self.is_connected = False
        except Exception as e:
            print(f"❌ Error while listening: {e}")
            self.is_connected = False


async def basic_websocket_example():
    """Demonstrate basic WebSocket connection."""
    print("🚀 Basic WebSocket Example")
    print("=" * 50)

    # Initialize the Standard client
    # Note: You'll need to provide your actual credentials
    client = StandardClient(
        private_key="your_private_key_here",  # Replace with your private key
        http_rpc_url="https://your-rpc-url.com",  # Replace with your RPC URL
        networkName="Somnia Testnet",
        matching_engine_address=(
            "0x1234567890123456789012345678901234567890"  # Replace with actual address
        ),
    )

    # Get the WebSocket URL
    websocket_url = client.websocket_url
    print(f"WebSocket URL: {websocket_url}")

    # Create WebSocket client
    ws_client = StandardWebSocketClient(websocket_url)

    try:
        # Connect to WebSocket
        if await ws_client.connect():
            # Subscribe to different channels
            await ws_client.subscribe_to_trades("ETH/USDC")
            await ws_client.subscribe_to_orderbook("ETH/USDC")
            await ws_client.subscribe_to_bars("ETH/USDC", "1m")

            # Listen for messages for 30 seconds
            print("\n⏰ Listening for 30 seconds...")
            try:
                await asyncio.wait_for(ws_client.listen(), timeout=30.0)
            except asyncio.TimeoutError:
                print("⏰ Timeout reached, stopping...")

    except Exception as e:
        print(f"❌ Error in example: {e}")
    finally:
        await ws_client.disconnect()


async def advanced_websocket_example():
    """Advanced WebSocket example with custom message handling."""
    print("\n🚀 Advanced WebSocket Example")
    print("=" * 50)

    # Custom WebSocket client with additional features
    class AdvancedWebSocketClient(StandardWebSocketClient):
        def __init__(self, websocket_url: str):
            super().__init__(websocket_url)
            self.trade_count = 0
            self.order_count = 0

        async def handle_trade_update(self, trade: SpotTradeEvent):
            """Handle trade updates with statistics."""
            self.trade_count += 1
            print(
                f"💰 Trade #{self.trade_count}: "
                f"{trade.base_symbol}/{trade.quote_symbol} @ ${trade.price}"
            )

        async def handle_order_update(self, order: SpotOrderEvent):
            """Handle order updates with statistics."""
            self.order_count += 1
            print(
                f"📋 Order #{self.order_count}: {order.base_symbol}/{order.quote_symbol}"
            )

        def get_stats(self):
            """Get connection statistics."""
            return {
                "trades_received": self.trade_count,
                "orders_received": self.order_count,
                "active_subscriptions": len(self.subscriptions),
            }

    # Initialize advanced client
    websocket_url = (
        "wss://story-odyssey-websocket.standardweb3.com"  # Default testnet URL
    )
    ws_client = AdvancedWebSocketClient(websocket_url)

    try:
        if await ws_client.connect():
            # Subscribe to multiple pairs
            pairs = ["ETH/USDC", "BTC/USDT"]
            for pair in pairs:
                await ws_client.subscribe_to_trades(pair)
                await ws_client.subscribe_to_bars(pair, "5m")

            # Listen for messages
            print(f"\n⏰ Listening for messages on {len(pairs)} pairs...")
            try:
                await asyncio.wait_for(ws_client.listen(), timeout=60.0)
            except asyncio.TimeoutError:
                print("⏰ Timeout reached")

            # Print statistics
            stats = ws_client.get_stats()
            print("\n📊 Session Statistics:")
            print(f"    Trades received: {stats['trades_received']}")
            print(f"    Orders received: {stats['orders_received']}")
            print(f"    Active subscriptions: {stats['active_subscriptions']}")

    except Exception as e:
        print(f"❌ Error in advanced example: {e}")
    finally:
        await ws_client.disconnect()


async def reconnection_example():
    """Demonstrate automatic reconnection logic."""
    print("\n🚀 WebSocket Reconnection Example")
    print("=" * 50)

    class ReconnectingWebSocketClient(StandardWebSocketClient):
        def __init__(self, websocket_url: str, max_retries: int = 5):
            super().__init__(websocket_url)
            self.max_retries = max_retries
            self.retry_count = 0

        async def connect_with_retry(self):
            """Connect with automatic retry logic."""
            while self.retry_count < self.max_retries:
                try:
                    if await self.connect():
                        self.retry_count = 0  # Reset on successful connection
                        return True
                except Exception as e:
                    print(f"❌ Connection attempt {self.retry_count + 1} failed: {e}")

                self.retry_count += 1
                if self.retry_count < self.max_retries:
                    wait_time = min(2**self.retry_count, 30)  # Exponential backoff
                    print(f"⏳ Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)

            print(f"❌ Failed to connect after {self.max_retries} attempts")
            return False

        async def listen_with_reconnect(self):
            """Listen with automatic reconnection."""
            while True:
                try:
                    if not self.is_connected:
                        if not await self.connect_with_retry():
                            break

                        # Re-subscribe after reconnection
                        await self.subscribe_to_trades("ETH/USDC")

                    await self.listen()
                except Exception as e:
                    print(f"❌ Listen error: {e}")
                    self.is_connected = False
                    await asyncio.sleep(5)  # Wait before retry

    # Test reconnecting client
    websocket_url = "wss://story-odyssey-websocket.standardweb3.com"
    ws_client = ReconnectingWebSocketClient(websocket_url)

    try:
        print("🔄 Starting reconnecting WebSocket client...")
        await asyncio.wait_for(ws_client.listen_with_reconnect(), timeout=120.0)
    except asyncio.TimeoutError:
        print("⏰ Timeout reached")
    except KeyboardInterrupt:
        print("\n⏹️ Interrupted by user")
    finally:
        await ws_client.disconnect()


async def main():
    """Run all WebSocket examples."""
    print("🌟 Standard Protocol WebSocket Examples")
    print("=" * 60)

    try:
        # Run basic example
        await basic_websocket_example()

        # Wait between examples
        await asyncio.sleep(2)

        # Run advanced example
        await advanced_websocket_example()

        # Wait between examples
        await asyncio.sleep(2)

        # Run reconnection example
        await reconnection_example()

    except KeyboardInterrupt:
        print("\n⏹️ Examples interrupted by user")
    except Exception as e:
        print(f"❌ Error in main: {e}")

    print("\n✅ WebSocket examples completed!")


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())

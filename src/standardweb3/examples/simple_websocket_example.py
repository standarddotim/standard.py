"""Simple WebSocket example for Standard Protocol.

A minimal example showing how to connect to the Standard Protocol WebSocket
and receive real-time trading data.
"""

import asyncio
import json
from standardweb3 import StandardClient


async def simple_websocket_connection():
    """Connect to WebSocket using StandardClient."""
    # Initialize the Standard client
    # Replace these with your actual credentials
    client = StandardClient(
        private_key="your_private_key_here",
        http_rpc_url="https://your-rpc-url.com",
        networkName="Somnia Testnet",  # Use predefined network
        matching_engine_address="0x1234567890123456789012345678901234567890",
    )

    print(f"🔗 Connecting to: {client.websocket_url}")

    # Start the WebSocket connection
    try:
        await client.start_ws()
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")


async def custom_websocket_handler():
    """Handle WebSocket messages with custom processing."""
    import websockets

    # WebSocket URL for Somnia Testnet
    websocket_url = "wss://story-odyssey-websocket.standardweb3.com"

    try:
        print(f"🔗 Connecting to {websocket_url}")

        async with websockets.connect(websocket_url) as websocket:
            print("✅ Connected!")

            # Send subscription message for trades
            subscribe_message = {
                "type": "subscribe",
                "channel": "trades",
                "pair": "ETH/USDC",
            }

            await websocket.send(json.dumps(subscribe_message))
            print("📤 Subscribed to ETH/USDC trades")

            # Listen for messages
            message_count = 0
            while message_count < 10:  # Limit to 10 messages for demo
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                    message_count += 1

                    # Parse and display the message
                    try:
                        data = json.loads(message)
                        print(f"📨 Message {message_count}: {data}")
                    except json.JSONDecodeError:
                        print(f"📨 Raw message {message_count}: {message}")

                except asyncio.TimeoutError:
                    print("⏰ No messages received in 30 seconds")
                    break

    except Exception as e:
        print(f"❌ Connection error: {e}")


async def trade_stream_example():
    """Process trade stream data from WebSocket."""
    import websockets
    from standardweb3.types import stream_to_spot_trade_event

    websocket_url = "wss://story-odyssey-websocket.standardweb3.com"

    try:
        async with websockets.connect(websocket_url) as websocket:
            print("✅ Connected to Standard Protocol WebSocket")

            # Subscribe to all trades
            await websocket.send(json.dumps({"type": "subscribe", "channel": "trades"}))
            print("📊 Subscribed to all trades")

            async for message in websocket:
                try:
                    data = json.loads(message)

                    if data.get("channel") == "trades":
                        # Try to parse as trade stream
                        stream_data = data.get("data")
                        if isinstance(stream_data, list) and len(stream_data) == 29:
                            try:
                                trade = stream_to_spot_trade_event(tuple(stream_data))
                                print(
                                    f"💰 TRADE: {trade.base_symbol}/{trade.quote_symbol}"
                                )
                                print(f"    Price: ${trade.price}")
                                print(f"    Amount: {trade.amount}")
                                print(f"    Value: ${trade.value_usd}")
                                print(f"    Side: {'BUY' if trade.is_bid else 'SELL'}")
                                print("-" * 40)
                            except Exception as parse_error:
                                print(f"⚠️ Failed to parse trade: {parse_error}")
                                print(f"Raw data: {stream_data}")
                        else:
                            print(f"📨 Non-trade message: {data}")
                    else:
                        print(f"📨 Other channel: {data}")

                except json.JSONDecodeError:
                    print(f"⚠️ Invalid JSON: {message}")
                except KeyboardInterrupt:
                    print("\n⏹️ Stopped by user")
                    break
                except Exception as e:
                    print(f"❌ Error processing message: {e}")

    except Exception as e:
        print(f"❌ Connection error: {e}")


async def main():
    """Run the simple WebSocket examples."""
    print("🌟 Simple WebSocket Examples for Standard Protocol")
    print("=" * 60)

    print("\n1️⃣ Custom WebSocket Handler Example:")
    await custom_websocket_handler()

    await asyncio.sleep(2)

    print("\n2️⃣ Trade Stream Example:")
    print("Press Ctrl+C to stop...")
    try:
        await trade_stream_example()
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")


if __name__ == "__main__":
    asyncio.run(main())

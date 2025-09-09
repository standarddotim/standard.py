# WebSocket Examples for Standard Protocol

This directory contains comprehensive examples for connecting to the Standard Protocol WebSocket to receive real-time trading data.

## Overview

The Standard Protocol WebSocket provides real-time streams for:
- **Trades** - Live trade executions
- **Orders** - Order placements and updates
- **Order History** - Historical order data
- **Orderbook** - Bid/ask price levels
- **Price Bars** - OHLCV candlestick data

## Quick Start

### 1. Simple WebSocket Connection

```python
from standardweb3 import StandardClient

# Initialize client
client = StandardClient(
    private_key="your_private_key",
    http_rpc_url="https://your-rpc-url.com",
    ws_url="wss://ws-server-url.com",
    networkName="Somnia Testnet"
)

# Connect to WebSocket
await client.start_ws()
```

### 2. Custom WebSocket Handler

```python
import websockets
import json

websocket_url = "wss://story-odyssey-websocket.standardweb3.com"

async with websockets.connect(websocket_url) as websocket:
    # Subscribe to trades
    await websocket.send(json.dumps({
        "type": "subscribe",
        "channel": "trades",
        "pair": "ETH/USDC"
    }))

    # Listen for messages
    async for message in websocket:
        data = json.loads(message)
        print(f"Received: {data}")
```

## Available Examples

### 1. `simple_websocket_example.py`
**Best for beginners** - Minimal examples showing:
- Basic WebSocket connection
- Trade stream parsing
- Message handling

**Run it:**
```bash
python src/standardweb3/examples/simple_websocket_example.py
```

### 2. `websocket_example.py`
**Advanced features** - Comprehensive examples with:
- Typed stream data parsing
- Multiple subscription management
- Custom event handlers
- Automatic reconnection
- Statistics tracking

**Run it:**
```bash
python src/standardweb3/examples/websocket_example.py
```

## WebSocket Channels

### Trades Channel
Receive real-time trade executions:

```python
# Subscribe to all trades
await websocket.send(json.dumps({
    "type": "subscribe",
    "channel": "trades"
}))

# Subscribe to specific pair
await websocket.send(json.dumps({
    "type": "subscribe",
    "channel": "trades",
    "pair": "ETH/USDC"
}))
```

**Stream Data Format:**
```python
[
    "spotTrade",        # eventId
    "trade_123",        # tradeId
    12345,              # orderId
    "0x...",            # base token
    "0x...",            # quote token
    "ETH",              # baseSymbol
    "USDC",             # quoteSymbol
    # ... 22 more fields
]
```

### Orders Channel
Receive order placement and updates:

```python
await websocket.send(json.dumps({
    "type": "subscribe",
    "channel": "orders",
    "account": "0x1234..."  # Optional: filter by account
}))
```

### Orderbook Channel
Receive orderbook depth updates:

```python
await websocket.send(json.dumps({
    "type": "subscribe",
    "channel": "orderbook",
    "pair": "ETH/USDC"
}))
```

### Price Bars Channel
Receive OHLCV candlestick data:

```python
await websocket.send(json.dumps({
    "type": "subscribe",
    "channel": "bars",
    "pair": "ETH/USDC",
    "interval": "1m"  # 1m, 5m, 15m, 1h, 1d
}))
```

## Stream Data Parsing

The examples show how to parse raw stream data into typed objects:

```python
from standardweb3.types import stream_to_spot_trade_event

# Parse trade stream data
if data["channel"] == "trades":
    stream_data = data["data"]
    trade = stream_to_spot_trade_event(tuple(stream_data))

    print(f"Trade: {trade.base_symbol}/{trade.quote_symbol}")
    print(f"Price: ${trade.price}")
    print(f"Amount: {trade.amount}")
    print(f"Side: {'BUY' if trade.is_bid else 'SELL'}")
```

## Configuration

### Network URLs

**Somnia Testnet:**
- WebSocket: `wss://story-odyssey-websocket.standardweb3.com`
- API: `https://story-odyssey-ponder.standardweb3.com`

### Error Handling

The examples include comprehensive error handling:

```python
try:
    async with websockets.connect(url) as websocket:
        # WebSocket operations
        pass
except websockets.exceptions.ConnectionClosed:
    print("Connection closed")
except Exception as e:
    print(f"Error: {e}")
```

### Automatic Reconnection

The advanced example includes reconnection logic:

```python
class ReconnectingWebSocketClient:
    async def connect_with_retry(self):
        while self.retry_count < self.max_retries:
            try:
                if await self.connect():
                    return True
            except Exception as e:
                self.retry_count += 1
                wait_time = min(2 ** self.retry_count, 30)
                await asyncio.sleep(wait_time)
```

## Best Practices

1. **Handle Connection Drops**: Always implement reconnection logic
2. **Parse Stream Data**: Use the provided type parsers for clean data handling
3. **Manage Subscriptions**: Keep track of active subscriptions for reconnection
4. **Rate Limiting**: Be mindful of subscription limits
5. **Error Handling**: Gracefully handle JSON parsing and connection errors

## Troubleshooting

### Common Issues

1. **Connection Refused**: Check network connectivity and URL
2. **Invalid JSON**: Ensure proper message formatting
3. **Parse Errors**: Verify stream data format matches expected structure
4. **Timeout**: Implement appropriate timeout handling

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Requirements

- Python 3.7+
- `websockets` library
- `standardweb3` package

Install dependencies:
```bash
pip install websockets
```

## Support

For issues or questions:
- Check the main Standard Protocol documentation
- Review the example code for implementation patterns
- Test with the simple examples first before advanced features

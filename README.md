<div align="center">

<img src="./media/standard_profile.jpeg" width=100/>

  <h1><code>Standard Python Client</code></h1>

  <p>
    <strong>A Python API client for Standard Exchange</strong>
  </p>

  <p>
    <a href="https://t.me/standard_protocol"><img alt="Telegram Chat" src="https://img.shields.io/badge/telegram-chat-blue?logo=telegram"></a>
  </p>
</div>

# Standard Exchange Python API Client

This is a Python API client for connecting to the Standard Exchange. It provides a set of asynchronous methods to interact with the exchange's API, allowing you to fetch order books, trade histories, token information, and more.

## Installation

To install the client, you can use pip:

```bash
pip install standardweb3
```

## Quick Start

### Environment Setup

1. Create a `.env` file in your project root:

```bash
# Copy the example environment file
cp env.example .env
```

2. Edit `.env` with your actual values:

```bash
# Your Ethereum private key (without 0x prefix)
PRIVATE_KEY=your_actual_private_key_here

# RPC URL for your network
RPC_URL=https://rpc.testnet.mode.network

# Network name (must match supported networks)
NETWORK=Somnia Testnet
```

3. Install python-dotenv for environment variable loading:

```bash
pip install python-dotenv
```

### Basic Trading Example

```python
import asyncio
import os
from dotenv import load_dotenv
from standardweb3 import StandardClient

async def quick_trade():
    load_dotenv()

    client = StandardClient(
        private_key=os.getenv("PRIVATE_KEY"),
        http_rpc_url=os.getenv("RPC_URL"),
        networkName=os.getenv("NETWORK"),
        api_url=None,
        websocket_url=None
    )

    # Market buy example
    tx_receipt = await client.market_buy(
        base="0xTokenAddress1",
        quote="0xTokenAddress2",
        quote_amount=client.w3.to_wei(0.01, "ether"),
        is_maker=False,
        n=1,
        recipient=client.address,
        slippage_limit=1000000
    )
    print(f"Trade successful: {tx_receipt['transactionHash'].hex()}")

asyncio.run(quick_trade())
```

## Usage

First, import the necessary modules and initialize the `StandardClient`:

```python
from standardweb3 import StandardClient

# Initialize the client
client = StandardClient(
    private_key="your_private_key",
    http_rpc_url="https://your_rpc_url",
    networkName="Monad Devnet",
    api_key="your_api_key_from_standard"
)
```

## Methods

The `StandardClient` class provides the following asynchronous methods:

### Order Book

```python
orderbook = await client.fetch_orderbook(base="BASE_TOKEN", quote="QUOTE_TOKEN")
```

### Account Order History

```python
order_history = await client.fetch_user_account_order_history_paginated_with_limit(
    address="USER_ADDRESS", limit=10, page=1
)
```

### Account Orders

```python
account_orders = await client.fetch_user_account_orders_paginated_with_limit(
    address="USER_ADDRESS", limit=10, page=1
)
```

### Pairs

```python
all_pairs = await client.fetch_all_pairs(limit=10, page=1)
new_listing_pairs = await client.fetch_new_listing_pairs(limit=10, page=1)
pair_info = await client.fetch_pair_info(base="BASE_TOKEN", quote="QUOTE_TOKEN")
top_gainer_pairs = await client.fetch_top_gainer_pairs(limit=10, page=1)
top_loser_pairs = await client.fetch_top_loser_pairs(limit=10, page=1)
```

### Tokens

```python
all_tokens = await client.fetch_all_tokens(limit=10, page=1)
new_listing_tokens = await client.fetch_new_listing_tokens(limit=10, page=1)
token_info = await client.fetch_token_info(address="TOKEN_ADDRESS")
top_gainer_tokens = await client.fetch_top_gainer_tokens(limit=10, page=1)
top_loser_tokens = await client.fetch_top_loser_tokens(limit=10, page=1)
```

### Trade History

```python
trade_history = await client.fetch_account_trade_history_paginated_with_limit(
    address="USER_ADDRESS", limit=10, page=1
)
recent_overall_trades = await client.fetch_recent_overall_trades_paginated(limit=10, page=1)
recent_pair_trades = await client.fetch_recent_pair_trades_paginated(
    base="BASE_TOKEN", quote="QUOTE_TOKEN", limit=10, page=1
)
```

### Trading Operations

The client supports both market and limit orders for buying and selling tokens:

#### Market Orders

Market orders execute immediately at the current market price:

```python
# Market Buy - Buy tokens immediately at market price
tx_receipt = await client.market_buy(
    base="0x1234...",  # Base token address
    quote="0x5678...", # Quote token address
    quote_amount=1000000000000000000,  # Amount in wei (1 ETH)
    is_maker=False,
    n=1,
    recipient=client.address,
    slippage_limit=1000000  # 10% slippage tolerance
)

# Market Sell - Sell tokens immediately at market price
tx_receipt = await client.market_sell(
    base="0x1234...",  # Base token address
    quote="0x5678...", # Quote token address
    base_amount=1000000000000000000,  # Amount in wei (1 token)
    is_maker=False,
    n=1,
    recipient=client.address,
    slippage_limit=1000000  # 10% slippage tolerance
)
```

#### Limit Orders

Limit orders are placed at a specific price and execute when the market reaches that price:

```python
# Limit Buy - Buy tokens at or below specified price
tx_receipt = await client.limit_buy(
    base="0x1234...",  # Base token address
    quote="0x5678...", # Quote token address
    price=2000000000000000000,  # Price in wei (2 ETH per token)
    quote_amount=1000000000000000000,  # Amount in wei (1 ETH worth)
    is_maker=True,
    n=1,
    recipient=client.address
)

# Limit Sell - Sell tokens at or above specified price
tx_receipt = await client.limit_sell(
    base="0x1234...",  # Base token address
    quote="0x5678...", # Quote token address
    price=3000000000000000000,  # Price in wei (3 ETH per token)
    base_amount=1000000000000000000,  # Amount in wei (1 token)
    is_maker=True,
    n=1,
    recipient=client.address
)
```

#### Helper Functions for Wei Conversion

Use the Web3 instance to convert between ETH and wei:

```python
# Convert ETH to wei
amount_wei = client.w3.to_wei(1.5, "ether")  # 1.5 ETH

# Convert wei to ETH
amount_eth = client.w3.from_wei(1500000000000000000, "ether")  # Returns "1.5"
```

## Use Cases

The Standard Exchange Python API Client can be used for various purposes, including but not limited to:

- **Trade Automation**: Automate your trading strategies by interacting with the exchange's API to place and manage orders programmatically.
- **AI Trading Agent**: Develop AI-driven trading agents that can analyze market data, make trading decisions, and execute trades autonomously.
- **Market Research**: Gather and analyze market data such as order books, trade histories, and token information to conduct in-depth market research and analysis.

## Examples

You can find example code in the `examples` folder. Here are some examples:

### Complete Trading Example

```python
# examples/complete_trading.py
import asyncio
import os
from dotenv import load_dotenv
from standardweb3 import StandardClient

async def main():
    # Load environment variables
    load_dotenv()

    # Initialize the client
    client = StandardClient(
        private_key=os.getenv("PRIVATE_KEY"),
        http_rpc_url=os.getenv("RPC_URL", "https://rpc.testnet.mode.network"),
        networkName=os.getenv("NETWORK", "Somnia Testnet"),
        api_url=None,
        websocket_url=None
    )

    # Example token addresses (replace with actual addresses)
    base_token = "0x1234567890123456789012345678901234567890"
    quote_token = "0x0987654321098765432109876543210987654321"

    try:
        # 1. Market Buy Example
        print("Executing market buy...")
        quote_amount = client.w3.to_wei(0.1, "ether")  # 0.1 ETH
        tx_receipt = await client.market_buy(
            base=base_token,
            quote=quote_token,
            quote_amount=quote_amount,
            is_maker=False,
            n=1,
            recipient=client.address,
            slippage_limit=1000000  # 10% slippage
        )
        print(f"Market buy successful! TX: {tx_receipt['transactionHash'].hex()}")

        # 2. Limit Sell Example
        print("Placing limit sell order...")
        price = client.w3.to_wei(2.0, "ether")  # 2 ETH per token
        base_amount = client.w3.to_wei(0.5, "ether")  # 0.5 tokens
        tx_receipt = await client.limit_sell(
            base=base_token,
            quote=quote_token,
            price=price,
            base_amount=base_amount,
            is_maker=True,
            n=1,
            recipient=client.address
        )
        print(f"Limit sell placed! TX: {tx_receipt['transactionHash'].hex()}")

    except Exception as e:
        print(f"Trading failed: {e}")

asyncio.run(main())
```

### Fetch Order Book

```python
# examples/fetch_orderbook.py
import asyncio
from standardweb3 import StandardClient

async def main():
    client = StandardClient(
        private_key="your_private_key",
        http_rpc_url="https://your_rpc_url",
        networkName="Somnia Testnet",
        api_key="your_api_key"
    )
    orderbook = await client.fetch_orderbook(base="BASE_TOKEN", quote="QUOTE_TOKEN")
    print(orderbook)

asyncio.run(main())
```

### Fetch User Account Order History

```python
# examples/fetch_user_account_order_history.py
import asyncio
from standardweb3 import StandardClient

async def main():
    client = StandardClient(
        private_key="your_private_key",
        http_rpc_url="https://your_rpc_url",
        networkName="Somnia Testnet",
        api_key="your_api_key"
    )
    order_history = await client.fetch_user_account_order_history_paginated_with_limit(
        address="USER_ADDRESS", limit=10, page=1
    )
    print(order_history)

asyncio.run(main())
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

For the guide, check [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

This project is licensed under the MIT License.

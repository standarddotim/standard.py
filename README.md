<div align="center">

<img src="./memes/standard_profile.jpeg" width=100/>

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

## Use Cases

The Standard Exchange Python API Client can be used for various purposes, including but not limited to:

- **Trade Automation**: Automate your trading strategies by interacting with the exchange's API to place and manage orders programmatically.
- **AI Trading Agent**: Develop AI-driven trading agents that can analyze market data, make trading decisions, and execute trades autonomously.
- **Market Research**: Gather and analyze market data such as order books, trade histories, and token information to conduct in-depth market research and analysis.

## Examples

You can find example code in the `examples` folder. Here are some examples:

### Fetch Order Book

```python
# examples/fetch_orderbook.py
import asyncio
from standardweb3 import StandardClient

async def main():
    client = StandardClient(
        private_key="your_private_key",
        http_rpc_url="https://your_rpc_url",
        networkName="Story Odyssey Testnet",
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
        networkName="Story Odyssey Testnet",
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

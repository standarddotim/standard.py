#!/usr/bin/env python3
"""
API Example using StandardWeb3 API Functions.

This example demonstrates how to use the StandardClient to call various
API functions for fetching market data, order information, and trade history
from the Standard Protocol exchange.

Features demonstrated:
- Orderbook data retrieval
- Trading pairs information
- Token information
- Account order history
- Trade history
- Market statistics
- Error handling and logging
"""

import asyncio
import json
import os
from dotenv import load_dotenv

# Import the StandardClient
from standardweb3 import StandardClient


class APIExample:
    """Comprehensive API example using StandardWeb3 client."""

    def __init__(
        self,
        rpc_url: str,
        private_key: str,
        api_url: str = "https://somnia-testnet-ponder-release.standardweb3.com",
        api_key: str = "defaultApiKey",
    ):
        """
        Initialize the API example.

        Args:
            rpc_url: RPC endpoint URL
            private_key: Private key for account identification
            api_url: API endpoint URL (default: Somnia Testnet Ponder Release)
            api_key: API key for authentication
        """
        # Initialize StandardClient with custom API URL
        self.client = StandardClient(
            private_key=private_key,
            http_rpc_url=rpc_url,
            matching_engine_address=(
                "0x0000000000000000000000000000000000000000"  # Placeholder
            ),
            api_url=api_url,
            api_key=api_key,
        )

        print("🚀 Initialized API Example")
        print(f"Account: {self.client.address}")
        print(f"API URL: {api_url}")
        print("-" * 60)

    def print_json(self, data: dict, title: str = "API Response"):
        """Pretty print JSON data."""
        print(f"\n📊 {title}")
        print("=" * 50)
        print(json.dumps(data, indent=2, default=str))
        print("=" * 50)

    async def fetch_orderbook_example(self, base: str, quote: str):
        """
        Fetch orderbook data for a trading pair.

        Args:
            base: Base token address
            quote: Quote token address
        """
        print(f"\n📈 Fetching Orderbook for {base}/{quote}")
        try:
            orderbook = await self.client.fetch_orderbook(base, quote)
            print("✅ Orderbook fetched successfully!")
            print(f"  Market Price: {orderbook.mktPrice}")
            print(f"  Bid Head: {orderbook.bidHead}")
            print(f"  Ask Head: {orderbook.askHead}")
            print(f"  Number of Bids: {len(orderbook.bids)}")
            print(f"  Number of Asks: {len(orderbook.asks)}")

            if orderbook.bids:
                print(
                    f"  Best Bid: {orderbook.bids[0].price} "
                    f"(Amount: {orderbook.bids[0].amount})"
                )
            if orderbook.asks:
                print(
                    f"  Best Ask: {orderbook.asks[0].price} "
                    f"(Amount: {orderbook.asks[0].amount})"
                )

            return orderbook

        except Exception as e:
            print(f"❌ Failed to fetch orderbook: {str(e)}")
            return None

    async def fetch_all_pairs_example(self, limit: int = 10, page: int = 1):
        """
        Fetch all trading pairs.

        Args:
            limit: Number of pairs per page
            page: Page number
        """
        print(f"\n💱 Fetching All Pairs (Limit: {limit}, Page: {page})")
        try:
            pairs_data = await self.client.fetch_all_pairs(limit, page)

            print("✅ Pairs fetched successfully!")
            print(pairs_data)
            print(f"  Total Count: {pairs_data.totalCount}")
            print(f"  Total Pages: {pairs_data.totalPages}")
            print(f"  Current Page: {page}")
            print(f"  Pairs on this page: {len(pairs_data.pairs)}")

            for i, pair in enumerate(pairs_data.pairs[:3]):  # Show first 3 pairs
                print(f"  Pair {i+1}: {pair.symbol}")
                print(f"    Price: {pair.price}")
                print(f"    24h Change: {pair.dayPriceDifferencePercentage}%")
                print(f"    24h Volume: {pair.dayBaseVolumeUSD} USD")

            return pairs_data

        except Exception as e:
            print(f"❌ Failed to fetch pairs: {str(e)}")
            return None

    async def fetch_top_gainer_pairs_example(self, limit: int = 5, page: int = 1):
        """
        Fetch top gaining trading pairs.

        Args:
            limit: Number of pairs to fetch
            page: Page number
        """
        print(f"\n📈 Fetching Top Gainer Pairs (Limit: {limit})")
        try:
            pairs_data = await self.client.fetch_top_gainer_pairs(limit, page)

            print("✅ Top gainers fetched successfully!")
            print(f"  Found {len(pairs_data.pairs)} gaining pairs")

            for i, pair in enumerate(pairs_data.pairs):
                print(f"  #{i+1}: {pair.symbol}")
                print(f"    Price: {pair.price}")
                print(f"    24h Change: +{pair.dayPriceDifferencePercentage}%")
                print(f"    24h Volume: {pair.dayBaseVolumeUSD} USD")

            return pairs_data

        except Exception as e:
            print(f"❌ Failed to fetch top gainers: {str(e)}")
            return None

    async def fetch_top_loser_pairs_example(self, limit: int = 5, page: int = 1):
        """
        Fetch top losing trading pairs.

        Args:
            limit: Number of pairs to fetch
            page: Page number
        """
        print(f"\n📉 Fetching Top Loser Pairs (Limit: {limit})")
        try:
            pairs_data = await self.client.fetch_top_loser_pairs(limit, page)

            print("✅ Top losers fetched successfully!")
            print(f"  Found {len(pairs_data.pairs)} losing pairs")

            for i, pair in enumerate(pairs_data.pairs):
                print(f"  #{i+1}: {pair.symbol}")
                print(f"    Price: {pair.price}")
                print(f"    24h Change: {pair.dayPriceDifferencePercentage}%")
                print(f"    24h Volume: {pair.dayBaseVolumeUSD} USD")

            return pairs_data

        except Exception as e:
            print(f"❌ Failed to fetch top losers: {str(e)}")
            return None

    async def fetch_pair_info_example(self, base: str, quote: str):
        """
        Fetch detailed information for a specific trading pair.

        Args:
            base: Base token address
            quote: Quote token address
        """
        print(f"\n🔍 Fetching Pair Info for {base}/{quote}")
        try:
            pair = await self.client.fetch_pair_info(base, quote)

            print("✅ Pair info fetched successfully!")
            print(f"  Symbol: {pair.symbol}")
            print(f"  Description: {pair.description}")
            print(f"  Current Price: {pair.price}")
            print(f"  All-Time High: {pair.ath}")
            print(f"  All-Time Low: {pair.atl}")
            print(f"  24h Price Change: {pair.dayPriceDifferencePercentage}%")
            print(f"  24h Base Volume: {pair.dayBaseVolume}")
            print(f"  24h Quote Volume: {pair.dayQuoteVolume}")
            print(f"  Base Token: {pair.base.name} ({pair.base.symbol})")
            print(f"  Quote Token: {pair.quote.name} ({pair.quote.symbol})")

            return pair

        except Exception as e:
            print(f"❌ Failed to fetch pair info: {str(e)}")
            return None

    async def fetch_all_tokens_example(self, limit: int = 10, page: int = 1):
        """
        Fetch all available tokens.

        Args:
            limit: Number of tokens per page
            page: Page number
        """
        print(f"\n🪙 Fetching All Tokens (Limit: {limit}, Page: {page})")
        try:
            tokens_data = await self.client.fetch_all_tokens(limit, page)

            print("✅ Tokens fetched successfully!")
            print(f"  Total Count: {tokens_data.totalCount}")
            print(f"  Total Pages: {tokens_data.totalPages}")
            print(f"  Tokens on this page: {len(tokens_data.tokens)}")

            for i, token in enumerate(tokens_data.tokens[:3]):  # Show first 3 tokens
                print(f"  Token {i+1}: {token.name} ({token.symbol})")
                print(f"    Price: ${token.price}")
                print(f"    24h Change: {token.dayPriceDifferencePercentage}%")
                print(f"    Total Supply: {token.totalSupply}")
                print(f"    Decimals: {token.decimals}")

            return tokens_data

        except Exception as e:
            print(f"❌ Failed to fetch tokens: {str(e)}")
            return None

    async def fetch_token_info_example(self, token_address: str):
        """
        Fetch detailed information for a specific token.

        Args:
            token_address: Token contract address
        """
        print(f"\n🪙 Fetching Token Info for {token_address}")
        try:
            token = await self.client.fetch_token_info(token_address)

            print("✅ Token info fetched successfully!")
            print(f"  Name: {token.name}")
            print(f"  Symbol: {token.symbol}")
            print(f"  Address: {token.address}")
            print(f"  Decimals: {token.decimals}")
            print(f"  Price: ${token.price}")

            return token

        except Exception as e:
            print(f"❌ Failed to fetch token info: {str(e)}")
            return None

    async def fetch_account_orders_example(
        self, address: str, limit: int = 10, page: int = 1
    ):
        """
        Fetch active orders for an account.

        Args:
            address: Account address
            limit: Number of orders per page
            page: Page number
        """
        print(f"\n📋 Fetching Account Orders for {address}")
        try:
            orders = await self.client.fetch_account_orders_paginated_with_limit(
                address, limit, page
            )

            print("✅ Account orders fetched successfully!")
            print(f"  Total orders: {len(orders.orders)}")

            for i, order in enumerate(orders.orders[:3]):  # Show first 3 orders
                print(f"  Order {i+1}:")
                print(f"    ID: {order.id}")
                print(f"    Type: {order.orderType}")
                print(f"    Side: {order.side}")
                print(f"    Amount: {order.amount}")
                print(f"    Price: {order.price}")
                print(f"    Status: {order.status}")

            return orders

        except Exception as e:
            print(f"❌ Failed to fetch account orders: {str(e)}")
            return None

    async def fetch_account_order_history_example(
        self, address: str, limit: int = 10, page: int = 1
    ):
        """
        Fetch order history for an account.

        Args:
            address: Account address
            limit: Number of orders per page
            page: Page number
        """
        print(f"\n📚 Fetching Account Order History for {address}")
        try:
            history = (
                await self.client.fetch_account_order_history_paginated_with_limit(
                    address, limit, page
                )
            )

            print("✅ Account order history fetched successfully!")
            print(f"  Total historical orders: {len(history.orders)}")

            for i, order in enumerate(history.orders[:3]):  # Show first 3 orders
                print(f"  Historical Order {i+1}:")
                print(f"    ID: {order.id}")
                print(f"    Type: {order.orderType}")
                print(f"    Side: {order.side}")
                print(f"    Amount: {order.amount}")
                print(f"    Price: {order.price}")
                print(f"    Status: {order.status}")

            return history

        except Exception as e:
            print(f"❌ Failed to fetch account order history: {str(e)}")
            return None

    async def fetch_account_trade_history_example(
        self, address: str, limit: int = 10, page: int = 1
    ):
        """
        Fetch trade history for an account.

        Args:
            address: Account address
            limit: Number of trades per page
            page: Page number
        """
        print(f"\n📈 Fetching Account Trade History for {address}")
        try:
            history = (
                await self.client.fetch_account_trade_history_paginated_with_limit(
                    address, limit, page
                )
            )

            print("✅ Account trade history fetched successfully!")
            print(f"  Total trades: {len(history.trades)}")

            for i, trade in enumerate(history.trades[:3]):  # Show first 3 trades
                print(f"  Trade {i+1}:")
                print(f"    ID: {trade.id}")
                print(f"    Price: {trade.price}")
                print(f"    Amount: {trade.amount}")
                print(f"    Side: {trade.side}")
                print(f"    Timestamp: {trade.timestamp}")

            return history

        except Exception as e:
            print(f"❌ Failed to fetch account trade history: {str(e)}")
            return None

    async def fetch_recent_trades_example(self, limit: int = 10, page: int = 1):
        """
        Fetch recent trades across all pairs.

        Args:
            limit: Number of trades per page
            page: Page number
        """
        print(f"\n🔥 Fetching Recent Overall Trades (Limit: {limit})")
        try:
            trades = await self.client.fetch_recent_overall_trades_paginated(
                limit, page
            )

            print("✅ Recent trades fetched successfully!")
            print(f"  Total trades: {len(trades.trades)}")

            for i, trade in enumerate(trades.trades[:5]):  # Show first 5 trades
                print(f"  Trade {i+1}:")
                print(f"    Pair: {trade.pair}")
                print(f"    Price: {trade.price}")
                print(f"    Amount: {trade.amount}")
                print(f"    Side: {trade.side}")
                print(f"    Timestamp: {trade.timestamp}")

            return trades

        except Exception as e:
            print(f"❌ Failed to fetch recent trades: {str(e)}")
            return None

    async def fetch_pair_trades_example(
        self, base: str, quote: str, limit: int = 10, page: int = 1
    ):
        """
        Fetch recent trades for a specific pair.

        Args:
            base: Base token address
            quote: Quote token address
            limit: Number of trades per page
            page: Page number
        """
        print(f"\n📊 Fetching Recent Trades for {base}/{quote}")
        try:
            trades = await self.client.fetch_recent_pair_trades_paginated(
                base, quote, limit, page
            )

            print("✅ Pair trades fetched successfully!")
            print(f"  Total trades: {len(trades.trades)}")

            for i, trade in enumerate(trades.trades[:5]):  # Show first 5 trades
                print(f"  Trade {i+1}:")
                print(f"    Price: {trade.price}")
                print(f"    Amount: {trade.amount}")
                print(f"    Side: {trade.side}")
                print(f"    Timestamp: {trade.timestamp}")

            return trades

        except Exception as e:
            print(f"❌ Failed to fetch pair trades: {str(e)}")
            return None

    async def run_comprehensive_api_examples(self):
        """Execute a comprehensive series of API examples."""
        print("🌟 Starting Comprehensive API Examples")
        print("=" * 60)

        # Example token addresses (replace with actual addresses for your network)
        example_base_token = "0x4A3BC48C156384f9564Fd65A53a2f3D534D8f2b7"
        example_quote_token = "0x0ED782B8079529f7385c3eDA9fAf1EaA0DbC6a17"
        example_account = self.client.address

        try:
            # 1. Market Data Examples
            print("\n🏪 === MARKET DATA EXAMPLES ===")

            # Fetch all pairs
            await self.fetch_all_pairs_example(limit=5, page=1)

            # Fetch top gainers and losers
            await self.fetch_top_gainer_pairs_example(limit=3)
            await self.fetch_top_loser_pairs_example(limit=3)

            # Fetch specific pair info
            await self.fetch_pair_info_example(example_base_token, example_quote_token)

            # Fetch orderbook
            await self.fetch_orderbook_example(example_base_token, example_quote_token)

            # 2. Token Information Examples
            print("\n🪙 === TOKEN INFORMATION EXAMPLES ===")

            # Fetch all tokens
            await self.fetch_all_tokens_example(limit=5, page=1)

            # Fetch specific token info
            await self.fetch_token_info_example(example_base_token)

            # 3. Account-Specific Examples
            print("\n👤 === ACCOUNT EXAMPLES ===")

            # Fetch account orders
            await self.fetch_account_orders_example(example_account, limit=5)

            # Fetch account order history
            await self.fetch_account_order_history_example(example_account, limit=5)

            # Fetch account trade history
            await self.fetch_account_trade_history_example(example_account, limit=5)

            # 4. Trading Activity Examples
            print("\n📈 === TRADING ACTIVITY EXAMPLES ===")

            # Fetch recent overall trades
            await self.fetch_recent_trades_example(limit=5)

            # Fetch recent pair trades
            await self.fetch_pair_trades_example(
                example_base_token, example_quote_token, limit=5
            )

            print("\n✅ All API examples completed successfully!")
            print("=" * 60)

        except Exception as e:
            print(f"\n❌ Error running API examples: {e}")
            print("\nTroubleshooting tips:")
            print("1. Make sure the API URL is correct and accessible")
            print("2. Check your internet connection")
            print("3. Verify that the token addresses are valid for the network")
            print("4. Ensure the API service is operational")

    async def run_parallel_api_examples(self):
        """Execute multiple API calls in parallel for better performance."""
        print("\n⚡ Running Parallel API Examples")
        print("=" * 40)

        try:
            # Execute multiple API calls concurrently
            results = await asyncio.gather(
                self.client.fetch_all_pairs(5, 1),
                self.client.fetch_all_tokens(5, 1),
                self.client.fetch_top_gainer_pairs(3, 1),
                self.client.fetch_recent_overall_trades_paginated(5, 1),
                return_exceptions=True,
            )

            print("✅ Parallel API calls completed!")

            def get_status(result):
                return "Success" if not isinstance(result, Exception) else "Failed"

            print(f"  Pairs result: {get_status(results[0])}")
            print(f"  Tokens result: {get_status(results[1])}")
            print(f"  Top gainers result: {get_status(results[2])}")
            print(f"  Recent trades result: {get_status(results[3])}")

        except Exception as e:
            print(f"❌ Parallel API calls failed: {e}")


async def main():
    """Run the API examples."""
    # Load environment variables from .env file
    load_dotenv()

    # Configuration - Replace with your actual values
    RPC_URL = os.getenv("RPC_URL", "https://your-rpc-url.com")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
    API_URL = os.getenv(
        "API_URL", "https://somnia-testnet-ponder-release.standardweb3.com"
    )
    API_KEY = os.getenv("API_KEY", "defaultApiKey")

    if not PRIVATE_KEY:
        print("❌ Please set your PRIVATE_KEY environment variable")
        print("Example: export PRIVATE_KEY='your_private_key_here'")
        return

    if not RPC_URL or RPC_URL == "https://your-rpc-url.com":
        print("❌ Please set your RPC_URL environment variable")
        print("Example: export RPC_URL='your_rpc_url_here'")
        return

    try:
        # Initialize API example
        api_example = APIExample(
            rpc_url=RPC_URL,
            private_key=PRIVATE_KEY,
            api_url=API_URL,
            api_key=API_KEY,
        )

        # Run comprehensive API examples
        await api_example.run_comprehensive_api_examples()

        # Demonstrate parallel API calls
        await api_example.run_parallel_api_examples()

    except Exception as e:
        print(f"❌ Error running API examples: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure your RPC_URL is correct and accessible")
        print("2. Ensure your PRIVATE_KEY is valid")
        print("3. Check that the API_URL is correct")
        print("4. Verify your internet connection")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())

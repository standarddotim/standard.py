#!/usr/bin/env python3
"""
Trading Example using StandardWeb3 Contract Functions.

This example demonstrates how to use the contract functions to perform various
trading operations on the Standard Protocol exchange.

Features demonstrated:
- Market Buy/Sell orders
- Limit Buy/Sell orders
- Order cancellation
- Transaction monitoring
- Error handling
"""

import asyncio
import os
from typing import Optional

from dotenv import load_dotenv

# Import the StandardClient
from standardweb3 import StandardClient


class TradingExample:
    """Comprehensive trading example using StandardWeb3 client."""

    def __init__(
        self,
        rpc_url: str,
        private_key: str,
        network: str = "Somnia Testnet",
    ):
        """
        Initialize the trading example.

        Args:
            rpc_url: RPC endpoint URL
            private_key: Private key for signing transactions
            network: Network name (default: Somnia Testnet)
        """
        # Initialize StandardClient
        self.client = StandardClient(
            private_key=private_key,
            http_rpc_url=rpc_url,
            networkName=network,
            api_url=None,
            websocket_url=None,
        )

        print(f"Initialized trading example for {network}")
        print(f"Account: {self.client.contract.address}")
        print(f"Network ID: {self.client.contract.w3.eth.chain_id}")
        print("-" * 50)

    async def check_balance(self, token_address: str) -> int:
        """Check token balance for the connected account."""
        # Simple ERC20 balance check (you might want to use a proper ERC20 ABI)
        balance = self.client.w3.eth.get_balance(self.client.address)
        print(f"ETH Balance: {self.client.w3.from_wei(balance, 'ether')} ETH")
        return balance

    async def market_buy_example(
        self,
        base_token: str,
        quote_token: str,
        quote_amount: int,
        is_maker: bool = False,
        n: int = 1,
        recipient: Optional[str] = None,
        slippageLimit: int = 10000000,
    ):
        """
        Execute a market buy order.

        Args:
            base_token: Address of the base token (token to buy)
            quote_token: Address of the quote token (token to spend)
            quote_amount: Amount of quote token to spend (in wei)
            is_maker: Whether this is a maker order
            n: Number of matches
            uid: User ID
            recipient: Recipient address (defaults to sender)
        """
        if recipient is None:
            recipient = self.client.address

        print("Executing Market Buy:")
        print(f"  Base Token: {base_token}")
        print(f"  Quote Token: {quote_token}")
        print(f"  Quote Amount: {self.client.w3.from_wei(quote_amount, 'ether')} ETH")
        print(f"  Is Maker: {is_maker}")
        print(f"  Recipient: {recipient}")
        print(f"  Slippage Limit: {slippageLimit}")

        try:
            tx_receipt = await self.client.market_buy(
                base=base_token,
                quote=quote_token,
                quote_amount=quote_amount,
                is_maker=is_maker,
                n=n,
                recipient=recipient,
                slippageLimit=slippageLimit,
            )

            print("✅ Market Buy successful!")
            print(f"  Transaction Hash: {tx_receipt['transactionHash'].hex()}")
            print(f"  Gas Used: {tx_receipt['gasUsed']}")
            print(f"  Status: {'Success' if tx_receipt['status'] == 1 else 'Failed'}")

            return tx_receipt

        except Exception as e:
            print(f"❌ Market Buy failed: {str(e)}")
            raise

    async def market_sell_example(
        self,
        base_token: str,
        quote_token: str,
        base_amount: int,
        is_maker: bool = False,
        n: int = 1,
        recipient: Optional[str] = None,
        slippageLimit: int = 10000000,
    ):
        """
        Execute a market sell order.

        Args:
            base_token: Address of the base token (token to sell)
            quote_token: Address of the quote token (token to receive)
            base_amount: Amount of base token to sell (in wei)
            is_maker: Whether this is a maker order
            n: Number of matches
            uid: User ID
            recipient: Recipient address (defaults to sender)
        """
        if recipient is None:
            recipient = self.client.address

        print("Executing Market Sell:")
        print(f"  Base Token: {base_token}")
        print(f"  Quote Token: {quote_token}")
        print(f"  Base Amount: {self.client.w3.from_wei(base_amount, 'ether')} tokens")
        print(f"  Is Maker: {is_maker}")
        print(f"  Recipient: {recipient}")
        print(f"  Slippage Limit: {slippageLimit}")

        try:
            tx_receipt = await self.client.market_sell(
                base=base_token,
                quote=quote_token,
                base_amount=base_amount,
                is_maker=is_maker,
                n=n,
                recipient=recipient,
                slippageLimit=slippageLimit,
            )

            print("✅ Market Sell successful!")
            print(f"  Transaction Hash: {tx_receipt['transactionHash'].hex()}")
            print(f"  Gas Used: {tx_receipt['gasUsed']}")
            print(f"  Status: {'Success' if tx_receipt['status'] == 1 else 'Failed'}")

            return tx_receipt

        except Exception as e:
            print(f"❌ Market Sell failed: {str(e)}")
            raise

    async def limit_buy_example(
        self,
        base_token: str,
        quote_token: str,
        price: int,
        quote_amount: int,
        is_maker: bool = False,
        n: int = 1,
        uid: int = 0,
        recipient: Optional[str] = None,
    ):
        """
        Execute a limit buy order.

        Args:
            base_token: Address of the base token (token to buy)
            quote_token: Address of the quote token (token to spend)
            price: Price per unit (in wei)
            quote_amount: Amount of quote token to spend (in wei)
            is_maker: Whether this is a maker order
            n: Number of matches
            uid: User ID
            recipient: Recipient address (defaults to sender)
        """
        if recipient is None:
            recipient = self.client.address

        print("Executing Limit Buy:")
        print(f"  Base Token: {base_token}")
        print(f"  Quote Token: {quote_token}")
        print(f"  Price: {self.client.w3.from_wei(price, 'ether')} ETH per token")
        print(f"  Quote Amount: {self.client.w3.from_wei(quote_amount, 'ether')} ETH")
        print(f"  Is Maker: {is_maker}")
        print(f"  Recipient: {recipient}")

        try:
            tx_receipt = await self.client.limit_buy(
                base=base_token,
                quote=quote_token,
                price=price,
                quote_amount=quote_amount,
                is_maker=is_maker,
                n=n,
                recipient=recipient,
            )

            print("✅ Limit Buy successful!")
            print(f"  Transaction Hash: {tx_receipt['transactionHash'].hex()}")
            print(f"  Gas Used: {tx_receipt['gasUsed']}")
            print(f"  Status: {'Success' if tx_receipt['status'] == 1 else 'Failed'}")

            return tx_receipt

        except Exception as e:
            print(f"❌ Limit Buy failed: {str(e)}")
            raise

    async def limit_sell_example(
        self,
        base_token: str,
        quote_token: str,
        price: int,
        base_amount: int,
        is_maker: bool = False,
        n: int = 1,
        uid: int = 0,
        recipient: Optional[str] = None,
    ):
        """
        Execute a limit sell order.

        Args:
            base_token: Address of the base token (token to sell)
            quote_token: Address of the quote token (token to receive)
            price: Price per unit (in wei)
            base_amount: Amount of base token to sell (in wei)
            is_maker: Whether this is a maker order
            n: Number of matches
            uid: User ID
            recipient: Recipient address (defaults to sender)
        """
        if recipient is None:
            recipient = self.client.address

        print("Executing Limit Sell:")
        print(f"  Base Token: {base_token}")
        print(f"  Quote Token: {quote_token}")
        print(f"  Price: {self.client.w3.from_wei(price, 'ether')} ETH per token")
        print(f"  Base Amount: {self.client.w3.from_wei(base_amount, 'ether')} tokens")
        print(f"  Is Maker: {is_maker}")
        print(f"  Recipient: {recipient}")

        try:
            tx_receipt = await self.client.limit_sell(
                base=base_token,
                quote=quote_token,
                price=price,
                base_amount=base_amount,
                is_maker=is_maker,
                n=n,
                recipient=recipient,
            )

            print("✅ Limit Sell successful!")
            print(f"  Transaction Hash: {tx_receipt['transactionHash'].hex()}")
            print(f"  Gas Used: {tx_receipt['gasUsed']}")
            print(f"  Status: {'Success' if tx_receipt['status'] == 1 else 'Failed'}")

            return tx_receipt

        except Exception as e:
            print(f"❌ Limit Sell failed: {str(e)}")
            raise

    async def cancel_orders_example(self, orders_to_cancel: list):
        """
        Execute order cancellation example.

        Args:
            orders_to_cancel: List of order data dictionaries to cancel
        """
        print("🗑️  Executing Order Cancellation Example")
        print(f"  Orders to cancel: {len(orders_to_cancel)}")

        # Display orders being cancelled
        for i, order in enumerate(orders_to_cancel):
            print(f"  Order {i+1}:")
            print(f"    Pair: {order['base'][:8]}.../{order['quote'][:8]}...")
            print(f"    Type: {'Buy' if order['isBid'] else 'Sell'}")
            print(f"    Order ID: {order['orderId']}")

        try:
            tx_receipt = await self.client.cancel_orders(orders_to_cancel)

            print("✅ Order cancellation successful!")
            print(f"  Transaction Hash: {tx_receipt['transactionHash'].hex()}")
            print(f"  Gas Used: {tx_receipt['gasUsed']}")
            print(f"  Status: {'Success' if tx_receipt['status'] == 1 else 'Failed'}")
            print(f"  Orders cancelled: {len(orders_to_cancel)}")

            return tx_receipt

        except Exception as e:
            print(f"❌ Order cancellation failed: {str(e)}")
            raise

    async def cancel_user_orders_example(self, account_address: str):
        """
        Practical example: Cancel actual orders from account history.

        This shows how to:
        1. Fetch active orders for an account
        2. Select orders to cancel
        3. Cancel them using the cancel_orders function

        Args:
            account_address: Address to fetch orders for
        """
        print("🔄 Practical Example: Cancel Real Orders")
        print("-" * 40)

        try:
            # Step 1: Fetch active orders for the account
            print("📋 Step 1: Fetching active orders...")
            orders = await self.client.fetch_account_orders_paginated_with_limit(
                account_address, limit=10, page=1
            )

            if isinstance(orders, dict) and orders.get("orders"):
                active_orders = orders["orders"]
            elif hasattr(orders, "orders"):
                active_orders = orders.orders
            else:
                active_orders = []

            if not active_orders:
                print("  No active orders found to cancel")
                return

            print(f"  Found {len(active_orders)} active orders")

            # Step 2: Prepare cancellation data from real orders
            orders_to_cancel = []
            for order in active_orders[:3]:  # Cancel up to 3 orders as example
                # Extract order data - structure may vary based on API response
                if isinstance(order, dict):
                    order_data = {
                        "base": order.get("baseToken", ""),
                        "quote": order.get("quoteToken", ""),
                        "isBid": order.get("side", "").lower() == "buy",
                        "orderId": int(order.get("id", 0)),
                    }
                else:
                    # If it's an object with attributes
                    order_data = {
                        "base": getattr(order, "baseToken", ""),
                        "quote": getattr(order, "quoteToken", ""),
                        "isBid": getattr(order, "side", "").lower() == "buy",
                        "orderId": int(getattr(order, "id", 0)),
                    }

                orders_to_cancel.append(order_data)

            print(
                f"📝 Step 2: Prepared {len(orders_to_cancel)} orders for cancellation"
            )

            # Step 3: Cancel the orders
            print("🗑️  Step 3: Cancelling orders...")
            await self.cancel_orders_example(orders_to_cancel)

        except Exception as e:
            print(f"❌ Practical cancel orders example failed: {str(e)}")
            print("💡 This is normal if there are no active orders to cancel")

    async def run_trading_examples(self):
        """Execute a series of trading examples."""
        print("🚀 Starting Trading Examples")
        print("=" * 50)

        # Check initial balance
        await self.check_balance(self.client.address)
        print()

        # Example token addresses
        # (you should replace these with actual token addresses)
        # These are example addresses - replace with actual token addresses
        # for your network
        example_base_token = (
            "0x4A3BC48C156384f9564Fd65A53a2f3D534D8f2b7"  # Example token
        )
        example_quote_token = (
            "0x0ED782B8079529f7385c3eDA9fAf1EaA0DbC6a17"  # Example token
        )

        # Example 1: Market Buy
        print("📈 Example 1: Market Buy")
        print("-" * 30)
        try:
            # Small amount for testing (0.001 ETH)
            quote_amount = self.client.w3.to_wei(0.001, "ether")
            await self.market_buy_example(
                base_token=example_base_token,
                quote_token=example_quote_token,
                quote_amount=quote_amount,
                is_maker=False,
                slippageLimit=10000000,
            )
        except Exception as e:
            print(f"Market buy example failed: {e}")
        print()

        # Example 2: Market Sell
        print("📉 Example 2: Market Sell")
        print("-" * 30)
        try:
            # Small amount for testing (0.001 tokens)
            base_amount = self.client.w3.to_wei(0.001, "ether")
            await self.market_sell_example(
                base_token=example_base_token,
                quote_token=example_quote_token,
                base_amount=base_amount,
                is_maker=False,
                slippageLimit=10000000,
            )
        except Exception as e:
            print(f"Market sell example failed: {e}")
        print()

        # Example 3: Limit Buy
        print("💰 Example 3: Limit Buy")
        print("-" * 30)
        try:
            price = self.client.w3.to_wei(0.1, "ether")  # 0.1 ETH per token
            quote_amount = self.client.w3.to_wei(0.01, "ether")  # 0.01 ETH
            await self.limit_buy_example(
                base_token=example_base_token,
                quote_token=example_quote_token,
                price=price,
                quote_amount=quote_amount,
                is_maker=True,
            )
        except Exception as e:
            print(f"Limit buy example failed: {e}")
        print()

        # Example 4: Limit Sell
        print("💸 Example 4: Limit Sell")
        print("-" * 30)
        try:
            price = self.client.w3.to_wei(0.15, "ether")  # 0.15 ETH per token
            base_amount = self.client.w3.to_wei(0.01, "ether")  # 0.01 tokens
            await self.limit_sell_example(
                base_token=example_base_token,
                quote_token=example_quote_token,
                price=price,
                base_amount=base_amount,
                is_maker=True,
            )
        except Exception as e:
            print(f"Limit sell example failed: {e}")
        print()

        # Example 5: Cancel Orders
        print("🗑️  Example 5: Cancel Orders")
        print("-" * 30)
        try:
            # Example order cancellation data
            # In a real scenario, you would get these order IDs from:
            # 1. Previous order placements
            # 2. Account order history API calls
            # 3. User input
            example_orders_to_cancel = [
                {
                    "base": example_base_token,
                    "quote": example_quote_token,
                    "isBid": True,  # Cancel a buy order
                    "orderId": 12345,  # Replace with actual order ID
                },
                {
                    "base": example_base_token,
                    "quote": example_quote_token,
                    "isBid": False,  # Cancel a sell order
                    "orderId": 12346,  # Replace with actual order ID
                },
            ]

            print("⚠️  Note: This example uses dummy order IDs.")
            print("   In practice, you would get real order IDs from:")
            print("   - Previous limit order transactions")
            print("   - Account order history API calls")
            print("   - User interface interactions")
            print()

            await self.cancel_orders_example(example_orders_to_cancel)

        except Exception as e:
            print(f"Cancel orders example failed: {e}")
            print("💡 This is expected if the order IDs don't exist on-chain")
        print()

        # Example 6: Practical Cancel Orders (using real order data)
        print("🔄 Example 6: Practical Cancel Orders")
        print("-" * 30)
        try:
            print("This example shows how to cancel real orders from your account.")
            await self.cancel_user_orders_example(self.client.address)
        except Exception as e:
            print(f"Practical cancel orders example failed: {e}")
            print("💡 This is normal if you have no active orders")
        print()

        print("✅ Trading examples completed!")


async def main():
    """Run the trading examples."""
    # Load environment variables from .env file
    load_dotenv()

    # Configuration - Replace with your actual values
    RPC_URL = os.getenv("RPC_URL", "https://rpc.testnet.mode.network")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")  # Your private key
    NETWORK = os.getenv("NETWORK", "Somnia Testnet")

    if not PRIVATE_KEY:
        print("❌ Please set your PRIVATE_KEY environment variable")
        print("Example: export PRIVATE_KEY='your_private_key_here'")
        return

    if not RPC_URL:
        print("❌ Please set your RPC_URL environment variable")
        print("Example: export RPC_URL='your_rpc_url_here'")
        return

    try:
        # Initialize trading example
        trading_example = TradingExample(
            rpc_url=RPC_URL, private_key=PRIVATE_KEY, network=NETWORK
        )

        # Run trading examples
        await trading_example.run_trading_examples()

    except Exception as e:
        print(f"❌ Error running trading examples: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure your RPC_URL is correct and accessible")
        print("2. Ensure your PRIVATE_KEY is valid and has sufficient funds")
        print("3. Check that the network you're using is correct")
        print("4. Verify that the token addresses are valid for your network")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())

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
        network: str = "Story Odyssey Testnet",
    ):
        """
        Initialize the trading example.

        Args:
            rpc_url: RPC endpoint URL
            private_key: Private key for signing transactions
            network: Network name (default: Story Odyssey Testnet)
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
            "0x0000000000000000000000000000000000000001"  # Example token
        )
        example_quote_token = (
            "0x0000000000000000000000000000000000000002"  # Example token
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

        print("✅ Trading examples completed!")


async def main():
    """Run the trading examples."""
    # Load environment variables from .env file
    load_dotenv()

    # Configuration - Replace with your actual values
    RPC_URL = os.getenv("RPC_URL", "https://rpc.testnet.mode.network")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")  # Your private key
    NETWORK = os.getenv("NETWORK", "Story Odyssey Testnet")

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

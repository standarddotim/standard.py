#!/usr/bin/env python3
"""
Simple Trading Example using StandardWeb3 Contract Functions.

This is a minimal example showing how to use the contract functions
for basic trading operations.
"""

import asyncio
import os
from dotenv import load_dotenv

# Import the StandardClient
from standardweb3 import StandardClient


async def simple_trading_example():
    """Demonstrate simple contract function usage for trading."""
    # Load environment variables from .env file
    load_dotenv()

    # Configuration
    RPC_URL = os.getenv("RPC_URL", "https://rpc.testnet.mode.network")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
    NETWORK = os.getenv("NETWORK", "Story Odyssey Testnet")

    if not PRIVATE_KEY:
        print("❌ Please set your PRIVATE_KEY environment variable")
        return

    # Initialize StandardClient
    client = StandardClient(
        private_key=PRIVATE_KEY,
        http_rpc_url=RPC_URL,
        networkName=NETWORK,
        api_url=None,
        websocket_url=None,
    )

    print(f"Account: {client.contract.address}")
    print(f"Network: {NETWORK}")
    print("-" * 40)

    # Example token addresses (replace with actual token addresses)
    base_token = "0x0000000000000000000000000000000000000001"  # Token to buy/sell
    quote_token = "0x0000000000000000000000000000000000000002"  # Token to spend/receive

    # Example 1: Market Buy
    print("📈 Market Buy Example")
    try:
        quote_amount = client.w3.to_wei(0.001, "ether")  # 0.001 ETH
        tx_receipt = await client.market_buy(
            base=base_token,
            quote=quote_token,
            quote_amount=quote_amount,
            is_maker=False,
            n=1,
            recipient=client.address,
            slippageLimit=10000000,
        )
        print(f"✅ Market buy successful! TX: {tx_receipt['transactionHash'].hex()}")
    except Exception as e:
        print(f"❌ Market buy failed: {e}")

    print()

    # Example 2: Limit Buy
    print("💰 Limit Buy Example")
    try:
        price = client.w3.to_wei(0.1, "ether")  # 0.1 ETH per token
        quote_amount = client.w3.to_wei(0.01, "ether")  # 0.01 ETH
        tx_receipt = await client.limit_buy(
            base=base_token,
            quote=quote_token,
            price=price,
            quote_amount=quote_amount,
            is_maker=True,
            n=1,
            recipient=client.address,
        )
        print(f"✅ Limit buy successful! TX: {tx_receipt['transactionHash'].hex()}")
    except Exception as e:
        print(f"❌ Limit buy failed: {e}")

    print()

    # Example 3: Market Sell
    print("📉 Market Sell Example")
    try:
        base_amount = client.w3.to_wei(0.001, "ether")  # 0.001 tokens
        tx_receipt = await client.market_sell(
            base=base_token,
            quote=quote_token,
            base_amount=base_amount,
            is_maker=False,
            n=1,
            recipient=client.address,
            slippageLimit=10000000,
        )
        print(f"✅ Market sell successful! TX: {tx_receipt['transactionHash'].hex()}")
    except Exception as e:
        print(f"❌ Market sell failed: {e}")

    print()

    # Example 4: Limit Sell
    print("💸 Limit Sell Example")
    try:
        price = client.w3.to_wei(0.15, "ether")  # 0.15 ETH per token
        base_amount = client.w3.to_wei(0.01, "ether")  # 0.01 tokens
        tx_receipt = await client.limit_sell(
            base=base_token,
            quote=quote_token,
            price=price,
            base_amount=base_amount,
            is_maker=True,
            n=1,
            recipient=client.address,
        )
        print(f"✅ Limit sell successful! TX: {tx_receipt['transactionHash'].hex()}")
    except Exception as e:
        print(f"❌ Limit sell failed: {e}")


async def main():
    """Run the simple trading example."""
    print("🚀 Simple Trading Example")
    print("=" * 30)
    await simple_trading_example()
    print("\n✅ Example completed!")


if __name__ == "__main__":
    asyncio.run(main())

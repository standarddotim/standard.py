#!/usr/bin/env python3
"""
ETH Trading Example using StandardWeb3.

This example demonstrates how to use the ETH-specific trading functions
that allow direct trading with ETH without needing WETH.
"""

import asyncio
import os
from dotenv import load_dotenv

# Import the StandardClient
from standardweb3 import StandardClient


async def match_trade():
    """Demonstrate ETH-specific trading functions."""
    # Load environment variables from .env file
    load_dotenv()

    # Configuration
    RPC_URL = os.getenv("RPC_URL", "https://rpc.testnet.mode.network")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
    NETWORK = os.getenv("NETWORK", "Somnia Testnet")

    if not PRIVATE_KEY:
        print("❌ Please set your PRIVATE_KEY environment variable")
        return

    # Initialize StandardClient
    client = StandardClient(
        private_key=PRIVATE_KEY,
        http_rpc_url=RPC_URL,
        networkName=NETWORK,
        api_url="https://new-api.standardweb3.com",
        matching_engine_address="0xa19D92429b00Da62Ce1B87713dee4688F75aFF2A",
        websocket_url=None,
    )

    print(f"Account: {client.contract.address}")
    print(f"Network: {NETWORK}")
    print("-" * 50)

    # Example token addresses
    base_token = "0x4A3BC48C156384f9564Fd65A53a2f3D534D8f2b7"  # Token to buy with ETH
    quote_token = "0x0ED782B8079529f7385c3eDA9fAf1EaA0DbC6a17"  # Token to receive

    # Example 1: Market Buy
    print("📈 Market Buy Example")
    try:
        quote_amount = 100  # 100 USDC
        result = await client.market_buy(
            base=base_token,
            quote=quote_token,
            quote_amount=quote_amount,
            is_maker=True,
            n=20,
            recipient=client.address,
            slippageLimit=0.1,
        )

    except Exception as e:
        print(f"❌ Market buy failed: {e}")

    print()

    # Example 2: Market Sell ETH
    print("📉 Market Sell ETH Example")
    try:
        quote_token = "0x0ED782B8079529f7385c3eDA9fAf1EaA0DbC6a17"  # Token to receive
        eth_amount = 1  # Sell 1 ETH

        result = await client.market_sell_eth(
            quote=quote_token,
            is_maker=True,
            n=1,
            recipient=client.address,
            slippage_limit=0.1,  # 0.1% slippage
            eth_amount=eth_amount,
        )

        print("✅ Market sell ETH successful!")
        print(f"  TX Hash: {result['tx_hash']}")
        print(f"  Gas Used: {result['gas_used']}")
        print(f"  ETH Sold: {eth_amount} ETH")

    except Exception as e:
        print(f"❌ Market sell ETH failed: {e}")

    print()
    print("✅ ETH trading examples completed!")


async def main():
    """Run the ETH trading example."""
    await match_trade()


if __name__ == "__main__":
    asyncio.run(main())

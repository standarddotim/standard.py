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


async def eth_trading_example():
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

    # Example 1: Limit Buy with ETH
    print("💰 Limit Buy ETH Example")
    try:
        price = client.w3.to_wei(0.001, "ether")  # 0.001 ETH per token
        eth_amount = client.w3.to_wei(0.01, "ether")  # Send 0.01 ETH

        result = await client.limit_buy_eth(
            base=base_token,
            price=price,
            is_maker=True,
            n=1,
            recipient=client.address,
            eth_amount=eth_amount,
        )

        print("✅ Limit buy ETH successful!")
        print(f"  TX Hash: {result['tx_hash']}")
        print(f"  Gas Used: {result['gas_used']}")
        print(f"  ETH Sent: {client.w3.from_wei(eth_amount, 'ether')} ETH")

        if result["decoded_logs"]:
            for event in result["decoded_logs"]:
                print(f"  📊 Event: {event['event']}")
                if event["event"] == "OrderPlaced":
                    args = event["args"]
                    print(f"    Order ID: {args.get('id', 'N/A')}")
                    print(f"    Price: {args.get('price', 'N/A')}")

    except Exception as e:
        print(f"❌ Limit buy ETH failed: {e}")

    print()

    # Example 2: Market Buy with ETH
    print("📈 Market Buy ETH Example")
    try:
        eth_amount = client.w3.to_wei(0.005, "ether")  # Send 0.005 ETH

        result = await client.market_buy_eth(
            base=base_token,
            is_maker=False,
            n=1,
            recipient=client.address,
            slippage_limit=10000000,  # 10% slippage
            eth_amount=eth_amount,
        )

        print("✅ Market buy ETH successful!")
        print(f"  TX Hash: {result['tx_hash']}")
        print(f"  Gas Used: {result['gas_used']}")
        print(f"  ETH Sent: {client.w3.from_wei(eth_amount, 'ether')} ETH")

        if result["decoded_logs"]:
            for event in result["decoded_logs"]:
                print(f"  📊 Event: {event['event']}")

    except Exception as e:
        print(f"❌ Market buy ETH failed: {e}")

    print()

    # Example 3: Limit Sell ETH
    print("💸 Limit Sell ETH Example")
    try:
        quote_token = "0x0ED782B8079529f7385c3eDA9fAf1EaA0DbC6a17"  # Token to receive
        price = 38600000000  # 1000 tokens per ETH
        eth_amount = client.w3.to_wei(0.01, "ether")  # Sell 0.01 ETH

        result = await client.limit_sell_eth(
            quote=quote_token,
            price=price,
            is_maker=True,
            n=1,
            recipient=client.address,
            eth_amount=eth_amount,
        )

        print("✅ Limit sell ETH successful!")
        print(f"  TX Hash: {result['tx_hash']}")
        print(f"  Gas Used: {result['gas_used']}")
        print(f"  ETH Sold: {client.w3.from_wei(eth_amount, 'ether')} ETH")

    except Exception as e:
        print(f"❌ Limit sell ETH failed: {e}")

    print()

    # Example 4: Market Sell ETH
    print("📉 Market Sell ETH Example")
    try:
        quote_token = "0x0ED782B8079529f7385c3eDA9fAf1EaA0DbC6a17"  # Token to receive
        eth_amount = client.w3.to_wei(0.005, "ether")  # Sell 0.005 ETH

        result = await client.market_sell_eth(
            quote=quote_token,
            is_maker=False,
            n=1,
            recipient=client.address,
            slippage_limit=10000000,  # 10% slippage
            eth_amount=eth_amount,
        )

        print("✅ Market sell ETH successful!")
        print(f"  TX Hash: {result['tx_hash']}")
        print(f"  Gas Used: {result['gas_used']}")
        print(f"  ETH Sold: {client.w3.from_wei(eth_amount, 'ether')} ETH")

    except Exception as e:
        print(f"❌ Market sell ETH failed: {e}")

    print()
    print("✅ ETH trading examples completed!")


async def main():
    """Run the ETH trading example."""
    await eth_trading_example()


if __name__ == "__main__":
    asyncio.run(main())

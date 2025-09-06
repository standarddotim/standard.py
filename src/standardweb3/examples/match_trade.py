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
        quote_amount = 100000000  # 0.001 ETH
        result = await client.market_buy(
            base=base_token,
            quote=quote_token,
            quote_amount=quote_amount,
            is_maker=True,
            n=20,
            recipient=client.address,
            slippageLimit=10000000,
        )
        print("✅ Market buy successful!")
        print(f"  TX Hash: {result['tx_hash']}")
        print(f"  Gas Used: {result['gas_used']}")
        print(f"  Status: {'Success' if result['status'] == 1 else 'Failed'}")

        if result["decoded_logs"]:
            print(f"  📊 Events Decoded: {len(result['decoded_logs'])}")
            for event in result["decoded_logs"]:
                print(f"    - {event['event']}")
                if event["event"] == "OrderPlaced":
                    args = event["args"]
                    print(f"      Order ID: {args.get('id', 'N/A')}")
                    print(f"      Price: {args.get('price', 'N/A')}")
                    print(f"      Amount Placed: {args.get('placed', 'N/A')}")
                elif event["event"] == "OrderMatched":
                    args = event["args"]
                    print(f"      Order ID: {args.get('id', 'N/A')}")
                    print(f"      Price: {args.get('price', 'N/A')}")
                    print(f"      Total: {args.get('total', 'N/A')}")
                elif event["event"] == "OrderCanceled":
                    args = event["args"]
                    print(f"      Order ID: {args.get('id', 'N/A')}")
                    print(f"      Price: {args.get('price', 'N/A')}")
                    print(f"      Amount Canceled: {args.get('amount', 'N/A')}")
                elif event["event"] == "NewMarketPrice":
                    args = event["args"]
                    print(f"      Price: {args.get('price', 'N/A')}")
                    print(f"      Base Token: {args.get('base', 'N/A')}")
                    print(f"      Quote Token: {args.get('quote', 'N/A')}")
                elif event["event"] == "PairAdded":
                    args = event["args"]
                    print(f"      Pair Address: {args.get('pair', 'N/A')}")
                    print(f"      Base Token: {args.get('base', 'N/A')}")
                    print(f"      Quote Token: {args.get('quote', 'N/A')}")
        else:
            print("  📊 No events decoded")
    except Exception as e:
        print(f"❌ Market buy failed: {e}")

    print()

    # Example 2: Market Sell ETH
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
    await match_trade()


if __name__ == "__main__":
    asyncio.run(main())

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
    print("-" * 40)

    # Fetch and display tokens
    try:
        tokens = client.tokens
        print(f"Tokens: {tokens}")
        print(f"Available tokens: {len(tokens) if tokens else 0}")
        if tokens and len(tokens) > 0:
            print("First few tokens:")
            for token in tokens[:3]:  # Show first 3 tokens
                print(
                    f"  - {token.get('symbol', 'N/A')}: {token.get('address', 'N/A')}"
                )
    except Exception as e:
        print(f"Could not fetch tokens: {e}")

    # Example token addresses (replace with actual token addresses)
    base_token = "0x4A3BC48C156384f9564Fd65A53a2f3D534D8f2b7"  # Token to buy/sell
    quote_token = "0x0ED782B8079529f7385c3eDA9fAf1EaA0DbC6a17"  # Token to spend/receive

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
            slippage_limit=10000000,
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

    # Example 2: Limit Buy
    print("💰 Limit Buy Example")
    try:
        price = 100000000  # 0.1 ETH per token
        quote_amount = 100000000  # 0.01 ETH
        result = await client.limit_buy(
            base=base_token,
            quote=quote_token,
            price=price,
            quote_amount=quote_amount,
            is_maker=True,
            n=20,
            recipient=client.address,
        )
        print("✅ Limit buy successful!")
        print(f"  TX Hash: {result['tx_hash']}")
        event_count = len(result["decoded_logs"]) if result["decoded_logs"] else 0
        print(f"  Events: {event_count} decoded")
    except Exception as e:
        print(f"❌ Limit buy failed: {e}")

    print()

    # Example 3: Market Sell
    print("📉 Market Sell Example")
    try:
        base_amount = 100000000  # 0.001 tokens
        result = await client.market_sell(
            base=base_token,
            quote=quote_token,
            base_amount=base_amount,
            is_maker=True,
            n=20,
            recipient=client.address,
            slippage_limit=10000000,
        )
        print("✅ Market sell successful! TX: {result}")
    except Exception as e:
        print(f"❌ Market sell failed: {e}")

    print()

    # Example 4: Limit Sell
    print("💸 Limit Sell Example")
    try:
        price = 100000000  # 0.15 ETH per token
        base_amount = 100000000  # 0.01 tokens
        result = await client.limit_sell(
            base=base_token,
            quote=quote_token,
            price=price,
            base_amount=base_amount,
            is_maker=True,
            n=20,
            recipient=client.address,
        )
        print(f"✅ Limit sell successful! TX: {result}")
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

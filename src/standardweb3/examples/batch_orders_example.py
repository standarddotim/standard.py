#!/usr/bin/env python3
"""
Batch Orders Example using StandardWeb3.

This example demonstrates how to create, update, and cancel multiple orders
in batch operations using the new create_orders and update_orders functions.
"""

import asyncio
import os
from dotenv import load_dotenv

# Import the StandardClient
from standardweb3 import StandardClient


def parse_units(value: float, decimals: int) -> int:
    """
    Parse a float value to wei with specified decimal places.

    Args:
        value: The float value to parse
        decimals: Number of decimal places

    Returns:
        int: The value in the smallest unit (wei equivalent)
    """
    return int(value * (10**decimals))


async def batch_orders_example():
    """Demonstrate batch order operations."""
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
    base_token = "0x4A3BC48C156384f9564Fd65A53a2f3D534D8f2b7"
    quote_token = "0x0ED782B8079529f7385c3eDA9fAf1EaA0DbC6a17"

    # Example 1: Create Multiple Orders
    print("📦 Create Multiple Orders Example")
    try:
        create_data = [
            {
                "base": base_token,
                "quote": quote_token,
                "isBid": True,  # Buy order
                "isLimit": True,  # Limit order
                "orderId": 1,
                "price": 0.001,  # 0.001 USDC per STT
                "amount": 10,  # 10 USDC
                "n": 1,
                "recipient": client.address,
                "isETH": False,
            },
            {
                "base": base_token,
                "quote": quote_token,
                "isBid": True,  # Buy order
                "isLimit": True,  # Limit order
                "orderId": 2,
                "price": 0.0009,  # 0.0009 USDC per STT
                "amount": 20,  # 20 USDC
                "n": 1,
                "recipient": client.address,
                "isETH": False,
            },
            {
                "base": base_token,
                "quote": quote_token,
                "isBid": False,  # Sell order
                "isLimit": True,  # Limit order
                "orderId": 3,
                "price": 400,  # 0.002 USDC per STT
                "amount": 5,  # 5 USDC
                "n": 1,
                "recipient": client.address,
                "isETH": True,
            },
        ]

        result = await client.create_orders(create_data)

        print("✅ Multiple orders created successfully!")
        print(f"  TX Hash: {result['tx_hash']}")
        print(f"  Gas Used: {result['gas_used']}")
        print(f"  Created Orders: {result['order_infos']}")

        if result["decoded_logs"]:
            print(f"  📊 Events Decoded: {len(result['decoded_logs'])}")
            for event in result["decoded_logs"]:
                print(f"    - {event['event']}")
                if event["event"] == "OrderPlaced":
                    args = event["args"]
                    print(f"      Order ID: {args.get('id', 'N/A')}")
                    print(f"      Price: {args.get('price', 'N/A')}")
                    print(f"      Amount: {args.get('placed', 'N/A')}")

    except Exception as e:
        print(f"❌ Create orders failed: {e}")

    print()

    # Example 2: Update Multiple Orders
    print("🔄 Update Multiple Orders Example")
    try:
        update_data = [
            {
                "base": base_token,
                "quote": quote_token,
                "isBid": True,
                "isLimit": True,
                "orderId": 2,
                "price": 0.0011,  # Updated price: 0.0011 USDC per STT
                "amount": 25,  # Updated amount
                "n": 1,
                "recipient": client.address,
                "isETH": False,
            },
            {
                "base": base_token,
                "quote": quote_token,
                "isBid": False,  # Keep as BUY order (same as original)
                "isLimit": True,  # Limit order
                "orderId": 1,
                "price": 400,  # Updated price: 0.0012 USDC per STT
                "amount": 15,  # Updated amount: 15 USDC
                "n": 1,
                "recipient": client.address,
                "isETH": True,  # Keep as token order
            },
        ]

        result = await client.update_orders(update_data)

        print("✅ Multiple orders updated successfully!")
        print(f"  TX Hash: {result['tx_hash']}")
        print(f"  Gas Used: {result['gas_used']}")
        print(f"  TX Result: {result}")

        if result["decoded_logs"]:
            print(f"  📊 Events Decoded: {len(result['decoded_logs'])}")
            for event in result["decoded_logs"]:
                print(f"    - {event['event']}")

    except Exception as e:
        print(f"❌ Update orders failed: {e}")

    print()

    # Example 3: Create Orders with Default OrderId
    print("🆔 Create Orders with Default OrderId Example")
    try:
        # When orderId is not provided, it defaults to 0
        create_data_no_id = [
            {
                "base": base_token,
                "quote": quote_token,
                "isBid": True,
                "isLimit": True,
                # orderId not provided - will default to 0
                "price": 0.0015,  # 0.0015 USDC per STT
                "amount": 8,
                "n": 1,
                "recipient": client.address,
                "isETH": False,
            }
        ]

        result = await client.create_orders(create_data_no_id)

        print("✅ Order created with default ID!")
        print(f"  TX Hash: {result['tx_hash']}")
        print(f"  Gas Used: {result['gas_used']}")

    except Exception as e:
        print(f"❌ Create order with default ID failed: {e}")

    print()
    print("✅ Batch orders examples completed!")


async def main():
    """Run the batch orders example."""
    await batch_orders_example()


if __name__ == "__main__":
    asyncio.run(main())

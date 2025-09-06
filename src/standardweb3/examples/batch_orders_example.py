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
                "price": client.w3.to_wei(0.001, "ether"),  # 0.001 ETH per token
                "amount": client.w3.to_wei(10, "ether"),  # 10 tokens
                "n": 1,
                "recipient": client.address,
            },
            {
                "base": base_token,
                "quote": quote_token,
                "isBid": True,  # Buy order
                "isLimit": True,  # Limit order
                "orderId": 2,
                "price": client.w3.to_wei(0.0009, "ether"),  # 0.0009 ETH per token
                "amount": client.w3.to_wei(20, "ether"),  # 20 tokens
                "n": 1,
                "recipient": client.address,
            },
            {
                "base": base_token,
                "quote": quote_token,
                "isBid": False,  # Sell order
                "isLimit": True,  # Limit order
                "orderId": 3,
                "price": client.w3.to_wei(0.002, "ether"),  # 0.002 ETH per token
                "amount": client.w3.to_wei(5, "ether"),  # 5 tokens
                "n": 1,
                "recipient": client.address,
            },
        ]

        result = await client.create_orders(create_data)

        print("✅ Multiple orders created successfully!")
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
                "orderId": 1,
                "price": client.w3.to_wei(0.0012, "ether"),  # Updated price
                "amount": client.w3.to_wei(15, "ether"),  # Updated amount
                "n": 1,
                "recipient": client.address,
            },
            {
                "base": base_token,
                "quote": quote_token,
                "isBid": True,
                "isLimit": True,
                "orderId": 2,
                "price": client.w3.to_wei(0.0011, "ether"),  # Updated price
                "amount": client.w3.to_wei(25, "ether"),  # Updated amount
                "n": 1,
                "recipient": client.address,
            },
        ]

        result = await client.update_orders(update_data)

        print("✅ Multiple orders updated successfully!")
        print(f"  TX Hash: {result['tx_hash']}")
        print(f"  Gas Used: {result['gas_used']}")
        print(f"  Status: {'Success' if result['status'] == 1 else 'Failed'}")

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
                "price": client.w3.to_wei(0.0015, "ether"),
                "amount": client.w3.to_wei(8, "ether"),
                "n": 1,
                "recipient": client.address,
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

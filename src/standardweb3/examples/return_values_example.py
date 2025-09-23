#!/usr/bin/env python3
"""
Contract Return Values Example using StandardWeb3.

This example demonstrates how to access return values from contract interactions,
including both transaction results and view function calls.
"""

import asyncio
import os
from dotenv import load_dotenv

# Import the StandardClient
from standardweb3 import StandardClient


async def return_values_example():
    """Demonstrate how to access return values from contract interactions."""
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
        api_url=None,
        websocket_url=None,
    )

    print(f"Account: {client.contract.address}")
    print(f"Network: {NETWORK}")
    print("-" * 50)

    # Example token addresses (replace with actual token addresses)
    base_token = "0x4A3BC48C156384f9564Fd65A53a2f3D534D8f2b7"  # Token to buy/sell
    quote_token = "0x0ED782B8079529f7385c3eDA9fAf1EaA0DbC6a17"  # Token to spend/receive

    # Example 1: View Functions (no transactions, direct return values)
    print("🔍 View Functions Example")
    try:
        # Get pair address
        pair_address = await client.contract.get_pair(base_token, quote_token)
        print(f"Pair address: {pair_address}")

        # Get market price
        market_price = await client.contract.get_market_price(base_token, quote_token)
        print(f"Market price: {market_price}")

        # Get order book heads
        heads = await client.contract.get_heads(base_token, quote_token)
        print(f"Bid head: {heads['bid_head']}, Ask head: {heads['ask_head']}")

        # Convert amount
        amount_to_convert = client.w3.to_wei(1, "ether")
        converted = await client.contract.convert(
            base_token, quote_token, amount_to_convert, True
        )
        print(f"Converted amount: {converted}")

        # Get fee
        fee = await client.contract.get_fee_of(
            base_token, quote_token, client.address, True
        )
        print(f"Fee for account: {fee}")

    except Exception as e:
        print(f"❌ View functions failed: {e}")

    print()

    # Example 2: Transaction with Return Values
    print("💰 Limit Buy with Return Values")
    try:
        price = client.w3.to_wei(0.1, "ether")  # 0.1 ETH per token
        quote_amount = client.w3.to_wei(0.01, "ether")  # 0.01 ETH

        # Execute limit buy and get full result
        result = await client.contract.limit_buy(
            base=base_token,
            quote=quote_token,
            price=price,
            quote_amount=quote_amount,
            is_maker=True,
            n=1,
            recipient=client.address,
        )

        # Access transaction details
        print("✅ Transaction successful!")
        print(f"TX Hash: {result['tx_hash']}")
        print(f"Gas used: {result['gas_used']}")
        print(f"Status: {'Success' if result['status'] == 1 else 'Failed'}")

        # Access return values from events (if any)
        if result["return_values"]:
            print("📋 Events emitted:")
            for event in result["return_values"]:
                print(f"  - {event['event']}: {event['args']}")
        else:
            print("📋 No events decoded (this is normal for some functions)")

        # Access the full transaction receipt if needed
        tx_receipt = result["tx_receipt"]
        print(f"Block number: {tx_receipt.blockNumber}")

    except Exception as e:
        print(f"❌ Limit buy failed: {e}")

    print()

    # Example 3: Market Buy with Return Values
    print("📈 Market Buy with Return Values")
    try:
        quote_amount = client.w3.to_wei(0.001, "ether")  # 0.001 ETH

        result = await client.contract.market_buy(
            base=base_token,
            quote=quote_token,
            quote_amount=quote_amount,
            is_maker=False,
            n=1,
            recipient=client.address,
            slippage_limit=10000000,
        )

        print("✅ Market buy successful!")
        print(f"TX Hash: {result['tx_hash']}")
        print(f"Gas used: {result['gas_used']}")

        # The actual return values (OrderResult struct) would typically be in events
        if result["return_values"]:
            print("📊 Order Results:")
            for event in result["return_values"]:
                if event["event"] == "OrderPlaced":
                    args = event["args"]
                    print(f"  Order ID: {args.get('id', 'N/A')}")
                    print(f"  Price: {args.get('price', 'N/A')}")
                    print(f"  Amount Placed: {args.get('placed', 'N/A')}")

    except Exception as e:
        print(f"❌ Market buy failed: {e}")

    print()

    # Example 4: Cancel Orders with Return Values
    print("❌ Cancel Orders Example")
    try:
        # Example cancel data (replace with actual order IDs)
        cancel_data = [
            {
                "base": base_token,
                "quote": quote_token,
                "isBid": True,
                "orderId": 12345,  # Replace with actual order ID
            }
        ]

        result = await client.contract.cancel_orders(cancel_data)

        print("✅ Orders canceled!")
        print(f"TX Hash: {result['tx_hash']}")
        print(f"Gas used: {result['gas_used']}")

        # Check for cancellation events
        if result["return_values"]:
            for event in result["return_values"]:
                if event["event"] == "OrderCanceled":
                    args = event["args"]
                    print(f"  Canceled Order ID: {args.get('id', 'N/A')}")
                    print(f"  Refunded Amount: {args.get('amount', 'N/A')}")

    except Exception as e:
        print(f"❌ Cancel orders failed: {e}")

    print()

    # Example 5: Get Specific Order Details
    print("📋 Get Order Details Example")
    try:
        # Get details of a specific order (replace with actual order ID)
        order_id = 12345
        order_details = await client.contract.get_order(
            base_token, quote_token, True, order_id  # True for bid order
        )

        print(f"Order {order_id} details:")
        print(f"  Owner: {order_details['owner']}")
        print(f"  Price: {order_details['price']}")
        print(f"  Deposit Amount: {order_details['deposit_amount']}")

    except Exception as e:
        print(f"❌ Get order details failed: {e}")


if __name__ == "__main__":
    asyncio.run(return_values_example())

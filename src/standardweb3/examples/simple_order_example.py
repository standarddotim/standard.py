"""Simple Order Management Example for Standard Protocol.

A minimal example showing how to create, update, and cancel orders
using the Standard Protocol contract functions.
"""

import asyncio
from standardweb3 import StandardClient


async def create_order_example():
    """Demonstrate creating a single order."""
    print("📝 Creating Order Example")
    print("-" * 30)

    # Initialize client (replace with your credentials)
    client = StandardClient(
        private_key="your_private_key_here",
        http_rpc_url="https://your-rpc-url.com",
        networkName="Somnia Testnet",
        matching_engine_address="0x1234567890123456789012345678901234567890",
    )

    # Example token addresses (replace with actual addresses)
    eth_address = "0x0000000000000000000000000000000000000000"
    usdc_address = "0xA0b86a33E6441c8C06DD2b7c47d2a82f0e7B3C2D"

    # Create order data
    order_data = {
        "base": eth_address,  # Base token (ETH)
        "quote": usdc_address,  # Quote token (USDC)
        "isBid": True,  # True = Buy order, False = Sell order
        "isLimit": True,  # True = Limit order, False = Market order
        "orderId": 0,  # 0 for new orders
        "price": int(2000 * 10**18),  # $2000 per ETH (in wei)
        "amount": int(1 * 10**18),  # 1 ETH (in wei)
        "n": 1,  # Number parameter
        "recipient": client.account.address,  # Recipient address
        "isETH": False,  # True if using ETH directly
    }

    try:
        print("Creating buy order: 1 ETH at $2000...")
        result = await client.create_orders([order_data])

        if result.get("status") == "success":
            print("✅ Order created successfully!")
            print(f"Transaction Hash: {result.get('tx_hash')}")
            print(f"Gas Used: {result.get('gas_used')}")

            order_info = result.get("order_info", {})
            order_id = order_info.get("orderId", "N/A")
            print(f"Order ID: {order_id}")

            return order_id
        else:
            print("❌ Order creation failed!")
            print(f"Error: {result}")
            return None

    except Exception as e:
        print(f"❌ Error creating order: {e}")
        return None


async def update_order_example(order_id: int):
    """Demonstrate updating an existing order."""
    print("\n🔄 Updating Order Example")
    print("-" * 30)

    if order_id is None:
        print("⏭️ Skipping update (no order ID)")
        return

    client = StandardClient(
        private_key="your_private_key_here",
        http_rpc_url="https://your-rpc-url.com",
        networkName="Somnia Testnet",
        matching_engine_address="0x1234567890123456789012345678901234567890",
    )

    eth_address = "0x0000000000000000000000000000000000000000"
    usdc_address = "0xA0b86a33E6441c8C06DD2b7c47d2a82f0e7B3C2D"

    # Update order data (change price and amount)
    update_data = {
        "base": eth_address,
        "quote": usdc_address,
        "isBid": True,  # Same as original
        "isLimit": True,  # Same as original
        "orderId": order_id,  # Order ID to update
        "price": int(1950 * 10**18),  # New price: $1950 per ETH
        "amount": int(1.2 * 10**18),  # New amount: 1.2 ETH
        "n": 1,
        "recipient": client.account.address,
        "isETH": False,
    }

    try:
        print(f"Updating order #{order_id}: new price $1950, amount 1.2 ETH...")
        result = await client.update_orders([update_data])

        if result.get("status") == "success":
            print("✅ Order updated successfully!")
            print(f"Transaction Hash: {result.get('tx_hash')}")
            print(f"Gas Used: {result.get('gas_used')}")
        else:
            print("❌ Order update failed!")
            print(f"Error: {result}")

    except Exception as e:
        print(f"❌ Error updating order: {e}")


async def cancel_order_example(order_id: int):
    """Demonstrate cancelling an order."""
    print("\n❌ Cancelling Order Example")
    print("-" * 30)

    if order_id is None:
        print("⏭️ Skipping cancel (no order ID)")
        return

    client = StandardClient(
        private_key="your_private_key_here",
        http_rpc_url="https://your-rpc-url.com",
        networkName="Somnia Testnet",
        matching_engine_address="0x1234567890123456789012345678901234567890",
    )

    eth_address = "0x0000000000000000000000000000000000000000"
    usdc_address = "0xA0b86a33E6441c8C06DD2b7c47d2a82f0e7B3C2D"

    # Create cancel order ID string: "base_quote_isBid_orderId"
    cancel_id = f"{eth_address}_{usdc_address}_True_{order_id}"

    try:
        print(f"Cancelling order #{order_id}...")
        tx_hash = await client.cancel_orders([cancel_id])

        if tx_hash:
            print("✅ Order cancelled successfully!")
            print(f"Transaction Hash: {tx_hash}")
        else:
            print("❌ Order cancellation failed!")

    except Exception as e:
        print(f"❌ Error cancelling order: {e}")


async def batch_orders_example():
    """Demonstrate creating multiple orders at once."""
    print("\n📝 Batch Orders Example")
    print("-" * 30)

    client = StandardClient(
        private_key="your_private_key_here",
        http_rpc_url="https://your-rpc-url.com",
        networkName="Somnia Testnet",
        matching_engine_address="0x1234567890123456789012345678901234567890",
    )

    eth_address = "0x0000000000000000000000000000000000000000"
    usdc_address = "0xA0b86a33E6441c8C06DD2b7c47d2a82f0e7B3C2D"

    # Create multiple orders
    batch_orders = [
        # Buy order 1: 0.5 ETH at $1900
        {
            "base": eth_address,
            "quote": usdc_address,
            "isBid": True,
            "isLimit": True,
            "orderId": 0,
            "price": int(1900 * 10**18),
            "amount": int(0.5 * 10**18),
            "n": 1,
            "recipient": client.account.address,
            "isETH": False,
        },
        # Buy order 2: 0.3 ETH at $1850
        {
            "base": eth_address,
            "quote": usdc_address,
            "isBid": True,
            "isLimit": True,
            "orderId": 0,
            "price": int(1850 * 10**18),
            "amount": int(0.3 * 10**18),
            "n": 1,
            "recipient": client.account.address,
            "isETH": False,
        },
        # Sell order: 0.8 ETH at $2100
        {
            "base": eth_address,
            "quote": usdc_address,
            "isBid": False,  # Sell order
            "isLimit": True,
            "orderId": 0,
            "price": int(2100 * 10**18),
            "amount": int(0.8 * 10**18),
            "n": 1,
            "recipient": client.account.address,
            "isETH": False,
        },
    ]

    try:
        print(f"Creating {len(batch_orders)} orders in one transaction...")
        print("  - Buy 0.5 ETH at $1900")
        print("  - Buy 0.3 ETH at $1850")
        print("  - Sell 0.8 ETH at $2100")

        result = await client.create_orders(batch_orders)

        if result.get("status") == "success":
            print("✅ Batch orders created successfully!")
            print(f"Transaction Hash: {result.get('tx_hash')}")
            print(f"Gas Used: {result.get('gas_used')}")

            # Show order IDs if available
            order_infos = result.get("order_infos", [])
            if order_infos:
                print("Order IDs created:")
                for i, order_info in enumerate(order_infos):
                    order_id = order_info.get("orderId", "N/A")
                    print(f"  Order {i+1}: #{order_id}")

            return order_infos
        else:
            print("❌ Batch order creation failed!")
            print(f"Error: {result}")
            return []

    except Exception as e:
        print(f"❌ Error creating batch orders: {e}")
        return []


async def main():
    """Run simple order management examples."""
    print("🌟 Simple Order Management Examples")
    print("=" * 50)

    try:
        # 1. Create a single order
        order_id = await create_order_example()

        await asyncio.sleep(2)  # Wait between operations

        # 2. Update the order
        await update_order_example(order_id)

        await asyncio.sleep(2)

        # 3. Cancel the order
        await cancel_order_example(order_id)

        await asyncio.sleep(2)

        # 4. Create batch orders
        await batch_orders_example()

    except KeyboardInterrupt:
        print("\n⏹️ Examples interrupted by user")
    except Exception as e:
        print(f"❌ Error in main: {e}")

    print("\n✅ Simple order management examples completed!")


if __name__ == "__main__":
    asyncio.run(main())

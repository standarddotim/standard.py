"""Order Management Example for Standard Protocol.

This example demonstrates how to create, update, and cancel orders using
the Standard Protocol contract functions. It includes both single and batch
operations with proper error handling and validation.
"""

import asyncio
from typing import List, Dict, Any
from standardweb3 import StandardClient


class OrderManager:
    """Order management helper class for Standard Protocol."""

    def __init__(self, client: StandardClient):
        """Initialize the OrderManager.

        Args:
            client: StandardClient instance
        """
        self.client = client
        self.created_orders = []  # Track created orders for examples

    def create_order_data(
        self,
        base_token: str,
        quote_token: str,
        is_buy: bool,
        is_limit: bool,
        price: float,
        amount: float,
        order_id: int = 0,
        n: int = 1,
        recipient: str = None,
        is_eth: bool = False,
    ) -> Dict[str, Any]:
        """Create order data dictionary.

        Args:
            base_token: Base token address
            quote_token: Quote token address
            is_buy: True for buy orders, False for sell orders
            is_limit: True for limit orders, False for market orders
            price: Order price (will be converted to wei)
            amount: Order amount (will be converted to wei)
            order_id: Order ID (0 for new orders)
            n: Number parameter (default: 1)
            recipient: Recipient address (defaults to client address)
            is_eth: True if using ETH as quote token

        Returns:
            Dictionary containing order data
        """
        if recipient is None:
            recipient = self.client.account.address

        # Convert to wei (assuming 18 decimals)
        price_wei = int(price * 10**18)
        amount_wei = int(amount * 10**18)

        return {
            "base": base_token,
            "quote": quote_token,
            "isBid": is_buy,
            "isLimit": is_limit,
            "orderId": order_id,
            "price": price_wei,
            "amount": amount_wei,
            "n": n,
            "recipient": recipient,
            "isETH": is_eth,
        }

    def create_cancel_order_id(
        self, base_token: str, quote_token: str, is_buy: bool, order_id: int
    ) -> str:
        """Create cancel order ID string.

        Args:
            base_token: Base token address
            quote_token: Quote token address
            is_buy: True for buy orders, False for sell orders
            order_id: Order ID to cancel

        Returns:
            Formatted order ID string for cancellation
        """
        return f"{base_token}_{quote_token}_{is_buy}_{order_id}"

    async def create_single_order(
        self,
        base_token: str,
        quote_token: str,
        is_buy: bool,
        price: float,
        amount: float,
        is_limit: bool = True,
        is_eth: bool = False,
    ) -> Dict[str, Any]:
        """Create a single order.

        Args:
            base_token: Base token address
            quote_token: Quote token address
            is_buy: True for buy, False for sell
            price: Order price
            amount: Order amount
            is_limit: True for limit order, False for market
            is_eth: True if using ETH

        Returns:
            Transaction result
        """
        print(f"📝 Creating {'BUY' if is_buy else 'SELL'} order:")
        print(f"    Pair: {base_token[:6]}.../{quote_token[:6]}...")
        print(f"    Price: ${price}")
        print(f"    Amount: {amount}")
        print(f"    Type: {'LIMIT' if is_limit else 'MARKET'}")

        order_data = self.create_order_data(
            base_token=base_token,
            quote_token=quote_token,
            is_buy=is_buy,
            is_limit=is_limit,
            price=price,
            amount=amount,
            is_eth=is_eth,
        )

        try:
            result = await self.client.create_orders([order_data])

            if result.get("status") == "success":
                print("✅ Order created successfully!")
                print(f"    Transaction Hash: {result.get('tx_hash')}")
                print(f"    Gas Used: {result.get('gas_used')}")

                # Track the order for later examples
                order_info = {
                    "base": base_token,
                    "quote": quote_token,
                    "is_buy": is_buy,
                    "order_id": result.get("order_info", {}).get("orderId", 1),
                    "price": price,
                    "amount": amount,
                }
                self.created_orders.append(order_info)

            else:
                print("❌ Order creation failed!")
                print(f"    Error: {result}")

            return result

        except Exception as e:
            print(f"❌ Error creating order: {e}")
            return {"status": "error", "error": str(e)}

    async def create_batch_orders(self, orders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple orders in a single transaction.

        Args:
            orders: List of order data dictionaries

        Returns:
            Transaction result
        """
        print(f"📝 Creating batch of {len(orders)} orders:")

        for i, order in enumerate(orders, 1):
            print(f"    Order {i}: {'BUY' if order['isBid'] else 'SELL'}")
            print(f"        Price: ${order['price'] / 10**18}")
            print(f"        Amount: {order['amount'] / 10**18}")

        try:
            result = await self.client.create_orders(orders)

            if result.get("status") == "success":
                print("✅ Batch orders created successfully!")
                print(f"    Transaction Hash: {result.get('tx_hash')}")
                print(f"    Gas Used: {result.get('gas_used')}")

                # Track orders for later examples
                order_infos = result.get("order_infos", [])
                for i, order_info in enumerate(order_infos):
                    if i < len(orders):
                        order_data = orders[i]
                        tracked_order = {
                            "base": order_data["base"],
                            "quote": order_data["quote"],
                            "is_buy": order_data["isBid"],
                            "order_id": order_info.get("orderId", i + 1),
                            "price": order_data["price"] / 10**18,
                            "amount": order_data["amount"] / 10**18,
                        }
                        self.created_orders.append(tracked_order)
            else:
                print("❌ Batch order creation failed!")
                print(f"    Error: {result}")

            return result

        except Exception as e:
            print(f"❌ Error creating batch orders: {e}")
            return {"status": "error", "error": str(e)}

    async def update_order(
        self,
        base_token: str,
        quote_token: str,
        order_id: int,
        is_buy: bool,
        new_price: float,
        new_amount: float,
        is_eth: bool = False,
    ) -> Dict[str, Any]:
        """Update an existing order.

        Args:
            base_token: Base token address
            quote_token: Quote token address
            order_id: Order ID to update
            is_buy: True for buy orders, False for sell orders
            new_price: New price for the order
            new_amount: New amount for the order
            is_eth: True if using ETH

        Returns:
            Transaction result
        """
        print(f"🔄 Updating order #{order_id}:")
        print(f"    Pair: {base_token[:6]}.../{quote_token[:6]}...")
        print(f"    New Price: ${new_price}")
        print(f"    New Amount: {new_amount}")

        update_data = self.create_order_data(
            base_token=base_token,
            quote_token=quote_token,
            is_buy=is_buy,
            is_limit=True,  # Updates are typically for limit orders
            price=new_price,
            amount=new_amount,
            order_id=order_id,
            is_eth=is_eth,
        )

        try:
            result = await self.client.update_orders([update_data])

            if result.get("status") == "success":
                print("✅ Order updated successfully!")
                print(f"    Transaction Hash: {result.get('tx_hash')}")
                print(f"    Gas Used: {result.get('gas_used')}")
            else:
                print("❌ Order update failed!")
                print(f"    Error: {result}")

            return result

        except Exception as e:
            print(f"❌ Error updating order: {e}")
            return {"status": "error", "error": str(e)}

    async def cancel_order(
        self, base_token: str, quote_token: str, is_buy: bool, order_id: int
    ) -> str:
        """Cancel a single order.

        Args:
            base_token: Base token address
            quote_token: Quote token address
            is_buy: True for buy orders, False for sell orders
            order_id: Order ID to cancel

        Returns:
            Transaction hash
        """
        print(f"❌ Cancelling order #{order_id}:")
        print(f"    Pair: {base_token[:6]}.../{quote_token[:6]}...")
        print(f"    Side: {'BUY' if is_buy else 'SELL'}")

        cancel_id = self.create_cancel_order_id(
            base_token, quote_token, is_buy, order_id
        )

        try:
            tx_hash = await self.client.cancel_orders([cancel_id])
            print("✅ Order cancelled successfully!")
            print(f"    Transaction Hash: {tx_hash}")
            return tx_hash

        except Exception as e:
            print(f"❌ Error cancelling order: {e}")
            return None

    async def cancel_multiple_orders(self, order_ids: List[str]) -> str:
        """Cancel multiple orders in a single transaction.

        Args:
            order_ids: List of order ID strings to cancel

        Returns:
            Transaction hash
        """
        print(f"❌ Cancelling {len(order_ids)} orders:")
        for i, order_id in enumerate(order_ids, 1):
            parts = order_id.split("_")
            print(
                f"    Order {i}: {parts[0][:6]}.../{parts[1][:6]}... "
                f"({'BUY' if parts[2] == 'True' else 'SELL'}) #{parts[3]}"
            )

        try:
            tx_hash = await self.client.cancel_orders(order_ids)
            print("✅ Orders cancelled successfully!")
            print(f"    Transaction Hash: {tx_hash}")
            return tx_hash

        except Exception as e:
            print(f"❌ Error cancelling orders: {e}")
            return None


async def basic_order_management_example():
    """Demonstrate basic order management operations."""
    print("🚀 Basic Order Management Example")
    print("=" * 50)

    # Initialize the Standard client
    # Replace these with your actual credentials
    client = StandardClient(
        private_key="your_private_key_here",
        http_rpc_url="https://your-rpc-url.com",
        networkName="Somnia Testnet",
        matching_engine_address="0x1234567890123456789012345678901234567890",
    )

    # Example token addresses (replace with actual addresses)
    eth_address = "0x0000000000000000000000000000000000000000"
    usdc_address = "0xA0b86a33E6441c8C06DD2b7c47d2a82f0e7B3C2D"

    # Initialize order manager
    order_manager = OrderManager(client)

    try:
        # 1. Create a single buy order
        print("\n1️⃣ Creating a single buy order...")
        await order_manager.create_single_order(
            base_token=eth_address,
            quote_token=usdc_address,
            is_buy=True,
            price=2000.0,  # $2000 per ETH
            amount=1.0,  # 1 ETH
            is_limit=True,
        )

        await asyncio.sleep(2)  # Wait between operations

        # 2. Create a single sell order
        print("\n2️⃣ Creating a single sell order...")
        await order_manager.create_single_order(
            base_token=eth_address,
            quote_token=usdc_address,
            is_buy=False,
            price=2100.0,  # $2100 per ETH
            amount=0.5,  # 0.5 ETH
            is_limit=True,
        )

        await asyncio.sleep(2)

        # 3. Update an order (if we have created orders)
        if order_manager.created_orders:
            print("\n3️⃣ Updating the first order...")
            first_order = order_manager.created_orders[0]
            await order_manager.update_order(
                base_token=first_order["base"],
                quote_token=first_order["quote"],
                order_id=first_order["order_id"],
                is_buy=first_order["is_buy"],
                new_price=1950.0,  # New price
                new_amount=1.2,  # New amount
            )

        await asyncio.sleep(2)

        # 4. Cancel an order (if we have created orders)
        if order_manager.created_orders:
            print("\n4️⃣ Cancelling the last order...")
            last_order = order_manager.created_orders[-1]
            await order_manager.cancel_order(
                base_token=last_order["base"],
                quote_token=last_order["quote"],
                is_buy=last_order["is_buy"],
                order_id=last_order["order_id"],
            )

    except Exception as e:
        print(f"❌ Error in basic example: {e}")

    print("\n✅ Basic order management example completed!")


async def batch_order_management_example():
    """Batch order management example."""
    print("\n🚀 Batch Order Management Example")
    print("=" * 50)

    # Initialize the Standard client
    client = StandardClient(
        private_key="your_private_key_here",
        http_rpc_url="https://your-rpc-url.com",
        networkName="Somnia Testnet",
        matching_engine_address="0x1234567890123456789012345678901234567890",
    )

    # Example token addresses
    eth_address = "0x0000000000000000000000000000000000000000"
    usdc_address = "0xA0b86a33E6441c8C06DD2b7c47d2a82f0e7B3C2D"
    btc_address = "0x1234567890123456789012345678901234567890"

    order_manager = OrderManager(client)

    try:
        # 1. Create multiple orders in a single transaction
        print("\n1️⃣ Creating batch orders...")

        batch_orders = [
            order_manager.create_order_data(
                base_token=eth_address,
                quote_token=usdc_address,
                is_buy=True,
                is_limit=True,
                price=1900.0,
                amount=0.5,
            ),
            order_manager.create_order_data(
                base_token=eth_address,
                quote_token=usdc_address,
                is_buy=True,
                is_limit=True,
                price=1850.0,
                amount=0.3,
            ),
            order_manager.create_order_data(
                base_token=btc_address,
                quote_token=usdc_address,
                is_buy=False,
                is_limit=True,
                price=45000.0,
                amount=0.1,
            ),
        ]

        await order_manager.create_batch_orders(batch_orders)

        await asyncio.sleep(3)

        # 2. Update multiple orders
        if len(order_manager.created_orders) >= 2:
            print("\n2️⃣ Updating multiple orders...")

            # Update first two orders
            update_orders = []
            for i in range(min(2, len(order_manager.created_orders))):
                order = order_manager.created_orders[i]
                update_data = order_manager.create_order_data(
                    base_token=order["base"],
                    quote_token=order["quote"],
                    is_buy=order["is_buy"],
                    is_limit=True,
                    price=order["price"] * 0.95,  # 5% lower price
                    amount=order["amount"] * 1.1,  # 10% more amount
                    order_id=order["order_id"],
                )
                update_orders.append(update_data)

            try:
                result = await client.update_orders(update_orders)
                print("✅ Batch updates completed!")
                print(f"    Transaction Hash: {result.get('tx_hash')}")
            except Exception as e:
                print(f"❌ Error updating orders: {e}")

        await asyncio.sleep(3)

        # 3. Cancel multiple orders
        if order_manager.created_orders:
            print("\n3️⃣ Cancelling multiple orders...")

            # Create cancel IDs for all created orders
            cancel_ids = []
            for order in order_manager.created_orders:
                cancel_id = order_manager.create_cancel_order_id(
                    base_token=order["base"],
                    quote_token=order["quote"],
                    is_buy=order["is_buy"],
                    order_id=order["order_id"],
                )
                cancel_ids.append(cancel_id)

            await order_manager.cancel_multiple_orders(cancel_ids)

    except Exception as e:
        print(f"❌ Error in batch example: {e}")

    print("\n✅ Batch order management example completed!")


async def advanced_order_strategies_example():
    """Advanced order management strategies."""
    print("\n🚀 Advanced Order Strategies Example")
    print("=" * 50)

    client = StandardClient(
        private_key="your_private_key_here",
        http_rpc_url="https://your-rpc-url.com",
        networkName="Somnia Testnet",
        matching_engine_address="0x1234567890123456789012345678901234567890",
    )

    eth_address = "0x0000000000000000000000000000000000000000"
    usdc_address = "0xA0b86a33E6441c8C06DD2b7c47d2a82f0e7B3C2D"

    order_manager = OrderManager(client)

    try:
        # 1. Grid Trading Strategy
        print("\n1️⃣ Grid Trading Strategy...")
        base_price = 2000.0
        grid_levels = 5
        grid_spacing = 50.0  # $50 between levels
        order_size = 0.1

        grid_orders = []
        for i in range(grid_levels):
            # Buy orders below current price
            buy_price = base_price - (i + 1) * grid_spacing
            buy_order = order_manager.create_order_data(
                base_token=eth_address,
                quote_token=usdc_address,
                is_buy=True,
                is_limit=True,
                price=buy_price,
                amount=order_size,
            )
            grid_orders.append(buy_order)

            # Sell orders above current price
            sell_price = base_price + (i + 1) * grid_spacing
            sell_order = order_manager.create_order_data(
                base_token=eth_address,
                quote_token=usdc_address,
                is_buy=False,
                is_limit=True,
                price=sell_price,
                amount=order_size,
            )
            grid_orders.append(sell_order)

        print(f"Creating grid with {len(grid_orders)} orders...")
        await order_manager.create_batch_orders(grid_orders)

        await asyncio.sleep(3)

        # 2. Dollar Cost Averaging (DCA) Strategy
        print("\n2️⃣ Dollar Cost Averaging Strategy...")
        dca_orders = []
        investment_amount = 1000.0  # $1000 total
        num_orders = 4
        amount_per_order = investment_amount / num_orders

        for i in range(num_orders):
            # Spread orders across different price levels
            price = base_price * (0.95 + i * 0.02)  # 95% to 101% of base price
            eth_amount = amount_per_order / price

            dca_order = order_manager.create_order_data(
                base_token=eth_address,
                quote_token=usdc_address,
                is_buy=True,
                is_limit=True,
                price=price,
                amount=eth_amount,
            )
            dca_orders.append(dca_order)

        print(f"Creating DCA orders with ${investment_amount} total...")
        await order_manager.create_batch_orders(dca_orders)

        await asyncio.sleep(5)

        # 3. Order Management - Cancel and Replace
        print("\n3️⃣ Order Management - Cancel and Replace...")
        if order_manager.created_orders:
            # Cancel all current orders
            cancel_ids = []
            for order in order_manager.created_orders:
                cancel_id = order_manager.create_cancel_order_id(
                    base_token=order["base"],
                    quote_token=order["quote"],
                    is_buy=order["is_buy"],
                    order_id=order["order_id"],
                )
                cancel_ids.append(cancel_id)

            print("Cancelling all existing orders...")
            await order_manager.cancel_multiple_orders(cancel_ids)

            await asyncio.sleep(2)

            # Create new orders with updated strategy
            print("Creating replacement orders with new strategy...")
            new_base_price = 2050.0  # Updated market price
            replacement_orders = []

            for i in range(3):
                # Create tighter spread orders
                buy_price = new_base_price * (0.98 - i * 0.01)
                sell_price = new_base_price * (1.02 + i * 0.01)

                buy_order = order_manager.create_order_data(
                    base_token=eth_address,
                    quote_token=usdc_address,
                    is_buy=True,
                    is_limit=True,
                    price=buy_price,
                    amount=0.2,
                )

                sell_order = order_manager.create_order_data(
                    base_token=eth_address,
                    quote_token=usdc_address,
                    is_buy=False,
                    is_limit=True,
                    price=sell_price,
                    amount=0.2,
                )

                replacement_orders.extend([buy_order, sell_order])

            await order_manager.create_batch_orders(replacement_orders)

    except Exception as e:
        print(f"❌ Error in advanced strategies: {e}")

    print("\n✅ Advanced order strategies example completed!")


async def error_handling_example():
    """Demonstrate error handling in order management."""
    print("\n🚀 Error Handling Example")
    print("=" * 50)

    client = StandardClient(
        private_key="your_private_key_here",
        http_rpc_url="https://your-rpc-url.com",
        networkName="Somnia Testnet",
        matching_engine_address="0x1234567890123456789012345678901234567890",
    )

    order_manager = OrderManager(client)

    # Example of various error scenarios
    print("\n1️⃣ Testing invalid order data...")
    try:
        # This should fail due to invalid address
        invalid_order = order_manager.create_order_data(
            base_token="invalid_address",
            quote_token="0xA0b86a33E6441c8C06DD2b7c47d2a82f0e7B3C2D",
            is_buy=True,
            is_limit=True,
            price=2000.0,
            amount=1.0,
        )
        await client.create_orders([invalid_order])
    except Exception as e:
        print(f"✅ Caught expected error: {e}")

    print("\n2️⃣ Testing empty order list...")
    try:
        await client.create_orders([])
    except Exception as e:
        print(f"✅ Caught expected error: {e}")

    print("\n3️⃣ Testing invalid cancel order ID...")
    try:
        await client.cancel_orders(["invalid_format"])
    except Exception as e:
        print(f"✅ Caught expected error: {e}")

    print("\n✅ Error handling example completed!")


async def main():
    """Run all order management examples."""
    print("🌟 Standard Protocol Order Management Examples")
    print("=" * 60)

    try:
        # Run basic example
        await basic_order_management_example()

        # Wait between examples
        await asyncio.sleep(3)

        # Run batch example
        await batch_order_management_example()

        # Wait between examples
        await asyncio.sleep(3)

        # Run advanced strategies
        await advanced_order_strategies_example()

        # Wait between examples
        await asyncio.sleep(3)

        # Run error handling
        await error_handling_example()

    except KeyboardInterrupt:
        print("\n⏹️ Examples interrupted by user")
    except Exception as e:
        print(f"❌ Error in main: {e}")

    print("\n✅ All order management examples completed!")


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())

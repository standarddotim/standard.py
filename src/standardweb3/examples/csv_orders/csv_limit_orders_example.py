#!/usr/bin/env python3
"""
CSV Limit Orders Example using StandardWeb3 with Pandas and NumPy.

This example demonstrates how to:
1. Read price ladder data from a CSV file using pandas
2. Process the data using numpy for calculations
3. Submit multiple limit orders based on CSV data
4. Handle batch order creation efficiently
"""

import asyncio
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from typing import List, Dict, Any

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


class CSVOrderManager:
    """Manages limit orders from CSV data using pandas and numpy."""

    def __init__(self, client: StandardClient):
        """Initialize the CSV order manager with client and token addresses."""
        self.client = client
        self.base_token = "0x4A3BC48C156384f9564Fd65A53a2f3D534D8f2b7"  # STT
        self.quote_token = "0x0ED782B8079529f7385c3eDA9fAf1EaA0DbC6a17"  # USDC

    def load_csv_data(self, csv_path: str) -> pd.DataFrame:
        """
        Load and validate CSV data using pandas.

        Args:
            csv_path: Path to the CSV file

        Returns:
            pd.DataFrame: Loaded and validated data
        """
        try:
            # Load CSV with pandas
            df = pd.read_csv(csv_path)

            print(f"📊 Loaded CSV with {len(df)} rows and {len(df.columns)} columns")
            print(f"Columns: {list(df.columns)}")

            # Validate required columns
            required_columns = ["Price", "Tokens"]
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")

            # Display basic statistics using numpy
            prices = df["Price"].values
            tokens = df["Tokens"].values

            print("\n📈 Price Statistics:")
            print(f"  Min Price: ${np.min(prices):.6f}")
            print(f"  Max Price: ${np.max(prices):.6f}")
            print(f"  Mean Price: ${np.mean(prices):.6f}")
            print(f"  Median Price: ${np.median(prices):.6f}")

            print("\n🪙 Token Statistics:")
            print(f"  Min Tokens: {np.min(tokens):,.2f}")
            print(f"  Max Tokens: {np.max(tokens):,.2f}")
            print(f"  Total Tokens: {np.sum(tokens):,.2f}")

            return df

        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            raise

    def filter_orders(
        self,
        df: pd.DataFrame,
        min_price: float = None,
        max_price: float = None,
        max_orders: int = None,
    ) -> pd.DataFrame:
        """
        Filter orders based on criteria using pandas.

        Args:
            df: DataFrame with order data
            min_price: Minimum price filter
            max_price: Maximum price filter
            max_orders: Maximum number of orders to include

        Returns:
            pd.DataFrame: Filtered data
        """
        filtered_df = df.copy()

        # Price filtering
        if min_price is not None:
            filtered_df = filtered_df[filtered_df["Price"] >= min_price]
            print(
                f"🔍 Filtered by min_price >= ${min_price}: {len(filtered_df)} orders"
            )

        if max_price is not None:
            filtered_df = filtered_df[filtered_df["Price"] <= max_price]
            print(
                f"🔍 Filtered by max_price <= ${max_price}: {len(filtered_df)} orders"
            )

        # Limit number of orders
        if max_orders is not None:
            filtered_df = filtered_df.head(max_orders)
            print(f"🔍 Limited to {max_orders} orders: {len(filtered_df)} orders")

        return filtered_df

    def prepare_buy_orders(
        self,
        df: pd.DataFrame,
        price_multiplier: float = 1.0,
        amount_multiplier: float = 1.0,
    ) -> List[Dict[str, Any]]:
        """
        Prepare buy order data from CSV using numpy calculations.

        Args:
            df: DataFrame with order data
            price_multiplier: Multiplier for prices (e.g., 0.95 for 5% below)
            amount_multiplier: Multiplier for amounts

        Returns:
            List[Dict]: List of order dictionaries
        """
        orders = []

        # Use numpy for vectorized calculations
        prices = df["Price"].values * price_multiplier
        amounts = df["Tokens"].values * amount_multiplier

        # Convert to proper units
        price_units = np.array([parse_units(price, 6) for price in prices])
        amount_units = np.array([parse_units(amount, 6) for amount in amounts])

        for i, (price, amount) in enumerate(zip(price_units, amount_units)):
            order = {
                "base": self.base_token,
                "quote": self.quote_token,
                "isBid": True,  # Buy orders
                "isLimit": True,
                "orderId": i + 1,  # Sequential order IDs
                "price": int(price),
                "amount": int(amount),
                "n": 1,
                "recipient": self.client.address,
                "isETH": False,
            }
            orders.append(order)

        print(f"🛒 Prepared {len(orders)} buy orders")
        return orders

    def prepare_sell_orders(
        self,
        df: pd.DataFrame,
        price_multiplier: float = 1.0,
        amount_multiplier: float = 1.0,
    ) -> List[Dict[str, Any]]:
        """
        Prepare sell order data from CSV using numpy calculations.

        Args:
            df: DataFrame with order data
            price_multiplier: Multiplier for prices (e.g., 1.05 for 5% above)
            amount_multiplier: Multiplier for amounts

        Returns:
            List[Dict]: List of order dictionaries
        """
        orders = []

        # Use numpy for vectorized calculations
        prices = df["Price"].values * price_multiplier
        amounts = df["Tokens"].values * amount_multiplier

        # Convert to proper units
        price_units = np.array(
            [parse_units(price, 6) for price in prices]
        )  # USDC decimals
        amount_units = np.array(
            [parse_units(amount, 18) for amount in amounts]
        )  # STT decimals (18)

        for i, (price, amount) in enumerate(zip(price_units, amount_units)):
            order = {
                "base": self.base_token,
                "quote": self.quote_token,
                "isBid": False,  # Sell orders
                "isLimit": True,
                "orderId": i + 1000,  # Offset to avoid conflicts with buy orders
                "price": int(price),
                "amount": int(amount),
                "n": 1,
                "recipient": self.client.address,
                "isETH": False,
            }
            orders.append(order)

        print(f"💰 Prepared {len(orders)} sell orders")
        return orders

    async def submit_orders_in_batches(
        self, orders: List[Dict[str, Any]], batch_size: int = 10
    ) -> List[Dict]:
        """
        Submit orders in batches to avoid gas limits.

        Args:
            orders: List of order dictionaries
            batch_size: Number of orders per batch

        Returns:
            List[Dict]: List of transaction results
        """
        results = []
        total_batches = len(orders) // batch_size + (
            1 if len(orders) % batch_size else 0
        )

        print(
            f"📦 Submitting {len(orders)} orders in {total_batches} "
            f"batches of {batch_size}"
        )

        for i in range(0, len(orders), batch_size):
            batch = orders[i : i + batch_size]
            batch_num = i // batch_size + 1

            print(
                f"\n🚀 Submitting batch {batch_num}/{total_batches} "
                f"({len(batch)} orders)"
            )

            try:
                result = await self.client.create_orders(batch)

                if result and result.get("status") == 1:
                    print(f"✅ Batch {batch_num} successful!")
                    print(f"  TX Hash: {result['tx_hash']}")
                    print(f"  Gas Used: {result['gas_used']:,}")

                    if result.get("decoded_logs"):
                        placed_orders = [
                            log
                            for log in result["decoded_logs"]
                            if log["event"] == "OrderPlaced"
                        ]
                        print(f"  📊 Orders Placed: {len(placed_orders)}")

                else:
                    print(f"❌ Batch {batch_num} failed!")
                    if result and result.get("error"):
                        print(f"  Error: {result['error']}")

                results.append(result)

                # Add delay between batches to avoid rate limiting
                if i + batch_size < len(orders):
                    print("⏳ Waiting 2 seconds before next batch...")
                    await asyncio.sleep(2)

            except Exception as e:
                print(f"❌ Batch {batch_num} error: {e}")
                results.append({"error": str(e), "batch": batch_num})

        return results


async def main():
    """Demonstrate CSV-based limit orders functionality."""
    # Load environment variables
    load_dotenv()

    # Configuration
    RPC_URL = os.getenv("RPC_URL", "https://rpc.testnet.mode.network")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
    NETWORK = os.getenv("NETWORK", "Somnia Testnet")
    CSV_FILE = "src/standardweb3/examples/csv_orders/momo_price_ladder_supply_900M.csv"

    if not PRIVATE_KEY:
        print("❌ Please set your PRIVATE_KEY environment variable")
        return

    print("🚀 CSV Limit Orders Example")
    print("=" * 60)

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
    print("-" * 60)

    # Initialize order manager
    order_manager = CSVOrderManager(client)

    try:
        # Load CSV data
        print("\n📂 Loading CSV Data")
        df = order_manager.load_csv_data(CSV_FILE)

        # Filter data for demonstration (first 5 orders, prices under $0.0001)
        print("\n🔍 Filtering Data")
        filtered_df = order_manager.filter_orders(
            df,
            max_price=0.0001,  # Only prices under $0.0001
            max_orders=5,  # Limit to 5 orders for demo
        )

        if len(filtered_df) == 0:
            print("❌ No orders match the filter criteria")
            return

        # Example 1: Create Buy Orders (bidding below market)
        print("\n🛒 Creating Buy Orders (5% below CSV prices)")
        buy_orders = order_manager.prepare_buy_orders(
            filtered_df,
            price_multiplier=0.95,  # 5% below CSV prices
            amount_multiplier=0.1,  # 10% of CSV amounts
        )

        # Submit buy orders
        buy_results = await order_manager.submit_orders_in_batches(
            buy_orders, batch_size=3
        )

        # Example 2: Create Sell Orders (asking above market)
        print("\n💰 Creating Sell Orders (10% above CSV prices)")
        sell_orders = order_manager.prepare_sell_orders(
            filtered_df,
            price_multiplier=1.10,  # 10% above CSV prices
            amount_multiplier=0.1,  # 10% of CSV amounts
        )

        # Submit sell orders
        sell_results = await order_manager.submit_orders_in_batches(
            sell_orders, batch_size=3
        )

        # Summary
        print("\n📊 Summary")
        print("-" * 40)
        successful_buys = sum(1 for r in buy_results if r and r.get("status") == 1)
        successful_sells = sum(1 for r in sell_results if r and r.get("status") == 1)

        print(f"Buy Orders Submitted: {len(buy_orders)}")
        print(f"Buy Batches Successful: {successful_buys}/{len(buy_results)}")
        print(f"Sell Orders Submitted: {len(sell_orders)}")
        print(f"Sell Batches Successful: {successful_sells}/{len(sell_results)}")

        total_gas = sum(
            r.get("gas_used", 0)
            for r in buy_results + sell_results
            if r and r.get("gas_used")
        )
        print(f"Total Gas Used: {total_gas:,}")

    except Exception as e:
        print(f"❌ Error in main execution: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

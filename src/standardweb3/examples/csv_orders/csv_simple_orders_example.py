#!/usr/bin/env python3
"""
Simple CSV Limit Orders Example using StandardWeb3 with Pandas and NumPy.

This example demonstrates a simpler approach to CSV-based order creation
with more realistic order sizes and better error handling.
"""

import asyncio
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Import the StandardClient
from standardweb3 import StandardClient


def parse_units(value: float, decimals: int) -> int:
    """Convert a float value to wei with specified decimal places."""
    return int(value * (10**decimals))


async def simple_csv_orders():
    """Create orders from CSV data with simple processing."""
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

    print("🚀 Simple CSV Limit Orders Example")
    print("=" * 50)

    # Initialize StandardClient
    client = StandardClient(
        private_key=PRIVATE_KEY,
        http_rpc_url=RPC_URL,
        networkName=NETWORK,
        api_url="https://api-somi.standardweb3.com",
        matching_engine_address="0x3Cb2CBb0CeB96c9456b11DbC7ab73c4848F9a14c",
        websocket_url=None,
    )

    print(f"Account: {client.contract.address}")
    print(f"Network: {NETWORK}")
    print("-" * 50)

    try:
        # Load CSV with pandas
        print("📂 Loading CSV data...")
        df = pd.read_csv(CSV_FILE)
        print(f"Loaded {len(df)} price points")

        # Filter to first 3 rows with small prices for demo
        filtered_df = df[df["Price"] <= 0.00005].head(3)
        print(f"Using {len(filtered_df)} price points for demo")

        # Display the data we'll use
        print("\n📊 Price Data:")
        for idx, row in filtered_df.iterrows():
            print(f"  Step {int(row['Step'])}: ${row['Price']:.6f} per token")

        # Token addresses
        base_token = "0x492620a940ad6A7bC4c597f2681C22c6acF34c62"  # MOMO
        quote_token = "0x0ED782B8079529f7385c3eDA9fAf1EaA0DbC6a17"  # SOMI

        # Create small buy orders using numpy for calculations
        print("\n🛒 Creating Buy Orders...")

        # Use numpy for vectorized operations
        prices = filtered_df["Price"].values * 0.95  # 5% below CSV price
        amounts = np.full(len(prices), 10.0)  # $10 USDC orders

        orders = []
        for i, (price, amount) in enumerate(zip(prices, amounts)):
            order = {
                "base": base_token,
                "quote": quote_token,
                "isBid": True,  # Buy orders
                "isLimit": True,
                "orderId": i + 1,
                "price": price,  # USDC has 6 decimals
                "amount": amount,  # $10 USDC
                "n": 1,
                "recipient": client.address,
                "isETH": False,
            }
            orders.append(order)
            print(f"  Order {i + 1}: Buy at ${price:.6f} with ${amount} USDC")

        # Submit orders
        print(f"\n🚀 Submitting {len(orders)} orders...")
        result = await client.create_orders(orders)

        if result and result.get("status") == 1:
            print("✅ Orders submitted successfully!")
            print(f"  TX Hash: {result['tx_hash']}")
            print(f"  Gas Used: {result['gas_used']:,}")

            # Count placed orders
            if result.get("decoded_logs"):
                placed_orders = [
                    log
                    for log in result["decoded_logs"]
                    if log["event"] == "OrderPlaced"
                ]
                print(f"  📊 Orders Placed: {len(placed_orders)}")

                for i, log in enumerate(placed_orders):
                    args = log["args"]
                    price_readable = args["price"] / 1e6  # Convert back from 6 decimals
                    amount_readable = (
                        args["placed"] / 1e6
                    )  # Convert back from 6 decimals
                    print(
                        f"    Order {i + 1}: ID {args['id']}, "
                        f"Price ${price_readable:.6f}, Amount ${amount_readable:.2f}"
                    )
        else:
            print("❌ Orders submission failed!")
            if result and result.get("error"):
                print(f"  Error: {result['error']}")

        # Pandas data analysis
        print("\n📈 Data Analysis with Pandas:")
        print(
            f"Price range: ${filtered_df['Price'].min():.6f} - "
            f"${filtered_df['Price'].max():.6f}"
        )
        print(f"Average price: ${filtered_df['Price'].mean():.6f}")

        # NumPy calculations
        price_array = filtered_df["Price"].values
        print("\n🔢 NumPy Statistics:")
        print(f"Standard deviation: ${np.std(price_array):.8f}")
        print(f"Price increase per step: ${np.diff(price_array).mean():.8f}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(simple_csv_orders())

#!/usr/bin/env python3
"""
Simple Trading Example using StandardWeb3 Contract Functions.

This is a minimal example showing how to use the contract functions
for basic trading operations.
"""

import asyncio
import os
from web3 import Web3
from eth_account import Account

# Import the contract functions
from standardweb3.contract import ContractFunctions
from standardweb3.abis.matching_engine import matching_engine_abi
from standardweb3.consts.contracts import matching_engine_addresses


async def simple_trading_example():
    """Demonstrate simple contract function usage for trading."""
    # Configuration
    RPC_URL = "https://rpc.testnet.mode.network"  # Replace with your RPC URL
    PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")  # Your private key
    NETWORK = "Story Odyssey Testnet"

    if not PRIVATE_KEY:
        print("❌ Please set your PRIVATE_KEY environment variable")
        return

    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    account = Account.from_key(PRIVATE_KEY)
    address = account.address

    # Get matching engine address
    matching_engine_address = matching_engine_addresses[NETWORK]

    print(f"Account: {address}")
    print(f"Network: {NETWORK}")
    print(f"Matching Engine: {matching_engine_address}")
    print("-" * 40)

    # Initialize contract functions
    contract_functions = ContractFunctions(
        w3=w3,
        private_key=PRIVATE_KEY,
        address=address,
        matching_engine=matching_engine_address,
        matching_engine_abi=matching_engine_abi,
    )

    # Example token addresses (replace with actual token addresses)
    base_token = "0x0000000000000000000000000000000000000001"  # Token to buy/sell
    quote_token = "0x0000000000000000000000000000000000000002"  # Token to spend/receive

    # Example 1: Market Buy
    print("📈 Market Buy Example")
    try:
        quote_amount = w3.to_wei(0.001, "ether")  # 0.001 ETH
        tx_receipt = await contract_functions.market_buy(
            base=base_token,
            quote=quote_token,
            quote_amount=quote_amount,
            is_maker=False,
            n=1,
            uid=0,
            recipient=address,
        )
        print(f"✅ Market buy successful! TX: {tx_receipt['transactionHash'].hex()}")
    except Exception as e:
        print(f"❌ Market buy failed: {e}")

    print()

    # Example 2: Limit Buy
    print("💰 Limit Buy Example")
    try:
        price = w3.to_wei(0.1, "ether")  # 0.1 ETH per token
        quote_amount = w3.to_wei(0.01, "ether")  # 0.01 ETH
        tx_receipt = await contract_functions.limit_buy(
            base=base_token,
            quote=quote_token,
            price=price,
            quote_amount=quote_amount,
            is_maker=True,
            n=1,
            uid=0,
            recipient=address,
        )
        print(f"✅ Limit buy successful! TX: {tx_receipt['transactionHash'].hex()}")
    except Exception as e:
        print(f"❌ Limit buy failed: {e}")

    print()

    # Example 3: Market Sell
    print("📉 Market Sell Example")
    try:
        base_amount = w3.to_wei(0.001, "ether")  # 0.001 tokens
        tx_receipt = await contract_functions.market_sell(
            base=base_token,
            quote=quote_token,
            base_amount=base_amount,
            is_maker=False,
            n=1,
            uid=0,
            recipient=address,
        )
        print(f"✅ Market sell successful! TX: {tx_receipt['transactionHash'].hex()}")
    except Exception as e:
        print(f"❌ Market sell failed: {e}")

    print()

    # Example 4: Limit Sell
    print("💸 Limit Sell Example")
    try:
        price = w3.to_wei(0.15, "ether")  # 0.15 ETH per token
        base_amount = w3.to_wei(0.01, "ether")  # 0.01 tokens
        tx_receipt = await contract_functions.limit_sell(
            base=base_token,
            quote=quote_token,
            price=price,
            base_amount=base_amount,
            is_maker=True,
            n=1,
            uid=0,
            recipient=address,
        )
        print(f"✅ Limit sell successful! TX: {tx_receipt['transactionHash'].hex()}")
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

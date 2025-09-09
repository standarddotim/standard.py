"""Example usage of spot order histories stream types.

This example demonstrates how to use the Python equivalent of the TypeScript
spot order histories stream types for Standard Protocol.
"""

from standardweb3.types import (
    SpotOrderHistoryEvent,
    SpotOrderHistoryStream,
    event_to_spot_order_history_stream,
    stream_to_spot_order_history_event,
    validate_spot_order_history_stream,
)


def main():
    """Demonstrate spot order history stream type usage."""
    # Create a comprehensive SpotOrderHistoryEvent object
    order_history = SpotOrderHistoryEvent(
        event_id="spotOrderHistory",
        order_history_id=12345,
        block_number=18500000,
        order_id=67890,
        is_bid=True,
        base="0x1234567890123456789012345678901234567890",
        base_symbol="ETH",
        base_logo_uri=(
            "https://assets.coingecko.com/coins/images/279/large/ethereum.png"
        ),
        quote="0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
        quote_symbol="USDC",
        quote_logo_uri=(
            "https://assets.coingecko.com/coins/images/6319/large/USD_Coin_icon.png"
        ),
        pair="0x9876543210987654321098765432109876543210",
        pair_symbol="ETH/USDC",
        price=2500.75,
        asset="0x1234567890123456789012345678901234567890",
        asset_symbol="ETH",
        asset_decimals=18,
        executed=1.5,
        amount=2.0,
        timestamp=1640995200.0,
        account="0xuser123456789012345678901234567890123456",
        tx_hash="0xabcd1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd",
        status="filled",
        eid="eth_usdc_order_12345",
    )

    print("Original SpotOrderHistoryEvent:")
    print(f"  Event ID: {order_history.event_id}")
    print(f"  Order History ID: {order_history.order_history_id}")
    print(f"  Block Number: {order_history.block_number}")
    print(f"  Order ID: {order_history.order_id}")
    print(f"  Is Bid: {order_history.is_bid}")
    print(f"  Base: {order_history.base}")
    print(f"  Base Symbol: {order_history.base_symbol}")
    print(f"  Quote Symbol: {order_history.quote_symbol}")
    print(f"  Pair Symbol: {order_history.pair_symbol}")
    print(f"  Price: ${order_history.price}")
    print(f"  Asset Symbol: {order_history.asset_symbol}")
    print(f"  Asset Decimals: {order_history.asset_decimals}")
    print(f"  Executed: {order_history.executed}")
    print(f"  Amount: {order_history.amount}")
    print(f"  Status: {order_history.status}")
    print(f"  Account: {order_history.account}")
    print(f"  TX Hash: {order_history.tx_hash}")

    # Convert to stream format (tuple)
    stream_data = event_to_spot_order_history_stream(order_history)
    print(f"\nStream format (tuple with {len(stream_data)} elements):")
    print(f"  First 5 elements: {stream_data[:5]}")
    print(f"  Last 5 elements: {stream_data[-5:]}")

    # Convert back to event format
    reconstructed_event = stream_to_spot_order_history_event(stream_data)
    print("\nReconstructed SpotOrderHistoryEvent:")
    print(f"  Event ID: {reconstructed_event.event_id}")
    print(f"  Order History ID: {reconstructed_event.order_history_id}")
    print(f"  Status: {reconstructed_event.status}")
    print(f"  Price: ${reconstructed_event.price}")

    # Example with partial data (many None values)
    partial_stream: SpotOrderHistoryStream = (
        "spotOrderHistory",  # eventId (required)
        54321,  # orderHistoryId
        None,  # blockNumber
        98765,  # orderId
        False,  # isBid (ask order)
        "0xbtc123...",  # base
        "BTC",  # baseSymbol
        None,  # baseLogoURI
        "0xusdt456...",  # quote
        "USDT",  # quoteSymbol
        None,  # quoteLogoURI
        "0xpair789...",  # pair
        "BTC/USDT",  # pairSymbol
        45000.0,  # price
        "0xbtc123...",  # asset
        "BTC",  # assetSymbol
        8,  # assetDecimals
        0.5,  # executed
        1.0,  # amount
        None,  # timestamp
        "0xuser789...",  # account
        None,  # txHash
        "open",  # status
        "btc_usdt_order_54321",  # eid
    )

    print("\nPartial stream data (24 elements):")
    print(f"  Event ID: {partial_stream[0]}")
    print(f"  Order History ID: {partial_stream[1]}")
    print(f"  Is Bid: {partial_stream[4]} (False = Ask)")
    print(f"  Base Symbol: {partial_stream[6]}")
    print(f"  Quote Symbol: {partial_stream[9]}")
    print(f"  Price: ${partial_stream[13]}")
    print(f"  Status: {partial_stream[22]}")

    # Validate the stream data
    try:
        validated_stream = validate_spot_order_history_stream(partial_stream)
        print(f"\nValidated stream (first 5 elements): {validated_stream[:5]}")

        # Convert to event with None values handled
        partial_event = stream_to_spot_order_history_event(validated_stream)
        print("Partial event:")
        print(f"  Event ID: {partial_event.event_id}")
        print(f"  Order History ID: {partial_event.order_history_id}")
        print(f"  Block Number: {partial_event.block_number} (None)")
        print(f"  Is Bid: {partial_event.is_bid}")
        print(f"  Base Symbol: {partial_event.base_symbol}")
        print(f"  Quote Symbol: {partial_event.quote_symbol}")
        print(f"  Price: ${partial_event.price}")
        print(f"  Asset Decimals: {partial_event.asset_decimals}")
        print(f"  Status: {partial_event.status}")

    except ValueError as e:
        print(f"Validation error: {e}")

    # Example with type conversion
    try:
        # Test various type conversions
        mixed_data = [
            "spotOrderHistory",  # eventId
            "12345",  # orderHistoryId (string -> int)
            18500000,  # blockNumber (int)
            "67890",  # orderId (string -> int)
            "true",  # isBid (string -> bool)
            "0x123...",  # base
            "ETH",  # baseSymbol
            None,  # baseLogoURI
            "0xabc...",  # quote
            "USDC",  # quoteSymbol
            None,  # quoteLogoURI
            "0x987...",  # pair
            "ETH/USDC",  # pairSymbol
            "2500.75",  # price (string -> float)
            "0x123...",  # asset
            "ETH",  # assetSymbol
            "18",  # assetDecimals (string -> int)
            "1.5",  # executed (string -> float)
            "2.0",  # amount (string -> float)
            "1640995200.0",  # timestamp (string -> float)
            "0xuser...",  # account
            "0xabcd...",  # txHash
            "filled",  # status
            "eth_usdc_12345",  # eid
        ]

        validated_mixed = validate_spot_order_history_stream(mixed_data)
        mixed_event = stream_to_spot_order_history_event(validated_mixed)
        print("\nType conversion test:")
        print(
            f"  Order History ID: {mixed_event.order_history_id} "
            f"(converted from string)"
        )
        print(f"  Is Bid: {mixed_event.is_bid} (converted from 'true')")
        print(f"  Price: {mixed_event.price} (converted from string)")
        print(f"  Asset Decimals: {mixed_event.asset_decimals} (converted from string)")

    except ValueError as e:
        print(f"Type conversion error: {e}")

    # Example of invalid data
    try:
        invalid_data = ["invalid", "data", "format"]  # Wrong length
        validate_spot_order_history_stream(invalid_data)
    except ValueError as e:
        print(f"\nExpected validation error (wrong length): {e}")

    try:
        invalid_eventid = [None] + [None] * 23  # eventId cannot be None
        validate_spot_order_history_stream(invalid_eventid)
    except ValueError as e:
        print(f"Expected validation error (None eventId): {e}")


if __name__ == "__main__":
    main()

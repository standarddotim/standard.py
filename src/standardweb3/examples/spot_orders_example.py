"""Example usage of spot orders stream types.

This example demonstrates how to use the Python equivalent of the TypeScript
spot orders stream types for Standard Protocol. Includes three event types:
- SpotOrderMatchedEvent (27 fields)
- SpotOrderEvent (23 fields)
- SpotDeleteOrderItemEvent (9 fields)
"""

from standardweb3.types import (
    SpotOrderMatchedEvent,
    event_to_spot_order_matched_stream,
    stream_to_spot_order_matched_event,
    validate_spot_order_matched_stream,
    SpotOrderEvent,
    event_to_spot_order_stream,
    stream_to_spot_order_event,
    validate_spot_order_stream,
    SpotDeleteOrderItemEvent,
    event_to_spot_delete_order_item_stream,
    stream_to_spot_delete_order_item_event,
    validate_spot_delete_order_item_stream,
)


def demonstrate_spot_order_matched():
    """Demonstrate SpotOrderMatchedEvent (27 fields)."""
    print("=== SpotOrderMatchedEvent Demo ===")

    # Create a comprehensive order matched event
    matched_order = SpotOrderMatchedEvent(
        event_id="spotOrderMatched",
        id="match_12345",
        is_bid=True,
        order_history_id=67890,
        block_number=18500000,
        order_id=11111,
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
        pair_symbol="ETH/USDC",
        pair="0x9876543210987654321098765432109876543210",
        price=2500.75,
        price_bn="250075000000",  # Price as BigNumber string
        asset="0x1234567890123456789012345678901234567890",
        asset_symbol="ETH",
        asset_decimals=18,
        amount=2.0,
        placed=2.0,
        matched=1.5,
        total=3750.0,  # 1.5 ETH * 2500 USDC
        timestamp=1640995200.0,
        account="0xuser123456789012345678901234567890123456",
        tx_hash="0xabcd1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd",
        eid="eth_usdc_match_12345",
    )

    print(f"  Event ID: {matched_order.event_id}")
    print(f"  Match ID: {matched_order.id}")
    print(f"  Is Bid: {matched_order.is_bid}")
    print(f"  Order ID: {matched_order.order_id}")
    print(f"  Pair Symbol: {matched_order.pair_symbol}")
    print(f"  Price: ${matched_order.price}")
    print(f"  Price BN: {matched_order.price_bn}")
    print(f"  Amount: {matched_order.amount}")
    print(f"  Placed: {matched_order.placed}")
    print(f"  Matched: {matched_order.matched}")
    print(f"  Total: ${matched_order.total}")

    # Convert to stream and back
    stream_data = event_to_spot_order_matched_stream(matched_order)
    print(f"  Stream length: {len(stream_data)} elements")

    reconstructed = stream_to_spot_order_matched_event(stream_data)
    print(f"  Reconstructed match ID: {reconstructed.id}")
    print(f"  Reconstructed matched amount: {reconstructed.matched}")


def demonstrate_spot_order():
    """Demonstrate SpotOrderEvent (23 fields)."""
    print("\n=== SpotOrderEvent Demo ===")

    # Create a spot order event
    order = SpotOrderEvent(
        event_id="spotOrder",
        is_bid=False,  # Ask order
        order_history_id=54321,
        block_number=18500100,
        order_id=22222,
        base="0xbtc123456789012345678901234567890123456",
        base_symbol="BTC",
        base_logo_uri="https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
        quote="0xusdt456789012345678901234567890123456789",
        quote_symbol="USDT",
        quote_logo_uri="https://assets.coingecko.com/coins/images/325/large/Tether.png",
        pair_symbol="BTC/USDT",
        pair="0xpair456789012345678901234567890123456789",
        price=45000.0,
        asset="0xbtc123456789012345678901234567890123456",
        asset_symbol="BTC",
        asset_decimals=8,
        amount=1.0,
        placed=1.0,
        timestamp=1640995300.0,
        account="0xtrader789012345678901234567890123456789",
        tx_hash="0xdef456789012345678901234567890123456789012345678901234567890def4",
        eid="btc_usdt_order_22222",
    )

    print(f"  Event ID: {order.event_id}")
    print(f"  Is Bid: {order.is_bid} (False = Ask)")
    print(f"  Order ID: {order.order_id}")
    print(f"  Base Symbol: {order.base_symbol}")
    print(f"  Quote Symbol: {order.quote_symbol}")
    print(f"  Price: ${order.price}")
    print(f"  Amount: {order.amount}")
    print(f"  Asset Decimals: {order.asset_decimals}")

    # Test validation
    stream_data = event_to_spot_order_stream(order)
    print(f"  Stream length: {len(stream_data)} elements")

    try:
        validated = validate_spot_order_stream(stream_data)
        reconstructed = stream_to_spot_order_event(validated)
        print(
            f"  Validation successful: {reconstructed.base_symbol}/"
            f"{reconstructed.quote_symbol}"
        )
    except ValueError as e:
        print(f"  Validation error: {e}")


def demonstrate_spot_delete_order():
    """Demonstrate SpotDeleteOrderItemEvent (9 fields)."""
    print("\n=== SpotDeleteOrderItemEvent Demo ===")

    # Create delete order events for both types
    delete_order = SpotDeleteOrderItemEvent(
        event_id="deleteSpotOrder",
        is_bid=True,
        pair="0xpair123456789012345678901234567890123456",
        account="0xuser456789012345678901234567890123456789",
        order_id=33333,
        tx_hash="0x123abc456def789012345678901234567890123456789012345678901234567890",
        timestamp=1640995400.0,
        status="canceled",
        eid="delete_order_33333",
    )

    delete_history = SpotDeleteOrderItemEvent(
        event_id="deleteSpotOrderHistory",
        is_bid=False,
        pair="0xpair789012345678901234567890123456789012",
        account="0xuser123456789012345678901234567890123456",
        order_id=44444,
        tx_hash=None,  # Can be None
        timestamp=1640995500.0,
        status="filled",
        eid="delete_history_44444",
    )

    print(f"  Delete Order - Event ID: {delete_order.event_id}")
    print(f"  Delete Order - Is Bid: {delete_order.is_bid}")
    print(f"  Delete Order - Order ID: {delete_order.order_id}")
    print(f"  Delete Order - Status: {delete_order.status}")

    print(f"  Delete History - Event ID: {delete_history.event_id}")
    print(f"  Delete History - Is Bid: {delete_history.is_bid}")
    print(f"  Delete History - Order ID: {delete_history.order_id}")
    print(f"  Delete History - Status: {delete_history.status}")
    print(f"  Delete History - TX Hash: {delete_history.tx_hash}")

    # Test both delete events
    for i, delete_event in enumerate([delete_order, delete_history], 1):
        stream_data = event_to_spot_delete_order_item_stream(delete_event)
        print(f"  Delete Event {i} - Stream length: {len(stream_data)} elements")

        try:
            validated = validate_spot_delete_order_item_stream(stream_data)
            reconstructed = stream_to_spot_delete_order_item_event(validated)
            print(
                f"  Delete Event {i} - Reconstructed: {reconstructed.event_id}, "
                f"Order {reconstructed.order_id}"
            )
        except ValueError as e:
            print(f"  Delete Event {i} - Validation error: {e}")


def demonstrate_type_conversions():
    """Demonstrate type conversion capabilities."""
    print("\n=== Type Conversion Demo ===")

    # Test SpotOrderMatchedEvent validation with mixed types
    mixed_matched_data = [
        "spotOrderMatched",  # eventId
        "match_999",  # id
        "true",  # isBid (string -> bool)
        "12345",  # orderHistoryId (string -> int)
        18500000,  # blockNumber (int)
        "67890",  # orderId (string -> int)
        "0x123...",  # base
        "ETH",  # baseSymbol
        None,  # baseLogoURI
        "0xabc...",  # quote
        "USDC",  # quoteSymbol
        None,  # quoteLogoURI
        "ETH/USDC",  # pairSymbol
        "0x987...",  # pair
        "2500.75",  # price (string -> float)
        "250075000000",  # priceBN
        "0x123...",  # asset
        "ETH",  # assetSymbol
        "18",  # assetDecimals (string -> int)
        "2.0",  # amount (string -> float)
        "2.0",  # placed (string -> float)
        "1.5",  # matched (string -> float)
        "3750.0",  # total (string -> float)
        "1640995200.0",  # timestamp (string -> float)
        "0xuser...",  # account
        "0xabcd...",  # txHash
        "match_999_eid",  # eid
    ]

    try:
        validated_matched = validate_spot_order_matched_stream(mixed_matched_data)
        converted_matched = stream_to_spot_order_matched_event(validated_matched)
        print(
            f"  Matched conversion - Is Bid: {converted_matched.is_bid} "
            f"(from 'true')"
        )
        print(
            f"  Matched conversion - Order ID: {converted_matched.order_id} "
            f"(from string)"
        )
        print(f"  Matched conversion - Price: {converted_matched.price} (from string)")
        print(
            f"  Matched conversion - Asset Decimals: "
            f"{converted_matched.asset_decimals} (from string)"
        )
    except ValueError as e:
        print(f"  Matched conversion error: {e}")

    # Test error cases
    print("\n  Testing error cases:")

    try:
        # Wrong length for SpotOrderEvent
        invalid_order = ["spotOrder", True, 123]  # Only 3 elements instead of 23
        validate_spot_order_stream(invalid_order)
    except ValueError as e:
        print(f"    Expected error (wrong length): {e}")

    try:
        # Invalid type conversion
        invalid_matched = (
            ["spotOrderMatched"] + [None] * 25 + ["invalid_number"]
        )  # 27 elements
        invalid_matched[14] = "not_a_number"  # price field
        validate_spot_order_matched_stream(invalid_matched)
    except ValueError as e:
        print(f"    Expected error (invalid number): {e}")


def main():
    """Run all demonstrations."""
    print("Spot Orders Stream Types Demo")
    print("=" * 50)

    demonstrate_spot_order_matched()
    demonstrate_spot_order()
    demonstrate_spot_delete_order()
    demonstrate_type_conversions()

    print(f"\n{'='*50}")
    print("Demo completed successfully!")


if __name__ == "__main__":
    main()

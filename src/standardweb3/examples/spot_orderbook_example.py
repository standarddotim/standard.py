"""Example usage of spot orderbook stream types.

This example demonstrates how to use the Python equivalent of the TypeScript
spot orderbook stream types for Standard Protocol.
"""

from standardweb3.types import (
    SpotOrderBlockEvent,
    SpotOrderBlockStream,
    event_to_spot_order_block_stream,
    stream_to_spot_order_block_event,
    validate_spot_order_block_stream,
)


def main():
    """Demonstrate spot orderbook stream type usage."""
    # Create a SpotOrderBlockEvent object (bid order)
    bid_order_block = SpotOrderBlockEvent(
        event_id="spotOrderBlock",
        is_bid=True,
        price=2500.75,
        base_liquidity=50.25,
        quote_liquidity=125643.75,
        scale="0.01",
        timestamp=1640995200.0,
        eid="eth_usdc_bid_block",
    )

    print("Original SpotOrderBlockEvent (Bid):")
    print(f"  Event ID: {bid_order_block.event_id}")
    print(f"  Is Bid: {bid_order_block.is_bid}")
    print(f"  Price: ${bid_order_block.price}")
    print(f"  Base Liquidity: {bid_order_block.base_liquidity}")
    print(f"  Quote Liquidity: ${bid_order_block.quote_liquidity}")
    print(f"  Scale: {bid_order_block.scale}")
    print(f"  Timestamp: {bid_order_block.timestamp}")
    print(f"  EID: {bid_order_block.eid}")

    # Convert to stream format (tuple)
    stream_data = event_to_spot_order_block_stream(bid_order_block)
    print(f"\nStream format (tuple): {stream_data}")

    # Convert back to event format
    reconstructed_event = stream_to_spot_order_block_event(stream_data)
    print("\nReconstructed SpotOrderBlockEvent:")
    print(f"  Event ID: {reconstructed_event.event_id}")
    print(f"  Is Bid: {reconstructed_event.is_bid}")
    print(f"  Price: ${reconstructed_event.price}")
    print(f"  Base Liquidity: {reconstructed_event.base_liquidity}")

    # Create an ask order block with partial data
    ask_stream: SpotOrderBlockStream = (
        "spotOrderBlock",
        False,  # is_bid = False (ask)
        2501.25,  # price
        None,  # base_liquidity
        75000.0,  # quote_liquidity
        "0.01",  # scale
        None,  # timestamp
        "eth_usdc_ask_block",  # eid
    )

    print(f"\nAsk order stream data: {ask_stream}")

    # Validate the stream data
    try:
        validated_stream = validate_spot_order_block_stream(ask_stream)
        print(f"Validated stream: {validated_stream}")

        # Convert to event
        ask_event = stream_to_spot_order_block_event(validated_stream)
        print("Ask order block event:")
        print(f"  Event ID: {ask_event.event_id}")
        print(f"  Is Bid: {ask_event.is_bid} (False = Ask)")
        print(f"  Price: ${ask_event.price}")
        print(f"  Base Liquidity: {ask_event.base_liquidity} (None)")
        print(f"  Quote Liquidity: ${ask_event.quote_liquidity}")
        print(f"  Scale: {ask_event.scale}")
        print(f"  Timestamp: {ask_event.timestamp} (None)")
        print(f"  EID: {ask_event.eid}")

    except ValueError as e:
        print(f"Validation error: {e}")

    # Example with boolean conversion
    try:
        # Test boolean conversion from string/number
        test_data = [
            "spotOrderBlock",
            "1",  # String "1" should convert to True
            2500.0,
            100.0,
            250000.0,
            "0.1",
            1640995300.0,
            "test_eid",
        ]

        validated_test = validate_spot_order_block_stream(test_data)
        test_event = stream_to_spot_order_block_event(validated_test)
        print("\nBoolean conversion test:")
        print(f"  Original is_bid value: '{test_data[1]}'")
        print(f"  Converted is_bid: {test_event.is_bid}")

    except ValueError as e:
        print(f"Boolean conversion error: {e}")

    # Example of invalid data
    try:
        invalid_data = ["invalid", "data"]  # Wrong length
        validate_spot_order_block_stream(invalid_data)
    except ValueError as e:
        print(f"\nExpected validation error: {e}")


if __name__ == "__main__":
    main()

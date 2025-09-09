"""Example usage of spot bars stream types.

This example demonstrates how to use the Python equivalent of the TypeScript
spot bars stream types for Standard Protocol.
"""

from standardweb3.types import (
    SpotBarEvent,
    SpotBarStream,
    event_to_spot_bar_stream,
    stream_to_spot_bar_event,
    validate_spot_bar_stream,
)


def main():
    """Demonstrate spot bar stream type usage."""
    # Create a SpotBarEvent object
    spot_bar = SpotBarEvent(
        event_id="spotBar",
        id="ETH/USDC:1m",
        price=2500.50,
        timestamp=1640995200.0,
        base_volume=100.5,
        quote_volume=251275.0,
        volume_usd=251275.0,
        eid="eth_usdc_1m",
    )

    print("Original SpotBarEvent:")
    print(f"  Event ID: {spot_bar.event_id}")
    print(f"  ID: {spot_bar.id}")
    print(f"  Price: ${spot_bar.price}")
    print(f"  Timestamp: {spot_bar.timestamp}")
    print(f"  Base Volume: {spot_bar.base_volume}")
    print(f"  Quote Volume: ${spot_bar.quote_volume}")
    print(f"  Volume USD: ${spot_bar.volume_usd}")
    print(f"  EID: {spot_bar.eid}")

    # Convert to stream format (tuple)
    stream_data = event_to_spot_bar_stream(spot_bar)
    print(f"\nStream format (tuple): {stream_data}")

    # Convert back to event format
    reconstructed_event = stream_to_spot_bar_event(stream_data)
    print("\nReconstructed SpotBarEvent:")
    print(f"  Event ID: {reconstructed_event.event_id}")
    print(f"  ID: {reconstructed_event.id}")
    print(f"  Price: ${reconstructed_event.price}")

    # Example with partial data (None values)
    partial_stream: SpotBarStream = (
        "spotBar",
        "BTC/USDT:5m",
        45000.0,
        None,  # timestamp
        None,  # base_volume
        None,  # quote_volume
        None,  # volume_usd
        "btc_usdt_5m",
    )

    print(f"\nPartial stream data: {partial_stream}")

    # Validate the stream data
    try:
        validated_stream = validate_spot_bar_stream(partial_stream)
        print(f"Validated stream: {validated_stream}")

        # Convert to event with defaults
        partial_event = stream_to_spot_bar_event(validated_stream)
        print("Partial event with defaults:")
        print(f"  Event ID: {partial_event.event_id}")
        print(f"  ID: {partial_event.id}")
        print(f"  Price: ${partial_event.price}")
        print(f"  Timestamp: {partial_event.timestamp} (default)")
        print(f"  Base Volume: {partial_event.base_volume} (default)")
        print(f"  Quote Volume: {partial_event.quote_volume} (default)")

    except ValueError as e:
        print(f"Validation error: {e}")

    # Example of invalid data
    try:
        invalid_data = ["invalid", "data", "format"]  # Wrong length
        validate_spot_bar_stream(invalid_data)
    except ValueError as e:
        print(f"\nExpected validation error: {e}")


if __name__ == "__main__":
    main()

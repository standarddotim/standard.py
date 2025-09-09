"""Example usage of spot trades stream types.

This example demonstrates how to use the Python equivalent of the TypeScript
spot trades stream types for Standard Protocol.
"""

from standardweb3.types import (
    SpotTradeEvent,
    SpotTradeStream,
    event_to_spot_trade_stream,
    stream_to_spot_trade_event,
    validate_spot_trade_stream,
)


def main():
    """Demonstrate spot trade stream type usage."""
    # Create a comprehensive SpotTradeEvent object
    trade_event = SpotTradeEvent(
        event_id="spotTrade",
        trade_id="trade_abc123",
        order_id=12345,
        base="0x1234567890123456789012345678901234567890",
        quote="0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
        base_symbol="ETH",
        quote_symbol="USDC",
        base_logo_uri=(
            "https://assets.coingecko.com/coins/images/279/large/ethereum.png"
        ),
        quote_logo_uri=(
            "https://assets.coingecko.com/coins/images/6319/large/USD_Coin_icon.png"
        ),
        pair="0x9876543210987654321098765432109876543210",
        pair_symbol="ETH/USDC",
        is_bid=True,
        price=2500.75,
        account="0xtrader123456789012345678901234567890123456",
        asset="0x1234567890123456789012345678901234567890",
        asset_symbol="ETH",
        amount=2.0,
        value_usd=5001.50,  # 2.0 ETH * 2500.75 USDC
        base_amount=2.0,
        quote_amount=5001.50,
        base_fee=0.002,  # 0.1% fee on base
        quote_fee=5.0015,  # 0.1% fee on quote
        timestamp=1640995200.0,
        taker="0xtaker456789012345678901234567890123456789",
        taker_order_history_id=67890,
        maker="0xmaker789012345678901234567890123456789012",
        maker_order_history_id=54321,
        tx_hash="0xabcd1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd",
        eid="eth_usdc_trade_abc123",
    )

    print("Original SpotTradeEvent:")
    print(f"  Event ID: {trade_event.event_id}")
    print(f"  Trade ID: {trade_event.trade_id}")
    print(f"  Order ID: {trade_event.order_id}")
    print(f"  Pair Symbol: {trade_event.pair_symbol}")
    print(f"  Is Bid: {trade_event.is_bid}")
    print(f"  Price: ${trade_event.price}")
    print(f"  Amount: {trade_event.amount} {trade_event.base_symbol}")
    print(f"  Value USD: ${trade_event.value_usd}")
    print(f"  Base Amount: {trade_event.base_amount} {trade_event.base_symbol}")
    print(f"  Quote Amount: {trade_event.quote_amount} {trade_event.quote_symbol}")
    print(f"  Base Fee: {trade_event.base_fee} {trade_event.base_symbol}")
    print(f"  Quote Fee: {trade_event.quote_fee} {trade_event.quote_symbol}")
    print(f"  Taker: {trade_event.taker}")
    print(f"  Taker Order History ID: {trade_event.taker_order_history_id}")
    print(f"  Maker: {trade_event.maker}")
    print(f"  Maker Order History ID: {trade_event.maker_order_history_id}")
    print(f"  TX Hash: {trade_event.tx_hash}")
    print(f"  Timestamp: {trade_event.timestamp}")

    # Convert to stream format (tuple)
    stream_data = event_to_spot_trade_stream(trade_event)
    print(f"\nStream format (tuple with {len(stream_data)} elements):")
    print(f"  First 5 elements: {stream_data[:5]}")
    print(f"  Middle 5 elements (10-14): {stream_data[10:15]}")
    print(f"  Last 5 elements: {stream_data[-5:]}")

    # Convert back to event format
    reconstructed_event = stream_to_spot_trade_event(stream_data)
    print("\nReconstructed SpotTradeEvent:")
    print(f"  Trade ID: {reconstructed_event.trade_id}")
    print(f"  Pair Symbol: {reconstructed_event.pair_symbol}")
    print(f"  Price: ${reconstructed_event.price}")
    print(f"  Amount: {reconstructed_event.amount}")
    print(f"  Value USD: ${reconstructed_event.value_usd}")

    # Example with partial data (BTC/USDT ask trade)
    partial_stream: SpotTradeStream = (
        "spotTrade",  # eventId
        "trade_xyz789",  # tradeId
        98765,  # orderId
        "0xbtc123...",  # base
        "0xusdt456...",  # quote
        "BTC",  # baseSymbol
        "USDT",  # quoteSymbol
        None,  # baseLogoURI
        None,  # quoteLogoURI
        "0xpair789...",  # pair
        "BTC/USDT",  # pairSymbol
        False,  # isBid (ask trade)
        45000.0,  # price
        "0xseller123...",  # account
        "0xbtc123...",  # asset
        "BTC",  # assetSymbol
        0.5,  # amount
        22500.0,  # valueUSD
        0.5,  # baseAmount
        22500.0,  # quoteAmount
        0.0005,  # baseFee
        22.5,  # quoteFee
        1640995300.0,  # timestamp
        "0xbuyer456...",  # taker
        11111,  # takerOrderHistoryId
        "0xseller123...",  # maker
        22222,  # makerOrderHistoryId
        "0xdef456...",  # txHash
        "btc_usdt_trade_xyz789",  # eid
    )

    print("\nPartial stream data (BTC/USDT Ask Trade):")
    print(f"  Event ID: {partial_stream[0]}")
    print(f"  Trade ID: {partial_stream[1]}")
    print(f"  Order ID: {partial_stream[2]}")
    print(f"  Base Symbol: {partial_stream[5]}")
    print(f"  Quote Symbol: {partial_stream[6]}")
    print(f"  Pair Symbol: {partial_stream[10]}")
    print(f"  Is Bid: {partial_stream[11]} (False = Ask)")
    print(f"  Price: ${partial_stream[12]}")
    print(f"  Amount: {partial_stream[16]}")
    print(f"  Value USD: ${partial_stream[17]}")

    # Validate the stream data
    try:
        validated_stream = validate_spot_trade_stream(partial_stream)
        print(f"\nValidated stream (first 5 elements): {validated_stream[:5]}")

        # Convert to event
        partial_event = stream_to_spot_trade_event(validated_stream)
        print("Partial trade event:")
        print(f"  Trade ID: {partial_event.trade_id}")
        print(f"  Pair Symbol: {partial_event.pair_symbol}")
        print(f"  Is Bid: {partial_event.is_bid} (Ask trade)")
        print(f"  Price: ${partial_event.price}")
        print(f"  Amount: {partial_event.amount} {partial_event.base_symbol}")
        print(f"  Value USD: ${partial_event.value_usd}")
        print(f"  Base Fee: {partial_event.base_fee} {partial_event.base_symbol}")
        print(f"  Quote Fee: {partial_event.quote_fee} {partial_event.quote_symbol}")
        print(f"  Taker Order History ID: {partial_event.taker_order_history_id}")
        print(f"  Maker Order History ID: {partial_event.maker_order_history_id}")

    except ValueError as e:
        print(f"Validation error: {e}")

    # Example with type conversion
    try:
        # Test various type conversions
        mixed_data = [
            "spotTrade",  # eventId
            "trade_convert",  # tradeId
            "55555",  # orderId (string -> int)
            "0x123...",  # base
            "0xabc...",  # quote
            "ETH",  # baseSymbol
            "DAI",  # quoteSymbol
            None,  # baseLogoURI
            None,  # quoteLogoURI
            "0x987...",  # pair
            "ETH/DAI",  # pairSymbol
            "1",  # isBid (string -> bool)
            "2400.50",  # price (string -> float)
            "0xtrader...",  # account
            "0x123...",  # asset
            "ETH",  # assetSymbol
            "1.5",  # amount (string -> float)
            "3600.75",  # valueUSD (string -> float)
            "1.5",  # baseAmount (string -> float)
            "3600.75",  # quoteAmount (string -> float)
            "0.0015",  # baseFee (string -> float)
            "3.60075",  # quoteFee (string -> float)
            "1640995400.0",  # timestamp (string -> float)
            "0xtaker...",  # taker
            "77777",  # takerOrderHistoryId (string -> int)
            "0xmaker...",  # maker
            "88888",  # makerOrderHistoryId (string -> int)
            "0xghi789...",  # txHash
            "eth_dai_convert",  # eid
        ]

        validated_mixed = validate_spot_trade_stream(mixed_data)
        mixed_event = stream_to_spot_trade_event(validated_mixed)
        print("\nType conversion test:")
        print(f"  Order ID: {mixed_event.order_id} (converted from string)")
        print(f"  Is Bid: {mixed_event.is_bid} (converted from '1')")
        print(f"  Price: {mixed_event.price} (converted from string)")
        print(f"  Amount: {mixed_event.amount} (converted from string)")
        print(f"  Value USD: {mixed_event.value_usd} (converted from string)")
        print(
            f"  Taker Order History ID: {mixed_event.taker_order_history_id} "
            f"(converted from string)"
        )
        print(
            f"  Maker Order History ID: {mixed_event.maker_order_history_id} "
            f"(converted from string)"
        )

    except ValueError as e:
        print(f"Type conversion error: {e}")

    # Example of invalid data
    try:
        invalid_data = ["spotTrade"] + [None] * 27  # Wrong length (28 instead of 29)
        validate_spot_trade_stream(invalid_data)
    except ValueError as e:
        print(f"\nExpected validation error (wrong length): {e}")

    try:
        # Invalid number conversion
        invalid_numbers = ["spotTrade"] + [None] * 28
        invalid_numbers[12] = "not_a_number"  # price field
        validate_spot_trade_stream(invalid_numbers)
    except ValueError as e:
        print(f"Expected validation error (invalid number): {e}")

    # Demonstrate trading scenarios
    print(f"\n{'='*60}")
    print("Trading Scenarios Demo:")
    print("=" * 60)

    # Scenario 1: Large ETH/USDC bid trade
    large_trade = SpotTradeEvent(
        event_id="spotTrade",
        trade_id="large_trade_001",
        order_id=999999,
        base_symbol="ETH",
        quote_symbol="USDC",
        pair_symbol="ETH/USDC",
        is_bid=True,
        price=2600.0,
        amount=100.0,  # Large trade
        value_usd=260000.0,
        base_amount=100.0,
        quote_amount=260000.0,
        base_fee=0.1,  # 0.1% fee
        quote_fee=260.0,  # 0.1% fee
        timestamp=1640995500.0,
        taker_order_history_id=123456,
        maker_order_history_id=654321,
    )

    print("Large Trade Scenario:")
    print(f"  {large_trade.amount} {large_trade.base_symbol} @ ${large_trade.price}")
    print(f"  Total Value: ${large_trade.value_usd}")
    print(
        f"  Fees: {large_trade.base_fee} {large_trade.base_symbol} + "
        f"${large_trade.quote_fee}"
    )

    # Scenario 2: Small BTC/ETH ask trade
    small_trade = SpotTradeEvent(
        event_id="spotTrade",
        trade_id="small_trade_002",
        order_id=111111,
        base_symbol="BTC",
        quote_symbol="ETH",
        pair_symbol="BTC/ETH",
        is_bid=False,  # Ask trade
        price=17.5,  # BTC/ETH rate
        amount=0.1,  # Small trade
        value_usd=4500.0,  # Assuming ETH = $2571.43
        base_amount=0.1,
        quote_amount=1.75,  # 0.1 BTC * 17.5 ETH/BTC
        base_fee=0.0001,
        quote_fee=0.00175,
        timestamp=1640995600.0,
    )

    print("\nSmall Trade Scenario:")
    print(
        f"  {small_trade.amount} {small_trade.base_symbol} @ "
        f"{small_trade.price} {small_trade.quote_symbol}"
    )
    print(f"  Quote Amount: {small_trade.quote_amount} {small_trade.quote_symbol}")
    print(f"  USD Value: ${small_trade.value_usd}")
    print(f"  Trade Type: {'Bid' if small_trade.is_bid else 'Ask'}")


if __name__ == "__main__":
    main()

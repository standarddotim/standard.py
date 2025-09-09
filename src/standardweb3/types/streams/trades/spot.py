"""Spot trades stream types for Standard Protocol.

This module provides Pydantic models for spot trade stream data,
equivalent to the TypeScript Zod schemas.
"""

from typing import Optional, Tuple, Union, List, Literal
from pydantic import BaseModel, Field


class SpotTradeEvent(BaseModel):
    """Spot trade event data structure."""

    event_id: Literal["spotTrade"] = Field("spotTrade", description="Event identifier")
    trade_id: Optional[str] = Field(None, description="Trade ID")
    order_id: Optional[int] = Field(None, description="Order ID")
    base: Optional[str] = Field(None, description="Base token address")
    quote: Optional[str] = Field(None, description="Quote token address")
    base_symbol: Optional[str] = Field(None, description="Base token symbol")
    quote_symbol: Optional[str] = Field(None, description="Quote token symbol")
    base_logo_uri: Optional[str] = Field(None, description="Base token logo URI")
    quote_logo_uri: Optional[str] = Field(None, description="Quote token logo URI")
    pair: Optional[str] = Field(None, description="Trading pair address")
    pair_symbol: Optional[str] = Field(None, description="Trading pair symbol")
    is_bid: Optional[bool] = Field(None, description="Whether this is a bid trade")
    price: Optional[float] = Field(None, description="Trade price")
    account: Optional[str] = Field(None, description="Account address")
    asset: Optional[str] = Field(None, description="Asset address")
    asset_symbol: Optional[str] = Field(None, description="Asset symbol")
    amount: Optional[float] = Field(None, description="Trade amount")
    value_usd: Optional[float] = Field(None, description="Trade value in USD")
    base_amount: Optional[float] = Field(None, description="Base token amount")
    quote_amount: Optional[float] = Field(None, description="Quote token amount")
    base_fee: Optional[float] = Field(None, description="Base token fee")
    quote_fee: Optional[float] = Field(None, description="Quote token fee")
    timestamp: Optional[float] = Field(None, description="Timestamp")
    taker: Optional[str] = Field(None, description="Taker address")
    taker_order_history_id: Optional[int] = Field(
        None, description="Taker order history ID"
    )
    maker: Optional[str] = Field(None, description="Maker address")
    maker_order_history_id: Optional[int] = Field(
        None, description="Maker order history ID"
    )
    tx_hash: Optional[str] = Field(None, description="Transaction hash")
    eid: Optional[str] = Field(None, description="EID")


# Type alias for the tuple representation (equivalent to z.tuple in Zod)
SpotTradeStream = Tuple[
    Optional[str],  # eventId
    Optional[str],  # tradeId
    Optional[int],  # orderId
    Optional[str],  # base
    Optional[str],  # quote
    Optional[str],  # baseSymbol
    Optional[str],  # quoteSymbol
    Optional[str],  # baseLogoURI
    Optional[str],  # quoteLogoURI
    Optional[str],  # pair
    Optional[str],  # pairSymbol
    Optional[bool],  # isBid
    Optional[float],  # price
    Optional[str],  # account
    Optional[str],  # asset
    Optional[str],  # assetSymbol
    Optional[float],  # amount
    Optional[float],  # valueUSD
    Optional[float],  # baseAmount
    Optional[float],  # quoteAmount
    Optional[float],  # baseFee
    Optional[float],  # quoteFee
    Optional[float],  # timestamp
    Optional[str],  # taker
    Optional[int],  # takerOrderHistoryId
    Optional[str],  # maker
    Optional[int],  # makerOrderHistoryId
    Optional[str],  # txHash
    Optional[str],  # eid
]


def event_to_spot_trade_stream(obj: SpotTradeEvent) -> SpotTradeStream:
    """Convert SpotTradeEvent to tuple format.

    Args:
        obj: The SpotTradeEvent object to convert

    Returns:
        Tuple representation of the spot trade data
    """
    return (
        obj.event_id,
        obj.trade_id,
        obj.order_id,
        obj.base,
        obj.quote,
        obj.base_symbol,
        obj.quote_symbol,
        obj.base_logo_uri,
        obj.quote_logo_uri,
        obj.pair,
        obj.pair_symbol,
        obj.is_bid,
        obj.price,
        obj.account,
        obj.asset,
        obj.asset_symbol,
        obj.amount,
        obj.value_usd,
        obj.base_amount,
        obj.quote_amount,
        obj.base_fee,
        obj.quote_fee,
        obj.timestamp,
        obj.taker,
        obj.taker_order_history_id,
        obj.maker,
        obj.maker_order_history_id,
        obj.tx_hash,
        obj.eid,
    )


def stream_to_spot_trade_event(data: SpotTradeStream) -> SpotTradeEvent:
    """Convert tuple format to SpotTradeEvent.

    Args:
        data: Tuple representation of spot trade data

    Returns:
        SpotTradeEvent object
    """
    return SpotTradeEvent(
        event_id=data[0] if data[0] is not None else "spotTrade",
        trade_id=data[1],
        order_id=data[2],
        base=data[3],
        quote=data[4],
        base_symbol=data[5],
        quote_symbol=data[6],
        base_logo_uri=data[7],
        quote_logo_uri=data[8],
        pair=data[9],
        pair_symbol=data[10],
        is_bid=data[11],
        price=data[12],
        account=data[13],
        asset=data[14],
        asset_symbol=data[15],
        amount=data[16],
        value_usd=data[17],
        base_amount=data[18],
        quote_amount=data[19],
        base_fee=data[20],
        quote_fee=data[21],
        timestamp=data[22],
        taker=data[23],
        taker_order_history_id=data[24],
        maker=data[25],
        maker_order_history_id=data[26],
        tx_hash=data[27],
        eid=data[28],
    )


def validate_spot_trade_stream(data: Union[List, Tuple]) -> SpotTradeStream:
    """Validate and convert input data to SpotTradeStream format.

    Args:
        data: Input data to validate (list or tuple)

    Returns:
        Validated SpotTradeStream tuple

    Raises:
        ValueError: If data format is invalid
    """
    if not isinstance(data, (list, tuple)):
        raise ValueError("Data must be a list or tuple")

    if len(data) != 29:
        raise ValueError("Data must have exactly 29 elements")

    # Convert to proper types, allowing None values
    converted_data = []
    for i, item in enumerate(data):
        if item is None:
            converted_data.append(None)
        elif i in [
            0,
            1,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            13,
            14,
            15,
            23,
            25,
            27,
            28,
        ]:  # String fields
            # eventId, tradeId, base, quote, baseSymbol, quoteSymbol, baseLogoURI,
            # quoteLogoURI, pair, pairSymbol, account, asset, assetSymbol,
            # taker, maker, txHash, eid
            converted_data.append(str(item) if item is not None else None)
        elif i in [
            2,
            24,
            26,
        ]:  # Integer fields: orderId, takerOrderHistoryId, makerOrderHistoryId
            try:
                converted_data.append(int(item) if item is not None else None)
            except (ValueError, TypeError):
                raise ValueError(f"Element at index {i} must be an integer or None")
        elif i == 11:  # isBid (boolean)
            if item is not None:
                if isinstance(item, bool):
                    converted_data.append(item)
                else:
                    # Convert string/number to boolean
                    converted_data.append(bool(item))
            else:
                converted_data.append(None)
        elif i in [12, 16, 17, 18, 19, 20, 21, 22]:  # Float fields
            # price, amount, valueUSD, baseAmount, quoteAmount, baseFee, quoteFee,
            # timestamp
            try:
                converted_data.append(float(item) if item is not None else None)
            except (ValueError, TypeError):
                raise ValueError(f"Element at index {i} must be a number or None")

    return tuple(converted_data)

"""Spot orders stream types for Standard Protocol.

This module provides Pydantic models for spot order stream data,
equivalent to the TypeScript Zod schemas. Contains three event types:
- SpotOrderMatchedEvent (27 fields)
- SpotOrderEvent (23 fields)
- SpotDeleteOrderItemEvent (9 fields)
"""

from typing import Optional, Tuple, Union, List, Literal
from pydantic import BaseModel, Field


class SpotOrderMatchedEvent(BaseModel):
    """Spot order matched event data structure."""

    event_id: Literal["spotOrderMatched"] = Field(
        "spotOrderMatched", description="Event identifier"
    )
    id: Optional[str] = Field(None, description="Match ID")
    is_bid: Optional[bool] = Field(None, description="Whether this is a bid order")
    order_history_id: Optional[int] = Field(None, description="Order history ID")
    block_number: Optional[int] = Field(None, description="Block number")
    order_id: Optional[int] = Field(None, description="Order ID")
    base: Optional[str] = Field(None, description="Base token address")
    base_symbol: Optional[str] = Field(None, description="Base token symbol")
    base_logo_uri: Optional[str] = Field(None, description="Base token logo URI")
    quote: Optional[str] = Field(None, description="Quote token address")
    quote_symbol: Optional[str] = Field(None, description="Quote token symbol")
    quote_logo_uri: Optional[str] = Field(None, description="Quote token logo URI")
    pair_symbol: Optional[str] = Field(None, description="Trading pair symbol")
    pair: Optional[str] = Field(None, description="Trading pair address")
    price: Optional[float] = Field(None, description="Order price")
    price_bn: Optional[str] = Field(None, description="Price as BigNumber string")
    asset: Optional[str] = Field(None, description="Asset address")
    asset_symbol: Optional[str] = Field(None, description="Asset symbol")
    asset_decimals: Optional[int] = Field(None, description="Asset decimals")
    amount: Optional[float] = Field(None, description="Order amount")
    placed: Optional[float] = Field(None, description="Amount placed")
    matched: Optional[float] = Field(None, description="Amount matched")
    total: Optional[float] = Field(None, description="Total amount")
    timestamp: Optional[float] = Field(None, description="Timestamp")
    account: Optional[str] = Field(None, description="Account address")
    tx_hash: Optional[str] = Field(None, description="Transaction hash")
    eid: Optional[str] = Field(None, description="EID")


class SpotOrderEvent(BaseModel):
    """Spot order event data structure."""

    event_id: Literal["spotOrder"] = Field("spotOrder", description="Event identifier")
    is_bid: Optional[bool] = Field(None, description="Whether this is a bid order")
    order_history_id: Optional[int] = Field(None, description="Order history ID")
    block_number: Optional[int] = Field(None, description="Block number")
    order_id: Optional[int] = Field(None, description="Order ID")
    base: Optional[str] = Field(None, description="Base token address")
    base_symbol: Optional[str] = Field(None, description="Base token symbol")
    base_logo_uri: Optional[str] = Field(None, description="Base token logo URI")
    quote: Optional[str] = Field(None, description="Quote token address")
    quote_symbol: Optional[str] = Field(None, description="Quote token symbol")
    quote_logo_uri: Optional[str] = Field(None, description="Quote token logo URI")
    pair_symbol: Optional[str] = Field(None, description="Trading pair symbol")
    pair: Optional[str] = Field(None, description="Trading pair address")
    price: Optional[float] = Field(None, description="Order price")
    asset: Optional[str] = Field(None, description="Asset address")
    asset_symbol: Optional[str] = Field(None, description="Asset symbol")
    asset_decimals: Optional[int] = Field(None, description="Asset decimals")
    amount: Optional[float] = Field(None, description="Order amount")
    placed: Optional[float] = Field(None, description="Amount placed")
    timestamp: Optional[float] = Field(None, description="Timestamp")
    account: Optional[str] = Field(None, description="Account address")
    tx_hash: Optional[str] = Field(None, description="Transaction hash")
    eid: Optional[str] = Field(None, description="EID")


class SpotDeleteOrderItemEvent(BaseModel):
    """Spot delete order item event data structure."""

    event_id: Union[Literal["deleteSpotOrder"], Literal["deleteSpotOrderHistory"]] = (
        Field("deleteSpotOrder", description="Event identifier")
    )
    is_bid: Optional[bool] = Field(None, description="Whether this is a bid order")
    pair: Optional[str] = Field(None, description="Trading pair")
    account: Optional[str] = Field(None, description="Account address")
    order_id: Optional[int] = Field(None, description="Order ID")
    tx_hash: Optional[str] = Field(None, description="Transaction hash")
    timestamp: Optional[float] = Field(None, description="Timestamp")
    status: Optional[str] = Field(
        None, description="Order status (open, filled, canceled)"
    )
    eid: Optional[str] = Field(None, description="EID")


# Type aliases for tuple representations

SpotOrderMatchedStream = Tuple[
    Optional[str],  # eventId
    Optional[str],  # id
    Optional[bool],  # isBid
    Optional[int],  # orderHistoryId
    Optional[int],  # blockNumber
    Optional[int],  # orderId
    Optional[str],  # base
    Optional[str],  # baseSymbol
    Optional[str],  # baseLogoURI
    Optional[str],  # quote
    Optional[str],  # quoteSymbol
    Optional[str],  # quoteLogoURI
    Optional[str],  # pairSymbol
    Optional[str],  # pair
    Optional[float],  # price
    Optional[str],  # priceBN
    Optional[str],  # asset
    Optional[str],  # assetSymbol
    Optional[int],  # assetDecimals
    Optional[float],  # amount
    Optional[float],  # placed
    Optional[float],  # matched
    Optional[float],  # total
    Optional[float],  # timestamp
    Optional[str],  # account
    Optional[str],  # txHash
    Optional[str],  # eid
]

SpotOrderStream = Tuple[
    Optional[str],  # eventId
    Optional[bool],  # isBid
    Optional[int],  # orderHistoryId
    Optional[int],  # blockNumber
    Optional[int],  # orderId
    Optional[str],  # base
    Optional[str],  # baseSymbol
    Optional[str],  # baseLogoURI
    Optional[str],  # quote
    Optional[str],  # quoteSymbol
    Optional[str],  # quoteLogoURI
    Optional[str],  # pairSymbol
    Optional[str],  # pair
    Optional[float],  # price
    Optional[str],  # asset
    Optional[str],  # assetSymbol
    Optional[int],  # assetDecimals
    Optional[float],  # amount
    Optional[float],  # placed
    Optional[float],  # timestamp
    Optional[str],  # account
    Optional[str],  # txHash
    Optional[str],  # eid
]

SpotDeleteOrderItemStream = Tuple[
    Optional[str],  # eventId
    Optional[bool],  # isBid
    Optional[str],  # pair
    Optional[str],  # account
    Optional[int],  # orderId
    Optional[str],  # txHash
    Optional[float],  # timestamp
    Optional[str],  # status
    Optional[str],  # eid
]


# Conversion functions for SpotOrderMatchedEvent


def event_to_spot_order_matched_stream(
    obj: SpotOrderMatchedEvent,
) -> SpotOrderMatchedStream:
    """Convert SpotOrderMatchedEvent to tuple format."""
    return (
        obj.event_id,
        obj.id,
        obj.is_bid,
        obj.order_history_id,
        obj.block_number,
        obj.order_id,
        obj.base,
        obj.base_symbol,
        obj.base_logo_uri,
        obj.quote,
        obj.quote_symbol,
        obj.quote_logo_uri,
        obj.pair_symbol,
        obj.pair,
        obj.price,
        obj.price_bn,
        obj.asset,
        obj.asset_symbol,
        obj.asset_decimals,
        obj.amount,
        obj.placed,
        obj.matched,
        obj.total,
        obj.timestamp,
        obj.account,
        obj.tx_hash,
        obj.eid,
    )


def stream_to_spot_order_matched_event(
    data: SpotOrderMatchedStream,
) -> SpotOrderMatchedEvent:
    """Convert tuple format to SpotOrderMatchedEvent."""
    return SpotOrderMatchedEvent(
        event_id=data[0] if data[0] is not None else "spotOrderMatched",
        id=data[1],
        is_bid=data[2],
        order_history_id=data[3],
        block_number=data[4],
        order_id=data[5],
        base=data[6],
        base_symbol=data[7],
        base_logo_uri=data[8],
        quote=data[9],
        quote_symbol=data[10],
        quote_logo_uri=data[11],
        pair_symbol=data[12],
        pair=data[13],
        price=data[14],
        price_bn=data[15],
        asset=data[16],
        asset_symbol=data[17],
        asset_decimals=data[18],
        amount=data[19],
        placed=data[20],
        matched=data[21],
        total=data[22],
        timestamp=data[23],
        account=data[24],
        tx_hash=data[25],
        eid=data[26],
    )


# Conversion functions for SpotOrderEvent


def event_to_spot_order_stream(obj: SpotOrderEvent) -> SpotOrderStream:
    """Convert SpotOrderEvent to tuple format."""
    return (
        obj.event_id,
        obj.is_bid,
        obj.order_history_id,
        obj.block_number,
        obj.order_id,
        obj.base,
        obj.base_symbol,
        obj.base_logo_uri,
        obj.quote,
        obj.quote_symbol,
        obj.quote_logo_uri,
        obj.pair_symbol,
        obj.pair,
        obj.price,
        obj.asset,
        obj.asset_symbol,
        obj.asset_decimals,
        obj.amount,
        obj.placed,
        obj.timestamp,
        obj.account,
        obj.tx_hash,
        obj.eid,
    )


def stream_to_spot_order_event(data: SpotOrderStream) -> SpotOrderEvent:
    """Convert tuple format to SpotOrderEvent."""
    return SpotOrderEvent(
        event_id=data[0] if data[0] is not None else "spotOrder",
        is_bid=data[1],
        order_history_id=data[2],
        block_number=data[3],
        order_id=data[4],
        base=data[5],
        base_symbol=data[6],
        base_logo_uri=data[7],
        quote=data[8],
        quote_symbol=data[9],
        quote_logo_uri=data[10],
        pair_symbol=data[11],
        pair=data[12],
        price=data[13],
        asset=data[14],
        asset_symbol=data[15],
        asset_decimals=data[16],
        amount=data[17],
        placed=data[18],
        timestamp=data[19],
        account=data[20],
        tx_hash=data[21],
        eid=data[22],
    )


# Conversion functions for SpotDeleteOrderItemEvent


def event_to_spot_delete_order_item_stream(
    obj: SpotDeleteOrderItemEvent,
) -> SpotDeleteOrderItemStream:
    """Convert SpotDeleteOrderItemEvent to tuple format."""
    return (
        obj.event_id,
        obj.is_bid,
        obj.pair,
        obj.account,
        obj.order_id,
        obj.tx_hash,
        obj.timestamp,
        obj.status,
        obj.eid,
    )


def stream_to_spot_delete_order_item_event(
    data: SpotDeleteOrderItemStream,
) -> SpotDeleteOrderItemEvent:
    """Convert tuple format to SpotDeleteOrderItemEvent."""
    return SpotDeleteOrderItemEvent(
        event_id=data[0] if data[0] is not None else "deleteSpotOrder",
        is_bid=data[1],
        pair=data[2],
        account=data[3],
        order_id=data[4],
        tx_hash=data[5],
        timestamp=data[6],
        status=data[7],
        eid=data[8],
    )


# Validation functions


def validate_spot_order_matched_stream(
    data: Union[List, Tuple]
) -> SpotOrderMatchedStream:
    """Validate and convert input data to SpotOrderMatchedStream format."""
    if not isinstance(data, (list, tuple)):
        raise ValueError("Data must be a list or tuple")

    if len(data) != 27:
        raise ValueError("Data must have exactly 27 elements")

    converted_data = []
    for i, item in enumerate(data):
        if item is None:
            converted_data.append(None)
        elif i in [
            0,
            1,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            15,
            16,
            17,
            24,
            25,
            26,
        ]:  # String fields
            converted_data.append(str(item) if item is not None else None)
        elif i in [
            3,
            4,
            5,
            18,
        ]:  # Integer fields: orderHistoryId, blockNumber, orderId, assetDecimals
            try:
                converted_data.append(int(item) if item is not None else None)
            except (ValueError, TypeError):
                raise ValueError(f"Element at index {i} must be an integer or None")
        elif i == 2:  # isBid (boolean)
            converted_data.append(bool(item) if item is not None else None)
        elif i in [
            14,
            19,
            20,
            21,
            22,
            23,
        ]:  # Float fields: price, amount, placed, matched, total, timestamp
            try:
                converted_data.append(float(item) if item is not None else None)
            except (ValueError, TypeError):
                raise ValueError(f"Element at index {i} must be a number or None")

    return tuple(converted_data)


def validate_spot_order_stream(data: Union[List, Tuple]) -> SpotOrderStream:
    """Validate and convert input data to SpotOrderStream format."""
    if not isinstance(data, (list, tuple)):
        raise ValueError("Data must be a list or tuple")

    if len(data) != 23:
        raise ValueError("Data must have exactly 23 elements")

    converted_data = []
    for i, item in enumerate(data):
        if item is None:
            converted_data.append(None)
        elif i in [0, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 20, 21, 22]:  # String fields
            converted_data.append(str(item) if item is not None else None)
        elif i in [
            2,
            3,
            4,
            16,
        ]:  # Integer fields: orderHistoryId, blockNumber, orderId, assetDecimals
            try:
                converted_data.append(int(item) if item is not None else None)
            except (ValueError, TypeError):
                raise ValueError(f"Element at index {i} must be an integer or None")
        elif i == 1:  # isBid (boolean)
            converted_data.append(bool(item) if item is not None else None)
        elif i in [13, 17, 18, 19]:  # Float fields: price, amount, placed, timestamp
            try:
                converted_data.append(float(item) if item is not None else None)
            except (ValueError, TypeError):
                raise ValueError(f"Element at index {i} must be a number or None")

    return tuple(converted_data)


def validate_spot_delete_order_item_stream(
    data: Union[List, Tuple]
) -> SpotDeleteOrderItemStream:
    """Validate and convert input data to SpotDeleteOrderItemStream format."""
    if not isinstance(data, (list, tuple)):
        raise ValueError("Data must be a list or tuple")

    if len(data) != 9:
        raise ValueError("Data must have exactly 9 elements")

    converted_data = []
    for i, item in enumerate(data):
        if item is None:
            converted_data.append(None)
        elif i in [
            0,
            2,
            3,
            5,
            7,
            8,
        ]:  # String fields: eventId, pair, account, txHash, status, eid
            converted_data.append(str(item) if item is not None else None)
        elif i == 1:  # isBid (boolean)
            converted_data.append(bool(item) if item is not None else None)
        elif i == 4:  # orderId (integer)
            try:
                converted_data.append(int(item) if item is not None else None)
            except (ValueError, TypeError):
                raise ValueError(f"Element at index {i} must be an integer or None")
        elif i == 6:  # timestamp (float)
            try:
                converted_data.append(float(item) if item is not None else None)
            except (ValueError, TypeError):
                raise ValueError(f"Element at index {i} must be a number or None")

    return tuple(converted_data)

"""Spot order histories stream types for Standard Protocol.

This module provides Pydantic models for spot order history stream data,
equivalent to the TypeScript Zod schemas.
"""

from typing import Optional, Tuple, Union, List, Literal
from pydantic import BaseModel, Field


class SpotOrderHistoryEvent(BaseModel):
    """Spot order history event data structure."""

    event_id: Literal["spotOrderHistory"] = Field(
        "spotOrderHistory", description="Event identifier"
    )
    order_history_id: Optional[int] = Field(None, description="Order history ID")
    block_number: Optional[int] = Field(None, description="Block number")
    order_id: Optional[int] = Field(None, description="Order ID")
    is_bid: Optional[bool] = Field(None, description="Whether this is a bid order")
    base: Optional[str] = Field(None, description="Base token address")
    base_symbol: Optional[str] = Field(None, description="Base token symbol")
    base_logo_uri: Optional[str] = Field(None, description="Base token logo URI")
    quote: Optional[str] = Field(None, description="Quote token address")
    quote_symbol: Optional[str] = Field(None, description="Quote token symbol")
    quote_logo_uri: Optional[str] = Field(None, description="Quote token logo URI")
    pair: Optional[str] = Field(None, description="Trading pair address")
    pair_symbol: Optional[str] = Field(None, description="Trading pair symbol")
    price: Optional[float] = Field(None, description="Order price")
    asset: Optional[str] = Field(None, description="Asset address")
    asset_symbol: Optional[str] = Field(None, description="Asset symbol")
    asset_decimals: Optional[int] = Field(None, description="Asset decimals")
    executed: Optional[float] = Field(None, description="Executed amount")
    amount: Optional[float] = Field(None, description="Order amount")
    timestamp: Optional[float] = Field(None, description="Timestamp")
    account: Optional[str] = Field(None, description="Account address")
    tx_hash: Optional[str] = Field(None, description="Transaction hash")
    status: Optional[str] = Field(
        None, description="Order status (open, filled, canceled, etc.)"
    )
    eid: Optional[str] = Field(None, description="EID")


# Type alias for the tuple representation (equivalent to z.tuple in Zod)
SpotOrderHistoryStream = Tuple[
    str,  # eventId (required)
    Optional[int],  # orderHistoryId
    Optional[int],  # blockNumber
    Optional[int],  # orderId
    Optional[bool],  # isBid
    Optional[str],  # base
    Optional[str],  # baseSymbol
    Optional[str],  # baseLogoURI
    Optional[str],  # quote
    Optional[str],  # quoteSymbol
    Optional[str],  # quoteLogoURI
    Optional[str],  # pair
    Optional[str],  # pairSymbol
    Optional[float],  # price
    Optional[str],  # asset
    Optional[str],  # assetSymbol
    Optional[int],  # assetDecimals
    Optional[float],  # executed
    Optional[float],  # amount
    Optional[float],  # timestamp
    Optional[str],  # account
    Optional[str],  # txHash
    Optional[str],  # status
    Optional[str],  # eid
]


def event_to_spot_order_history_stream(
    obj: SpotOrderHistoryEvent,
) -> SpotOrderHistoryStream:
    """Convert SpotOrderHistoryEvent to tuple format.

    Args:
        obj: The SpotOrderHistoryEvent object to convert

    Returns:
        Tuple representation of the spot order history data
    """
    return (
        obj.event_id,
        obj.order_history_id,
        obj.block_number,
        obj.order_id,
        obj.is_bid,
        obj.base,
        obj.base_symbol,
        obj.base_logo_uri,
        obj.quote,
        obj.quote_symbol,
        obj.quote_logo_uri,
        obj.pair,
        obj.pair_symbol,
        obj.price,
        obj.asset,
        obj.asset_symbol,
        obj.asset_decimals,
        obj.executed,
        obj.amount,
        obj.timestamp,
        obj.account,
        obj.tx_hash,
        obj.status,
        obj.eid,
    )


def stream_to_spot_order_history_event(
    data: SpotOrderHistoryStream,
) -> SpotOrderHistoryEvent:
    """Convert tuple format to SpotOrderHistoryEvent.

    Args:
        data: Tuple representation of spot order history data

    Returns:
        SpotOrderHistoryEvent object
    """
    return SpotOrderHistoryEvent(
        event_id=data[0] if data[0] is not None else "spotOrderHistory",
        order_history_id=data[1],
        block_number=data[2],
        order_id=data[3],
        is_bid=data[4],
        base=data[5],
        base_symbol=data[6],
        base_logo_uri=data[7],
        quote=data[8],
        quote_symbol=data[9],
        quote_logo_uri=data[10],
        pair=data[11],
        pair_symbol=data[12],
        price=data[13],
        asset=data[14],
        asset_symbol=data[15],
        asset_decimals=data[16],
        executed=data[17],
        amount=data[18],
        timestamp=data[19],
        account=data[20],
        tx_hash=data[21],
        status=data[22],
        eid=data[23],
    )


def validate_spot_order_history_stream(
    data: Union[List, Tuple]
) -> SpotOrderHistoryStream:
    """Validate and convert input data to SpotOrderHistoryStream format.

    Args:
        data: Input data to validate (list or tuple)

    Returns:
        Validated SpotOrderHistoryStream tuple

    Raises:
        ValueError: If data format is invalid
    """
    if not isinstance(data, (list, tuple)):
        raise ValueError("Data must be a list or tuple")

    if len(data) != 24:
        raise ValueError("Data must have exactly 24 elements")

    # Convert to proper types, allowing None values
    converted_data = []
    for i, item in enumerate(data):
        if item is None and i == 0:
            # eventId is required (first element)
            raise ValueError("Element at index 0 (eventId) cannot be None")
        elif item is None:
            converted_data.append(None)
        elif i == 0:  # eventId (string, required)
            converted_data.append(str(item))
        elif i in [
            1,
            2,
            3,
            16,
        ]:  # orderHistoryId, blockNumber, orderId, assetDecimals (integers)
            try:
                converted_data.append(int(item) if item is not None else None)
            except (ValueError, TypeError):
                raise ValueError(f"Element at index {i} must be an integer or None")
        elif i == 4:  # isBid (boolean)
            if item is not None:
                if isinstance(item, bool):
                    converted_data.append(item)
                else:
                    # Convert string/number to boolean
                    converted_data.append(bool(item))
            else:
                converted_data.append(None)
        elif i in [13, 17, 18, 19]:  # price, executed, amount, timestamp (floats)
            try:
                converted_data.append(float(item) if item is not None else None)
            except (ValueError, TypeError):
                raise ValueError(f"Element at index {i} must be a number or None")
        else:  # All other fields are strings
            converted_data.append(str(item) if item is not None else None)

    return tuple(converted_data)

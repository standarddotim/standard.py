"""Spot orderbook stream types for Standard Protocol.

This module provides Pydantic models for spot orderbook stream data,
equivalent to the TypeScript Zod schemas.
"""

from typing import Optional, Tuple, Union, List, Literal
from pydantic import BaseModel, Field


class SpotOrderBlockEvent(BaseModel):
    """Spot order block event data structure."""

    event_id: Literal["spotOrderBlock"] = Field(
        "spotOrderBlock", description="Event identifier"
    )
    is_bid: Optional[bool] = Field(None, description="Whether this is a bid order")
    price: Optional[float] = Field(None, description="Order price")
    base_liquidity: Optional[float] = Field(None, description="Base liquidity amount")
    quote_liquidity: Optional[float] = Field(None, description="Quote liquidity amount")
    scale: Optional[str] = Field(None, description="Scale information")
    timestamp: Optional[float] = Field(None, description="Timestamp")
    eid: Optional[str] = Field(None, description="EID")


# Type alias for the tuple representation (equivalent to z.tuple in Zod)
SpotOrderBlockStream = Tuple[
    Optional[str],  # eventId
    Optional[bool],  # isBid
    Optional[float],  # price
    Optional[float],  # baseVolume (baseLiquidity in event)
    Optional[float],  # quoteVolume (quoteLiquidity in event)
    Optional[str],  # scale
    Optional[float],  # timestamp
    Optional[str],  # eid
]


def event_to_spot_order_block_stream(obj: SpotOrderBlockEvent) -> SpotOrderBlockStream:
    """Convert SpotOrderBlockEvent to tuple format.

    Args:
        obj: The SpotOrderBlockEvent object to convert

    Returns:
        Tuple representation of the spot order block data
    """
    return (
        obj.event_id,
        obj.is_bid,
        obj.price,
        obj.base_liquidity,
        obj.quote_liquidity,
        obj.scale,
        obj.timestamp,
        obj.eid,
    )


def stream_to_spot_order_block_event(data: SpotOrderBlockStream) -> SpotOrderBlockEvent:
    """Convert tuple format to SpotOrderBlockEvent.

    Args:
        data: Tuple representation of spot order block data

    Returns:
        SpotOrderBlockEvent object
    """
    return SpotOrderBlockEvent(
        event_id=data[0] if data[0] is not None else "spotOrderBlock",
        is_bid=data[1],
        price=data[2],
        base_liquidity=data[3],
        quote_liquidity=data[4],
        scale=data[5],
        timestamp=data[6],
        eid=data[7],
    )


def validate_spot_order_block_stream(data: Union[List, Tuple]) -> SpotOrderBlockStream:
    """Validate and convert input data to SpotOrderBlockStream format.

    Args:
        data: Input data to validate (list or tuple)

    Returns:
        Validated SpotOrderBlockStream tuple

    Raises:
        ValueError: If data format is invalid
    """
    if not isinstance(data, (list, tuple)):
        raise ValueError("Data must be a list or tuple")

    if len(data) != 8:
        raise ValueError("Data must have exactly 8 elements")

    # Convert to proper types, allowing None values
    converted_data = []
    for i, item in enumerate(data):
        if item is None:
            converted_data.append(None)
        elif i == 0:  # eventId (string)
            converted_data.append(str(item) if item is not None else None)
        elif i == 1:  # isBid (boolean)
            if item is not None:
                if isinstance(item, bool):
                    converted_data.append(item)
                else:
                    # Convert string/number to boolean
                    converted_data.append(bool(item))
            else:
                converted_data.append(None)
        elif i in [2, 3, 4, 6]:  # price, baseVolume, quoteVolume, timestamp (numbers)
            try:
                converted_data.append(float(item) if item is not None else None)
            except (ValueError, TypeError):
                raise ValueError(f"Element at index {i} must be a number or None")
        elif i in [5, 7]:  # scale, eid (strings)
            converted_data.append(str(item) if item is not None else None)

    return tuple(converted_data)

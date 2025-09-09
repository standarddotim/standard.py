"""Spot bars stream types for Standard Protocol.

This module provides Pydantic models for spot bar stream data,
equivalent to the TypeScript Zod schemas.
"""

from typing import Optional, Tuple, Union, List
from pydantic import BaseModel, Field


class SpotBarEvent(BaseModel):
    """Spot bar event data structure."""

    event_id: Optional[str] = Field(None, description="Event identifier")
    id: Optional[str] = Field(None, description="Bar identifier (e.g. 'ETH/USDC:1m')")
    price: Optional[float] = Field(None, description="Current price")
    timestamp: Optional[float] = Field(None, description="Timestamp")
    base_volume: Optional[float] = Field(None, description="Base volume")
    quote_volume: Optional[float] = Field(None, description="Quote volume")
    volume_usd: Optional[float] = Field(None, description="Volume in USD")
    eid: Optional[str] = Field(None, description="EID")


# Type alias for the tuple representation (equivalent to z.tuple in Zod)
SpotBarStream = Tuple[
    Optional[str],  # eventId
    Optional[str],  # id (e.g. "ETH/USDC:1m")
    Optional[float],  # current price
    Optional[float],  # timestamp
    Optional[float],  # baseVolume
    Optional[float],  # quoteVolume
    Optional[float],  # volumeUSD
    Optional[str],  # eid
]


def event_to_spot_bar_stream(obj: SpotBarEvent) -> SpotBarStream:
    """Convert SpotBarEvent to tuple format.

    Args:
        obj: The SpotBarEvent object to convert

    Returns:
        Tuple representation of the spot bar data
    """
    return (
        obj.event_id,
        obj.id,
        obj.price,
        obj.timestamp,
        obj.base_volume,
        obj.quote_volume,
        obj.volume_usd,
        obj.eid,
    )


def stream_to_spot_bar_event(data: SpotBarStream) -> SpotBarEvent:
    """Convert tuple format to SpotBarEvent.

    Args:
        data: Tuple representation of spot bar data

    Returns:
        SpotBarEvent object with default values for None fields
    """
    return SpotBarEvent(
        event_id=data[0] if data[0] is not None else "spotBar",
        id=data[1] if data[1] is not None else "",
        price=data[2] if data[2] is not None else 0.0,
        timestamp=data[3] if data[3] is not None else 0.0,
        base_volume=data[4] if data[4] is not None else 0.0,
        quote_volume=data[5] if data[5] is not None else 0.0,
        volume_usd=data[6] if data[6] is not None else 0.0,
        eid=data[7] if data[7] is not None else "",
    )


def validate_spot_bar_stream(data: Union[List, Tuple]) -> SpotBarStream:
    """Validate and convert input data to SpotBarStream format.

    Args:
        data: Input data to validate (list or tuple)

    Returns:
        Validated SpotBarStream tuple

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
        elif i in [0, 1, 7]:  # String fields: eventId, id, eid
            converted_data.append(str(item) if item is not None else None)
        elif i in [2, 3, 4, 5, 6]:  # Number fields: price, timestamp, volumes
            try:
                converted_data.append(float(item) if item is not None else None)
            except (ValueError, TypeError):
                raise ValueError(f"Element at index {i} must be a number or None")

    return tuple(converted_data)

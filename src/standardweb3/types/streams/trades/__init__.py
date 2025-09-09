"""Trades stream types for Standard Protocol."""

from .spot import (
    SpotTradeEvent,
    SpotTradeStream,
    event_to_spot_trade_stream,
    stream_to_spot_trade_event,
    validate_spot_trade_stream,
)

__all__ = [
    "SpotTradeEvent",
    "SpotTradeStream",
    "event_to_spot_trade_stream",
    "stream_to_spot_trade_event",
    "validate_spot_trade_stream",
]

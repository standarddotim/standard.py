"""
Constants module for StandardWeb3.

Provides network-specific constants including contract addresses,
API URLs, and WebSocket endpoints.
"""

from .contracts import matching_engine_addresses
from .urls import api_urls, websocket_urls

__all__ = ["matching_engine_addresses", "api_urls", "websocket_urls"]

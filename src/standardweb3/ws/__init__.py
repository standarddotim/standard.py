"""
WebSocket Functions Module.

Provides WebSocket client functionality for real-time communication
with the Standard Protocol exchange.
"""

from typing import Callable, Dict
import websockets
import asyncio


class WebsocketFunctions:
    """WebSocket client functions for Standard Protocol."""

    def __init__(self, ws: websockets.WebSocketClientProtocol, server_url: str):
        """
        Initialize WebSocket functions.

        Args:
            ws: WebSocket client protocol instance
            server_url: WebSocket server URL
        """
        self.ws = ws
        self.ws_url = server_url
        self.event_handlers: Dict[str, Callable] = {}

    async def connect_to_ws(self, url: str):
        """Connect to WebSocket server with automatic reconnection."""
        while True:
            try:
                async with websockets.connect(url) as websocket:
                    self.ws = websocket
                    print("Connected")
                    while True:
                        message = await websocket.recv()
                        print(f"Received: {message}")
                        if message == "Hello":
                            await websocket.send("Hello")
            except Exception as e:
                print(f"Connection failed: {e}. Reconnecting in 5s...")
                await asyncio.sleep(5)

    async def disconnect_from_ws(self):
        """Disconnect from WebSocket server."""
        await self.ws.close()
        print("Disconnected from the websocket")

    async def send_to_ws(self, message: str):
        """Send message to WebSocket server."""
        await self.ws.send(message)

    async def receive_from_ws(self):
        """Receive message from WebSocket server."""
        return await self.ws.recv()

    def start_ws(self):
        """Start WebSocket connection."""
        asyncio.run(self.connect_to_ws(self.ws_url))

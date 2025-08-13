"""
Test WebSocket functions for StandardWeb3 client.

Tests WebSocket connection, subscription management, and real-time data handling.
"""

import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from standardweb3 import StandardClient


class TestWebSocketFunctions:
    """Test cases for StandardClient WebSocket functions."""

    @pytest_asyncio.fixture
    async def mock_client(self):
        """Create a mocked StandardClient for testing WebSocket functions."""
        test_private_key = "0x" + "1" * 64
        test_rpc_url = "https://test-rpc.example.com"
        test_matching_engine = "0x1234567890123456789012345678901234567890"
        test_websocket_url = "wss://test-ws.example.com"

        with (
            patch("standardweb3.contract.ContractFunctions"),
            patch("standardweb3.ws.WebsocketFunctions") as mock_ws,
        ):

            # Mock WebSocket methods
            mock_ws.return_value.start_ws = AsyncMock()
            mock_ws.return_value.close_ws = AsyncMock()
            mock_ws.return_value.subscribe = AsyncMock()
            mock_ws.return_value.unsubscribe = AsyncMock()
            mock_ws.return_value.is_connected = MagicMock(return_value=False)

            client = StandardClient(
                private_key=test_private_key,
                http_rpc_url=test_rpc_url,
                matching_engine_address=test_matching_engine,
                websocket_url=test_websocket_url,
            )

            return client

    @pytest.mark.asyncio
    async def test_start_websocket_connection(self, mock_client):
        """Test starting WebSocket connection."""
        # Execute the function
        await mock_client.start_ws()

        # Verify the WebSocket start method was called
        mock_client.ws.start_ws.assert_called_once()

    @pytest.mark.asyncio
    async def test_websocket_connection_error_handling(self, mock_client):
        """Test WebSocket connection error handling."""
        # Mock the WebSocket start method to raise an exception
        mock_client.ws.start_ws.side_effect = Exception("WebSocket connection failed")

        # Test that the exception is properly propagated
        with pytest.raises(Exception, match="WebSocket connection failed"):
            await mock_client.start_ws()

    @pytest.mark.asyncio
    async def test_websocket_with_different_urls(self):
        """Test WebSocket initialization with different URLs."""
        test_private_key = "0x" + "1" * 64
        test_rpc_url = "https://test-rpc.example.com"
        test_matching_engine = "0x1234567890123456789012345678901234567890"

        websocket_urls = [
            "wss://mainnet-ws.example.com",
            "wss://testnet-ws.example.com",
            "wss://localhost:8080",
        ]

        for ws_url in websocket_urls:
            with (
                patch("standardweb3.contract.ContractFunctions"),
                patch("standardweb3.ws.WebsocketFunctions") as mock_ws,
            ):

                client = StandardClient(
                    private_key=test_private_key,
                    http_rpc_url=test_rpc_url,
                    matching_engine_address=test_matching_engine,
                    websocket_url=ws_url,
                )

                # Verify the WebSocket was initialized with the correct URL
                assert client.websocket_url == ws_url
                # Verify WebsocketFunctions was called with the correct URL
                mock_ws.assert_called_with(None, ws_url)

    @pytest.mark.asyncio
    async def test_websocket_with_network_specific_urls(self):
        """Test WebSocket initialization with network-specific URLs."""
        test_private_key = "0x" + "1" * 64
        test_rpc_url = "https://testnet-rpc.somnia.network"

        with (
            patch("standardweb3.contract.ContractFunctions"),
            patch("standardweb3.ws.WebsocketFunctions") as mock_ws,
        ):

            client = StandardClient(
                private_key=test_private_key,
                http_rpc_url=test_rpc_url,
                networkName="Somnia Testnet",
                matching_engine_address="0x4Ca2C768773F6E0e9255da5B4e21ED9BA282B85e",
            )

            # Verify the WebSocket was initialized with Somnia Testnet URL
            expected_ws_url = "wss://story-odyssey-websocket.standardweb3.com"
            assert client.websocket_url == expected_ws_url
            mock_ws.assert_called_with(None, expected_ws_url)

    def test_websocket_attributes_exist(self, mock_client):
        """Test that WebSocket-related attributes exist on the client."""
        # Check that the client has the expected WebSocket attributes
        assert hasattr(mock_client, "ws")
        assert hasattr(mock_client, "websocket_url")

        # Verify the WebSocket object has expected methods
        assert hasattr(mock_client.ws, "start_ws")

    @pytest.mark.asyncio
    async def test_websocket_reconnection_scenario(self, mock_client):
        """Test WebSocket reconnection scenario."""
        # Simulate first connection
        await mock_client.start_ws()

        # Simulate disconnection by raising an exception
        mock_client.ws.start_ws.side_effect = Exception("Connection lost")

        # Test reconnection attempt
        with pytest.raises(Exception, match="Connection lost"):
            await mock_client.start_ws()

        # Reset the side effect and test successful reconnection
        mock_client.ws.start_ws.side_effect = None
        await mock_client.start_ws()

        # Verify start_ws was called multiple times
        assert mock_client.ws.start_ws.call_count == 3

    @pytest.mark.asyncio
    async def test_websocket_multiple_start_calls(self, mock_client):
        """Test multiple calls to start WebSocket."""
        # Call start_ws multiple times
        await mock_client.start_ws()
        await mock_client.start_ws()
        await mock_client.start_ws()

        # Verify start_ws was called the expected number of times
        assert mock_client.ws.start_ws.call_count == 3

    @pytest.mark.asyncio
    async def test_websocket_initialization_without_url(self):
        """Test WebSocket initialization without explicit URL."""
        test_private_key = "0x" + "1" * 64
        test_rpc_url = "https://test-rpc.example.com"
        test_matching_engine = "0x1234567890123456789012345678901234567890"

        with (
            patch("standardweb3.contract.ContractFunctions"),
            patch("standardweb3.ws.WebsocketFunctions") as mock_ws,
        ):

            StandardClient(
                private_key=test_private_key,
                http_rpc_url=test_rpc_url,
                matching_engine_address=test_matching_engine,
                # No websocket_url provided
            )

            # Verify WebsocketFunctions was called with None URL
            mock_ws.assert_called_with(None, None)

    @pytest.mark.asyncio
    async def test_websocket_timeout_handling(self, mock_client):
        """Test WebSocket timeout handling."""
        import asyncio

        # Mock the WebSocket start method to timeout
        async def timeout_coroutine():
            await asyncio.sleep(10)  # Simulate long-running operation

        mock_client.ws.start_ws.side_effect = timeout_coroutine

        # Test with a timeout
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(mock_client.start_ws(), timeout=0.1)

    @pytest.mark.asyncio
    async def test_websocket_concurrent_operations(self, mock_client):
        """Test concurrent WebSocket operations."""
        import asyncio

        # Define multiple WebSocket operations
        operations = [
            mock_client.start_ws(),
            mock_client.start_ws(),
            mock_client.start_ws(),
        ]

        # Execute all operations concurrently
        await asyncio.gather(*operations)

        # Verify all operations completed
        assert mock_client.ws.start_ws.call_count == 3

    def test_websocket_url_validation(self):
        """Test WebSocket URL validation and formatting."""
        test_private_key = "0x" + "1" * 64
        test_rpc_url = "https://test-rpc.example.com"
        test_matching_engine = "0x1234567890123456789012345678901234567890"

        valid_websocket_urls = [
            "wss://example.com",
            "wss://example.com:8080",
            "wss://example.com/path",
            "wss://subdomain.example.com/path?query=value",
        ]

        for ws_url in valid_websocket_urls:
            with (
                patch("standardweb3.contract.ContractFunctions"),
                patch("standardweb3.ws.WebsocketFunctions"),
            ):

                client = StandardClient(
                    private_key=test_private_key,
                    http_rpc_url=test_rpc_url,
                    matching_engine_address=test_matching_engine,
                    websocket_url=ws_url,
                )

                assert client.websocket_url == ws_url

    @pytest.mark.asyncio
    async def test_websocket_state_management(self, mock_client):
        """Test WebSocket state management."""
        # Initially not connected
        assert hasattr(mock_client.ws, "start_ws")

        # Start connection
        await mock_client.start_ws()

        # Verify start_ws was called
        mock_client.ws.start_ws.assert_called_once()

    @pytest.mark.asyncio
    async def test_websocket_error_propagation(self, mock_client):
        """Test that WebSocket errors are properly propagated."""
        # Define different types of exceptions
        exceptions = [
            ConnectionError("Connection failed"),
            TimeoutError("Connection timeout"),
            ValueError("Invalid URL"),
            RuntimeError("WebSocket runtime error"),
        ]

        for exception in exceptions:
            # Reset the mock
            mock_client.ws.start_ws.reset_mock()
            mock_client.ws.start_ws.side_effect = exception

            # Test that the specific exception is propagated
            with pytest.raises(type(exception)):
                await mock_client.start_ws()

            # Verify the method was called
            mock_client.ws.start_ws.assert_called_once()

    def test_websocket_configuration_integration(self):
        """Test WebSocket configuration with different client setups."""
        test_private_key = "0x" + "1" * 64
        test_rpc_url = "https://test-rpc.example.com"

        configurations = [
            {
                "matching_engine_address": "0x1234567890123456789012345678901234567890",
                "websocket_url": "wss://custom-ws.example.com",
            },
            {
                "networkName": "Somnia Testnet",
                "matching_engine_address": "0x4Ca2C768773F6E0e9255da5B4e21ED9BA282B85e",
            },
        ]

        for config in configurations:
            with (
                patch("standardweb3.contract.ContractFunctions"),
                patch("standardweb3.ws.WebsocketFunctions") as mock_ws,
            ):

                client = StandardClient(
                    private_key=test_private_key, http_rpc_url=test_rpc_url, **config
                )

                # Verify WebSocket was properly configured
                assert hasattr(client, "ws")
                assert hasattr(client, "websocket_url")
                mock_ws.assert_called_once()

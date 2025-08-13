"""
Test setup and initialization for StandardWeb3 client.

Tests basic client initialization and configuration validation.
"""

import os
import pytest
from unittest.mock import patch
from dotenv import load_dotenv
from standardweb3 import StandardClient

# Load environment variables for testing
load_dotenv()


class TestStandardClientSetup:
    """Test cases for StandardClient initialization and setup."""

    def test_init_with_environment_variables(self):
        """Test client initialization with environment variables."""
        private_key = os.environ.get("PRIVATE_KEY")
        rpc_url = os.environ.get("RPC_URL")

        if not private_key or not rpc_url:
            pytest.skip("Environment variables PRIVATE_KEY and RPC_URL not set")

        client = StandardClient(
            private_key=private_key, http_rpc_url=rpc_url, networkName="Somnia Testnet"
        )

        assert client is not None
        assert client.w3 is not None
        assert client.account is not None
        assert client.address is not None
        assert hasattr(client, "contract")
        assert hasattr(client, "api")
        assert hasattr(client, "ws")

    def test_init_with_custom_parameters(self):
        """Test client initialization with custom parameters."""
        test_private_key = "0x" + "1" * 64  # Mock private key
        test_rpc_url = "https://test-rpc.example.com"
        test_matching_engine = "0x1234567890123456789012345678901234567890"

        with patch("standardweb3.contract.ContractFunctions"):
            client = StandardClient(
                private_key=test_private_key,
                http_rpc_url=test_rpc_url,
                matching_engine_address=test_matching_engine,
                api_url="https://test-api.example.com",
                websocket_url="wss://test-ws.example.com",
                api_key="test_api_key",
            )

            assert client is not None
            assert client.matching_engine_address == test_matching_engine

    def test_init_with_somnia_testnet(self):
        """Test client initialization with Somnia Testnet."""
        test_private_key = "0x" + "1" * 64
        test_rpc_url = "https://testnet-rpc.somnia.network"

        with patch("standardweb3.contract.ContractFunctions"):
            client = StandardClient(
                private_key=test_private_key,
                http_rpc_url=test_rpc_url,
                networkName="Somnia Testnet",
                matching_engine_address="0x4Ca2C768773F6E0e9255da5B4e21ED9BA282B85e",
            )

            assert client is not None
            assert (
                client.matching_engine_address
                == "0x4Ca2C768773F6E0e9255da5B4e21ED9BA282B85e"
            )

    def test_init_with_mode_mainnet(self):
        """Test client initialization with Mode Mainnet."""
        test_private_key = "0x" + "1" * 64
        test_rpc_url = "https://mainnet.mode.network"

        with patch("standardweb3.contract.ContractFunctions"):
            client = StandardClient(
                private_key=test_private_key,
                http_rpc_url=test_rpc_url,
                networkName="Mode Mainnet",
                matching_engine_address="0x240aA2c15fBf6F65882A847462b04d5DA51A37Df",
            )

            assert client is not None
            assert (
                client.matching_engine_address
                == "0x240aA2c15fBf6F65882A847462b04d5DA51A37Df"
            )

    def test_invalid_network_name_raises_error(self):
        """Test that invalid network name raises ValueError."""
        test_private_key = "0x" + "1" * 64
        test_rpc_url = "https://test-rpc.example.com"

        with pytest.raises(ValueError, match="Invalid Network Name"):
            StandardClient(
                private_key=test_private_key,
                http_rpc_url=test_rpc_url,
                networkName="Invalid Network",
                matching_engine_address="0x1234567890123456789012345678901234567890",
            )

    def test_client_attributes_exist(self):
        """Test that all expected client attributes exist."""
        test_private_key = "0x" + "1" * 64
        test_rpc_url = "https://test-rpc.example.com"
        test_matching_engine = "0x1234567890123456789012345678901234567890"

        with patch("standardweb3.contract.ContractFunctions") as mock_contract:
            # Mock the contract functions to avoid actual blockchain connection
            mock_contract.return_value.w3 = "mocked_w3"
            mock_contract.return_value.address = "mocked_address"
            mock_contract.return_value.account = "mocked_account"

            client = StandardClient(
                private_key=test_private_key,
                http_rpc_url=test_rpc_url,
                matching_engine_address=test_matching_engine,
            )

            # Check that all expected attributes are present
            expected_attributes = [
                "contract",
                "api",
                "ws",
                "w3",
                "address",
                "account",
                "matching_engine_address",
                "api_url",
                "websocket_url",
            ]

            for attr in expected_attributes:
                assert hasattr(client, attr), f"Client missing attribute: {attr}"

    @pytest.mark.parametrize(
        "network_name,expected_address",
        [
            ("Somnia Testnet", "0x4Ca2C768773F6E0e9255da5B4e21ED9BA282B85e"),
            ("Mode Mainnet", "0x240aA2c15fBf6F65882A847462b04d5DA51A37Df"),
        ],
    )
    def test_network_specific_addresses(self, network_name, expected_address):
        """Test that network-specific addresses are set correctly."""
        test_private_key = "0x" + "1" * 64
        test_rpc_url = "https://test-rpc.example.com"

        with patch("standardweb3.contract.ContractFunctions"):
            client = StandardClient(
                private_key=test_private_key,
                http_rpc_url=test_rpc_url,
                networkName=network_name,
                matching_engine_address=expected_address,
            )

            assert client.matching_engine_address == expected_address

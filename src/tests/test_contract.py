"""
Test contract functions for StandardWeb3 client.

Tests trading operations including market orders, limit orders, and other
blockchain-related functionality.
"""

import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from standardweb3 import StandardClient


class TestContractFunctions:
    """Test cases for StandardClient contract functions."""

    @pytest_asyncio.fixture
    async def mock_client(self):
        """Create a mocked StandardClient for testing."""
        test_private_key = "0x" + "1" * 64
        test_rpc_url = "https://test-rpc.example.com"
        test_matching_engine = "0x1234567890123456789012345678901234567890"

        with patch("standardweb3.contract.ContractFunctions") as mock_contract:
            # Mock the contract functions
            mock_contract.return_value.w3 = MagicMock()
            mock_contract.return_value.address = "0xtest_address"
            mock_contract.return_value.account = MagicMock()

            # Mock async trading methods
            mock_contract.return_value.market_buy = AsyncMock(
                return_value="0xmarket_buy_hash"
            )
            mock_contract.return_value.market_sell = AsyncMock(
                return_value="0xmarket_sell_hash"
            )
            mock_contract.return_value.limit_buy = AsyncMock(
                return_value="0xlimit_buy_hash"
            )
            mock_contract.return_value.limit_sell = AsyncMock(
                return_value="0xlimit_sell_hash"
            )

            client = StandardClient(
                private_key=test_private_key,
                http_rpc_url=test_rpc_url,
                matching_engine_address=test_matching_engine,
            )

            return client

    @pytest.mark.asyncio
    async def test_market_buy(self, mock_client):
        """Test market buy order execution."""
        # Test parameters
        base = "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087"
        quote = "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063"
        quote_amount = 1000
        is_maker = False
        n = 1
        recipient = "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087"
        slippage_limit = 50  # 0.5%

        # Execute market buy
        result = await mock_client.market_buy(
            base, quote, quote_amount, is_maker, n, recipient, slippage_limit
        )

        # Verify the result
        assert result == "0xmarket_buy_hash"

        # Verify the underlying contract method was called with correct parameters
        mock_client.contract.market_buy.assert_called_once_with(
            base, quote, quote_amount, is_maker, n, recipient, slippage_limit
        )

    @pytest.mark.asyncio
    async def test_market_sell(self, mock_client):
        """Test market sell order execution."""
        # Test parameters
        base = "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087"
        quote = "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063"
        base_amount = 500
        is_maker = False
        n = 1
        recipient = "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087"
        slippage_limit = 75  # 0.75%

        # Execute market sell
        result = await mock_client.market_sell(
            base, quote, base_amount, is_maker, n, recipient, slippage_limit
        )

        # Verify the result
        assert result == "0xmarket_sell_hash"

        # Verify the underlying contract method was called with correct parameters
        mock_client.contract.market_sell.assert_called_once_with(
            base, quote, base_amount, is_maker, n, recipient, slippage_limit
        )

    @pytest.mark.asyncio
    async def test_limit_buy(self, mock_client):
        """Test limit buy order execution."""
        # Test parameters
        base = "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087"
        quote = "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063"
        price = 2000  # Price in quote token units
        quote_amount = 1000
        is_maker = True
        n = 1
        recipient = "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087"

        # Execute limit buy
        result = await mock_client.limit_buy(
            base, quote, price, quote_amount, is_maker, n, recipient
        )

        # Verify the result
        assert result == "0xlimit_buy_hash"

        # Verify the underlying contract method was called with correct parameters
        mock_client.contract.limit_buy.assert_called_once_with(
            base, quote, price, quote_amount, is_maker, n, recipient
        )

    @pytest.mark.asyncio
    async def test_limit_sell(self, mock_client):
        """Test limit sell order execution."""
        # Test parameters
        base = "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087"
        quote = "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063"
        price = 1800  # Price in quote token units
        base_amount = 500
        is_maker = True
        n = 1
        recipient = "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087"

        # Execute limit sell
        result = await mock_client.limit_sell(
            base, quote, price, base_amount, is_maker, n, recipient
        )

        # Verify the result
        assert result == "0xlimit_sell_hash"

        # Verify the underlying contract method was called with correct parameters
        mock_client.contract.limit_sell.assert_called_once_with(
            base, quote, price, base_amount, is_maker, n, recipient
        )

    @pytest.mark.asyncio
    async def test_contract_function_error_handling(self, mock_client):
        """Test error handling in contract functions."""
        # Mock a contract function to raise an exception
        mock_client.contract.market_buy.side_effect = Exception("Contract error")

        # Test that the exception is properly propagated
        with pytest.raises(Exception, match="Contract error"):
            await mock_client.market_buy(
                "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
                "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
                1000,
                False,
                1,
                "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
                50,
            )

    @pytest.mark.parametrize(
        "trading_function,expected_hash,params",
        [
            (
                "market_buy",
                "0xmarket_buy_hash",
                [
                    "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
                    "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
                    1000,
                    False,
                    1,
                    "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
                    50,
                ],
            ),
            (
                "market_sell",
                "0xmarket_sell_hash",
                [
                    "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
                    "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
                    500,
                    False,
                    1,
                    "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
                    75,
                ],
            ),
            (
                "limit_buy",
                "0xlimit_buy_hash",
                [
                    "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
                    "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
                    2000,
                    1000,
                    True,
                    1,
                    "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
                ],
            ),
            (
                "limit_sell",
                "0xlimit_sell_hash",
                [
                    "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
                    "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
                    1800,
                    500,
                    True,
                    1,
                    "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
                ],
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_all_trading_functions(
        self, mock_client, trading_function, expected_hash, params
    ):
        """Test all trading functions with parameterized test data."""
        # Get the function from the client
        func = getattr(mock_client, trading_function)

        # Execute the function with the provided parameters
        result = await func(*params)

        # Verify the result
        assert result == expected_hash

        # Verify the underlying contract method was called
        contract_func = getattr(mock_client.contract, trading_function)
        contract_func.assert_called_once_with(*params)

    def test_client_has_contract_attributes(self, mock_client):
        """Test that client properly exposes contract attributes."""
        # Check that the client has the expected contract-related attributes
        assert hasattr(mock_client, "w3")
        assert hasattr(mock_client, "address")
        assert hasattr(mock_client, "account")
        assert hasattr(mock_client, "contract")

        # Verify the attributes are properly set from the contract
        assert mock_client.w3 is mock_client.contract.w3
        assert mock_client.address == mock_client.contract.address
        assert mock_client.account is mock_client.contract.account

    @pytest.mark.asyncio
    async def test_trading_function_type_validation(self, mock_client):
        """Test that trading functions work with various parameter types."""
        # Test with string parameters (typical usage)
        result = await mock_client.market_buy(
            "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
            "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
            "1000",
            False,
            "1",
            "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
            "50",
        )
        assert result == "0xmarket_buy_hash"

        # Test with integer parameters
        result = await mock_client.limit_buy(
            "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
            "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
            2000,
            1000,
            True,
            1,
            "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
        )
        assert result == "0xlimit_buy_hash"

    @pytest.mark.asyncio
    async def test_concurrent_trading_operations(self, mock_client):
        """Test that multiple trading operations can be executed concurrently."""
        import asyncio

        # Define multiple trading operations
        base = "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087"
        quote = "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063"
        recipient = "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087"
        operations = [
            mock_client.market_buy(base, quote, 100, False, 1, recipient, 50),
            mock_client.market_sell(base, quote, 100, False, 1, recipient, 50),
            mock_client.limit_buy(base, quote, 1000, 100, True, 1, recipient),
            mock_client.limit_sell(base, quote, 1000, 100, True, 1, recipient),
        ]

        # Execute all operations concurrently
        results = await asyncio.gather(*operations)

        # Verify all operations completed successfully
        expected_results = [
            "0xmarket_buy_hash",
            "0xmarket_sell_hash",
            "0xlimit_buy_hash",
            "0xlimit_sell_hash",
        ]
        assert results == expected_results

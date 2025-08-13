"""
Test API functions for StandardWeb3 client.

Tests API endpoints for fetching market data, order history, trade data,
and other information from the Standard Protocol exchange.
"""

import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from standardweb3 import StandardClient
from standardweb3.types.orderbook import Orderbook
from standardweb3.types.orderhistory import AccountOrderHistory
from standardweb3.types.order import AccountOrders
from standardweb3.types.pair import Pair, PairData
from standardweb3.types.token import TokenData, TokenInfo
from standardweb3.types.tradehistory import AccountTradeHistory
from standardweb3.types.trade import TradesData


class TestAPIFunctions:
    """Test cases for StandardClient API functions."""

    @pytest_asyncio.fixture
    async def mock_client(self):
        """Create a mocked StandardClient for testing API functions."""
        test_private_key = "0x" + "1" * 64
        test_rpc_url = "https://test-rpc.example.com"
        test_matching_engine = "0x1234567890123456789012345678901234567890"

        with (
            patch("standardweb3.contract.ContractFunctions"),
            patch("standardweb3.api.query.APIFunctions") as mock_api,
        ):

            # Mock API methods
            mock_api.return_value.fetch_orderbook = AsyncMock()
            mock_api.return_value.fetch_account_order_history_paginated_with_limit = (
                AsyncMock()
            )
            mock_api.return_value.fetch_account_orders_paginated_with_limit = (
                AsyncMock()
            )
            mock_api.return_value.fetch_all_pairs = AsyncMock()
            mock_api.return_value.fetch_new_listing_pairs = AsyncMock()
            mock_api.return_value.fetch_pair_info = AsyncMock()
            mock_api.return_value.fetch_top_gainer_pairs = AsyncMock()
            mock_api.return_value.fetch_top_loser_pairs = AsyncMock()
            mock_api.return_value.fetch_all_tokens = AsyncMock()
            mock_api.return_value.fetch_new_listing_tokens = AsyncMock()
            mock_api.return_value.fetch_top_gainer_tokens = AsyncMock()
            mock_api.return_value.fetch_top_loser_tokens = AsyncMock()
            mock_api.return_value.fetch_token_info = AsyncMock()
            mock_api.return_value.fetch_account_trade_history_paginated_with_limit = (
                AsyncMock()
            )
            mock_api.return_value.fetch_recent_overall_trades_paginated = AsyncMock()
            mock_api.return_value.fetch_recent_pair_trades_paginated = AsyncMock()

            client = StandardClient(
                private_key=test_private_key,
                http_rpc_url=test_rpc_url,
                matching_engine_address=test_matching_engine,
                api_url="https://test-api.example.com",
            )

            return client

    def create_mock_orderbook(self):
        """Create mock orderbook data."""
        from standardweb3.types.orderbook import Tick

        return Orderbook(
            orderbook="test_orderbook",
            mktPrice=100.0,
            bidHead=99.0,
            askHead=101.0,
            bids=[
                Tick(
                    id="bid1",
                    orderbook="test_orderbook",
                    price=99.0,
                    amount=8.0,
                    count=1,
                ),
                Tick(
                    id="bid2",
                    orderbook="test_orderbook",
                    price=98.0,
                    amount=12.0,
                    count=1,
                ),
            ],
            asks=[
                Tick(
                    id="ask1",
                    orderbook="test_orderbook",
                    price=101.0,
                    amount=10.0,
                    count=1,
                ),
                Tick(
                    id="ask2",
                    orderbook="test_orderbook",
                    price=102.0,
                    amount=5.0,
                    count=1,
                ),
            ],
            lastUpdated=1640995200.0,
        )

    def create_mock_pair_data(self):
        """Create mock pair data."""
        # Use the shared fixture data
        from standardweb3.types.token import Token

        base_token = Token(
            id="base_token_1",
            name="Base Token",
            symbol="BASE",
            ticker="BASE",
            totalSupply=1000000.0,
            logoURI="https://example.com/base.png",
            decimals=18,
            price=100.0,
            cpPrice=100.0,
            cgId="base-token",
            cmcId="1",
            ath=150.0,
            atl=50.0,
            listingDate=1640995200.0,
            dayPriceDifference=5.0,
            dayPriceDifferencePercentage=5.0,
            dayTvl=100000.0,
            dayTvlUSD=100000.0,
            dayVolume=50000.0,
            dayVolumeUSD=50000.0,
            creator="0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
            totalMinBuckets=1440,
            totalHourBuckets=24,
            totalDayBuckets=1,
            totalWeekBuckets=1,
            totalMonthBuckets=1,
        )

        quote_token = Token(
            id="quote_token_1",
            name="Quote Token",
            symbol="QUOTE",
            ticker="QUOTE",
            totalSupply=1000000.0,
            logoURI="https://example.com/quote.png",
            decimals=18,
            price=1.0,
            cpPrice=1.0,
            cgId="quote-token",
            cmcId="2",
            ath=1.5,
            atl=0.5,
            listingDate=1640995200.0,
            dayPriceDifference=0.1,
            dayPriceDifferencePercentage=10.0,
            dayTvl=50000.0,
            dayTvlUSD=50000.0,
            dayVolume=25000.0,
            dayVolumeUSD=25000.0,
            creator="0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
            totalMinBuckets=1440,
            totalHourBuckets=24,
            totalDayBuckets=1,
            totalWeekBuckets=1,
            totalMonthBuckets=1,
        )

        test_pair = Pair(
            id="pair_1",
            symbol="BASE/QUOTE",
            ticker="BASE-QUOTE",
            description="Base Token / Quote Token",
            type="DEX",
            exchange="Standard",
            base=base_token,
            quote=quote_token,
            price=100.0,
            ath=150.0,
            atl=50.0,
            listingDate=1640995200.0,
            dayPriceDifference=5.0,
            dayPriceDifferencePercentage=5.0,
            dayBaseVolume=1000.0,
            dayQuoteVolume=100000.0,
            dayBaseVolumeUSD=100000.0,
            dayQuoteVolumeUSD=100000.0,
            dayBaseTvl=10000.0,
            dayQuoteTvl=1000000.0,
            dayBaseTvlUSD=1000000.0,
            dayQuoteTvlUSD=1000000.0,
            orderbook="test_orderbook",
            bDecimal=18,
            qDecimal=18,
            totalMinBuckets=1440,
            totalHourBuckets=24,
            totalDayBuckets=1,
            totalWeekBuckets=1,
            totalMonthBuckets=1,
        )

        return PairData(pairs=[test_pair], totalCount=1, totalPages=1, pageSize=10)

    def create_mock_token_data(self):
        """Create mock token data."""
        from standardweb3.types.token import Token

        token = Token(
            id="test_token_1",
            name="Test Token",
            symbol="TEST",
            ticker="TEST",
            totalSupply=1000000.0,
            logoURI="https://example.com/test.png",
            decimals=18,
            price=1.50,
            cpPrice=1.50,
            cgId="test-token",
            cmcId="123",
            ath=2.0,
            atl=0.5,
            listingDate=1640995200.0,
            dayPriceDifference=0.1,
            dayPriceDifferencePercentage=7.1,
            dayTvl=75000.0,
            dayTvlUSD=75000.0,
            dayVolume=15000.0,
            dayVolumeUSD=15000.0,
            creator="0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
            totalMinBuckets=1440,
            totalHourBuckets=24,
            totalDayBuckets=1,
            totalWeekBuckets=1,
            totalMonthBuckets=1,
        )

        return TokenData(tokens=[token], totalCount=1, totalPages=1, pageSize=10)

    @pytest.mark.asyncio
    async def test_fetch_orderbook(self, mock_client):
        """Test fetching orderbook data."""
        # Setup mock response
        mock_orderbook = self.create_mock_orderbook()
        mock_client.api.fetch_orderbook.return_value = mock_orderbook

        # Test parameters
        base = "0xBaseToken"
        quote = "0xQuoteToken"

        # Execute the function
        result = await mock_client.fetch_orderbook(base, quote)

        # Verify the result
        assert isinstance(result, Orderbook)
        assert result == mock_orderbook

        # Verify the API method was called with correct parameters
        mock_client.api.fetch_orderbook.assert_called_once_with(base, quote)

    @pytest.mark.asyncio
    async def test_fetch_account_order_history_paginated_with_limit(
        self, mock_client, mock_account_order_history
    ):
        """Test fetching paginated account order history."""
        # Setup mock response
        api_method = mock_client.api.fetch_account_order_history_paginated_with_limit
        api_method.return_value = mock_account_order_history

        # Test parameters
        address = "0xTestAddress"
        limit = 10
        page = 1

        # Execute the function
        result = await mock_client.fetch_account_order_history_paginated_with_limit(
            address, limit, page
        )

        # Verify the result
        assert isinstance(result, AccountOrderHistory)
        assert result == mock_account_order_history

        # Verify the API method was called with correct parameters
        api_method = mock_client.api.fetch_account_order_history_paginated_with_limit
        api_method.assert_called_once_with(address, limit, page)

    @pytest.mark.asyncio
    async def test_fetch_account_orders_paginated_with_limit(
        self, mock_client, mock_account_orders
    ):
        """Test fetching paginated account orders."""
        # Setup mock response
        mock_client.api.fetch_account_orders_paginated_with_limit.return_value = (
            mock_account_orders
        )

        # Test parameters
        address = "0xTestAddress"
        limit = 10
        page = 1

        # Execute the function
        result = await mock_client.fetch_account_orders_paginated_with_limit(
            address, limit, page
        )

        # Verify the result
        assert isinstance(result, AccountOrders)
        assert result == mock_account_orders

        # Verify the API method was called with correct parameters
        api_method = mock_client.api.fetch_account_orders_paginated_with_limit
        api_method.assert_called_once_with(address, limit, page)

    @pytest.mark.asyncio
    async def test_fetch_all_pairs(self, mock_client):
        """Test fetching all trading pairs."""
        # Setup mock response
        mock_pairs = self.create_mock_pair_data()
        mock_client.api.fetch_all_pairs.return_value = mock_pairs

        # Test parameters
        limit = 10
        page = 1

        # Execute the function
        result = await mock_client.fetch_all_pairs(limit, page)

        # Verify the result
        assert isinstance(result, PairData)
        assert result == mock_pairs

        # Verify the API method was called with correct parameters
        mock_client.api.fetch_all_pairs.assert_called_once_with(limit, page)

    @pytest.mark.asyncio
    async def test_fetch_new_listing_pairs(self, mock_client):
        """Test fetching new listing pairs."""
        # Setup mock response
        mock_pairs = self.create_mock_pair_data()
        mock_client.api.fetch_new_listing_pairs.return_value = mock_pairs

        # Test parameters
        limit = 10
        page = 1

        # Execute the function
        result = await mock_client.fetch_new_listing_pairs(limit, page)

        # Verify the result
        assert isinstance(result, PairData)
        assert result == mock_pairs

        # Verify the API method was called with correct parameters
        mock_client.api.fetch_new_listing_pairs.assert_called_once_with(limit, page)

    @pytest.mark.asyncio
    async def test_fetch_pair_info(self, mock_client):
        """Test fetching specific pair information."""
        # Setup mock response
        mock_pair = Pair(
            base="0xBaseToken",
            quote="0xQuoteToken",
            volume24h="1000000",
            priceChange24h="5.5",
            lastPrice="100.0",
        )
        mock_client.api.fetch_pair_info.return_value = mock_pair

        # Test parameters
        base = "0xBaseToken"
        quote = "0xQuoteToken"

        # Execute the function
        result = await mock_client.fetch_pair_info(base, quote)

        # Verify the result
        assert isinstance(result, Pair)
        assert result == mock_pair

        # Verify the API method was called with correct parameters
        mock_client.api.fetch_pair_info.assert_called_once_with(base, quote)

    @pytest.mark.asyncio
    async def test_fetch_top_gainer_pairs(self, mock_client):
        """Test fetching top gainer pairs."""
        # Setup mock response
        mock_pairs = self.create_mock_pair_data()
        mock_client.api.fetch_top_gainer_pairs.return_value = mock_pairs

        # Test parameters
        limit = 10
        page = 1

        # Execute the function
        result = await mock_client.fetch_top_gainer_pairs(limit, page)

        # Verify the result
        assert isinstance(result, PairData)
        assert result == mock_pairs

        # Verify the API method was called with correct parameters
        mock_client.api.fetch_top_gainer_pairs.assert_called_once_with(limit, page)

    @pytest.mark.asyncio
    async def test_fetch_top_loser_pairs(self, mock_client):
        """Test fetching top loser pairs."""
        # Setup mock response
        mock_pairs = self.create_mock_pair_data()
        mock_client.api.fetch_top_loser_pairs.return_value = mock_pairs

        # Test parameters
        limit = 10
        page = 1

        # Execute the function
        result = await mock_client.fetch_top_loser_pairs(limit, page)

        # Verify the result
        assert isinstance(result, PairData)
        assert result == mock_pairs

        # Verify the API method was called with correct parameters
        mock_client.api.fetch_top_loser_pairs.assert_called_once_with(limit, page)

    @pytest.mark.asyncio
    async def test_fetch_all_tokens(self, mock_client):
        """Test fetching all tokens."""
        # Setup mock response
        mock_tokens = self.create_mock_token_data()
        mock_client.api.fetch_all_tokens.return_value = mock_tokens

        # Test parameters
        limit = 10
        page = 1

        # Execute the function
        result = await mock_client.fetch_all_tokens(limit, page)

        # Verify the result
        assert isinstance(result, TokenData)
        assert result == mock_tokens

        # Verify the API method was called with correct parameters
        mock_client.api.fetch_all_tokens.assert_called_once_with(limit, page)

    @pytest.mark.asyncio
    async def test_fetch_new_listing_tokens(self, mock_client):
        """Test fetching new listing tokens."""
        # Setup mock response
        mock_tokens = self.create_mock_token_data()
        mock_client.api.fetch_new_listing_tokens.return_value = mock_tokens

        # Test parameters
        limit = 10
        page = 1

        # Execute the function
        result = await mock_client.fetch_new_listing_tokens(limit, page)

        # Verify the result
        assert isinstance(result, TokenData)
        assert result == mock_tokens

        # Verify the API method was called with correct parameters
        mock_client.api.fetch_new_listing_tokens.assert_called_once_with(limit, page)

    @pytest.mark.asyncio
    async def test_fetch_token_info(self, mock_client):
        """Test fetching specific token information."""
        # Setup mock response
        mock_token = TokenInfo(
            address="0xToken123",
            symbol="TEST",
            name="Test Token",
            decimals=18,
            price="1.50",
        )
        mock_client.api.fetch_token_info.return_value = mock_token

        # Test parameters
        address = "0xToken123"

        # Execute the function
        result = await mock_client.fetch_token_info(address)

        # Verify the result
        assert isinstance(result, TokenInfo)
        assert result == mock_token

        # Verify the API method was called with correct parameters
        mock_client.api.fetch_token_info.assert_called_once_with(address)

    @pytest.mark.asyncio
    async def test_fetch_account_trade_history_paginated_with_limit(self, mock_client):
        """Test fetching paginated account trade history."""
        # Setup mock response
        mock_history = AccountTradeHistory(trades=[], total=0, page=1, limit=10)
        api_method = mock_client.api.fetch_account_trade_history_paginated_with_limit
        api_method.return_value = mock_history

        # Test parameters
        address = "0xTestAddress"
        limit = 10
        page = 1

        # Execute the function
        result = await mock_client.fetch_account_trade_history_paginated_with_limit(
            address, limit, page
        )

        # Verify the result
        assert isinstance(result, AccountTradeHistory)
        assert result == mock_history

        # Verify the API method was called with correct parameters
        api_method = mock_client.api.fetch_account_trade_history_paginated_with_limit
        api_method.assert_called_once_with(address, limit, page)

    @pytest.mark.asyncio
    async def test_fetch_recent_overall_trades_paginated(self, mock_client):
        """Test fetching recent overall trades."""
        # Setup mock response
        mock_trades = TradesData(trades=[], total=0, page=1, limit=10)
        mock_client.api.fetch_recent_overall_trades_paginated.return_value = mock_trades

        # Test parameters
        limit = 10
        page = 1

        # Execute the function
        result = await mock_client.fetch_recent_overall_trades_paginated(limit, page)

        # Verify the result
        assert isinstance(result, TradesData)
        assert result == mock_trades

        # Verify the API method was called with correct parameters
        mock_client.api.fetch_recent_overall_trades_paginated.assert_called_once_with(
            limit, page
        )

    @pytest.mark.asyncio
    async def test_fetch_recent_pair_trades_paginated(self, mock_client):
        """Test fetching recent trades for a specific pair."""
        # Setup mock response
        mock_trades = TradesData(trades=[], total=0, page=1, limit=10)
        mock_client.api.fetch_recent_pair_trades_paginated.return_value = mock_trades

        # Test parameters
        base = "0xBaseToken"
        quote = "0xQuoteToken"
        limit = 10
        page = 1

        # Execute the function
        result = await mock_client.fetch_recent_pair_trades_paginated(
            base, quote, limit, page
        )

        # Verify the result
        assert isinstance(result, TradesData)
        assert result == mock_trades

        # Verify the API method was called with correct parameters
        mock_client.api.fetch_recent_pair_trades_paginated.assert_called_once_with(
            base, quote, limit, page
        )

    @pytest.mark.asyncio
    async def test_api_error_handling(self, mock_client):
        """Test API error handling."""
        # Mock an API function to raise an exception
        mock_client.api.fetch_orderbook.side_effect = Exception("API error")

        # Test that the exception is properly propagated
        with pytest.raises(Exception, match="API error"):
            await mock_client.fetch_orderbook("0xBase", "0xQuote")

    @pytest.mark.parametrize(
        "api_function,params,expected_type",
        [
            ("fetch_all_pairs", [10, 1], PairData),
            ("fetch_new_listing_pairs", [10, 1], PairData),
            ("fetch_top_gainer_pairs", [10, 1], PairData),
            ("fetch_top_loser_pairs", [10, 1], PairData),
            ("fetch_all_tokens", [10, 1], TokenData),
            ("fetch_new_listing_tokens", [10, 1], TokenData),
            ("fetch_recent_overall_trades_paginated", [10, 1], TradesData),
        ],
    )
    @pytest.mark.asyncio
    async def test_paginated_api_functions(
        self, mock_client, api_function, params, expected_type
    ):
        """Test paginated API functions with parameterized test data."""
        # Setup mock response based on expected type
        if expected_type == PairData:
            mock_response = self.create_mock_pair_data()
        elif expected_type == TokenData:
            mock_response = self.create_mock_token_data()
        elif expected_type == TradesData:
            mock_response = TradesData(trades=[], total=0, page=1, limit=10)
        else:
            mock_response = MagicMock()

        # Setup mock
        api_mock = getattr(mock_client.api, api_function)
        api_mock.return_value = mock_response

        # Get the function from the client
        func = getattr(mock_client, api_function)

        # Execute the function with the provided parameters
        result = await func(*params)

        # Verify the result type
        assert isinstance(result, expected_type)
        assert result == mock_response

        # Verify the API method was called
        api_mock.assert_called_once_with(*params)

    @pytest.mark.asyncio
    async def test_concurrent_api_calls(self, mock_client):
        """Test that multiple API calls can be executed concurrently."""
        import asyncio

        # Setup mock responses
        mock_client.api.fetch_all_pairs.return_value = self.create_mock_pair_data()
        mock_client.api.fetch_all_tokens.return_value = self.create_mock_token_data()
        mock_client.api.fetch_orderbook.return_value = self.create_mock_orderbook()

        # Define multiple API operations
        operations = [
            mock_client.fetch_all_pairs(10, 1),
            mock_client.fetch_all_tokens(10, 1),
            mock_client.fetch_orderbook("0xBase", "0xQuote"),
        ]

        # Execute all operations concurrently
        results = await asyncio.gather(*operations)

        # Verify all operations completed successfully
        assert len(results) == 3
        assert isinstance(results[0], PairData)
        assert isinstance(results[1], TokenData)
        assert isinstance(results[2], Orderbook)

    @pytest.mark.asyncio
    async def test_missing_api_methods_coverage(self, mock_client):
        """Test that all expected API methods are available on the client."""
        expected_api_methods = [
            "fetch_orderbook",
            "fetch_account_order_history_paginated_with_limit",
            "fetch_account_orders_paginated_with_limit",
            "fetch_all_pairs",
            "fetch_new_listing_pairs",
            "fetch_pair_info",
            "fetch_top_gainer_pairs",
            "fetch_top_loser_pairs",
            "fetch_all_tokens",
            "fetch_new_listing_tokens",
            "fetch_top_gainer_tokens",
            "fetch_top_loser_tokens",
            "fetch_token_info",
            "fetch_account_trade_history_paginated_with_limit",
            "fetch_recent_overall_trades_paginated",
            "fetch_recent_pair_trades_paginated",
        ]

        for method_name in expected_api_methods:
            assert hasattr(
                mock_client, method_name
            ), f"Missing API method: {method_name}"
            assert callable(
                getattr(mock_client, method_name)
            ), f"API method not callable: {method_name}"

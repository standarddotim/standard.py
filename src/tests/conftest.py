"""
Shared test fixtures and configuration for StandardWeb3 tests.

This module provides common fixtures, test utilities, and configuration
that can be shared across all test modules.
"""

import os
import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from dotenv import load_dotenv
from standardweb3 import StandardClient
from standardweb3.types.orderbook import Orderbook
from standardweb3.types.orderhistory import AccountOrderHistory
from standardweb3.types.order import AccountOrders
from standardweb3.types.pair import Pair, PairData
from standardweb3.types.token import TokenData, TokenInfo
from standardweb3.types.tradehistory import AccountTradeHistory
from standardweb3.types.trade import TradesData

# Load environment variables for testing
load_dotenv()


@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration constants."""
    return {
        "test_private_key": "0x" + "1" * 64,
        "test_rpc_url": "https://test-rpc.example.com",
        "test_matching_engine": "0x1234567890123456789012345678901234567890",
        "test_api_url": "https://test-api.example.com",
        "test_websocket_url": "wss://test-ws.example.com",
        "test_address": "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
        "base_token": "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
        "quote_token": "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
    }


@pytest.fixture
def mock_contract_functions():
    """Mock ContractFunctions for testing."""
    with patch("standardweb3.contract.ContractFunctions") as mock:
        # Mock basic attributes
        mock.return_value.w3 = MagicMock()
        mock.return_value.address = "0xtest_address"
        mock.return_value.account = MagicMock()

        # Mock async trading methods
        mock.return_value.market_buy = AsyncMock(return_value="0xmarket_buy_hash")
        mock.return_value.market_sell = AsyncMock(return_value="0xmarket_sell_hash")
        mock.return_value.limit_buy = AsyncMock(return_value="0xlimit_buy_hash")
        mock.return_value.limit_sell = AsyncMock(return_value="0xlimit_sell_hash")

        yield mock


@pytest.fixture
def mock_api_functions():
    """Mock APIFunctions for testing."""
    with patch("standardweb3.api.query.APIFunctions") as mock:
        # Mock all API methods
        mock.return_value.fetch_orderbook = AsyncMock()
        mock.return_value.fetch_account_order_history_paginated_with_limit = AsyncMock()
        mock.return_value.fetch_account_orders_paginated_with_limit = AsyncMock()
        mock.return_value.fetch_all_pairs = AsyncMock()
        mock.return_value.fetch_new_listing_pairs = AsyncMock()
        mock.return_value.fetch_pair_info = AsyncMock()
        mock.return_value.fetch_top_gainer_pairs = AsyncMock()
        mock.return_value.fetch_top_loser_pairs = AsyncMock()
        mock.return_value.fetch_all_tokens = AsyncMock()
        mock.return_value.fetch_new_listing_tokens = AsyncMock()
        mock.return_value.fetch_top_gainer_tokens = AsyncMock()
        mock.return_value.fetch_top_loser_tokens = AsyncMock()
        mock.return_value.fetch_token_info = AsyncMock()
        mock.return_value.fetch_account_trade_history_paginated_with_limit = AsyncMock()
        mock.return_value.fetch_recent_overall_trades_paginated = AsyncMock()
        mock.return_value.fetch_recent_pair_trades_paginated = AsyncMock()

        yield mock


@pytest.fixture
def mock_websocket_functions():
    """Mock WebsocketFunctions for testing."""
    with patch("standardweb3.ws.WebsocketFunctions") as mock:
        # Mock WebSocket methods
        mock.return_value.start_ws = AsyncMock()
        mock.return_value.close_ws = AsyncMock()
        mock.return_value.subscribe = AsyncMock()
        mock.return_value.unsubscribe = AsyncMock()
        mock.return_value.is_connected = MagicMock(return_value=False)

        yield mock


@pytest_asyncio.fixture
async def basic_client(test_config, mock_contract_functions):
    """Create a basic mocked StandardClient for testing."""
    client = StandardClient(
        private_key=test_config["test_private_key"],
        http_rpc_url=test_config["test_rpc_url"],
        matching_engine_address=test_config["test_matching_engine"],
    )
    return client


@pytest_asyncio.fixture
async def full_client(
    test_config, mock_contract_functions, mock_api_functions, mock_websocket_functions
):
    """Create a fully mocked StandardClient with all components."""
    client = StandardClient(
        private_key=test_config["test_private_key"],
        http_rpc_url=test_config["test_rpc_url"],
        matching_engine_address=test_config["test_matching_engine"],
        api_url=test_config["test_api_url"],
        websocket_url=test_config["test_websocket_url"],
    )
    return client


@pytest.fixture
def mock_orderbook_data():
    """Provide mock orderbook data."""
    from standardweb3.types.orderbook import Tick

    return Orderbook(
        orderbook="test_orderbook",
        mktPrice=100.0,
        bidHead=99.0,
        askHead=101.0,
        bids=[
            Tick(
                id="bid1", orderbook="test_orderbook", price=99.0, amount=8.0, count=1
            ),
            Tick(
                id="bid2", orderbook="test_orderbook", price=98.0, amount=12.0, count=1
            ),
        ],
        asks=[
            Tick(
                id="ask1", orderbook="test_orderbook", price=101.0, amount=10.0, count=1
            ),
            Tick(
                id="ask2", orderbook="test_orderbook", price=102.0, amount=5.0, count=1
            ),
        ],
        lastUpdated=1640995200.0,
    )


@pytest.fixture
def mock_pair_data():
    """Provide mock pair data."""
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


@pytest.fixture
def mock_token_data():
    """Provide mock token data."""
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


@pytest.fixture
def mock_account_orders():
    """Provide mock account orders data."""
    from standardweb3.types.token import Token
    from standardweb3.types.order import Order

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

    order = Order(
        id="order_1",
        isBid=1,
        orderId=123,
        base=base_token,
        quote=quote_token,
        symbol="BASE/QUOTE",
        orderbook="test_orderbook",
        price=99.0,
        amount=100.0,
        placed=1640995200.0,
        timestamp=1640995200.0,
        account="0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
        txHash="0x1234567890123456789012345678901234567890123456789012345678901234",
    )

    return AccountOrders(
        orders=[order],
        totalCount=1,
        totalPages=1,
        pageSize=10,
        lastUpdated=1640995200.0,
    )


@pytest.fixture
def mock_account_order_history():
    """Provide mock account order history data."""
    from standardweb3.types.token import Token
    from standardweb3.types.orderhistory import OrderHistory

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

    order_history = OrderHistory(
        id="order_history_1",
        orderId=123,
        isBid=0,
        base=base_token,
        quote=quote_token,
        symbol="BASE/QUOTE",
        orderbook="test_orderbook",
        price=100.0,
        amount=50.0,
        timestamp=1640995200.0,
        account="0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
        txHash="0x1234567890123456789012345678901234567890123456789012345678901234",
    )

    return AccountOrderHistory(
        orderHistory=[order_history],
        totalCount=1,
        totalPages=1,
        pageSize=10,
        lastUpdated=1640995200.0,
    )


@pytest.fixture
def mock_trade_history():
    """Provide mock trade history data."""
    from standardweb3.types.token import Token
    from standardweb3.types.tradehistory import TradeHistory

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

    trade_history = TradeHistory(
        id="trade_1",
        orderId=123,
        isBid=1,
        base=base_token,
        quote=quote_token,
        symbol="BASE/QUOTE",
        orderbook="test_orderbook",
        price=99.5,
        amount=25.0,
        timestamp=1640995200.0,
        maker="0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
        taker="0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
        account="0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
        txHash="0x1234567890123456789012345678901234567890123456789012345678901234",
    )

    return AccountTradeHistory(
        tradeHistory=[trade_history],
        totalCount=1,
        totalPages=1,
        pageSize=10,
        lastUpdated=1640995200.0,
    )


@pytest.fixture
def mock_trades_data():
    """Provide mock trades data."""
    from standardweb3.types.token import Token
    from standardweb3.types.trade import Trade

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

    trade1 = Trade(
        id="trade_1",
        orderbook="test_orderbook",
        orderId=123,
        base=base_token,
        quote=quote_token,
        symbol="BASE/QUOTE",
        isBid=1,
        price=100.0,
        baseAmount=10.0,
        quoteAmount=1000.0,
        timestamp=1640995200.0,
        taker="0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
        maker="0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
        txHash="0x1234567890123456789012345678901234567890123456789012345678901234",
    )

    trade2 = Trade(
        id="trade_2",
        orderbook="test_orderbook",
        orderId=124,
        base=base_token,
        quote=quote_token,
        symbol="BASE/QUOTE",
        isBid=0,
        price=100.5,
        baseAmount=5.0,
        quoteAmount=502.5,
        timestamp=1640995260.0,
        taker="0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
        maker="0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087",
        txHash="0x5678901234567890123456789012345678901234567890123456789012345678",
    )

    return TradesData(
        trades=[trade1, trade2],
        totalCount=2,
        totalPages=1,
        pageSize=10,
        lastUpdated=1640995200.0,
    )


@pytest.fixture
def mock_pair_info():
    """Provide mock pair info data."""
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

    return Pair(
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


@pytest.fixture
def mock_token_info():
    """Provide mock token info data."""
    from standardweb3.types.token import TokenBucket

    mock_bucket = TokenBucket(
        id="bucket_1",
        index=1,
        token="test_token_1",
        open=1.40,
        high=1.60,
        low=1.30,
        close=1.50,
        average=1.45,
        difference=0.10,
        differencePercentage=7.1,
        tvl=75000.0,
        tvlUSD=75000.0,
        volume=15000.0,
        volumeUSD=15000.0,
        count=100,
        timestamp=1640995200.0,
    )

    return TokenInfo(
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
        latestMinBucket=mock_bucket,
        latestHourBucket=mock_bucket,
        latestDayBucket=mock_bucket,
        latestWeekBucket=mock_bucket,
        latestMonthBucket=mock_bucket,
    )


@pytest.fixture
def environment_variables():
    """Provide access to environment variables for testing."""
    return {
        "private_key": os.environ.get("PRIVATE_KEY"),
        "rpc_url": os.environ.get("RPC_URL"),
        "api_key": os.environ.get("API_KEY"),
        "address": os.environ.get("ADDRESS"),
    }


@pytest.fixture(scope="session")
def network_configs():
    """Provide network configuration data."""
    return {
        "somnia_testnet": {
            "name": "Somnia Testnet",
            "matching_engine": "0x4Ca2C768773F6E0e9255da5B4e21ED9BA282B85e",
            "api_url": "https://story-odyssey-ponder.standardweb3.com",
            "websocket_url": "wss://story-odyssey-websocket.standardweb3.com",
        },
        "mode_mainnet": {
            "name": "Mode Mainnet",
            "matching_engine": "0x240aA2c15fBf6F65882A847462b04d5DA51A37Df",
            "api_url": None,  # Not configured
            "websocket_url": None,  # Not configured
        },
    }


@pytest.fixture
def trading_parameters():
    """Provide common trading parameters for testing."""
    return {
        "market_buy": {
            "base": "0xBaseToken",
            "quote": "0xQuoteToken",
            "quote_amount": 1000,
            "is_maker": False,
            "n": 1,
            "recipient": "0xRecipient",
            "slippage_limit": 50,
        },
        "market_sell": {
            "base": "0xBaseToken",
            "quote": "0xQuoteToken",
            "base_amount": 500,
            "is_maker": False,
            "n": 1,
            "recipient": "0xRecipient",
            "slippage_limit": 75,
        },
        "limit_buy": {
            "base": "0xBaseToken",
            "quote": "0xQuoteToken",
            "price": 2000,
            "quote_amount": 1000,
            "is_maker": True,
            "n": 1,
            "recipient": "0xRecipient",
        },
        "limit_sell": {
            "base": "0xBaseToken",
            "quote": "0xQuoteToken",
            "price": 1800,
            "base_amount": 500,
            "is_maker": True,
            "n": 1,
            "recipient": "0xRecipient",
        },
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "network: mark test as requiring network access")


# Custom pytest options
def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="run integration tests",
    )
    parser.addoption(
        "--run-slow", action="store_true", default=False, help="run slow tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on command line options."""
    if not config.getoption("--run-integration"):
        # Skip integration tests unless explicitly requested
        skip_integration = pytest.mark.skip(
            reason="need --run-integration option to run"
        )
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)

    if not config.getoption("--run-slow"):
        # Skip slow tests unless explicitly requested
        skip_slow = pytest.mark.skip(reason="need --run-slow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)


# Helper functions for tests
def assert_transaction_hash(tx_hash):
    """Assert that a transaction hash is valid."""
    assert isinstance(tx_hash, str)
    assert tx_hash.startswith("0x")
    assert len(tx_hash) == 66  # 0x + 64 hex characters


def assert_ethereum_address(address):
    """Assert that an Ethereum address is valid."""
    assert isinstance(address, str)
    assert address.startswith("0x")
    assert len(address) == 42  # 0x + 40 hex characters


def assert_positive_number(value, field_name="value"):
    """Assert that a value is a positive number."""
    try:
        num_value = float(value)
        assert num_value > 0, f"{field_name} must be positive, got {value}"
    except (ValueError, TypeError):
        pytest.fail(f"{field_name} must be a valid number, got {value}")


# Test utilities
class TestDataFactory:
    """Factory for creating test data objects."""

    @staticmethod
    def create_orderbook(asks=None, bids=None):
        """Create a test orderbook."""
        if asks is None:
            asks = [["100.0", "10.0"], ["101.0", "5.0"]]
        if bids is None:
            bids = [["99.0", "8.0"], ["98.0", "12.0"]]

        return Orderbook(asks=asks, bids=bids, timestamp="2024-01-01T00:00:00Z")

    @staticmethod
    def create_pair_data(pairs_count=1):
        """Create test pair data."""
        pairs = []
        for i in range(pairs_count):
            pairs.append(
                {
                    "base": f"0xBase{i}",
                    "quote": f"0xQuote{i}",
                    "volume24h": str(1000000 * (i + 1)),
                    "priceChange24h": str(5.5 + i),
                    "lastPrice": str(100.0 + i),
                }
            )

        return PairData(pairs=pairs, total=pairs_count, page=1, limit=10)

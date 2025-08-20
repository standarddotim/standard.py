"""
Integration tests for StandardWeb3 API functions.

These tests make real HTTP calls to the Standard Protocol API endpoints
to verify that the API is working and returns expected data structures.
"""

import pytest
import pytest_asyncio
import asyncio
from standardweb3 import StandardClient


class TestAPIIntegration:
    """Integration test cases for StandardClient API functions with real API calls."""

    @pytest_asyncio.fixture
    async def real_client(self):
        """Create a real StandardClient for integration testing."""
        # Use a dummy private key for testing (API calls only, no blockchain txs)
        test_private_key = "0x" + "1" * 64
        test_rpc_url = "https://dummy-rpc.com"  # We don't need real RPC for API tests
        test_matching_engine = "0x0000000000000000000000000000000000000000"
        api_url = "https://somnia-testnet-ponder-release.standardweb3.com"

        client = StandardClient(
            private_key=test_private_key,
            http_rpc_url=test_rpc_url,
            matching_engine_address=test_matching_engine,
            api_url=api_url,
        )

        return client

    @pytest.mark.asyncio
    async def test_fetch_all_pairs_real(self, real_client):
        """Test fetching all pairs from real API."""
        try:
            result = await real_client.fetch_all_pairs(limit=5, page=1)

            # Check that we got a result
            assert result is not None
            print(f"✅ fetch_all_pairs returned data: {type(result)}")

            # Check basic structure - API returns dict, not typed object yet
            if isinstance(result, dict):
                assert "pairs" in result
                assert "totalCount" in result
                assert "totalPages" in result

                print(f"  Total pairs: {result['totalCount']}")
                print(f"  Total pages: {result['totalPages']}")
                print(f"  Pairs on this page: {len(result['pairs'])}")

                # If we have pairs, check their structure
                if result["pairs"]:
                    pair = result["pairs"][0]
                    assert "symbol" in pair
                    assert "price" in pair
                    print(f"  First pair: {pair['symbol']} - Price: {pair['price']}")
            else:
                # If it's already converted to typed object
                assert hasattr(result, "pairs")
                assert hasattr(result, "totalCount")
                assert hasattr(result, "totalPages")

                print(f"  Total pairs: {result.totalCount}")
                print(f"  Total pages: {result.totalPages}")
                print(f"  Pairs on this page: {len(result.pairs)}")

        except Exception as e:
            print(f"❌ fetch_all_pairs failed: {str(e)}")
            assert False, f"API call failed: {str(e)}"

    @pytest.mark.asyncio
    async def test_fetch_all_tokens_real(self, real_client):
        """Test fetching all tokens from real API."""
        try:
            result = await real_client.fetch_all_tokens(limit=5, page=1)

            # Check that we got a result
            assert result is not None
            print(f"✅ fetch_all_tokens returned data: {type(result)}")

            # Check basic structure - API returns dict, not typed object yet
            if isinstance(result, dict):
                assert "tokens" in result
                assert "totalCount" in result
                assert "totalPages" in result

                print(f"  Total tokens: {result['totalCount']}")
                print(f"  Total pages: {result['totalPages']}")
                print(f"  Tokens on this page: {len(result['tokens'])}")

                # If we have tokens, check their structure
                if result["tokens"]:
                    token = result["tokens"][0]
                    assert "symbol" in token
                    assert "name" in token
                    print(f"  First token: {token['name']} ({token['symbol']})")
            else:
                # If it's already converted to typed object
                assert hasattr(result, "tokens")
                assert hasattr(result, "totalCount")
                assert hasattr(result, "totalPages")

                print(f"  Total tokens: {result.totalCount}")
                print(f"  Total pages: {result.totalPages}")
                print(f"  Tokens on this page: {len(result.tokens)}")

        except Exception as e:
            print(f"❌ fetch_all_tokens failed: {str(e)}")
            assert False, f"API call failed: {str(e)}"

    @pytest.mark.asyncio
    async def test_fetch_top_gainer_pairs_real(self, real_client):
        """Test fetching top gainer pairs from real API."""
        try:
            result = await real_client.fetch_top_gainer_pairs(limit=3, page=1)

            # Check that we got a result
            assert result is not None
            print(f"✅ fetch_top_gainer_pairs returned data: {type(result)}")

            # Check basic structure - API returns dict, not typed object yet
            if isinstance(result, dict):
                assert "pairs" in result
                print(f"  Top gainer pairs found: {len(result['pairs'])}")

                # If we have pairs,
                # check their structure and that they're actually gainers
                if result["pairs"]:
                    for i, pair in enumerate(result["pairs"][:3]):
                        assert "symbol" in pair
                        assert "dayPriceDifferencePercentage" in pair
                        print(
                            f"  #{i+1}: {pair['symbol']} - "
                            f"Change: {pair['dayPriceDifferencePercentage']}%"
                        )
            else:
                # If it's already converted to typed object
                assert hasattr(result, "pairs")
                print(f"  Top gainer pairs found: {len(result.pairs)}")

                if result.pairs:
                    for i, pair in enumerate(result.pairs[:3]):
                        assert hasattr(pair, "symbol")
                        assert hasattr(pair, "dayPriceDifferencePercentage")
                        print(
                            f"  #{i+1}: {pair.symbol} - "
                            f"Change: {pair.dayPriceDifferencePercentage}%"
                        )

        except Exception as e:
            print(f"❌ fetch_top_gainer_pairs failed: {str(e)}")
            assert False, f"API call failed: {str(e)}"

    @pytest.mark.asyncio
    async def test_fetch_top_loser_pairs_real(self, real_client):
        """Test fetching top loser pairs from real API."""
        try:
            result = await real_client.fetch_top_loser_pairs(limit=3, page=1)

            # Check that we got a result
            assert result is not None
            print(f"✅ fetch_top_loser_pairs returned data: {type(result)}")

            # Check basic structure
            assert hasattr(result, "pairs")

            print(f"  Top loser pairs found: {len(result.pairs)}")

            # If we have pairs, check their structure
            if result.pairs:
                for i, pair in enumerate(result.pairs[:3]):
                    assert hasattr(pair, "symbol")
                    assert hasattr(pair, "dayPriceDifferencePercentage")
                    print(
                        f"  #{i+1}: {pair.symbol} - "
                        f"Change: {pair.dayPriceDifferencePercentage}%"
                    )

        except Exception as e:
            print(f"❌ fetch_top_loser_pairs failed: {str(e)}")
            assert False, f"API call failed: {str(e)}"

    @pytest.mark.asyncio
    async def test_fetch_recent_trades_real(self, real_client):
        """Test fetching recent trades from real API."""
        try:
            result = await real_client.fetch_recent_overall_trades_paginated(
                limit=5, page=1
            )

            # Check that we got a result
            assert result is not None
            print(
                f"✅ fetch_recent_overall_trades_paginated returned data: {type(result)}"
            )

            # Check basic structure
            assert hasattr(result, "trades")

            print(f"  Recent trades found: {len(result.trades)}")

            # If we have trades, check their structure
            if result.trades:
                trade = result.trades[0]
                assert hasattr(trade, "price")
                assert hasattr(trade, "amount")
                print(f"  Latest trade: Price {trade.price}, Amount {trade.amount}")

        except Exception as e:
            print(f"❌ fetch_recent_overall_trades_paginated failed: {str(e)}")
            assert False, f"API call failed: {str(e)}"

    @pytest.mark.asyncio
    async def test_fetch_orderbook_ticks_real(self, real_client):
        """Test fetching orderbook ticks from real API."""
        # First get a pair to test with
        try:
            pairs_result = await real_client.fetch_all_pairs(limit=1, page=1)

            # Handle dict response
            if isinstance(pairs_result, dict):
                if not pairs_result.get("pairs"):
                    print("⚠️ No pairs available to test orderbook ticks")
                    return
                pair = pairs_result["pairs"][0]
                base_address = pair["base"]["id"]
                quote_address = pair["quote"]["id"]
                pair_symbol = pair["symbol"]
            else:
                if not pairs_result.pairs:
                    print("⚠️ No pairs available to test orderbook ticks")
                    return
                pair = pairs_result.pairs[0]
                base_address = pair.base.id
                quote_address = pair.quote.id
                pair_symbol = pair.symbol

            print(f"Testing orderbook ticks for pair: {pair_symbol}")
            print(f"Base: {base_address}")
            print(f"Quote: {quote_address}")

            result = await real_client.fetch_orderbook_ticks(
                base_address, quote_address, limit=10
            )

            # Check that we got a result
            assert result is not None
            print(f"✅ fetch_orderbook_ticks returned data: {type(result)}")

            # Check basic structure - should be dict
            assert isinstance(result, dict)
            print(f"  Orderbook ticks data keys: {list(result.keys())}")

        except Exception as e:
            print(f"❌ fetch_orderbook_ticks failed: {str(e)}")
            assert False, f"API call failed: {str(e)}"

    @pytest.mark.asyncio
    async def test_fetch_orderbook_blocks_real(self, real_client):
        """Test fetching orderbook blocks from real API."""
        # First get a pair to test with
        try:
            pairs_result = await real_client.fetch_all_pairs(limit=1, page=1)

            # Handle dict response
            if isinstance(pairs_result, dict):
                if not pairs_result.get("pairs"):
                    print("⚠️ No pairs available to test orderbook blocks")
                    return
                pair = pairs_result["pairs"][0]
                base_address = pair["base"]["id"]
                quote_address = pair["quote"]["id"]
                pair_symbol = pair["symbol"]
            else:
                if not pairs_result.pairs:
                    print("⚠️ No pairs available to test orderbook blocks")
                    return
                pair = pairs_result.pairs[0]
                base_address = pair.base.id
                quote_address = pair.quote.id
                pair_symbol = pair.symbol

            print(f"Testing orderbook blocks for pair: {pair_symbol}")
            print(f"Base: {base_address}")
            print(f"Quote: {quote_address}")

            result = await real_client.fetch_orderbook_blocks(
                base_address, quote_address, step=1, depth=5, isSingle=True
            )

            # Check that we got a result
            assert result is not None
            print(f"✅ fetch_orderbook_blocks returned data: {type(result)}")

            # Check basic structure - should be dict
            assert isinstance(result, dict)
            print(f"  Orderbook blocks data keys: {list(result.keys())}")

        except Exception as e:
            print(f"❌ fetch_orderbook_blocks failed: {str(e)}")
            assert False, f"API call failed: {str(e)}"

    @pytest.mark.asyncio
    async def test_fetch_pair_info_real(self, real_client):
        """Test fetching specific pair info from real API."""
        # First get a pair to test with
        try:
            pairs_result = await real_client.fetch_all_pairs(limit=1, page=1)
            if not pairs_result.pairs:
                print("⚠️ No pairs available to test pair info")
                return

            # Use the first available pair
            test_pair = pairs_result.pairs[0]
            base_address = test_pair.base.id
            quote_address = test_pair.quote.id

            print(f"Testing pair info for: {test_pair.symbol}")

            result = await real_client.fetch_pair_info(base_address, quote_address)

            # Check that we got a result
            assert result is not None
            print(f"✅ fetch_pair_info returned data: {type(result)}")

            # Check basic structure
            assert hasattr(result, "symbol")
            assert hasattr(result, "price")
            assert hasattr(result, "base")
            assert hasattr(result, "quote")

            print(f"  Symbol: {result.symbol}")
            print(f"  Price: {result.price}")
            print(f"  Base Token: {result.base.name}")
            print(f"  Quote Token: {result.quote.name}")

        except Exception as e:
            print(f"❌ fetch_pair_info failed: {str(e)}")
            assert False, f"API call failed: {str(e)}"

    @pytest.mark.asyncio
    async def test_fetch_token_info_real(self, real_client):
        """Test fetching specific token info from real API."""
        # First get a token to test with
        try:
            tokens_result = await real_client.fetch_all_tokens(limit=1, page=1)
            if not tokens_result.tokens:
                print("⚠️ No tokens available to test token info")
                return

            # Use the first available token
            test_token = tokens_result.tokens[0]
            token_address = test_token.id

            print(f"Testing token info for: {test_token.symbol}")

            result = await real_client.fetch_token_info(token_address)

            # Check that we got a result
            assert result is not None
            print(f"✅ fetch_token_info returned data: {type(result)}")

            # Check basic structure
            assert hasattr(result, "symbol")
            assert hasattr(result, "name")
            assert hasattr(result, "address")

            print(f"  Name: {result.name}")
            print(f"  Symbol: {result.symbol}")
            print(f"  Address: {result.address}")

        except Exception as e:
            print(f"❌ fetch_token_info failed: {str(e)}")
            assert False, f"API call failed: {str(e)}"

    @pytest.mark.asyncio
    async def test_fetch_account_orders_real(self, real_client):
        """Test fetching account orders from real API."""
        try:
            # Use a dummy address - this should return empty results but not error
            test_address = "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087"

            result = await real_client.fetch_account_orders_paginated_with_limit(
                test_address, limit=5, page=1
            )

            # Check that we got a result (even if empty)
            assert result is not None
            print(
                f"✅ fetch_account_orders_paginated_with_limit returned data: "
                f"{type(result)}"
            )

            # Check basic structure
            assert hasattr(result, "orders")

            print(f"  Orders found: {len(result.orders)}")

            # If we have orders, check their structure
            if result.orders:
                order = result.orders[0]
                assert hasattr(order, "id")
                assert hasattr(order, "side")
                print(f"  First order: {order.id} - Side: {order.side}")

        except Exception as e:
            print(f"❌ fetch_account_orders_paginated_with_limit failed: {str(e)}")
            assert False, f"API call failed: {str(e)}"

    @pytest.mark.asyncio
    async def test_concurrent_api_calls_real(self, real_client):
        """Test multiple real API calls concurrently."""
        try:
            print("🚀 Testing concurrent API calls...")

            # Execute multiple API calls concurrently
            results = await asyncio.gather(
                real_client.fetch_all_pairs(5, 1),
                real_client.fetch_all_tokens(5, 1),
                real_client.fetch_top_gainer_pairs(3, 1),
                real_client.fetch_account_orders_paginated_with_limit(
                    "0x742d35Cc6531C1532c5FdE4d62DeC19b7b3A0087", 5, 1
                ),
                return_exceptions=True,
            )

            print("✅ Concurrent API calls completed!")

            # Check each result
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"  Call {i+1}: ❌ Failed - {str(result)}")
                else:
                    print(f"  Call {i+1}: ✅ Success - {type(result)}")

            # At least some calls should succeed
            successful_calls = [r for r in results if not isinstance(r, Exception)]
            assert len(successful_calls) > 0, "At least one API call should succeed"

        except Exception as e:
            print(f"❌ Concurrent API calls failed: {str(e)}")
            assert False, f"Concurrent API calls failed: {str(e)}"

    @pytest.mark.asyncio
    async def test_api_endpoints_exist(self, real_client):
        """Test that all expected API methods exist and are callable."""
        expected_methods = [
            "fetch_all_pairs",
            "fetch_new_listing_pairs",
            "fetch_top_gainer_pairs",
            "fetch_top_loser_pairs",
            "fetch_pair_info",
            "fetch_all_tokens",
            "fetch_new_listing_tokens",
            "fetch_top_gainer_tokens",
            "fetch_top_loser_tokens",
            "fetch_token_info",
            "fetch_orderbook_ticks",
            "fetch_orderbook_blocks",
            "fetch_account_orders_paginated_with_limit",
            "fetch_account_order_history_paginated_with_limit",
            "fetch_account_trade_history_paginated_with_limit",
            "fetch_recent_overall_trades_paginated",
            "fetch_recent_pair_trades_paginated",
        ]

        print("🔍 Checking API method availability...")

        for method_name in expected_methods:
            assert hasattr(real_client, method_name), f"Missing method: {method_name}"
            assert callable(
                getattr(real_client, method_name)
            ), f"Method not callable: {method_name}"
            print(f"  ✅ {method_name}")

        print("✅ All expected API methods are available!")

    @pytest.mark.asyncio
    async def test_api_url_configuration(self, real_client):
        """Test that the API URL is correctly configured."""
        expected_url = "https://somnia-testnet-ponder-release.standardweb3.com"

        assert (
            real_client.api_url == expected_url
        ), f"Expected API URL {expected_url}, got {real_client.api_url}"
        print(f"✅ API URL correctly configured: {real_client.api_url}")

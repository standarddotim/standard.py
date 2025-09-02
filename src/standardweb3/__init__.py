"""
StandardWeb3 Client Library.

A comprehensive Python library for interacting with the Standard Protocol
exchange, providing contract functions, API queries, and WebSocket support.
"""

from standardweb3.consts import (
    matching_engine_addresses,
    api_urls,
    websocket_urls,
)
from standardweb3.abis.matching_engine import matching_engine_abi
from standardweb3.contract import ContractFunctions
from standardweb3.api.query import APIFunctions
from standardweb3.ws import WebsocketFunctions


class StandardClient:
    """Standard Protocol Web3 client for trading and data access."""

    def __init__(
        self,
        private_key: str,
        http_rpc_url: str,
        matching_engine_address: str,
        networkName: str = None,
        api_url: str = None,
        websocket_url: str = None,
        api_key: str = "defaultApiKey",
    ) -> None:
        """
        Initialize the StandardClient.

        Args:
            private_key: Private key for signing transactions
            http_rpc_url: RPC endpoint URL
            networkName: Network name (e.g., "Somnia Testnet")
            api_url: Custom API URL (optional)
            websocket_url: Custom WebSocket URL (optional)
            matching_engine_address: Custom matching engine address (optional)
            api_key: API key for authentication
        """
        # Set default network if not provided
        if networkName is not None:
            if networkName not in matching_engine_addresses:
                raise ValueError(
                    f"Invalid Network Name: Network name {networkName} is not supported"
                )
            else:
                self.matching_engine_address = matching_engine_addresses[networkName]
            if networkName not in api_urls:
                raise ValueError(
                    f"Invalid Network Name: Network name {networkName} is not supported"
                )
            else:
                self.api_url = api_urls[networkName]
            if networkName not in websocket_urls:
                raise ValueError(
                    f"Invalid Network Name: Network name {networkName} is not supported"
                )
            else:
                self.websocket_url = websocket_urls[networkName]

        self.api_url = api_url
        self.websocket_url = websocket_url
        self.matching_engine_address = matching_engine_address

        # Initialize contract functions
        self.contract = ContractFunctions(
            http_rpc_url,
            private_key,
            self.matching_engine_address,
            matching_engine_abi,
        )

        # Expose commonly used attributes from contract
        self.w3 = self.contract.w3
        self.address = self.contract.address
        self.account = self.contract.account

        # Initialize api functions
        self.api = APIFunctions(self.api_url, api_key)

        # Initialize websocket functions
        self.ws = WebsocketFunctions(None, self.websocket_url)

    #########################################################

    # Contract functions
    async def market_buy(
        self, base, quote, quote_amount, is_maker, n, recipient, slippageLimit
    ) -> str:
        """Execute a market buy order."""
        return await self.contract.market_buy(
            base, quote, quote_amount, is_maker, n, recipient, slippageLimit
        )

    async def market_sell(
        self, base, quote, base_amount, is_maker, n, recipient, slippageLimit
    ) -> str:
        """Execute a market sell order."""
        return await self.contract.market_sell(
            base, quote, base_amount, is_maker, n, recipient, slippageLimit
        )

    async def limit_buy(
        self, base, quote, price, quote_amount, is_maker, n, recipient
    ) -> str:
        """Execute a limit buy order."""
        return await self.contract.limit_buy(
            base, quote, price, quote_amount, is_maker, n, recipient
        )

    async def limit_sell(
        self, base, quote, price, base_amount, is_maker, n, recipient
    ) -> str:
        """Execute a limit sell order."""
        return await self.contract.limit_sell(
            base, quote, price, base_amount, is_maker, n, recipient
        )

    async def cancel_orders(self, cancel_order_data: list) -> str:
        """Cancel multiple orders."""
        return await self.contract.cancel_orders(cancel_order_data)

    #########################################################

    # API functions
    async def fetch_orderbook_ticks(self, base: str, quote: str, limit: int) -> dict:
        """Fetch orderbook ticks for a trading pair."""
        return await self.api.fetch_orderbook_ticks(base, quote, limit)

    async def fetch_orderbook_blocks(
        self, base: str, quote: str, step: int, depth: int, isSingle: bool
    ) -> dict:
        """Fetch orderbook blocks for a trading pair."""
        return await self.api.fetch_orderbook_blocks(base, quote, step, depth, isSingle)

    async def fetch_account_order_history_paginated_with_limit(
        self, address: str, limit: int, page: int
    ) -> dict:
        """Fetch paginated order history for an account."""
        return await self.api.fetch_account_order_history_paginated_with_limit(
            address, limit, page
        )

    async def fetch_account_orders_paginated_with_limit(
        self, address: str, limit: int, page: int
    ) -> dict:
        """Fetch paginated active orders for an account."""
        return await self.api.fetch_account_orders_paginated_with_limit(
            address, limit, page
        )

    async def fetch_all_pairs(self, limit: int, page: int) -> dict:
        """Fetch all trading pairs."""
        return await self.api.fetch_all_pairs(limit, page)

    async def fetch_new_listing_pairs(self, limit: int, page: int) -> dict:
        """Fetch newly listed trading pairs."""
        return await self.api.fetch_new_listing_pairs(limit, page)

    async def fetch_pair_info(self, base: str, quote: str) -> dict:
        """Fetch information for a specific trading pair."""
        return await self.api.fetch_pair_info(base, quote)

    async def fetch_top_gainer_pairs(self, limit: int, page: int) -> dict:
        """Fetch top gaining trading pairs."""
        return await self.api.fetch_top_gainer_pairs(limit, page)

    async def fetch_top_loser_pairs(self, limit: int, page: int) -> dict:
        """Fetch top losing trading pairs."""
        return await self.api.fetch_top_loser_pairs(limit, page)

    async def fetch_all_tokens(self, limit: int, page: int) -> dict:
        """Fetch all available tokens."""
        return await self.api.fetch_all_tokens(limit, page)

    async def fetch_new_listing_tokens(self, limit: int, page: int) -> dict:
        """Fetch newly listed tokens."""
        return await self.api.fetch_new_listing_tokens(limit, page)

    async def fetch_top_gainer_tokens(self, limit: int, page: int) -> dict:
        """Fetch top gaining tokens."""
        return await self.api.fetch_top_gainer_tokens(limit, page)

    async def fetch_top_loser_tokens(self, limit: int, page: int) -> dict:
        """Fetch top losing tokens."""
        return await self.api.fetch_top_loser_tokens(limit, page)

    async def fetch_token_info(self, address: str) -> dict:
        """Fetch information for a specific token."""
        return await self.api.fetch_token_info(address)

    async def fetch_account_trade_history_paginated_with_limit(
        self, address: str, limit: int, page: int
    ) -> dict:
        """Fetch paginated trade history for an account."""
        return await self.api.fetch_account_trade_history_paginated_with_limit(
            address, limit, page
        )

    async def fetch_recent_overall_trades_paginated(
        self, limit: int, page: int
    ) -> dict:
        """Fetch recent trades across all pairs."""
        return await self.api.fetch_recent_overall_trades_paginated(limit, page)

    async def fetch_recent_pair_trades_paginated(
        self, base: str, quote: str, limit: int, page: int
    ) -> dict:
        """Fetch recent trades for a specific pair."""
        return await self.api.fetch_recent_pair_trades_paginated(
            base, quote, limit, page
        )

    #########################################################

    # Websocket functions
    async def start_ws(self):
        """Start the WebSocket connection."""
        await self.ws.start_ws()

    #########################################################

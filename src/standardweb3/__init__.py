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

        # Initialize api functions
        self.api = APIFunctions(self.api_url, api_key)

        # Initialize websocket functions
        self.ws = WebsocketFunctions(None, self.websocket_url)

        # Initialize token data (will be loaded lazily)
        try:
            token_data = self.api.fetch_all_tokens_sync(100, 1)
            self._tokens = token_data.get("tokens", []) if token_data else []
        except Exception as e:
            print(f"Warning: Could not fetch tokens during initialization: {e}")
            self._tokens = []

        # get token info in dict
        self._token_info = {}
        for token in self._tokens:
            self._token_info[token["id"]] = token

        # Initialize pair data (will be loaded lazily)
        try:
            pair_data = self.api.fetch_all_pairs_sync(100, 1)
            self._pairs = pair_data.get("pairs", []) if pair_data else []
        except Exception as e:
            print(f"Warning: Could not fetch pairs during initialization: {e}")
            self._pairs = []

        # get base and quote from pairs
        self._base_quote = {}
        for pair in self._pairs:
            base_id = pair["base"]["id"]
            quote_id = pair["quote"]["id"]
            self._base_quote[pair["id"]] = {"base": base_id, "quote": quote_id}

        # Initialize contract functions
        self.contract = ContractFunctions(
            http_rpc_url,
            private_key,
            self.matching_engine_address,
            matching_engine_abi,
            base_quote=self._base_quote,
        )

        # Expose commonly used attributes from contract
        self.w3 = self.contract.w3
        self.address = self.contract.address
        self.account = self.contract.account

    @property
    def pairs(self):
        """Get the loaded pairs."""
        return self._pairs

    @property
    def tokens(self):
        """Get the loaded tokens."""
        return self._tokens

    @property
    def base_quote(self):
        """Get the loaded base and quote."""
        return self._base_quote

    @property
    def token_info(self):
        """Get the loaded token info."""
        return self._token_info

    #########################################################

    # Contract functions
    async def market_buy(
        self, base, quote, quote_amount, is_maker, n, recipient, slippageLimit
    ) -> str:
        """Execute a market buy order.

        Args:
            base: Base token address
            quote: Quote token address
            quote_amount: Amount of quote token to spend in decimals,
            the amount is parsed to quote's decimals from token_info
            is_maker: Whether this is a maker order
            n: Number of matches
            recipient: Recipient address
            slippageLimit: Slippage limit (in percentage) (e.g. 0.1%)

        """
        # parse slippageLimit percentage to 8 decimals (1% -> 1000000)
        slippageLimit = slippageLimit * 10**6
        # parse quote_amount to quote's decimals from token_info
        quote_amount = quote_amount * 10 ** self.token_info[quote]["decimals"]
        return await self.contract.market_buy(
            base, quote, quote_amount, is_maker, n, recipient, slippageLimit
        )

    async def market_sell(
        self, base, quote, base_amount, is_maker, n, recipient, slippageLimit
    ) -> str:
        """Execute a market sell order.

        Args:
            base: Base token address
            quote: Quote token address
            base_amount: Amount of base token to sell in decimals,
            the amount is parsed to base's decimals from token_info
            is_maker: Whether this is a maker order
            n: Number of matches
            recipient: Recipient address
            slippageLimit: Slippage limit (in percentage) (e.g. 0.1%)
        """
        # parse slippageLimit percentage to 8 decimals (1% -> 1000000)
        slippageLimit = slippageLimit * 10**6
        # parse base_amount to base's decimals from token_info
        base_amount = base_amount * 10 ** self.token_info[base]["decimals"]

        return await self.contract.market_sell(
            base, quote, base_amount, is_maker, n, recipient, slippageLimit
        )

    async def limit_buy(
        self, base, quote, price, quote_amount, is_maker, n, recipient
    ) -> str:
        """Execute a limit buy order.

        Args:
            base: Base token address
            quote: Quote token address
            price: Price per unit (in wei)
            quote_amount: Amount of quote token to spend in decimals,
            the amount is parsed to quote's decimals from token_info
            is_maker: Whether this is a maker order
            n: Number of matches
            recipient: Recipient address
        """
        # parse price to 8 decimals
        price = price * 10**8
        # parse quote_amount to quote's decimals from token_info
        quote_amount = quote_amount * 10 ** self.token_info[quote]["decimals"]

        return await self.contract.limit_buy(
            base, quote, price, quote_amount, is_maker, n, recipient
        )

    async def limit_sell(
        self, base, quote, price, base_amount, is_maker, n, recipient
    ) -> str:
        """Execute a limit sell order.

        Args:
            base: Base token address
            quote: Quote token address
            price: Price per unit (in wei)
            base_amount: Amount of base token to sell in decimals,
            the amount is parsed to base's decimals from token_info
            is_maker: Whether this is a maker order
            n: Number of matches
            recipient: Recipient address
        """
        # parse price to 8 decimals
        price = price * 10**8
        # parse base_amount to base's decimals from token_info
        base_amount = base_amount * 10 ** self.token_info[base]["decimals"]

        return await self.contract.limit_sell(
            base, quote, price, base_amount, is_maker, n, recipient
        )

    async def create_orders(self, create_order_data: list) -> dict:
        """Create multiple orders.

        Args:
            create_order_data: List of dictionaries containing the order data.
            Each dictionary should contain:
                - base: address of base token
                - quote: address of quote token
                - isBid: bool, True for buy orders, False for sell orders
                - isLimit: bool, True for limit orders, False for market orders
                - orderId: int, order ID (optional, defaults to 0)
                - price: int, price in wei
                - amount: int, amount in wei
                - n: int, number parameter
                - recipient: address of recipient
                - isETH: bool, True for ETH orders, False for token orders
        """
        # parse price to 8 decimals
        for order in create_order_data:
            order["price"] = order["price"] * 10**8
        # parse amount to amount's decimals from token_info
        for order in create_order_data:
            order["amount"] = (
                order["amount"] * 10 ** self.token_info[order["base"]]["decimals"]
            )

        return await self.contract.create_orders(create_order_data)

    async def update_orders(self, update_order_data: list) -> dict:
        """Update multiple orders.

        Args:
            update_order_data: List of dictionaries containing the order data.
            Each dictionary should contain:
                - base: address of base token
                - quote: address of quote token
                - isBid: bool, True for buy orders, False for sell orders
                - isLimit: bool, True for limit orders, False for market orders
                - orderId: int, order ID (required for updates)
                - price: int, price in wei
                - amount: int, amount in wei
                - n: int, number parameter
                - recipient: address of recipient
                - isETH: bool, True for ETH orders, False for token orders
        """
        # parse price to 8 decimals
        for order in update_order_data:
            order["price"] = order["price"] * 10**8
        # parse amount to amount's decimals from token_info
        for order in update_order_data:
            order["amount"] = (
                order["amount"] * 10 ** self.token_info[order["base"]]["decimals"]
            )

        return await self.contract.update_orders(update_order_data)

    async def cancel_orders(self, cancel_order_data: list) -> str:
        """Cancel multiple orders.

        Args:
            cancel_order_data: List of order IDs to cancel.
            each order id is a string containing the base, quote, isBid, and orderId
            e.g. "0x..._0x..._True_12345"
        """
        return await self.contract.cancel_orders(cancel_order_data)

    # ETH-specific trading functions
    async def limit_buy_eth(self, base, price, is_maker, n, recipient, eth_amount):
        """Execute a limit buy order using ETH as quote token.

        Args:
            base: Base token address
            price: Price per unit (in wei)
            is_maker: Whether this is a maker order
            n: Number of matches
            recipient: Recipient address
            eth_amount: Amount of ETH to spend in decimals,
            the amount is parsed to ETH's decimals from token_info
        """
        # parse price to 8 decimals
        price = price * 10**8
        # parse eth_amount to 18 decimals
        eth_amount = eth_amount * 10**18
        return await self.contract.limit_buy_eth(
            base, price, is_maker, n, recipient, eth_amount
        )

    async def limit_sell_eth(self, quote, price, is_maker, n, recipient, eth_amount):
        """Execute a limit sell order selling ETH for quote tokens.

        Args:
            quote: Quote token address
            price: Price per unit (in wei)
            is_maker: Whether this is a maker order
            n: Number of matches
            recipient: Recipient address
            eth_amount: Amount of ETH to sell in decimals,
            the amount is parsed to ETH's decimals from token_info
        """
        # parse price to 8 decimals
        price = price * 10**8
        # parse eth_amount to 18 decimals
        eth_amount = eth_amount * 10**18
        return await self.contract.limit_sell_eth(
            quote, price, is_maker, n, recipient, eth_amount
        )

    async def market_buy_eth(
        self, base, is_maker, n, recipient, slippage_limit, eth_amount
    ):
        """Execute a market buy order using ETH as quote token.

        Args:
            base: Base token address
            is_maker: Whether this is a maker order
            n: Number of matches
            recipient: Recipient address
            slippage_limit: Slippage limit (in percentage) (e.g. 0.1%)
            eth_amount: Amount of ETH to spend in decimals,
            the amount is parsed to ETH's decimals from token_info
        """
        # parse slippage_limit percentage to 8 decimals (1% -> 1000000)
        slippage_limit = slippage_limit * 10**6
        # parse eth_amount to 18 decimals
        eth_amount = eth_amount * 10**18
        return await self.contract.market_buy_eth(
            base, is_maker, n, recipient, slippage_limit, eth_amount
        )

    async def market_sell_eth(
        self, quote, is_maker, n, recipient, slippage_limit, eth_amount
    ):
        """Execute a market sell order selling ETH for quote tokens.

        Args:
            quote: Quote token address
            is_maker: Whether this is a maker order
            n: Number of matches
            recipient: Recipient address
            slippage_limit: Slippage limit (in percentage) (e.g. 0.1%)
            eth_amount: Amount of ETH to sell in decimals,
            the amount is parsed to ETH's decimals from token_info
        """
        # parse slippage_limit percentage to 8 decimals (1% -> 1000000)
        slippage_limit = slippage_limit * 10**6
        # parse eth_amount to 18 decimals
        eth_amount = eth_amount * 10**18
        return await self.contract.market_sell_eth(
            quote, is_maker, n, recipient, slippage_limit, eth_amount
        )

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

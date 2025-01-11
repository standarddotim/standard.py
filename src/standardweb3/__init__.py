from standardweb3.consts import matching_engine_addresses, ponder_urls, websocket_urls
from standardweb3.abis.matching_engine import matching_engine_abi
from standardweb3.contract import ContractFunctions
from standardweb3.api import APIFunctions
from web3 import Web3
from eth_account import Account
import socketio
from standardweb3.types.orderbook import Orderbook
from standardweb3.types.orderhistory import AccountOrderHistory
from standardweb3.types.order import AccountOrders
from standardweb3.types.pair import Pair, PairData
from standardweb3.types.token import TokenData, TokenInfo
from standardweb3.types.tradehistory import AccountTradeHistory
from standardweb3.types.trade import TradesData
from typing import Callable, Dict


class StandardClient:
    def __init__(
        self,
        private_key: str,
        http_rpc_url: str,
        networkName: str = "Story Odyssey Testnet",
        api_key: str = "defaultApiKey",
    ) -> None:
        self.provider = Web3.HTTPProvider(http_rpc_url)
        self.w3 = Web3(self.provider)

        # Derive the Ethereum address from the private key
        self.account = Account.from_key(private_key)

        # Unlock account with private key
        self.w3.eth.default_account = self.w3.eth.account.from_key(private_key)

        # matching engine address
        self.matching_engine = matching_engine_addresses[networkName]

        self.contract = ContractFunctions(
            self.w3,
            private_key,
            self.account.address,
            self.matching_engine,
            matching_engine_abi,
        )

        self.api = APIFunctions(ponder_urls[networkName], api_key)

        # setup socket io client for making bots
        self.sio = socketio.AsyncClient()
        # Indexer link to fetch data
        self.indexer = ponder_urls[networkName]
        # Websocket link to listen to events
        self.server_url = websocket_urls[networkName]
        self.event_handlers: Dict[str, Callable] = {}

        @self.sio.event
        def connect():
            print("Connected to the server")

        @self.sio.event
        def disconnect():
            print("Disconnected from the server")

    # Web3 functions
    def get_contract(self, contract_address, contract_abi):
        return self.contract.get_contract(contract_address, contract_abi)

    def sign_tx(self, tx):
        signed_tx = self.contract.sign_tx(tx)
        return signed_tx

    def send_tx(self, signed_tx):
        tx_hash = self.contract.send_tx(signed_tx)
        return tx_hash

    def wait_for_tx_receipt(self, tx_hash):
        tx_receipt = self.contract.wait_for_tx_receipt(tx_hash)
        return tx_receipt

    # Contract functions
    async def market_buy(
        self, base, quote, quote_amount, is_maker, n, uid, recipient
    ) -> str:
        return await self.contract.market_buy(
            base, quote, quote_amount, is_maker, n, uid, recipient
        )

    async def market_sell(
        self, base, quote, base_amount, is_maker, n, uid, recipient
    ) -> str:
        return await self.contract.market_sell(
            base, quote, base_amount, is_maker, n, uid, recipient
        )

    async def limit_buy(
        self, base, quote, price, quote_amount, is_maker, n, uid, recipient
    ) -> str:
        return await self.contract.limit_buy(
            base, quote, price, quote_amount, is_maker, n, uid, recipient
        )

    async def limit_sell(
        self, base, quote, price, base_amount, is_maker, n, uid, recipient
    ) -> str:
        return await self.contract.limit_sell(
            base, quote, price, base_amount, is_maker, n, uid, recipient
        )

    # API functions
    async def fetch_orderbook(self, base: str, quote: str) -> Orderbook:
        return await self.api.fetch_orderbook(base, quote)

    async def fetch_account_order_history_paginated_with_limit(
        self, address: str, limit: int, page: int
    ) -> AccountOrderHistory:
        return await self.api.fetch_account_order_history_paginated_with_limit(
            address, limit, page
        )

    async def fetch_account_orders_paginated_with_limit(
        self, address: str, limit: int, page: int
    ) -> AccountOrders:
        return await self.api.fetch_account_orders_paginated_with_limit(
            address, limit, page
        )

    async def fetch_all_pairs(self, limit: int, page: int) -> PairData:
        return await self.api.fetch_all_pairs(limit, page)

    async def fetch_new_listing_pairs(self, limit: int, page: int) -> PairData:
        return await self.api.fetch_new_listing_pairs(limit, page)

    async def fetch_pair_info(self, base: str, quote: str) -> Pair:
        return await self.api.fetch_pair_info(base, quote)

    async def fetch_top_gainer_pairs(self, limit: int, page: int) -> PairData:
        return await self.api.fetch_top_gainer_pairs(limit, page)

    async def fetch_top_loser_pairs(self, limit: int, page: int) -> PairData:
        return await self.api.fetch_top_loser_pairs(limit, page)

    async def fetch_all_tokens(self, limit: int, page: int) -> TokenData:
        return await self.api.fetch_all_tokens(limit, page)

    async def fetch_new_listing_tokens(self, limit: int, page: int) -> TokenData:
        return await self.api.fetch_new_listing_tokens(limit, page)

    async def fetch_top_gainer_tokens(self, limit: int, page: int) -> TokenData:
        return await self.api.fetch_top_gainer_tokens(limit, page)

    async def fetch_top_loser_tokens(self, limit: int, page: int) -> TokenData:
        return await self.api.fetch_top_loser_tokens(limit, page)

    async def fetch_token_info(self, address: str) -> TokenInfo:
        return await self.api.fetch_token_info(address)

    async def fetch_account_trade_history_paginated_with_limit(
        self, address: str, limit: int, page: int
    ) -> AccountTradeHistory:
        return await self.api.fetch_account_trade_history_paginated_with_limit(
            address, limit, page
        )

    async def fetch_recent_overall_trades_paginated(
        self, limit: int, page: int
    ) -> TradesData:
        return await self.api.fetch_recent_overall_trades_paginated(limit, page)

    async def fetch_recent_pair_trades_paginated(
        self, base: str, quote: str, limit: int, page: int
    ) -> TradesData:
        return await self.api.fetch_recent_pair_trades_paginated(
            base, quote, limit, page
        )

    def on(self, event: str):
        def decorator(func: Callable):
            self.event_handlers[event] = func
            self.sio.on(event, func)
            return func

        return decorator

    async def run(self):
        self.sio.connect(self.server_url)
        self.sio.wait()

import aiohttp
import os, time
import web3
from standardweb3.types.orderbook import Orderbook, Tick
from standardweb3.types.orderhistory import AccountOrderHistory, OrderHistory
from standardweb3.types.order import AccountOrders, Order
from standardweb3.types.pair import Pair, PairData
from standardweb3.types.token import Token, TokenData, TokenInfo, TokenBucket
from standardweb3.types.tradehistory import AccountTradeHistory, TradeHistory
from standardweb3.types.trade import Trade, TradesData


class APIFunctions:
    def __init__(self, ponder_url: str, api_key: str):
        self.ponder_url = ponder_url
        self.api_key = api_key

    # register an API key
    def register_api_key(self, api_key: str) -> None:
        pass

    def get_address(self, address: str) -> str:
        # Implement the address encoding logic here
        return web3.Web3.to_checksum_address(address)

    async def fetch_orderbook(self, base: str, quote: str) -> Orderbook:
        encoded_base = self.get_address(base)
        encoded_quote = self.get_address(quote)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/orderbook/{encoded_base}/{encoded_quote}/100",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                bid_head = data["bids"][0]["price"] if data["bids"] else None
                ask_head = data["asks"][0]["price"] if data["asks"] else None

                return Orderbook(
                    orderbook=data["id"],
                    mktPrice=data["mktPrice"],
                    bidHead=bid_head,
                    askHead=ask_head,
                    bids=[Tick(**bid) for bid in data["bids"]],
                    asks=[Tick(**ask) for ask in data["asks"]],
                    lastUpdated=int(time.time() * 1000),
                )

    async def fetch_account_order_history_paginated_with_limit(
        self, address: str, limit: int, page: int
    ) -> AccountOrderHistory:
        encoded = self.get_address(address)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/orderhistory/{encoded}/{limit}/{page}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                return AccountOrderHistory(
                    orderHistory=[
                        OrderHistory(**orderHistoryItem)
                        for orderHistoryItem in data["orderHistory"]
                    ],
                    totalCount=data["totalCount"],
                    totalPages=data["totalPages"],
                    pageSize=data["pageSize"],
                    lastUpdated=int(time.time() * 1000),
                )

    async def fetch_account_orders_paginated_with_limit(
        self, address: str, limit: int, page: int
    ) -> AccountOrders:
        encoded = self.get_address(address)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/orders/{encoded}/{limit}/{page}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                return AccountOrders(
                    orders=[Order(**order) for order in data["orders"]],
                    totalCount=data["totalCount"],
                    totalPages=data["totalPages"],
                    pageSize=data["pageSize"],
                    lastUpdated=int(time.time() * 1000),
                )

    async def fetch_all_pairs(self, limit: int, page: int) -> PairData:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/pairs/{limit}/{page}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                return PairData(
                    pairs=[Pair(**pair) for pair in data["pairs"]],
                    totalCount=data["totalCount"],
                    totalPages=data["totalPages"],
                    pageSize=data["pageSize"],
                )

    async def fetch_new_listing_pairs(self, limit: int, page: int) -> PairData:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/pairs/new/{limit}/{page}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                return PairData(
                    pairs=[Pair(**pair) for pair in data["pairs"]],
                    totalCount=data["totalCount"],
                    totalPages=data["totalPages"],
                    pageSize=data["pageSize"],
                )

    async def fetch_pair_info(self, base: str, quote: str) -> Pair:
        encoded_base = self.get_address(base)
        encoded_quote = self.get_address(quote)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/pair/{encoded_base}/{encoded_quote}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                return Pair(**data)

    async def fetch_top_gainer_pairs(self, limit: int, page: int) -> PairData:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/pairs/top-gainer/{limit}/{page}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                return PairData(
                    pairs=[Pair(**pair) for pair in data["pairs"]],
                    totalCount=data["totalCount"],
                    totalPages=data["totalPages"],
                    pageSize=data["pageSize"],
                )

    async def fetch_top_loser_pairs(self, limit: int, page: int) -> PairData:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/pairs/top-loser/{limit}/{page}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                return PairData(
                    pairs=[Pair(**pair) for pair in data["pairs"]],
                    totalCount=data["totalCount"],
                    totalPages=data["totalPages"],
                    pageSize=data["pageSize"],
                )

    async def fetch_all_tokens(self, limit: int, page: int) -> TokenData:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/tokens/{limit}/{page}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                return TokenData(
                    tokens=[Token(**token) for token in data["tokens"]],
                    totalCount=data["totalCount"],
                    totalPages=data["totalPages"],
                    pageSize=data["pageSize"],
                )

    async def fetch_new_listing_tokens(self, limit: int, page: int) -> TokenData:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/tokens/new/{limit}/{page}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                return TokenData(
                    tokens=[Token(**token) for token in data["tokens"]],
                    totalCount=data["totalCount"],
                    totalPages=data["totalPages"],
                    pageSize=data["pageSize"],
                )

    async def fetch_top_gainer_tokens(self, limit: int, page: int) -> TokenData:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/tokens/top-gainer/{limit}/{page}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                return TokenData(
                    tokens=[Token(**token) for token in data["tokens"]],
                    totalCount=data["totalCount"],
                    totalPages=data["totalPages"],
                    pageSize=data["pageSize"],
                )

    async def fetch_top_loser_tokens(self, limit: int, page: int) -> TokenData:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/tokens/top-loser/{limit}/{page}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                return TokenData(
                    tokens=[Token(**token) for token in data["tokens"]],
                    totalCount=data["totalCount"],
                    totalPages=data["totalPages"],
                    pageSize=data["pageSize"],
                )

    async def fetch_token_info(self, address: str) -> TokenInfo:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/token/{address}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                return TokenInfo(
                    id=data["token"]["id"],
                    name=data["token"]["name"],
                    symbol=data["token"]["symbol"],
                    ticker=data["token"]["ticker"],
                    totalSupply=data["token"]["totalSupply"],
                    logoURI=data["token"]["logoURI"],
                    decimals=data["token"]["decimals"],
                    price=data["token"]["price"],
                    cpPrice=data["token"]["cpPrice"],
                    cgId=data["token"]["cgId"],
                    cmcId=data["token"]["cmcId"],
                    ath=data["token"]["ath"],
                    atl=data["token"]["atl"],
                    listingDate=data["token"]["listingDate"],
                    dayPriceDifference=data["token"]["dayPriceDifference"],
                    dayPriceDifferencePercentage=data["token"][
                        "dayPriceDifferencePercentage"
                    ],
                    dayTvl=data["token"]["dayTvl"],
                    dayTvlUSD=data["token"]["dayTvlUSD"],
                    dayVolume=data["token"]["dayVolume"],
                    dayVolumeUSD=data["token"]["dayVolumeUSD"],
                    creator=data["token"]["creator"],
                    totalMinBuckets=data["token"]["totalMinBuckets"],
                    totalHourBuckets=data["token"]["totalHourBuckets"],
                    totalDayBuckets=data["token"]["totalDayBuckets"],
                    totalWeekBuckets=data["token"]["totalWeekBuckets"],
                    totalMonthBuckets=data["token"]["totalMonthBuckets"],
                    latestMinBucket=TokenBucket(**data["latestMinBucket"]),
                    latestHourBucket=TokenBucket(**data["latestHourBucket"]),
                    latestDayBucket=TokenBucket(**data["latestDayBucket"]),
                    latestWeekBucket=TokenBucket(**data["latestWeekBucket"]),
                    latestMonthBucket=TokenBucket(**data["latestMonthBucket"]),
                )

    async def fetch_account_trade_history_paginated_with_limit(
        self, address: str, limit: int, page: int
    ) -> AccountTradeHistory:
        encoded = self.get_address(address)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/tradehistory/{encoded}/{limit}/{page}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                return AccountTradeHistory(
                    tradeHistory=[
                        TradeHistory(**trade) for trade in data["tradeHistory"]
                    ],
                    totalCount=data["totalCount"],
                    totalPages=data["totalPages"],
                    pageSize=data["pageSize"],
                    lastUpdated=int(time.time() * 1000),
                )

    async def fetch_recent_overall_trades_paginated(
        self, limit: int, page: int
    ) -> TradesData:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/trades/{limit}/{page}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                return TradesData(
                    trades=[Trade(**trade) for trade in data["trades"]],
                    totalCount=data["totalCount"],
                    totalPages=data["totalPages"],
                    pageSize=data["pageSize"],
                    lastUpdated=int(time.time() * 1000),
                )

    async def fetch_recent_pair_trades_paginated(
        self, base: str, quote: str, limit: int, page: int
    ) -> TradesData:
        encoded_base = self.get_address(base)
        encoded_quote = self.get_address(quote)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.ponder_url}/api/trades/{encoded_base}/{encoded_quote}/{limit}/{page}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            ) as response:

                if response.status == 427:
                    raise Exception("Rate limit exceeded")
                if response.status != 200:
                    raise Exception(f"HTTP error! status: {response.status}")

                data = await response.json()

                return TradesData(
                    trades=[Trade(**trade) for trade in data["trades"]],
                    totalCount=data["totalCount"],
                    totalPages=data["totalPages"],
                    pageSize=data["pageSize"],
                    lastUpdated=int(time.time() * 1000),
                )

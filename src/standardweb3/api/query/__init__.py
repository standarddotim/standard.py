"""
API Query Functions Module.

Provides async HTTP client functions for interacting with the Standard Protocol
API endpoints, including orderbook, orders, pairs, tokens, and trade data.
"""

import aiohttp
import http.client
import os
import web3


class APIFunctions:
    """API functions for Standard Protocol HTTP endpoints."""

    def __init__(self, api_url: str, api_key: str):
        """
        Initialize API functions.

        Args:
            api_url: Base URL for the API
            api_key: API key for authentication
        """
        self.api_url = api_url
        self.api_key = api_key

    def register_api_key(self, api_key: str) -> None:
        """Register an API key."""
        pass

    def get_address(self, address: str) -> str:
        """Convert address to checksum format."""
        return web3.Web3.to_checksum_address(address)

    async def fetch_orderbook_ticks(self, base: str, quote: str, limit: int) -> dict:
        """Fetch orderbook for a trading pair."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/orderbook/ticks/{base}/{quote}/{limit}",
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

                return data

    async def fetch_orderbook_blocks(
        self, base: str, quote: str, step: int, depth: int, isSingle: bool
    ) -> dict:
        """Fetch orderbook blocks for a trading pair."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/orderbook/blocks/{base}/{quote}/{step}/"
                f"{depth}/{isSingle}",
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
                return data

    async def fetch_account_order_history_paginated_with_limit(
        self, address: str, limit: int, page: int
    ) -> dict:
        """Fetch paginated order history for an account."""
        encoded = self.get_address(address)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/orderhistory/{encoded}/{limit}/{page}",
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

                return data

    async def fetch_account_orders_paginated_with_limit(
        self, address: str, limit: int, page: int
    ) -> dict:
        """Fetch paginated active orders for an account."""
        encoded = self.get_address(address)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/orders/{encoded}/{limit}/{page}",
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

                return data

    def fetch_all_pairs_sync(self, limit: int, page: int) -> dict:
        """Fetch all trading pairs."""
        from urllib.parse import urlparse
        import json

        # Parse the URL to extract just the hostname
        parsed_url = urlparse(self.api_url)
        host = parsed_url.netloc

        connection = http.client.HTTPSConnection(host)
        try:
            connection.request(
                "GET",
                f"/api/pairs/{limit}/{page}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            )
            response = connection.getresponse()
            data = response.read().decode("utf-8")
            return json.loads(data)
        finally:
            connection.close()

    async def fetch_all_pairs(self, limit: int, page: int) -> dict:
        """Fetch all trading pairs."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/pairs/{limit}/{page}",
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

                return data

    async def fetch_new_listing_pairs(self, limit: int, page: int) -> dict:
        """Fetch newly listed trading pairs."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/pairs/new/{limit}/{page}",
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

                return data

    async def fetch_pair_info(self, base: str, quote: str) -> dict:
        """Fetch information for a specific trading pair."""
        encoded_base = self.get_address(base)
        encoded_quote = self.get_address(quote)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/pair/{encoded_base}/{encoded_quote}",
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

                return data

    async def fetch_top_gainer_pairs(self, limit: int, page: int) -> dict:
        """Fetch top gaining trading pairs."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/pairs/top-gainer/{limit}/{page}",
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

                return data

    async def fetch_top_loser_pairs(self, limit: int, page: int) -> dict:
        """Fetch top losing trading pairs."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/pairs/top-loser/{limit}/{page}",
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

                return data

    def fetch_all_tokens_sync(self, limit: int, page: int) -> dict:
        """Fetch all available tokens by symbol."""
        from urllib.parse import urlparse
        import json

        # Parse the URL to extract just the hostname
        parsed_url = urlparse(self.api_url)
        host = parsed_url.netloc

        connection = http.client.HTTPSConnection(host)
        try:
            connection.request(
                "GET",
                f"/api/tokens/{limit}/{page}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("ADMIN_API_KEY", ""),
                },
            )
            response = connection.getresponse()
            data = response.read().decode("utf-8")
            return json.loads(data)
        finally:
            connection.close()

    async def fetch_all_tokens(self, limit: int, page: int) -> dict:
        """Fetch all available tokens."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/tokens/{limit}/{page}",
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

                return data

    async def fetch_new_listing_tokens(self, limit: int, page: int) -> dict:
        """Fetch newly listed tokens."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/tokens/new/{limit}/{page}",
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

                return data

    async def fetch_top_gainer_tokens(self, limit: int, page: int) -> dict:
        """Fetch top gaining tokens."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/tokens/top-gainer/{limit}/{page}",
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

                return data

    async def fetch_top_loser_tokens(self, limit: int, page: int) -> dict:
        """Fetch top losing tokens."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/tokens/top-loser/{limit}/{page}",
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

                return data

    async def fetch_token_info(self, address: str) -> dict:
        """Fetch detailed information for a specific token."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/token/{address}",
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

                return data

    async def fetch_account_trade_history_paginated_with_limit(
        self, address: str, limit: int, page: int
    ) -> dict:
        """Fetch paginated trade history for an account."""
        encoded = self.get_address(address)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/tradehistory/{encoded}/{limit}/{page}",
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

                return data

    async def fetch_recent_overall_trades_paginated(
        self, limit: int, page: int
    ) -> dict:
        """Fetch recent trades across all pairs."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/trades/{limit}/{page}",
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

                return data

    async def fetch_recent_pair_trades_paginated(
        self, base: str, quote: str, limit: int, page: int
    ) -> dict:
        """Fetch recent trades for a specific pair."""
        encoded_base = self.get_address(base)
        encoded_quote = self.get_address(quote)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/trades/{encoded_base}/"
                f"{encoded_quote}/{limit}/{page}",
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

                return data

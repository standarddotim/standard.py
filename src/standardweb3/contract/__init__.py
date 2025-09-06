"""
Contract Functions Module.

Provides blockchain interaction functions for the Standard Protocol
matching engine contract, including transaction signing and execution.
"""

from web3 import Web3
from eth_account import Account
import asyncio


class ContractFunctions:
    """Contract interaction functions for Standard Protocol."""

    def __init__(
        self,
        http_rpc_url: str,
        private_key: str,
        matching_engine: str,
        matching_engine_abi: dict,
        base_quote: dict,
    ):
        """
        Initialize contract functions.

        Args:
            http_rpc_url: RPC endpoint URL
            private_key: Private key for signing transactions
            matching_engine: Matching engine contract address
            matching_engine_abi: Contract ABI
        """
        # check if the private key is valid
        if not Account.from_key(private_key):
            raise ValueError(f"Invalid private key: {private_key}")

        self.provider = Web3.HTTPProvider(http_rpc_url)
        self.w3 = Web3(self.provider)

        # Derive the Ethereum address from the private key
        self.account = Account.from_key(private_key)

        self.address = self.account.address

        # Unlock account with private key
        self.w3.eth.default_account = self.w3.eth.account.from_key(private_key)

        self.private_key = private_key
        self.matching_engine = matching_engine
        self.matching_engine_abi = matching_engine_abi
        self.base_quote = base_quote

    def get_contract(self, contract_address, contract_abi):
        """Get contract instance."""
        # checksum out of address
        contract_address = Web3.to_checksum_address(contract_address)
        return self.w3.eth.contract(address=contract_address, abi=contract_abi)

    def sign_tx(self, tx):
        """Sign a transaction with the private key."""
        signed_tx = self.w3.eth.account.sign_transaction(
            tx, private_key=self.private_key
        )
        return signed_tx

    def send_tx(self, signed_tx):
        """Send a signed transaction."""
        if not hasattr(signed_tx, "raw_transaction"):
            raise Exception("Invalid signed transaction - missing raw_transaction")
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return tx_hash

    def wait_for_tx_receipt(self, tx_hash):
        """Wait for transaction receipt."""
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    async def _execute_transaction(self, function_name: str, *args, **kwargs) -> dict:
        """Execute a contract transaction."""
        contract = self.get_contract(self.matching_engine, self.matching_engine_abi)

        # Extract eth_amount if provided (for ETH functions)
        eth_amount = kwargs.pop("eth_amount", 0)

        # Get the contract function and build transaction
        try:
            contract_function = getattr(contract.functions, function_name)
            function_call = contract_function(*args)

            # Build the transaction using the correct method name
            if hasattr(function_call, "build_transaction"):
                tx_params = {
                    "from": self.address,
                    "nonce": self.w3.eth.get_transaction_count(self.address),
                    "gas": 3000000,
                    "gasPrice": self.w3.to_wei(6, "gwei"),
                }

                # Add value for ETH transactions
                if eth_amount > 0:
                    tx_params["value"] = eth_amount

                tx = function_call.build_transaction(tx_params)
                signed_tx = self.sign_tx(tx)

                tx_hash = await asyncio.to_thread(self.send_tx, signed_tx)
                tx_receipt = await asyncio.to_thread(self.wait_for_tx_receipt, tx_hash)

                if tx_receipt.status == 0:
                    raise Exception("Transaction failed")

                # Decode events from successful transaction
                decoded_events = self._decode_function_decoded_logs(
                    contract, function_name, tx_receipt
                )

                order_infos = self._parse_decoded_logs(decoded_events)

                result = {
                    "tx_receipt": tx_receipt,
                    "tx_hash": tx_hash.hex(),
                    "decoded_logs": decoded_events,
                    "gas_used": tx_receipt.gasUsed,
                    "status": tx_receipt.status,
                }
                if len(order_infos) == 1:
                    result["order_info"] = order_infos[0]
                else:
                    result["order_infos"] = order_infos

                return result
            else:
                raise AttributeError(
                    "Function call object does not have build_transaction method"
                )

        except Exception as e:
            print(f"Error in contract function call: {e}")

    def _decode_function_decoded_logs(self, contract, function_name: str, tx_receipt):
        """
        Decode events from transaction receipt.

        This method attempts to decode events from the matching engine contract only.
        """
        decoded_logs = []
        matching_engine_address = Web3.to_checksum_address(self.matching_engine)

        for log in tx_receipt.logs:
            # Skip logs not from our matching engine contract
            if log.address.lower() != matching_engine_address.lower():
                continue

            # Try to decode known events
            events_to_try = [
                ("OrderPlaced", contract.events.OrderPlaced),
                ("OrderMatched", contract.events.OrderMatched),
                ("OrderCanceled", contract.events.OrderCanceled),
                ("NewMarketPrice", contract.events.NewMarketPrice),
                ("PairAdded", contract.events.PairAdded),
                ("ListingCostSet", contract.events.ListingCostSet),
                ("PairUpdated", contract.events.PairUpdated),
            ]

            for event_name, event_function in events_to_try:
                try:
                    decoded_log = event_function().process_log(log)
                    decoded_logs.append(
                        {
                            "event": event_name,
                            "args": dict(decoded_log["args"]),
                            "transaction_hash": tx_receipt.transactionHash.hex(),
                            "block_number": tx_receipt.blockNumber,
                        }
                    )
                    print(f"✅ Decoded {event_name}: {dict(decoded_log['args'])}")
                    break  # Successfully decoded, move to next log
                except Exception:
                    continue  # Try next event type
            else:
                # If no event matched, log the topic for debugging
                topic = log.topics[0].hex() if log.topics else "No topics"
                print(f"⚠️  Could not decode log with topic: {topic}")

        return decoded_logs if decoded_logs else None

    def _parse_decoded_logs(self, decoded_logs):
        """Parse decoded logs."""
        order_info = {}
        order_infos = []
        for log in decoded_logs:
            print(f"📊 Decoded {log['event']}: {log['args']}")
            if log["event"] == "OrderPlaced":
                print(f"      Order ID: {log['args']['id']}")
                print(f"      Price: {log['args']['price']}")
                print(f"      Amount Placed: {log['args']['placed']}")
                base = self.base_quote[log["args"]["pair"]]["base"]
                quote = self.base_quote[log["args"]["pair"]]["quote"]
                is_bid = log["args"]["isBid"]
                order_id = log["args"]["orderId"]
                order_info["id"] = f"{base}_{quote}_{is_bid}_{order_id}"
                order_info["price"] = log["args"]["price"]
                order_info["amount"] = log["args"]["placed"]
                # if there are multiple orders placed, add them to order_info
                order_infos.append(order_info)
                order_info = {}
            elif log["event"] == "OrderMatched":
                print(f"      Order ID: {log['args']['id']}")
                print(f"      Price: {log['args']['price']}")
                print(f"      Total: {log['args']['total']}")
            elif log["event"] == "OrderCanceled":
                print(f"      Order ID: {log['args']['id']}")
                print(f"      Price: {log['args']['price']}")
                print(f"      Amount Canceled: {log['args']['amount']}")
            elif log["event"] == "NewMarketPrice":
                print(f"      Price: {log['args']['price']}")
                # NewMarketPrice event has 'pair' instead of 'base' and 'quote'
                if "pair" in log["args"]:
                    print(f"      Pair: {log['args']['pair']}")
                base = self.base_quote[log["args"]["pair"]]["base"]
                quote = self.base_quote[log["args"]["pair"]]["quote"]
                print(f"      Base Token: {base}")
                print(f"      Quote Token: {quote}")
            elif log["event"] == "PairAdded":
                if "pair" in log["args"]:
                    print(f"      Pair Address: {log['args']['pair']}")
                if "base" in log["args"]:
                    print(f"      Base Token: {log['args']['base']}")
                if "quote" in log["args"]:
                    print(f"      Quote Token: {log['args']['quote']}")

        return order_infos[0] if len(order_infos) == 1 else order_infos

    async def market_buy(
        self, base, quote, quote_amount, is_maker, n, recipient, slippageLimit
    ) -> dict:
        """Execute a market buy order."""
        # Ensure proper types for contract call
        base = Web3.to_checksum_address(base)
        quote = Web3.to_checksum_address(quote)
        recipient = Web3.to_checksum_address(recipient)
        quote_amount = int(quote_amount)
        n = int(n)
        slippageLimit = int(slippageLimit)

        return await self._execute_transaction(
            "marketBuy",
            base,
            quote,
            quote_amount,
            is_maker,
            n,
            recipient,
            slippageLimit,
        )

    async def market_sell(
        self, base, quote, base_amount, is_maker, n, recipient, slippageLimit
    ) -> dict:
        """Execute a market sell order."""
        # Ensure proper types for contract call
        base = Web3.to_checksum_address(base)
        quote = Web3.to_checksum_address(quote)
        recipient = Web3.to_checksum_address(recipient)
        base_amount = int(base_amount)
        n = int(n)
        slippageLimit = int(slippageLimit)

        return await self._execute_transaction(
            "marketSell",
            base,
            quote,
            base_amount,
            is_maker,
            n,
            recipient,
            slippageLimit,
        )

    async def limit_buy(
        self, base, quote, price, quote_amount, is_maker, n, recipient
    ) -> dict:
        """Execute a limit buy order."""
        # Ensure proper types for contract call
        base = Web3.to_checksum_address(base)
        quote = Web3.to_checksum_address(quote)
        recipient = Web3.to_checksum_address(recipient)
        price = int(price)
        quote_amount = int(quote_amount)
        n = int(n)

        return await self._execute_transaction(
            "limitBuy",
            base,
            quote,
            price,
            quote_amount,
            is_maker,
            n,
            recipient,
        )

    async def limit_sell(
        self, base, quote, price, base_amount, is_maker, n, recipient
    ) -> dict:
        """Execute a limit sell order."""
        # Ensure proper types for contract call
        base = Web3.to_checksum_address(base)
        quote = Web3.to_checksum_address(quote)
        recipient = Web3.to_checksum_address(recipient)
        price = int(price)
        base_amount = int(base_amount)
        n = int(n)

        return await self._execute_transaction(
            "limitSell",
            base,
            quote,
            price,
            base_amount,
            is_maker,
            n,
            recipient,
        )

    async def limit_buy_eth(
        self, base, price, is_maker, n, recipient, eth_amount
    ) -> dict:
        """Execute a limit buy order using ETH as quote token."""
        # Ensure proper types for contract call
        base = Web3.to_checksum_address(base)
        recipient = Web3.to_checksum_address(recipient)
        price = int(price)
        n = int(n)
        eth_amount = int(eth_amount)

        return await self._execute_transaction(
            "limitBuyETH",
            base,
            price,
            is_maker,
            n,
            recipient,
            eth_amount=eth_amount,  # This will be sent as msg.value
        )

    async def limit_sell_eth(
        self, quote, price, is_maker, n, recipient, eth_amount
    ) -> dict:
        """Execute a limit sell order selling ETH for quote tokens."""
        # Ensure proper types for contract call
        quote = Web3.to_checksum_address(quote)
        recipient = Web3.to_checksum_address(recipient)
        price = int(price)
        n = int(n)
        eth_amount = int(eth_amount)

        return await self._execute_transaction(
            "limitSellETH",
            quote,
            price,
            is_maker,
            n,
            recipient,
            eth_amount=eth_amount,  # This will be sent as msg.value
        )

    async def market_buy_eth(
        self, base, is_maker, n, recipient, slippage_limit, eth_amount
    ) -> dict:
        """Execute a market buy order using ETH as quote token."""
        # Ensure proper types for contract call
        base = Web3.to_checksum_address(base)
        recipient = Web3.to_checksum_address(recipient)
        n = int(n)
        slippage_limit = int(slippage_limit)
        eth_amount = int(eth_amount)

        return await self._execute_transaction(
            "marketBuyETH",
            base,
            is_maker,
            n,
            recipient,
            slippage_limit,
            eth_amount=eth_amount,  # This will be sent as msg.value
        )

    async def market_sell_eth(
        self, quote, is_maker, n, recipient, slippage_limit, eth_amount
    ) -> dict:
        """Execute a market sell order selling ETH for quote tokens."""
        # Ensure proper types for contract call
        quote = Web3.to_checksum_address(quote)
        recipient = Web3.to_checksum_address(recipient)
        n = int(n)
        slippage_limit = int(slippage_limit)
        eth_amount = int(eth_amount)

        return await self._execute_transaction(
            "marketSellETH",
            quote,
            is_maker,
            n,
            recipient,
            slippage_limit,
            eth_amount=eth_amount,  # This will be sent as msg.value
        )

    async def create_orders(self, create_order_data: list) -> dict:
        """
        Create multiple orders.

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

        Returns:
            dict: Transaction result with tx_hash, gas_used, status, decoded_logs
            if there are multiple orders placed, order_infos will return
            else it will return the order_info
        Example:
            create_data = [
                {
                    "base": "0x...",
                    "quote": "0x...",
                    "isBid": True,
                    "isLimit": True,
                    "orderId": 1,
                    "price": 1000000000000000000,
                    "amount": 1000000000000000000,
                    "n": 1,
                    "recipient": "0x...",
                    "isETH": False,
                }
            ]
            result = await contract.create_orders(create_data)
        """
        # Validate input
        if not isinstance(create_order_data, list):
            raise ValueError("create_order_data must be a list")

        if not create_order_data:
            raise ValueError("create_order_data cannot be empty")

        # Process and validate each create order input
        processed_data = []
        eth_amount = 0
        for i, order_data in enumerate(create_order_data):
            if not isinstance(order_data, dict):
                raise ValueError(f"Order data at index {i} must be a dictionary")

            # Set default orderId if not provided
            if "orderId" not in order_data:
                order_data = order_data.copy()  # Don't modify original
                order_data["orderId"] = 0

            # Required fields
            required_fields = [
                "base",
                "quote",
                "isBid",
                "isLimit",
                "orderId",
                "price",
                "amount",
                "n",
                "recipient",
            ]

            for field in required_fields:
                if field not in order_data:
                    raise ValueError(
                        f"Order data at index {i} missing required field: {field}"
                    )

            # Process the order data with proper types
            processed_order = (
                Web3.to_checksum_address(order_data["base"]),
                Web3.to_checksum_address(order_data["quote"]),
                bool(order_data["isBid"]),
                bool(order_data["isLimit"]),
                int(order_data["orderId"]),
                int(order_data["price"]),
                int(order_data["amount"]),
                int(order_data["n"]),
                Web3.to_checksum_address(order_data["recipient"]),
                bool(order_data["isETH"]),
            )

            processed_data.append(processed_order)
            if order_data["isETH"]:
                eth_amount += int(order_data["amount"])

        return await self._execute_transaction(
            "createOrders", processed_data, eth_amount=eth_amount
        )

    async def update_orders(self, update_order_data: list) -> dict:
        """
        Update multiple orders.

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

        Returns:
            dict: Transaction result with tx_hash, gas_used, status, decoded_logs

        Example:
            update_data = [
                {
                    "base": "0x...",
                    "quote": "0x...",
                    "isBid": True,
                    "isLimit": True,
                    "orderId": 1,
                    "price": 2000000000000000000,
                    "amount": 1000000000000000000,
                    "n": 1,
                    "recipient": "0x...",
                    "isETH": False,
                }
            ]
            result = await contract.update_orders(update_data)
        """
        # Validate input
        if not isinstance(update_order_data, list):
            raise ValueError("update_order_data must be a list")

        if not update_order_data:
            raise ValueError("update_order_data cannot be empty")

        # Process and validate each update order input
        processed_data = []
        eth_amount = 0
        for i, order_data in enumerate(update_order_data):
            if not isinstance(order_data, dict):
                raise ValueError(f"Order data at index {i} must be a dictionary")

            # Required fields (orderId is required for updates)
            required_fields = [
                "base",
                "quote",
                "isBid",
                "isLimit",
                "orderId",
                "price",
                "amount",
                "n",
                "recipient",
                "isETH",
            ]

            for field in required_fields:
                if field not in order_data:
                    raise ValueError(
                        f"Order data at index {i} missing required field: {field}"
                    )

            # Process the order data with proper types
            processed_order = (
                Web3.to_checksum_address(order_data["base"]),
                Web3.to_checksum_address(order_data["quote"]),
                bool(order_data["isBid"]),
                bool(order_data["isLimit"]),
                int(order_data["orderId"]),
                int(order_data["price"]),
                int(order_data["amount"]),
                int(order_data["n"]),
                Web3.to_checksum_address(order_data["recipient"]),
                bool(order_data["isETH"]),
            )

            processed_data.append(processed_order)
            if order_data["isETH"]:
                eth_amount += int(order_data["amount"])

        return await self._execute_transaction(
            "updateOrders", processed_data, eth_amount=eth_amount
        )

    async def cancel_orders(self, cancel_order_data: list) -> str:
        """
        Cancel multiple orders.

        Args:
            cancel_order_data: List of ids containing the order to cancel

        Returns:
            str: Transaction hash

        Example:
            cancel_data = [
                 "0x..._0x..._True_12345",
                 "0x..._0x..._False_12346"
            ]
            tx_hash = await contract.cancel_orders(cancel_data)
        """
        # Validate input
        if not isinstance(cancel_order_data, list):
            raise ValueError("cancel_order_data must be a list")

        if not cancel_order_data:
            raise ValueError("cancel_order_data cannot be empty")

        # Process and validate each cancel order input
        processed_data = []
        for i, order_data in enumerate(cancel_order_data):
            if not isinstance(order_data, str):
                raise ValueError(
                    f"Order data at index {i} must be a string containing the order id"
                )

            # parse the order id
            order_id = order_data.split("_")
            order_data = {
                "base": order_id[0],
                "quote": order_id[1],
                "isBid": order_id[2],
                "orderId": order_id[3],
            }
            required_fields = ["base", "quote", "isBid", "orderId"]
            for field in required_fields:
                if field not in order_data:
                    raise ValueError(
                        f"Missing required field '{field}' in order data at index {i}"
                    )

            # Ensure proper types for contract call
            processed_order = (
                Web3.to_checksum_address(order_data["base"]),
                Web3.to_checksum_address(order_data["quote"]),
                bool(order_data["isBid"]),
                int(order_data["orderId"]),
            )
            processed_data.append(processed_order)

        return await self._execute_transaction("cancelOrders", processed_data)

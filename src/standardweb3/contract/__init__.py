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

    async def _execute_transaction(self, function_name: str, *args) -> str:
        """Execute a contract transaction."""
        contract = self.get_contract(self.matching_engine, self.matching_engine_abi)

        # Get the contract function and build transaction
        try:
            contract_function = getattr(contract.functions, function_name)
            function_call = contract_function(*args)

            # Build the transaction using the correct method name
            if hasattr(function_call, "build_transaction"):
                tx = function_call.build_transaction(
                    {
                        "from": self.address,
                        "nonce": self.w3.eth.get_transaction_count(self.address),
                        "gas": 2000000,
                        "gasPrice": self.w3.to_wei(50, "gwei"),
                    }
                )
            else:
                raise AttributeError(
                    "Function call object does not have build_transaction method"
                )

        except Exception as e:
            print(f"Error in contract function call: {e}")
            raise

        signed_tx = self.sign_tx(tx)

        tx_hash = await asyncio.to_thread(self.send_tx, signed_tx)
        tx_receipt = await asyncio.to_thread(self.wait_for_tx_receipt, tx_hash)
        return tx_receipt

    async def market_buy(
        self, base, quote, quote_amount, is_maker, n, recipient, slippageLimit
    ) -> str:
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
    ) -> str:
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
    ) -> str:
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
    ) -> str:
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

    async def cancel_orders(self, cancel_order_data: list) -> str:
        """
        Cancel multiple orders.

        Args:
            cancel_order_data: List of dictionaries containing order cancellation data.
                Each dictionary should have:
                - base (str): Base token address
                - quote (str): Quote token address
                - isBid (bool): True for buy orders, False for sell orders
                - orderId (int): Order ID to cancel

        Returns:
            str: Transaction hash

        Example:
            cancel_data = [
                {
                    "base": "0x...",
                    "quote": "0x...",
                    "isBid": True,
                    "orderId": 12345
                },
                {
                    "base": "0x...",
                    "quote": "0x...",
                    "isBid": False,
                    "orderId": 12346
                }
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
            if not isinstance(order_data, dict):
                raise ValueError(f"Order data at index {i} must be a dictionary")

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

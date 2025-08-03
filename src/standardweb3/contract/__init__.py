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
        return self.w3.eth.contract(address=contract_address, abi=contract_abi)

    def sign_tx(self, tx):
        """Sign a transaction with the private key."""
        signed_tx = self.w3.eth.account.sign_transaction(
            tx, private_key=self.private_key
        )
        return signed_tx

    def send_tx(self, signed_tx):
        """Send a signed transaction."""
        if not isinstance(signed_tx, dict):
            raise Exception("Invalid signed transaction")
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash

    def wait_for_tx_receipt(self, tx_hash):
        """Wait for transaction receipt."""
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    async def _execute_transaction(self, function_name: str, *args) -> str:
        """Execute a contract transaction."""
        contract = self.contract_functions.get_contract(
            self.matching_engine, self.matching_engine_abi
        )
        tx = getattr(contract.functions, function_name)(*args).buildTransaction(
            {
                "from": self.address,
                "nonce": self.w3.eth.getTransactionCount(self.address),
                "gas": 2000000,
                "gasPrice": self.w3.toWei(50000000000, "wei"),
            }
        )
        signed_tx = self.contract_functions.sign_tx(tx)
        tx_hash = await asyncio.to_thread(self.contract_functions.send_tx, signed_tx)
        tx_receipt = await asyncio.to_thread(
            self.contract_functions.wait_for_tx_receipt, tx_hash
        )
        return tx_receipt

    async def market_buy(
        self, base, quote, quote_amount, is_maker, n, uid, recipient
    ) -> str:
        """Execute a market buy order."""
        return await self._execute_transaction(
            "marketBuy", base, quote, quote_amount, is_maker, n, uid, recipient
        )

    async def market_sell(
        self, base, quote, base_amount, is_maker, n, uid, recipient
    ) -> str:
        """Execute a market sell order."""
        return await self._execute_transaction(
            "marketSell", base, quote, base_amount, is_maker, n, uid, recipient
        )

    async def limit_buy(
        self, base, quote, price, quote_amount, is_maker, n, uid, recipient
    ) -> str:
        """Execute a limit buy order."""
        return await self._execute_transaction(
            "limitBuy",
            base,
            quote,
            price,
            quote_amount,
            is_maker,
            n,
            uid,
            recipient,
        )

    async def limit_sell(
        self, base, quote, price, base_amount, is_maker, n, uid, recipient
    ) -> str:
        """Execute a limit sell order."""
        return await self._execute_transaction(
            "limitSell",
            base,
            quote,
            price,
            base_amount,
            is_maker,
            n,
            uid,
            recipient,
        )

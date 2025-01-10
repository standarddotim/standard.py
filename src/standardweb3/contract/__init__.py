from web3 import Web3
import asyncio


class ContractFunctions:
    def __init__(
        self,
        w3: Web3,
        private_key: str,
        address: str,
        matching_engine: str,
        matching_engine_abi: dict,
    ):
        self.w3 = w3
        self.private_key = private_key
        self.address = address
        self.matching_engine = matching_engine
        self.matching_engine_abi = matching_engine_abi

    def get_contract(self, contract_address, contract_abi):
        return self.w3.eth.contract(address=contract_address, abi=contract_abi)

    def sign_tx(self, tx):
        signed_tx = self.w3.eth.account.sign_transaction(
            tx, private_key=self.private_key
        )
        return signed_tx

    def send_tx(self, signed_tx):
        if not isinstance(signed_tx, dict):
            raise Exception("Invalid signed transaction")
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash

    def wait_for_tx_receipt(self, tx_hash):
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    async def _execute_transaction(self, function_name: str, *args) -> str:
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
        return await self._execute_transaction(
            "marketBuy", base, quote, quote_amount, is_maker, n, uid, recipient
        )

    async def market_sell(
        self, base, quote, base_amount, is_maker, n, uid, recipient
    ) -> str:
        return await self._execute_transaction(
            "marketSell", base, quote, base_amount, is_maker, n, uid, recipient
        )

    async def limit_buy(
        self, base, quote, price, quote_amount, is_maker, n, uid, recipient
    ) -> str:
        return await self._execute_transaction(
            "limitBuy", base, quote, price, quote_amount, is_maker, n, uid, recipient
        )

    async def limit_sell(
        self, base, quote, price, base_amount, is_maker, n, uid, recipient
    ) -> str:
        return await self._execute_transaction(
            "limitSell", base, quote, price, base_amount, is_maker, n, uid, recipient
        )

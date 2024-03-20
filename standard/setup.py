from standard.types.trade import Trade
from standard.types.orderbook import Orderbook
from standard.addresses.matching_engine import matching_engine_addresses
from standard.abis.matching_engine import matching_engine_abi
from web3 import Web3
from eth_account import Account


class StandardClient:
    def __init__(
        self, private_key: str, http_rpc_url: str, networkName: str, api_key: str
    ) -> None:
        self.provider = Web3.HTTPProvider(http_rpc_url)
        self.w3 = Web3(self.provider)

        # Derive the Ethereum address from the private key
        self.wallet_address = Account.from_key(private_key).address

        # Unlock account with private key
        self.w3.eth.default_account = self.w3.eth.account.from_key(private_key)

        self.matching_engine_address = matching_engine_addresses[networkName]

        self.initialized = True

        # Optionally, you may want to set other properties or perform additional setup here

    def market_buy(self, base, quote, quote_amount, is_maker, n, uid, recipient) -> str:
        # check if the client is initialized
        if self.initialized != True:
            # raise ClientNotInitialized error and return
            return

        # get abi and address
        contract_address = self.matching_engine_address
        contract_abi = matching_engine_abi

        # make contract object
        contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)

        # make transaction
        transaction = contract.functions.marketSell(
            base, quote, quote_amount, is_maker, n, uid, recipient
        ).buildTransaction(
            {
                "from": self.address,
                "nonce": self.w3.eth.getTransactionCount(self.address),
                "gas": 2000000,
                "gasPrice": self.w3.toWei(50000000000, "wei"),
            }
        )

        # Sign and send the transaction
        signed_txn = self.w3.eth.account.signTransaction(
            transaction, private_key=self.private_key
        )
        tx_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        # get tx receipt
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        if tx_receipt is not None:
            # Parse event logs from the receipt
            for log in tx_receipt["logs"]:
                decoded_log = self.w3.eth.abi.decode_log(
                    contract_abi, log["data"], topics=log["topics"]
                )
                # handle OrderMatched

                # handle OrderPlaced

            # report result to backend
        else:
            print("Transaction receipt not found.")

        return tx_hash.hex()

    def market_sell(self, base, quote, base_amount, is_maker, n, uid, recipient) -> str:
        pass

    def limit_buy(
        self, base, quote, price, quote_amount, is_maker, n, uid, recipient
    ) -> str:
        pass

    def limit_sell(
        self, base, quote, price, base_amount, is_maker, n, uid, recipient
    ) -> str:
        pass

    def show_orderbook(self, base, quote) -> Orderbook:
        pass

    def recent_trades(self, base, quote) -> list[Trade]:
        pass

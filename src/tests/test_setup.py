# test_example.py
from dotenv import load_dotenv
from standardweb3 import StandardClient
import os

load_dotenv()


def test_init_standard_client():
    private_key = os.environ.get("LINEA_TESTNET_DEPLOYER_KEY")
    mode_rpc = os.environ.get("MODE_RPC")
    assert private_key is not None
    assert mode_rpc is not None
    client = StandardClient(private_key, mode_rpc)
    assert client is not None
    assert client.account.address == "0x34CCCa03631830cD8296c172bf3c31e126814ce9"

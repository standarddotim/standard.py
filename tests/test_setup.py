# test_example.py
from dotenv import load_dotenv
from standard.setup import StandardClient

load_dotenv()
import os


def test_init_standard_client():
    private_key = os.environ.get("LINEA_TESTNET_DEPLOYER_KEY")
    mode_rpc = os.environ.get("MODE_RPC")
    assert private_key is not None
    assert mode_rpc is not None
    client = StandardClient(private_key, mode_rpc)
    assert client is not None
    assert client.address == "0x34CCCa03631830cD8296c172bf3c31e126814ce9"


def test_subtraction():
    assert 5 - 3 == 2


def test_multiplication():
    assert 2 * 3 == 6


def test_division():
    assert 6 / 2 == 3

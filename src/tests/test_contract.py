# test_example.py
from dotenv import load_dotenv
from standardweb3 import StandardClient
import os

load_dotenv()


def test_market_buy():
    private_key = os.environ.get("LINEA_TESTNET_DEPLOYER_KEY")
    mode_rpc = os.environ.get("MODE_RPC")
    client = StandardClient(private_key, mode_rpc)
    base = "0x"


def test_subtraction():
    assert 5 - 3 == 2


def test_multiplication():
    assert 2 * 3 == 6


def test_division():
    assert 6 / 2 == 3

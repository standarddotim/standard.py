from dataclasses import dataclass
from typing import List
from .token import Token  # Assuming Token is defined in token.py


@dataclass
class OrderHistory:
    id: str
    orderId: int
    isBid: int
    base: Token
    quote: Token
    pair: str
    orderbook: str
    price: float
    amount: float
    timestamp: float
    maker: str
    taker: str
    account: str
    txHash: str


@dataclass
class AccountOrderHistory:
    orderHistory: List[OrderHistory]
    totalCount: int
    totalPages: int
    pageSize: int
    lastUpdated: float

from dataclasses import dataclass
from typing import List
from .token import Token  # Assuming Token is defined in token.py


@dataclass
class UpdateTradeEvent:
    id: str
    orderId: int
    base: str
    quote: str
    pair: str
    isBid: int
    price: float
    orderbook: str
    baseAmount: float
    quoteAmount: float
    timestamp: float
    taker: str
    maker: str
    txHash: str


@dataclass
class Trade:
    id: str
    orderbook: str
    orderId: int
    base: Token
    quote: Token
    pair: str
    isBid: int
    price: float
    baseAmount: float
    quoteAmount: float
    timestamp: float
    taker: str
    maker: str
    txHash: str


@dataclass
class TradesData:
    trades: List[Trade]
    totalCount: int
    totalPages: int
    pageSize: int
    lastUpdated: float

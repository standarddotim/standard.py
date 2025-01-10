from dataclasses import dataclass
from typing import List
from .token import Token  # Assuming Token is defined in token.py


@dataclass
class UpdateTradeHistoryEvent:
    id: str
    orderId: int
    base: str
    quote: str
    isBid: int
    orderbook: str
    price: float
    amount: float
    taker: str
    maker: str
    account: str
    timestamp: float
    txHash: str


@dataclass
class TradeHistory:
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
class AccountTradeHistory:
    tradeHistory: List[TradeHistory]
    totalCount: int
    totalPages: int
    pageSize: int
    lastUpdated: float

from dataclasses import dataclass
from typing import List
from .token import Token  # Assuming Token is defined in token.py


@dataclass
class DeleteOrderEvent:
    id: str
    timestamp: float


@dataclass
class OrderEvent:
    id: str
    isBid: int
    orderId: int
    base: str
    quote: str
    orderbook: str
    price: float
    amount: float
    placed: float
    timestamp: float
    account: str
    txHash: str


@dataclass
class Order:
    id: str
    isBid: int
    orderId: int
    base: Token
    quote: Token
    pair: str
    orderbook: str
    price: float
    amount: float
    placed: float
    timestamp: float
    account: str
    txHash: str


@dataclass
class AccountOrders:
    orders: List[Order]
    totalCount: int
    totalPages: int
    pageSize: int
    lastUpdated: float

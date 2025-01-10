from dataclasses import dataclass
from typing import List


@dataclass
class Tick:
    id: str
    orderbook: str
    price: float
    amount: float
    count: int


@dataclass
class Orderbook:
    orderbook: str
    mktPrice: float
    bidHead: float
    askHead: float
    bids: List[Tick]
    asks: List[Tick]
    lastUpdated: float


@dataclass
class TickEvent:
    id: str
    isBid: bool
    orderbook: str
    price: float
    amount: float
    count: int
    timestamp: float


@dataclass
class MarketPriceEvent:
    id: str
    price: float
    timestamp: float


@dataclass
class DeleteTickEvent:
    id: str
    isBid: bool
    timestamp: float

from dataclasses import dataclass
from typing import List
from .token import Token  # Assuming Token is defined in token.py


@dataclass
class Pair:
    id: str
    symbol: str
    ticker: str
    description: str
    type: str
    exchange: str
    base: Token
    quote: Token
    price: float
    ath: float
    atl: float
    listingDate: float
    dayPriceDifference: float
    dayPriceDifferencePercentage: float
    dayBaseVolume: float
    dayQuoteVolume: float
    dayBaseVolumeUSD: float
    dayQuoteVolumeUSD: float
    dayBaseTvl: float
    dayQuoteTvl: float
    dayBaseTvlUSD: float
    dayQuoteTvlUSD: float
    orderbook: str
    bDecimal: int
    qDecimal: int
    totalMinBuckets: int
    totalHourBuckets: int
    totalDayBuckets: int
    totalWeekBuckets: int
    totalMonthBuckets: int


@dataclass
class PairData:
    pairs: List[Pair]
    totalCount: int
    totalPages: int
    pageSize: int

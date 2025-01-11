from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Token:
    id: str
    name: str
    symbol: str
    ticker: str
    totalSupply: float
    logoURI: str
    decimals: int
    price: float
    cpPrice: float
    cgId: str
    cmcId: str
    ath: float
    atl: float
    listingDate: float
    dayPriceDifference: float
    dayPriceDifferencePercentage: float
    dayTvl: float
    dayTvlUSD: float
    dayVolume: float
    dayVolumeUSD: float
    creator: Optional[str]
    totalMinBuckets: int
    totalHourBuckets: int
    totalDayBuckets: int
    totalWeekBuckets: int
    totalMonthBuckets: int


@dataclass
class TokenBucket:
    id: str
    index: int
    token: str
    open: float
    high: float
    low: float
    close: float
    average: float
    difference: float
    differencePercentage: float
    tvl: float
    tvlUSD: float
    volume: float
    volumeUSD: float
    count: int
    timestamp: float


@dataclass
class TokenInfo:
    id: str
    name: str
    symbol: str
    ticker: str
    totalSupply: float
    logoURI: str
    decimals: int
    price: float
    cpPrice: float
    cgId: str
    cmcId: str
    ath: float
    atl: float
    listingDate: float
    dayPriceDifference: float
    dayPriceDifferencePercentage: float
    dayTvl: float
    dayTvlUSD: float
    dayVolume: float
    dayVolumeUSD: float
    creator: Optional[str]
    totalMinBuckets: int
    totalHourBuckets: int
    totalDayBuckets: int
    totalWeekBuckets: int
    totalMonthBuckets: int
    latestMinBucket: TokenBucket
    latestHourBucket: TokenBucket
    latestDayBucket: TokenBucket
    latestWeekBucket: TokenBucket
    latestMonthBucket: TokenBucket


@dataclass
class TokenData:
    tokens: List[Token]
    totalCount: int
    totalPages: int
    pageSize: int

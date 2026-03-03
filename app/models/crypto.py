from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TimeFrame(str, Enum):
    HOUR_1 = "1h"
    HOUR_24 = "24h"
    DAY_7 = "7d"
    DAY_30 = "30d"


class CryptoPrice(BaseModel):
    symbol: str = Field(..., examples=["BTC"])
    name: str = Field(..., examples=["Bitcoin"])
    price_usd: float = Field(..., ge=0, examples=[67432.18])
    change_24h: float = Field(..., examples=[2.34])
    market_cap: float = Field(..., ge=0)
    volume_24h: float = Field(..., ge=0)
    last_updated: datetime


class CryptoDetail(CryptoPrice):
    """Extended crypto info with historical data and metadata."""

    rank: int = Field(..., ge=1)
    circulating_supply: float
    max_supply: float | None = None
    ath: float = Field(..., description="All-time high price in USD")
    ath_date: datetime
    change_1h: float
    change_7d: float
    description: str = ""


class MarketOverview(BaseModel):
    total_market_cap: float
    total_volume_24h: float
    btc_dominance: float
    eth_dominance: float
    active_cryptocurrencies: int
    top_gainers: list[CryptoPrice]
    top_losers: list[CryptoPrice]
    last_updated: datetime


class PriceHistoryPoint(BaseModel):
    timestamp: datetime
    price: float
    volume: float


class PriceHistory(BaseModel):
    symbol: str
    timeframe: TimeFrame
    data: list[PriceHistoryPoint]

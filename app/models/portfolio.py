from datetime import datetime

from pydantic import BaseModel, Field


class PortfolioHolding(BaseModel):
    symbol: str
    quantity: float = Field(..., gt=0)
    avg_buy_price: float = Field(..., ge=0)
    current_price: float = 0.0
    value_usd: float = 0.0
    pnl: float = 0.0
    pnl_percent: float = 0.0


class PortfolioCreate(BaseModel):
    user_id: str
    holdings: list[PortfolioHolding]


class Portfolio(BaseModel):
    user_id: str
    holdings: list[PortfolioHolding]
    total_value: float = 0.0
    total_pnl: float = 0.0
    total_pnl_percent: float = 0.0
    updated_at: datetime


class PortfolioSummary(BaseModel):
    """Quick overview without individual holding details."""

    user_id: str
    total_value: float
    total_pnl: float
    total_pnl_percent: float
    num_holdings: int
    top_holding: str | None = None

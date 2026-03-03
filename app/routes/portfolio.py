from fastapi import APIRouter, HTTPException

from app.models.portfolio import Portfolio, PortfolioCreate
from app.services.portfolio_service import PortfolioService

router = APIRouter()
portfolio_service = PortfolioService()


@router.post("", response_model=Portfolio, status_code=201)
async def create_or_update_portfolio(data: PortfolioCreate):
    """Create a new portfolio or update existing holdings for a user."""
    try:
        return portfolio_service.upsert(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=Portfolio)
async def get_portfolio(user_id: str):
    portfolio = portfolio_service.get_by_user(user_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio


@router.delete("/{user_id}", status_code=204)
async def delete_portfolio(user_id: str):
    deleted = portfolio_service.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Portfolio not found")


@router.delete("/{user_id}/holdings/{symbol}", response_model=Portfolio)
async def remove_holding(user_id: str, symbol: str):
    """Remove a specific holding from a portfolio."""
    portfolio = portfolio_service.remove_holding(user_id, symbol.upper())
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio or holding not found")
    return portfolio

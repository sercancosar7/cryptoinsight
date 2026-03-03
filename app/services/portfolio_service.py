from datetime import datetime, timezone

from app.models.portfolio import Portfolio, PortfolioCreate, PortfolioHolding
from app.services.crypto_service import CryptoService

# in-memory store
_portfolios: dict[str, Portfolio] = {}

crypto_service = CryptoService()


class PortfolioService:

    def _enrich_holdings(self, holdings: list[PortfolioHolding]) -> list[PortfolioHolding]:
        """Attach current prices and calculate PnL for each holding."""
        enriched = []
        for h in holdings:
            price = crypto_service.get_price(h.symbol.upper())
            if price is None:
                # TODO: should we skip unknown symbols or raise?
                price = h.avg_buy_price

            value = round(h.quantity * price, 2)
            cost = round(h.quantity * h.avg_buy_price, 2)
            pnl = round(value - cost, 2)
            pnl_pct = round((pnl / cost) * 100, 2) if cost > 0 else 0.0

            enriched.append(PortfolioHolding(
                symbol=h.symbol.upper(),
                quantity=h.quantity,
                avg_buy_price=h.avg_buy_price,
                current_price=price,
                value_usd=value,
                pnl=pnl,
                pnl_percent=pnl_pct,
            ))
        return enriched

    def upsert(self, data: PortfolioCreate) -> Portfolio:
        if not data.holdings:
            raise ValueError("Portfolio must contain at least one holding")

        enriched = self._enrich_holdings(data.holdings)
        total_value = sum(h.value_usd for h in enriched)
        total_cost = sum(h.quantity * h.avg_buy_price for h in enriched)
        total_pnl = round(total_value - total_cost, 2)
        total_pnl_pct = round((total_pnl / total_cost) * 100, 2) if total_cost > 0 else 0.0

        portfolio = Portfolio(
            user_id=data.user_id,
            holdings=enriched,
            total_value=round(total_value, 2),
            total_pnl=total_pnl,
            total_pnl_percent=total_pnl_pct,
            updated_at=datetime.now(timezone.utc),
        )
        _portfolios[data.user_id] = portfolio
        return portfolio

    def get_by_user(self, user_id: str) -> Portfolio | None:
        portfolio = _portfolios.get(user_id)
        if not portfolio:
            return None

        # recalculate with latest prices
        enriched = self._enrich_holdings(portfolio.holdings)
        total_value = sum(h.value_usd for h in enriched)
        total_cost = sum(h.quantity * h.avg_buy_price for h in enriched)
        total_pnl = round(total_value - total_cost, 2)
        total_pnl_pct = round((total_pnl / total_cost) * 100, 2) if total_cost > 0 else 0.0

        return Portfolio(
            user_id=user_id,
            holdings=enriched,
            total_value=round(total_value, 2),
            total_pnl=total_pnl,
            total_pnl_percent=total_pnl_pct,
            updated_at=datetime.now(timezone.utc),
        )

    def delete(self, user_id: str) -> bool:
        return _portfolios.pop(user_id, None) is not None

    def remove_holding(self, user_id: str, symbol: str) -> Portfolio | None:
        portfolio = _portfolios.get(user_id)
        if not portfolio:
            return None

        remaining = [h for h in portfolio.holdings if h.symbol != symbol]
        if len(remaining) == len(portfolio.holdings):
            return None  # symbol wasn't in portfolio

        if not remaining:
            _portfolios.pop(user_id, None)
            return Portfolio(
                user_id=user_id,
                holdings=[],
                total_value=0,
                total_pnl=0,
                total_pnl_percent=0,
                updated_at=datetime.now(timezone.utc),
            )

        # rebuild with updated holdings
        from app.models.portfolio import PortfolioCreate
        return self.upsert(PortfolioCreate(user_id=user_id, holdings=remaining))

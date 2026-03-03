from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field

from app.services.crypto_service import CryptoService


class AlertCondition(str, Enum):
    ABOVE = "above"
    BELOW = "below"


class AlertCreate(BaseModel):
    user_id: str
    symbol: str
    condition: AlertCondition
    target_price: float = Field(..., gt=0)


class Alert(BaseModel):
    id: str
    user_id: str
    symbol: str
    condition: AlertCondition
    target_price: float
    current_price: float
    is_triggered: bool = False
    created_at: datetime


# in-memory store
_alerts: dict[str, list[Alert]] = {}

crypto_service = CryptoService()


class AlertService:

    def create(self, data: AlertCreate) -> Alert:
        symbol = data.symbol.upper()
        price = crypto_service.get_price(symbol)
        if price is None:
            raise ValueError(f"Unknown symbol: {symbol}")

        alert = Alert(
            id=str(uuid4()),
            user_id=data.user_id,
            symbol=symbol,
            condition=data.condition,
            target_price=data.target_price,
            current_price=price,
            is_triggered=self._check_triggered(data.condition, price, data.target_price),
            created_at=datetime.now(timezone.utc),
        )

        if data.user_id not in _alerts:
            _alerts[data.user_id] = []
        _alerts[data.user_id].append(alert)

        return alert

    def get_by_user(self, user_id: str, active_only: bool = True) -> list[Alert]:
        alerts = _alerts.get(user_id, [])
        if not active_only:
            return alerts

        # refresh triggered status with current prices
        refreshed = []
        for a in alerts:
            price = crypto_service.get_price(a.symbol) or a.current_price
            triggered = self._check_triggered(a.condition, price, a.target_price)
            refreshed.append(Alert(
                **{**a.model_dump(), "current_price": price, "is_triggered": triggered}
            ))

        if active_only:
            return [a for a in refreshed if not a.is_triggered]
        return refreshed

    def delete(self, user_id: str, alert_id: str) -> bool:
        alerts = _alerts.get(user_id, [])
        for i, a in enumerate(alerts):
            if a.id == alert_id:
                alerts.pop(i)
                return True
        return False

    @staticmethod
    def _check_triggered(condition: AlertCondition, current: float, target: float) -> bool:
        if condition == AlertCondition.ABOVE:
            return current >= target
        return current <= target

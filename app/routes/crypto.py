import asyncio
import json
import random
from datetime import datetime, timezone

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from app.models.crypto import CryptoDetail, CryptoPrice, MarketOverview
from app.services.crypto_service import CryptoService

router = APIRouter()
ws_router = APIRouter()  # separate router for websocket (mounted at root)
crypto_service = CryptoService()


@router.get("/prices", response_model=list[CryptoPrice])
async def get_prices(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    sort_by: str = Query(default="market_cap", enum=["market_cap", "price_usd", "change_24h", "volume_24h"]),
    order: str = Query(default="desc", enum=["asc", "desc"]),
):
    """Get current cryptocurrency prices with pagination and sorting."""
    prices = crypto_service.get_all_prices()

    reverse = order == "desc"
    prices.sort(key=lambda x: getattr(x, sort_by), reverse=reverse)

    return prices[offset : offset + limit]


@router.get("/market", response_model=MarketOverview)
async def get_market_overview():
    return crypto_service.get_market_overview()


@router.get("/{symbol}", response_model=CryptoDetail)
async def get_crypto_detail(symbol: str):
    """Get detailed information for a specific cryptocurrency."""
    return crypto_service.get_detail(symbol.upper())


# --- WebSocket for live price streaming ---

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        for conn in self.active_connections:
            try:
                await conn.send_json(data)
            except Exception:
                pass  # stale connections get cleaned up on next disconnect


manager = ConnectionManager()


@ws_router.websocket("/ws/prices")
async def websocket_prices(websocket: WebSocket):
    """
    Stream mock price updates every 2 seconds.
    Each tick randomly adjusts prices by a small percentage to simulate
    real market movement.
    """
    await manager.connect(websocket)
    try:
        while True:
            prices = crypto_service.get_all_prices()
            # simulate small price fluctuations
            updates = []
            for p in prices[:10]:  # top 10 only for ws
                delta = random.uniform(-0.8, 0.8)
                new_price = round(p.price_usd * (1 + delta / 100), 2)
                updates.append({
                    "symbol": p.symbol,
                    "price": new_price,
                    "change": round(delta, 4),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })

            await websocket.send_text(json.dumps(updates))
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

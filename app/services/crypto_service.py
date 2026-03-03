from datetime import datetime, timezone

from fastapi import HTTPException

from app.models.crypto import CryptoDetail, CryptoPrice, MarketOverview
from app.utils.mock_data import CRYPTO_DATA


class CryptoService:
    """
    Handles crypto price data retrieval and transformations.
    Currently uses mock data - swap in a real API client (CoinGecko, etc.)
    for production use.
    """

    def __init__(self):
        self._data = CRYPTO_DATA

    def get_all_prices(self) -> list[CryptoPrice]:
        now = datetime.now(timezone.utc)
        return [
            CryptoPrice(
                symbol=c["symbol"],
                name=c["name"],
                price_usd=c["price_usd"],
                change_24h=c["change_24h"],
                market_cap=c["market_cap"],
                volume_24h=c["volume_24h"],
                last_updated=now,
            )
            for c in self._data
        ]

    def get_detail(self, symbol: str) -> CryptoDetail:
        coin = next((c for c in self._data if c["symbol"] == symbol), None)
        if not coin:
            raise HTTPException(status_code=404, detail=f"Crypto '{symbol}' not found")

        now = datetime.now(timezone.utc)
        return CryptoDetail(
            symbol=coin["symbol"],
            name=coin["name"],
            price_usd=coin["price_usd"],
            change_24h=coin["change_24h"],
            market_cap=coin["market_cap"],
            volume_24h=coin["volume_24h"],
            last_updated=now,
            rank=coin["rank"],
            circulating_supply=coin["circulating_supply"],
            max_supply=coin.get("max_supply"),
            ath=coin["ath"],
            ath_date=datetime.fromisoformat(coin["ath_date"]),
            change_1h=coin["change_1h"],
            change_7d=coin["change_7d"],
            description=coin.get("description", ""),
        )

    def get_market_overview(self) -> MarketOverview:
        prices = self.get_all_prices()
        total_cap = sum(p.market_cap for p in prices)
        total_vol = sum(p.volume_24h for p in prices)

        btc = next((p for p in prices if p.symbol == "BTC"), None)
        eth = next((p for p in prices if p.symbol == "ETH"), None)

        btc_dom = (btc.market_cap / total_cap * 100) if btc else 0
        eth_dom = (eth.market_cap / total_cap * 100) if eth else 0

        sorted_by_change = sorted(prices, key=lambda p: p.change_24h, reverse=True)

        return MarketOverview(
            total_market_cap=total_cap,
            total_volume_24h=total_vol,
            btc_dominance=round(btc_dom, 2),
            eth_dominance=round(eth_dom, 2),
            active_cryptocurrencies=len(prices),
            top_gainers=sorted_by_change[:3],
            top_losers=sorted_by_change[-3:],
            last_updated=datetime.now(timezone.utc),
        )

    def get_price(self, symbol: str) -> float | None:
        """Get the current price for a single symbol. Returns None if not found."""
        coin = next((c for c in self._data if c["symbol"] == symbol), None)
        return coin["price_usd"] if coin else None

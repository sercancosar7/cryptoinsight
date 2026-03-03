# CryptoInsight – Real-Time Cryptocurrency Dashboard

Real-time cryptocurrency dashboard with portfolio tracking, alerts, and market analysis.

🔗 **Live Demo:** [sercod.com/demos/cryptoinsight](https://sercod.com/demos/cryptoinsight/)

## Features

- 💰 **Portfolio Tracker** – Track holdings, P&L, and allocation breakdown
- 📊 **Live Price Charts** – Real-time charts powered by Chart.js
- 🔔 **Price Alerts** – WebSocket-based alerts for price movements
- 🌍 **Market Overview** – Top coins, gainers, losers, and volume data
- 📈 **Market Analysis** – Technical indicators and trend summaries
- 🔐 **Secure Storage** – Encrypted local portfolio data

## Tech Stack

- **Backend:** Python + FastAPI
- **Real-time:** WebSocket
- **Frontend:** React
- **Charts:** Chart.js
- **Data:** CoinGecko API

## Getting Started

```bash
git clone https://github.com/sercancosar7/cryptoinsight.git
cd cryptoinsight

# Backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (in a new terminal)
cd frontend
npm install
npm run dev
```

## License

MIT – see [LICENSE](./LICENSE)

# CryptoInsight API

Real-time cryptocurrency tracking and portfolio management API. Built with Python and FastAPI for high-performance async operations.

## Features

- Real-time crypto price tracking (20+ coins)
- Portfolio management & analytics
- Price alert system with configurable thresholds
- WebSocket for live price updates
- Market analysis endpoints
- Rate limiting & caching

## Tech Stack

- Python 3.11+
- FastAPI + Uvicorn
- Pydantic v2
- WebSockets
- Redis (caching layer)

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
uvicorn main:app --reload
```

## API Docs

Visit `/docs` for interactive Swagger documentation.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/crypto/prices` | List all crypto prices |
| GET | `/api/v1/crypto/market` | Market overview |
| GET | `/api/v1/crypto/{symbol}` | Specific crypto details |
| POST | `/api/v1/portfolio` | Create/update portfolio |
| GET | `/api/v1/portfolio/{user_id}` | Get user portfolio |
| POST | `/api/v1/alerts` | Set price alert |
| GET | `/api/v1/alerts/{user_id}` | Get user alerts |
| WS | `/ws/prices` | Real-time price stream |

## Environment Variables

See `.env.example` for available configuration options.

## License

MIT

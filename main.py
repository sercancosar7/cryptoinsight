"""
CryptoInsight API - main entry point.

Run with: uvicorn main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.routes import alerts, auth, crypto, portfolio
from app.routes.crypto import ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    print(f"Starting {settings.app_name} v1.2.0")
    print(f"Environment: {settings.app_env}")
    yield
    # shutdown
    print("Shutting down...")


app = FastAPI(
    title=settings.app_name,
    description="Real-time cryptocurrency tracking and portfolio management API",
    version="1.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(crypto.router, prefix="/api/v1/crypto", tags=["Cryptocurrency"])
app.include_router(portfolio.router, prefix="/api/v1/portfolio", tags=["Portfolio"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])

# websocket mounted separately at root level
app.include_router(ws_router)


@app.get("/", tags=["Health"])
async def root():
    return {
        "name": settings.app_name,
        "version": "1.2.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

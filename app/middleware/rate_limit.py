"""
Simple in-memory rate limiter middleware.
For production, use redis-backed rate limiting or a dedicated service.
"""

import time
from collections import defaultdict

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests: dict[str, list[float]] = defaultdict(list)
        self.limit = settings.rate_limit_per_minute
        self.window = 60  # seconds

    async def dispatch(self, request: Request, call_next) -> Response:
        # skip rate limiting for docs and health
        if request.url.path in ("/docs", "/redoc", "/openapi.json", "/health", "/"):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        # clean old entries
        self.requests[client_ip] = [
            ts for ts in self.requests[client_ip]
            if now - ts < self.window
        ]

        if len(self.requests[client_ip]) >= self.limit:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "retry_after": self.window,
                },
                headers={"Retry-After": str(self.window)},
            )

        self.requests[client_ip].append(now)
        response = await call_next(request)

        # attach rate limit headers
        remaining = self.limit - len(self.requests[client_ip])
        response.headers["X-RateLimit-Limit"] = str(self.limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response

import logging
import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("cryptoinsight")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs request method, path, status code, and response time."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()

        response = await call_next(request)

        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        status = response.status_code
        method = request.method
        path = request.url.path

        # don't log health checks - too noisy
        if path in ("/health", "/"):
            return response

        log_line = f"{method} {path} -> {status} ({elapsed_ms}ms)"

        if status >= 500:
            logger.error(log_line)
        elif status >= 400:
            logger.warning(log_line)
        else:
            logger.info(log_line)

        response.headers["X-Response-Time"] = f"{elapsed_ms}ms"
        return response

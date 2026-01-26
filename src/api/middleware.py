"""
API middleware for request/response processing.

Provides logging, error handling, and request context middleware.
"""

import time
import uuid
from collections.abc import Callable

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from src.lib.logging import bind_request_context, clear_request_context, get_logger


logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging requests and responses.

    Logs:
    - Request details (method, path, client IP)
    - Response status and processing time
    - Binds request ID to log context
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log details."""
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Bind request context for structured logging
        bind_request_context(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        # Log request
        logger.info(
            "Request started",
            client_ip=request.client.host if request.client else "unknown",
            user_agent=request.headers.get("User-Agent", "unknown"),
        )

        # Track timing
        start_time = time.perf_counter()

        try:
            response = await call_next(request)

            # Calculate processing time
            processing_time_ms = int((time.perf_counter() - start_time) * 1000)

            # Add headers to response
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Processing-Time-Ms"] = str(processing_time_ms)

            # Log response
            logger.info(
                "Request completed",
                status_code=response.status_code,
                processing_time_ms=processing_time_ms,
            )

            return response

        except Exception as e:
            processing_time_ms = int((time.perf_counter() - start_time) * 1000)
            logger.exception(
                "Request failed",
                error=str(e),
                processing_time_ms=processing_time_ms,
            )
            raise

        finally:
            # Clear request context
            clear_request_context()


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Global error handler middleware.

    Catches unhandled exceptions and returns standardized error responses.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and handle errors."""
        try:
            return await call_next(request)
        except Exception as e:
            logger.exception("Unhandled exception", error=str(e))
            return JSONResponse(
                status_code=500,
                content={
                    "error_code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred",
                    "details": None,
                },
            )


def setup_middleware(app: FastAPI) -> None:
    """
    Configure all middleware for the FastAPI application.

    Args:
        app: The FastAPI application instance.
    """
    # Add middleware in reverse order (last added = first executed)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(ErrorHandlerMiddleware)
    
    # Allow all hosts to support Azure App Service and MCP SSE connections
    # Azure App Service can reject requests with 421 "Invalid Host header" otherwise
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"],
    )

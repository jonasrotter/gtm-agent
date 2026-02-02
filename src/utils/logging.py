"""
Structured logging configuration using structlog.

Provides consistent, structured logging with OpenTelemetry integration
for observability across the application.
"""

import logging
import sys
from typing import Any

import structlog
from structlog.types import Processor

from src.config import get_settings


def add_service_context(
    logger: logging.Logger, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Add service context to all log entries."""
    settings = get_settings()
    event_dict["service"] = settings.otel_service_name
    event_dict["version"] = settings.app_version
    return event_dict


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure structured logging for the application.

    Sets up structlog with appropriate processors for JSON or console output,
    and configures the root logger.

    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    settings = get_settings()

    # Shared processors for all output formats
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        add_service_context,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.log_format == "json":
        # JSON format for production
        processors: list[Processor] = [
            *shared_processors,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    else:
        # Console format for development
        processors = [
            *shared_processors,
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper(), logging.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging to work with structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper(), logging.INFO),
    )


def get_logger(name: str | None = None) -> structlog.BoundLogger:
    """
    Get a structured logger instance.

    Args:
        name: Optional logger name. If not provided, uses the calling module name.

    Returns:
        A bound structlog logger instance.
    """
    return structlog.get_logger(name)


def bind_request_context(request_id: str, **kwargs: Any) -> None:
    """
    Bind request context to all subsequent log entries in the current context.

    Args:
        request_id: Unique request identifier.
        **kwargs: Additional context to bind.
    """
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id, **kwargs)


def clear_request_context() -> None:
    """Clear the current request context."""
    structlog.contextvars.clear_contextvars()

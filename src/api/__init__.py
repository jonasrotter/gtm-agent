"""
API package for the Solution Engineering Agent.

Exports FastAPI application and common middleware/dependencies.
"""

from src.api.main import app


__all__ = ["app"]

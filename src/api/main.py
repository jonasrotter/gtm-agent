"""
FastAPI application entry point.

Creates and configures the Solution Engineering Agent API.
Includes MCP server for integration with M365 Copilot, GitHub Copilot Chat, etc.
"""

import contextlib
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import __version__
from src.api.middleware import setup_middleware
from src.api.routes import api_router
from src.config import get_settings
from src.utils.logging import get_logger, setup_logging
from src.mcp import mcp, mcp_lifespan


logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Application lifespan manager.

    Handles startup and shutdown events:
    - Startup: Initialize logging, MCP server, connections
    - Shutdown: Clean up resources, close connections
    """
    # Startup
    settings = get_settings()
    setup_logging(settings.log_level)

    logger.info(
        "Starting Orchestrator Agent",
        version=__version__,
        log_level=settings.log_level,
    )

    # Combine MCP lifespan with app lifespan
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp_lifespan(app))
        logger.info("MCP server initialized at /mcp/mcp")
        
        try:
            yield
        finally:
            # Shutdown logging happens before exiting context
            logger.info("Shutting down Solution Engineering Agent")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title="Solution Engineering Agent",
        description=(
            "A multi-agentic AI assistant that helps Solution Engineers by "
            "researching Azure documentation, sharing architecture best practices, "
            "and validating hypotheses through Azure deployments. "
            "Also available as MCP server at /mcp/mcp for M365 Copilot and GitHub Copilot integration."
        ),
        version=__version__,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Configure CORS from settings
    settings = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Setup custom middleware
    setup_middleware(app)

    # Include API routes
    app.include_router(api_router)

    # Mount MCP server at /mcp (streamable HTTP endpoint becomes /mcp/mcp)
    app.mount("/mcp", mcp.streamable_http_app())

    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower(),
    )

"""
Application configuration using Pydantic Settings.

Environment variables are loaded from .env file or system environment.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Azure Foundry/OpenAI Configuration
    azure_foundry_project_endpoint: str = Field(
        default="",
        description="Azure Foundry project endpoint URL",
    )
    azure_foundry_project_deployment_name: str = Field(
        default="gpt-4o",
        description="Model deployment name",
    )

    # Azure OpenAI Configuration (for Semantic Kernel)
    azure_openai_endpoint: str = Field(
        default="",
        description="Azure OpenAI endpoint URL",
    )
    azure_openai_deployment: str = Field(
        default="gpt-4o",
        description="Azure OpenAI deployment name",
    )
    azure_openai_api_version: str = Field(
        default="2024-02-15-preview",
        description="Azure OpenAI API version",
    )

    # API Security
    api_key: str = Field(
        default="",
        description="API key for authentication (empty allows all requests in dev)",
    )

    # Logging Configuration
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level",
    )
    log_format: Literal["json", "console"] = Field(
        default="json",
        description="Log output format",
    )

    # Azure Configuration (for hypothesis validation)
    azure_subscription_id: str = Field(
        default="",
        description="Azure subscription ID for hypothesis validation",
    )
    azure_default_region: str = Field(
        default="eastus",
        description="Default Azure region for resource deployment",
    )
    azure_resource_group: str = Field(
        default="gtm-agent-tests",
        description="Resource group for test deployments",
    )

    # OpenTelemetry Configuration
    otel_exporter_otlp_endpoint: str = Field(
        default="",
        description="OpenTelemetry collector endpoint",
    )
    otel_service_name: str = Field(
        default="gtm-agent",
        description="Service name for telemetry",
    )

    # Application Settings
    app_name: str = Field(default="Solution Engineering Agent")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)

    # MCP Server Configuration
    mcp_microsoft_docs_enabled: bool = Field(
        default=True,
        description="Enable Microsoft Docs MCP server",
    )
    mcp_azure_enabled: bool = Field(
        default=True,
        description="Enable Azure MCP server",
    )
    mcp_context7_enabled: bool = Field(
        default=True,
        description="Enable Context7 MCP server",
    )
    mcp_timeout_seconds: int = Field(
        default=30,
        description="Timeout for MCP tool calls in seconds",
    )

    @field_validator("log_level", mode="before")
    @classmethod
    def uppercase_log_level(cls, v: str) -> str:
        """Ensure log level is uppercase."""
        return v.upper() if isinstance(v, str) else v

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.debug and self.api_key != ""

    @property
    def has_azure_config(self) -> bool:
        """Check if Azure configuration is available for hypothesis validation."""
        return bool(self.azure_subscription_id)


@lru_cache
def get_settings() -> Settings:
    """
    Get cached application settings.

    Returns:
        Settings: Application settings instance.
    """
    return Settings()

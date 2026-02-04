"""
Application configuration using Pydantic Settings.

Environment variables are loaded from .env file or system environment.
"""

from functools import lru_cache
from typing import Literal

from dotenv import load_dotenv
from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file into os.environ BEFORE anything else
# This ensures Azure SDK's DefaultAzureCredential can find service principal credentials
load_dotenv()


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
    api_key: SecretStr | None = Field(
        default=None,
        description="API key for authentication (None allows all requests in dev)",
    )
    
    # CORS Configuration
    cors_allowed_origins: list[str] = Field(
        default=["*"],
        description="Allowed CORS origins. Use ['*'] for development only.",
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
    
    # Timeout Configuration
    api_request_timeout_seconds: int = Field(
        default=300,
        description="Maximum time for a single API request in seconds (increased for architecture queries)",
    )
    api_complex_timeout_seconds: int = Field(
        default=360,
        description="Extended timeout for complex multi-step queries in seconds",
    )
    pev_loop_timeout_seconds: int = Field(
        default=240,
        description="Maximum cumulative time for the Plan-Execute-Verify loop in seconds",
    )
    pev_complex_timeout_seconds: int = Field(
        default=330,
        description="Extended PEV loop timeout for complex queries in seconds",
    )
    step_execution_timeout_seconds: int = Field(
        default=90,  # Increased to handle slow MCP/architecture calls
        description="Timeout for each step execution in seconds",
    )

    # GitHub Copilot SDK Configuration
    copilot_cli_url: str = Field(
        default="",
        description="External Copilot CLI server URL (e.g., 'localhost:4321'). "
        "If empty, SDK will auto-spawn the CLI process locally.",
    )
    copilot_use_azure_openai: bool = Field(
        default=False,
        description="Use Azure OpenAI as the LLM provider (BYOK mode) instead of GitHub Copilot.",
    )
    copilot_model: str = Field(
        default="gpt-4o",
        description="Model to use for Copilot sessions.",
    )
    copilot_azure_openai_endpoint: str = Field(
        default="",
        description="Azure OpenAI endpoint URL for BYOK mode.",
    )
    copilot_azure_openai_api_key: str = Field(
        default="",
        description="Azure OpenAI API key for BYOK mode.",
    )
    copilot_azure_openai_api_version: str = Field(
        default="2024-10-21",
        description="Azure OpenAI API version for BYOK mode.",
    )

    @field_validator("log_level", mode="before")
    @classmethod
    def uppercase_log_level(cls, v: str) -> str:
        """Ensure log level is uppercase."""
        return v.upper() if isinstance(v, str) else v

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.debug and self.api_key is not None

    @property
    def has_azure_config(self) -> bool:
        """Check if Azure configuration is available for hypothesis validation."""
        return bool(self.azure_subscription_id)

    @property
    def copilot_has_azure_byok_config(self) -> bool:
        """Check if Azure OpenAI BYOK configuration is complete for Copilot SDK."""
        return (
            self.copilot_use_azure_openai
            and bool(self.copilot_azure_openai_endpoint)
            and bool(self.copilot_azure_openai_api_key)
        )

    @property
    def copilot_has_external_cli(self) -> bool:
        """Check if an external Copilot CLI server URL is configured."""
        return bool(self.copilot_cli_url)


@lru_cache
def get_settings() -> Settings:
    """
    Get cached application settings.

    Returns:
        Settings: Application settings instance.
    """
    return Settings()

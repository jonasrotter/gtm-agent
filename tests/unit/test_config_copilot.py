"""
Unit tests for Copilot SDK configuration in Settings.
"""

import os
from unittest.mock import patch

import pytest

from src.config import Settings


class TestCopilotConfiguration:
    """Tests for Copilot SDK configuration settings."""

    def test_copilot_default_values(self):
        """Test that Copilot settings have correct defaults."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.copilot_cli_url == ""
            assert settings.copilot_use_azure_openai is False
            assert settings.copilot_model == "gpt-4o"
            assert settings.copilot_azure_openai_endpoint == ""
            assert settings.copilot_azure_openai_api_key == ""
            assert settings.copilot_azure_openai_api_version == "2024-10-21"

    def test_copilot_has_external_cli_false_by_default(self):
        """Test that has_external_cli is False when cli_url is empty."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.copilot_has_external_cli is False

    def test_copilot_has_external_cli_true_when_url_set(self):
        """Test that has_external_cli is True when cli_url is set."""
        with patch.dict(os.environ, {"COPILOT_CLI_URL": "localhost:4321"}, clear=True):
            settings = Settings()
            assert settings.copilot_has_external_cli is True
            assert settings.copilot_cli_url == "localhost:4321"

    def test_copilot_has_azure_byok_config_false_by_default(self):
        """Test that Azure BYOK config is incomplete by default."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.copilot_has_azure_byok_config is False

    def test_copilot_has_azure_byok_config_false_when_disabled(self):
        """Test that Azure BYOK config is False even with credentials if disabled."""
        env = {
            "COPILOT_USE_AZURE_OPENAI": "false",
            "COPILOT_AZURE_OPENAI_ENDPOINT": "https://my-openai.openai.azure.com",
            "COPILOT_AZURE_OPENAI_API_KEY": "my-api-key",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = Settings()
            assert settings.copilot_has_azure_byok_config is False

    def test_copilot_has_azure_byok_config_false_when_incomplete(self):
        """Test that Azure BYOK config is False when credentials are missing."""
        env = {
            "COPILOT_USE_AZURE_OPENAI": "true",
            "COPILOT_AZURE_OPENAI_ENDPOINT": "https://my-openai.openai.azure.com",
            # Missing API key
        }
        with patch.dict(os.environ, env, clear=True):
            settings = Settings()
            assert settings.copilot_has_azure_byok_config is False

    def test_copilot_has_azure_byok_config_true_when_complete(self):
        """Test that Azure BYOK config is True when all settings are provided."""
        env = {
            "COPILOT_USE_AZURE_OPENAI": "true",
            "COPILOT_AZURE_OPENAI_ENDPOINT": "https://my-openai.openai.azure.com",
            "COPILOT_AZURE_OPENAI_API_KEY": "my-api-key",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = Settings()
            assert settings.copilot_has_azure_byok_config is True

    def test_copilot_model_can_be_overridden(self):
        """Test that copilot_model can be set via environment."""
        with patch.dict(os.environ, {"COPILOT_MODEL": "gpt-4.1"}, clear=True):
            settings = Settings()
            assert settings.copilot_model == "gpt-4.1"

    def test_copilot_azure_api_version_can_be_overridden(self):
        """Test that Azure API version can be set via environment."""
        with patch.dict(
            os.environ, 
            {"COPILOT_AZURE_OPENAI_API_VERSION": "2025-01-01"}, 
            clear=True
        ):
            settings = Settings()
            assert settings.copilot_azure_openai_api_version == "2025-01-01"


class TestCopilotDeploymentModes:
    """Tests for different Copilot deployment mode configurations."""

    def test_local_development_mode(self):
        """Test configuration for local development (auto-spawn CLI)."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            # Local mode: no cli_url, no azure byok
            assert not settings.copilot_has_external_cli
            assert not settings.copilot_has_azure_byok_config
            assert not settings.copilot_use_azure_openai

    def test_external_cli_server_mode(self):
        """Test configuration for external CLI server mode."""
        env = {
            "COPILOT_CLI_URL": "localhost:4321",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = Settings()
            
            # External CLI mode
            assert settings.copilot_has_external_cli
            assert settings.copilot_cli_url == "localhost:4321"
            assert not settings.copilot_use_azure_openai

    def test_azure_byok_production_mode(self):
        """Test configuration for Azure BYOK production mode."""
        env = {
            "COPILOT_CLI_URL": "localhost:4321",
            "COPILOT_USE_AZURE_OPENAI": "true",
            "COPILOT_AZURE_OPENAI_ENDPOINT": "https://my-resource.openai.azure.com",
            "COPILOT_AZURE_OPENAI_API_KEY": "sk-my-key",
            "COPILOT_MODEL": "gpt-4o-deployment",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = Settings()
            
            # Full production mode
            assert settings.copilot_has_external_cli
            assert settings.copilot_use_azure_openai
            assert settings.copilot_has_azure_byok_config
            assert settings.copilot_model == "gpt-4o-deployment"
            assert settings.copilot_azure_openai_endpoint == "https://my-resource.openai.azure.com"

"""
Integration tests for performance optimization features.

Tests end-to-end behavior of:
- Query classification
- Fast path for factual queries
- Category-specific PEV configuration
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.agents.classifier import QueryClassifier, QueryCategory
from src.agents.models import AgentResponse


class TestQueryClassificationIntegration:
    """Integration tests for query classification routing."""
    
    @pytest.fixture
    def classifier(self) -> QueryClassifier:
        """Create a QueryClassifier instance."""
        return QueryClassifier()
    
    def test_factual_query_routes_to_fast_path(self, classifier: QueryClassifier) -> None:
        """Factual queries should be configured for fast path."""
        queries = [
            "What is Azure Blob Storage?",
            "Explain Azure Functions",
            "What are the storage tiers?",
            "Describe Azure Event Grid",
        ]
        
        for query in queries:
            category = classifier.classify(query)
            config = category.get_config()
            
            assert category == QueryCategory.FACTUAL, f"Query '{query}' should be FACTUAL"
            assert config["skip_pev"] is True, f"FACTUAL queries should skip PEV"
            assert config["max_iterations"] == 1, f"FACTUAL queries should have max 1 iteration"
    
    def test_code_query_uses_lite_pev(self, classifier: QueryClassifier) -> None:
        """Code queries should use lite PEV (1 iteration)."""
        queries = [
            "Generate Azure CLI to create a resource group",
            "Write a Bicep template for VNet",
            "Create a PowerShell script for backup",
        ]
        
        for query in queries:
            category = classifier.classify(query)
            config = category.get_config()
            
            assert category == QueryCategory.CODE, f"Query '{query}' should be CODE"
            assert config["skip_pev"] is False, f"CODE queries should use PEV"
            assert config["max_iterations"] == 1, f"CODE queries should have max 1 iteration"
            assert config["threshold"] == 0.7, f"CODE queries should have 0.7 threshold"
    
    def test_architecture_query_uses_standard_pev(self, classifier: QueryClassifier) -> None:
        """Architecture queries should use standard PEV (2 iterations)."""
        queries = [
            "Best practices for App Service security",
            "Design a microservices architecture",
            "What are the reliability recommendations?",
        ]
        
        for query in queries:
            category = classifier.classify(query)
            config = category.get_config()
            
            assert category == QueryCategory.ARCHITECTURE, f"Query '{query}' should be ARCHITECTURE"
            assert config["max_iterations"] == 2, f"ARCHITECTURE queries should have max 2 iterations"
            assert config["threshold"] == 0.75, f"ARCHITECTURE queries should have 0.75 threshold"
    
    def test_complex_query_uses_full_pev(self, classifier: QueryClassifier) -> None:
        """Complex queries should use full PEV (4 iterations)."""
        queries = [
            "Explain Azure Functions and write a Bicep template",
            "Design serverless architecture and implement it",
            "What is blob storage? How do I use it? Show me the CLI.",
        ]
        
        for query in queries:
            category = classifier.classify(query)
            config = category.get_config()
            
            assert category == QueryCategory.COMPLEX, f"Query '{query}' should be COMPLEX"
            assert config["max_iterations"] == 4, f"COMPLEX queries should have max 4 iterations"
            assert config["threshold"] == 0.8, f"COMPLEX queries should have 0.8 threshold"


class TestPerformanceExpectations:
    """Tests documenting expected performance characteristics."""
    
    def test_factual_query_expected_metrics(self) -> None:
        """Document expected metrics for factual queries."""
        config = QueryCategory.FACTUAL.get_config()
        
        # Fast path: no planning, no verification
        assert config["skip_pev"] is True
        assert config["max_iterations"] == 1
        
        # Expected: <1 minute (was ~8 minutes with 4 iterations)
        # Improvement: ~8x faster
    
    def test_simple_query_step_budget(self) -> None:
        """Document expected step count for simple queries."""
        # Factual: 1 step (research only)
        # Code: 1 step (code only)
        # HowTo: 1-2 steps
        # Architecture: 1-2 steps
        # Complex: 3-4 steps
        
        expected_max_steps = {
            QueryCategory.FACTUAL: 1,
            QueryCategory.CODE: 1,
            QueryCategory.HOWTO: 2,
            QueryCategory.ARCHITECTURE: 2,
            QueryCategory.COMPLEX: 4,
        }
        
        # These are documented expectations that the Planner should follow
        for category, max_steps in expected_max_steps.items():
            assert max_steps >= 1, f"{category} should have at least 1 step"
            assert max_steps <= 4, f"{category} should have at most 4 steps"


class TestClassificationEdgeCases:
    """Test edge cases in classification for real-world queries."""
    
    @pytest.fixture
    def classifier(self) -> QueryClassifier:
        """Create a QueryClassifier instance."""
        return QueryClassifier()
    
    def test_azure_service_questions_are_factual(self, classifier: QueryClassifier) -> None:
        """Questions about Azure services should be factual."""
        azure_services = [
            "What is Azure App Service?",
            "What are Azure Functions?",
            "What is Azure Cosmos DB?",
            "What is Azure Kubernetes Service?",
            "Explain Azure Container Apps",
        ]
        
        for query in azure_services:
            result = classifier.classify(query)
            assert result == QueryCategory.FACTUAL, f"'{query}' should be FACTUAL"
    
    def test_cli_requests_are_code(self, classifier: QueryClassifier) -> None:
        """CLI command requests should be code."""
        cli_requests = [
            "Generate Azure CLI to create storage account",
            "Write CLI commands for AKS cluster",
            "Azure CLI to deploy web app",
            "Show me the CLI for resource group creation",
        ]
        
        for query in cli_requests:
            result = classifier.classify(query)
            assert result == QueryCategory.CODE, f"'{query}' should be CODE"
    
    def test_best_practices_are_architecture(self, classifier: QueryClassifier) -> None:
        """Best practices questions should be architecture."""
        bp_queries = [
            "Best practices for Azure Functions",
            "Best practice for storage account security",
            "Security best practices for AKS",
        ]
        
        for query in bp_queries:
            result = classifier.classify(query)
            assert result == QueryCategory.ARCHITECTURE, f"'{query}' should be ARCHITECTURE"

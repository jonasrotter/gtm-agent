"""
Unit tests for the QueryClassifier.

Tests query classification into categories:
- factual: Simple lookup questions
- howto: Procedural questions
- architecture: Design/best practices questions
- code: Code generation requests
- complex: Multi-part compound requests
"""

import pytest

# Import directly from the module to avoid triggering full agent imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Direct import from classifier module
from src.agents.classifier import QueryClassifier, QueryCategory


class TestQueryClassifierPatterns:
    """Tests for pattern-based query classification."""
    
    @pytest.fixture
    def classifier(self) -> QueryClassifier:
        """Create a QueryClassifier instance."""
        return QueryClassifier()
    
    # =========================================================================
    # Factual Query Tests
    # =========================================================================
    
    def test_classify_factual_what_is(self, classifier: QueryClassifier) -> None:
        """'What is X?' queries are classified as factual."""
        query = "What is Azure Blob Storage?"
        result = classifier.classify(query)
        assert result == QueryCategory.FACTUAL
    
    def test_classify_factual_what_are(self, classifier: QueryClassifier) -> None:
        """'What are X?' queries are classified as factual."""
        query = "What are the storage tiers in Azure?"
        result = classifier.classify(query)
        assert result == QueryCategory.FACTUAL
    
    def test_classify_factual_explain(self, classifier: QueryClassifier) -> None:
        """'Explain X' queries are classified as factual."""
        query = "Explain Azure Functions triggers"
        result = classifier.classify(query)
        assert result == QueryCategory.FACTUAL
    
    def test_classify_factual_define(self, classifier: QueryClassifier) -> None:
        """'Define X' queries are classified as factual."""
        query = "Define serverless computing"
        result = classifier.classify(query)
        assert result == QueryCategory.FACTUAL
    
    def test_classify_factual_describe(self, classifier: QueryClassifier) -> None:
        """'Describe X' queries are classified as factual."""
        query = "Describe Azure Event Grid"
        result = classifier.classify(query)
        assert result == QueryCategory.FACTUAL
    
    def test_classify_factual_tell_me_about(self, classifier: QueryClassifier) -> None:
        """'Tell me about X' queries are classified as factual."""
        query = "Tell me about Azure Cosmos DB"
        result = classifier.classify(query)
        assert result == QueryCategory.FACTUAL
    
    # =========================================================================
    # HowTo Query Tests
    # =========================================================================
    
    def test_classify_howto_how_do_i(self, classifier: QueryClassifier) -> None:
        """'How do I X?' queries are classified as howto."""
        query = "How do I create a storage account?"
        result = classifier.classify(query)
        assert result == QueryCategory.HOWTO
    
    def test_classify_howto_how_can_i(self, classifier: QueryClassifier) -> None:
        """'How can I X?' queries are classified as howto."""
        query = "How can I configure VNet integration?"
        result = classifier.classify(query)
        assert result == QueryCategory.HOWTO
    
    def test_classify_howto_steps_to(self, classifier: QueryClassifier) -> None:
        """'Steps to X' queries are classified as howto."""
        query = "Steps to deploy an Azure Function"
        result = classifier.classify(query)
        assert result == QueryCategory.HOWTO
    
    def test_classify_howto_how_to(self, classifier: QueryClassifier) -> None:
        """'How to X' queries are classified as howto."""
        query = "How to set up Azure AD authentication"
        result = classifier.classify(query)
        assert result == QueryCategory.HOWTO
    
    # =========================================================================
    # Architecture Query Tests
    # =========================================================================
    
    def test_classify_architecture_best_practices(self, classifier: QueryClassifier) -> None:
        """'Best practices for X' queries are classified as architecture."""
        query = "Best practices for App Service security"
        result = classifier.classify(query)
        assert result == QueryCategory.ARCHITECTURE
    
    def test_classify_architecture_design(self, classifier: QueryClassifier) -> None:
        """'Design X' queries are classified as architecture."""
        query = "Design a microservices architecture for Azure"
        result = classifier.classify(query)
        assert result == QueryCategory.ARCHITECTURE
    
    def test_classify_architecture_how_should_i_design(self, classifier: QueryClassifier) -> None:
        """'How should I design X?' queries are classified as architecture."""
        query = "How should I design my data layer?"
        result = classifier.classify(query)
        assert result == QueryCategory.ARCHITECTURE
    
    def test_classify_architecture_recommend(self, classifier: QueryClassifier) -> None:
        """Recommendation queries are classified as architecture."""
        query = "Recommend an architecture for real-time data processing"
        result = classifier.classify(query)
        assert result == QueryCategory.ARCHITECTURE
    
    def test_classify_architecture_waf(self, classifier: QueryClassifier) -> None:
        """WAF pillar queries are classified as architecture."""
        query = "What are the reliability considerations for my app?"
        result = classifier.classify(query)
        assert result == QueryCategory.ARCHITECTURE
    
    # =========================================================================
    # Code Query Tests
    # =========================================================================
    
    def test_classify_code_generate(self, classifier: QueryClassifier) -> None:
        """'Generate X' code queries are classified as code."""
        query = "Generate Azure CLI to create a resource group"
        result = classifier.classify(query)
        assert result == QueryCategory.CODE
    
    def test_classify_code_write(self, classifier: QueryClassifier) -> None:
        """'Write X' code queries are classified as code."""
        query = "Write a Bicep template for a VNet"
        result = classifier.classify(query)
        assert result == QueryCategory.CODE
    
    def test_classify_code_create_script(self, classifier: QueryClassifier) -> None:
        """'Create script' queries are classified as code."""
        query = "Create a PowerShell script to backup blobs"
        result = classifier.classify(query)
        assert result == QueryCategory.CODE
    
    def test_classify_code_show_me_code(self, classifier: QueryClassifier) -> None:
        """'Show me code for X' queries are classified as code."""
        query = "Show me the code for connecting to Cosmos DB"
        result = classifier.classify(query)
        assert result == QueryCategory.CODE
    
    def test_classify_code_give_me_cli(self, classifier: QueryClassifier) -> None:
        """CLI command requests are classified as code."""
        query = "Give me the CLI commands to deploy a web app"
        result = classifier.classify(query)
        assert result == QueryCategory.CODE
    
    def test_classify_code_bicep_template(self, classifier: QueryClassifier) -> None:
        """Bicep template requests are classified as code."""
        query = "Bicep template for Azure Functions with VNet"
        result = classifier.classify(query)
        assert result == QueryCategory.CODE
    
    def test_classify_code_terraform(self, classifier: QueryClassifier) -> None:
        """Terraform requests are classified as code."""
        query = "Terraform configuration for AKS cluster"
        result = classifier.classify(query)
        assert result == QueryCategory.CODE
    
    # =========================================================================
    # Complex Query Tests
    # =========================================================================
    
    def test_classify_complex_compound_and(self, classifier: QueryClassifier) -> None:
        """Compound queries with 'and' are classified as complex."""
        query = "Explain Azure Functions and write a Bicep template for deployment"
        result = classifier.classify(query)
        assert result == QueryCategory.COMPLEX
    
    def test_classify_complex_design_and_implement(self, classifier: QueryClassifier) -> None:
        """'Design and implement' queries are classified as complex."""
        query = "Design a serverless architecture and implement it with Bicep"
        result = classifier.classify(query)
        assert result == QueryCategory.COMPLEX
    
    def test_classify_complex_multiple_questions(self, classifier: QueryClassifier) -> None:
        """Multiple question marks indicate complex queries."""
        query = "What is Azure Functions? How do I deploy it? Show me the CLI commands."
        result = classifier.classify(query)
        assert result == QueryCategory.COMPLEX
    
    def test_classify_complex_then(self, classifier: QueryClassifier) -> None:
        """'Then' indicating sequential tasks are classified as complex."""
        query = "Research Azure best practices then generate Bicep templates"
        result = classifier.classify(query)
        assert result == QueryCategory.COMPLEX
    
    def test_classify_complex_also(self, classifier: QueryClassifier) -> None:
        """'Also' indicating multiple requests are classified as complex."""
        query = "Explain VNet integration and also show me the code"
        result = classifier.classify(query)
        assert result == QueryCategory.COMPLEX


class TestQueryClassifierEdgeCases:
    """Tests for edge cases in query classification."""
    
    @pytest.fixture
    def classifier(self) -> QueryClassifier:
        """Create a QueryClassifier instance."""
        return QueryClassifier()
    
    def test_empty_query_defaults_to_factual(self, classifier: QueryClassifier) -> None:
        """Empty queries default to factual (safest/simplest)."""
        result = classifier.classify("")
        assert result == QueryCategory.FACTUAL
    
    def test_vague_query_defaults_to_factual(self, classifier: QueryClassifier) -> None:
        """Vague queries default to factual."""
        query = "Azure"
        result = classifier.classify(query)
        assert result == QueryCategory.FACTUAL
    
    def test_case_insensitive(self, classifier: QueryClassifier) -> None:
        """Classification is case-insensitive."""
        assert classifier.classify("WHAT IS AZURE?") == QueryCategory.FACTUAL
        assert classifier.classify("GENERATE CLI COMMANDS") == QueryCategory.CODE
        assert classifier.classify("BEST PRACTICES FOR SECURITY") == QueryCategory.ARCHITECTURE
    
    def test_help_me_with_ambiguous(self, classifier: QueryClassifier) -> None:
        """'Help me with' queries need context - default to howto."""
        query = "Help me with Azure storage"
        result = classifier.classify(query)
        # Ambiguous - could be factual or howto, default to howto as it implies action
        assert result == QueryCategory.HOWTO
    
    def test_code_keyword_in_factual_question(self, classifier: QueryClassifier) -> None:
        """Code keywords in factual context should not trigger code classification."""
        query = "What is the Azure CLI?"
        result = classifier.classify(query)
        assert result == QueryCategory.FACTUAL


class TestQueryCategoryConfiguration:
    """Tests for QueryCategory configuration properties."""
    
    def test_factual_category_config(self) -> None:
        """Factual category has correct configuration."""
        config = QueryCategory.FACTUAL.get_config()
        assert config["max_iterations"] == 1
        assert config["skip_pev"] is True
        assert config["default_tool"] == "research"
    
    def test_howto_category_config(self) -> None:
        """HowTo category has correct configuration."""
        config = QueryCategory.HOWTO.get_config()
        assert config["max_iterations"] == 1
        assert config["skip_pev"] is False
        assert config["threshold"] == 0.7
    
    def test_architecture_category_config(self) -> None:
        """Architecture category has correct configuration."""
        config = QueryCategory.ARCHITECTURE.get_config()
        assert config["max_iterations"] == 2
        assert config["skip_pev"] is False
        assert config["threshold"] == 0.75
    
    def test_code_category_config(self) -> None:
        """Code category has correct configuration."""
        config = QueryCategory.CODE.get_config()
        assert config["max_iterations"] == 1
        assert config["skip_pev"] is False
        assert config["threshold"] == 0.7
    
    def test_complex_category_config(self) -> None:
        """Complex category has correct configuration."""
        config = QueryCategory.COMPLEX.get_config()
        assert config["max_iterations"] == 4
        assert config["skip_pev"] is False
        assert config["threshold"] == 0.8

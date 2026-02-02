"""
Unit tests for the refactored agents.

These tests verify the agent module structure and interfaces without
requiring Azure credentials (using mocks where needed).
"""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock


class TestBaseModule:
    """Tests for the base module."""
    
    def test_base_module_exports(self) -> None:
        """Base module exports expected items."""
        from src.agents.base import (
            MICROSOFT_LEARN_MCP_URL,
            AZURE_MCP_URL,
            create_azure_chat_client,
            ChatAgent,
            HostedMCPTool,
            ai_function,
        )
        
        assert MICROSOFT_LEARN_MCP_URL == "https://learn.microsoft.com/api/mcp"
        assert AZURE_MCP_URL == "https://api.mcp.github.com"
        assert callable(create_azure_chat_client)

    def test_create_azure_chat_client_requires_env_vars(self) -> None:
        """create_azure_chat_client raises when env vars missing."""
        from src.agents.base import create_azure_chat_client
        
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="AZURE_OPENAI_ENDPOINT"):
                create_azure_chat_client()

    def test_create_azure_chat_client_with_env_vars(self) -> None:
        """create_azure_chat_client works with proper env vars."""
        from src.agents.base import create_azure_chat_client
        
        with patch.dict('os.environ', {
            'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
            'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
        }):
            client = create_azure_chat_client()
            assert client is not None


class TestResearcherAgent:
    """Tests for the ResearcherAgent."""
    
    def test_researcher_module_imports(self) -> None:
        """ResearcherAgent can be imported."""
        from src.agents.researcher import ResearcherAgent, get_researcher_agent
        assert ResearcherAgent is not None
        assert callable(get_researcher_agent)

    def test_researcher_has_expected_attributes(self) -> None:
        """ResearcherAgent has expected attributes after init."""
        with patch.dict('os.environ', {
            'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
            'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
        }):
            from src.agents.researcher import ResearcherAgent
            
            agent = ResearcherAgent()
            # Has either mcp_tool (Azure AI) or uses local tools
            assert hasattr(agent, 'agent')
            assert hasattr(agent, 'run')
            assert hasattr(agent, 'as_tool')

    def test_researcher_as_tool_returns_callable(self) -> None:
        """ResearcherAgent.as_tool() returns a tool."""
        with patch.dict('os.environ', {
            'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
            'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
        }):
            from src.agents.researcher import ResearcherAgent
            
            agent = ResearcherAgent()
            tool = agent.as_tool()
            assert tool is not None


class TestArchitectAgent:
    """Tests for the ArchitectAgent."""
    
    def test_architect_module_imports(self) -> None:
        """ArchitectAgent can be imported."""
        from src.agents.architect import ArchitectAgent, get_architect_agent
        assert ArchitectAgent is not None
        assert callable(get_architect_agent)

    def test_architect_has_expected_attributes(self) -> None:
        """ArchitectAgent has expected attributes after init."""
        with patch.dict('os.environ', {
            'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
            'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
        }):
            from src.agents.architect import ArchitectAgent
            
            agent = ArchitectAgent()
            # Has either mcp_tool (Azure AI) or uses local tools
            assert hasattr(agent, 'agent')
            assert hasattr(agent, 'run')
            assert hasattr(agent, 'as_tool')

    def test_architect_as_tool_returns_callable(self) -> None:
        """ArchitectAgent.as_tool() returns a tool."""
        with patch.dict('os.environ', {
            'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
            'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
        }):
            from src.agents.architect import ArchitectAgent
            
            agent = ArchitectAgent()
            tool = agent.as_tool()
            assert tool is not None


class TestGHCPCodingAgent:
    """Tests for the GHCPCodingAgent."""
    
    def test_ghcp_coding_agent_module_imports(self) -> None:
        """GHCPCodingAgent can be imported."""
        from src.agents.ghcp_coding_agent import GHCPCodingAgent, get_ghcp_coding_agent
        assert GHCPCodingAgent is not None
        assert callable(get_ghcp_coding_agent)

    def test_ghcp_coding_agent_init(self) -> None:
        """GHCPCodingAgent can be initialized."""
        from src.agents.ghcp_coding_agent import GHCPCodingAgent
        
        agent = GHCPCodingAgent()
        assert agent is not None
        assert hasattr(agent, 'run')
        assert hasattr(agent, 'as_tool')
        assert hasattr(agent, 'start')
        assert hasattr(agent, 'close')

    def test_ghcp_coding_agent_as_tool_returns_callable(self) -> None:
        """GHCPCodingAgent.as_tool() returns a tool."""
        from src.agents.ghcp_coding_agent import GHCPCodingAgent
        
        agent = GHCPCodingAgent()
        tool = agent.as_tool()
        assert tool is not None
        assert callable(tool)

    def test_custom_tools_defined(self) -> None:
        """Custom tools are properly defined with @define_tool."""
        from src.agents.ghcp_coding_agent import create_test_plan, generate_cli_command
        
        # These are Tool objects created by @define_tool decorator
        # Check they have the expected structure
        assert create_test_plan is not None
        assert generate_cli_command is not None
        
        # Tool objects have a 'name' and 'handler' attribute
        assert hasattr(create_test_plan, 'name')
        assert hasattr(create_test_plan, 'handler')
        assert hasattr(generate_cli_command, 'name')
        assert hasattr(generate_cli_command, 'handler')
        
        # Verify tool names
        assert create_test_plan.name == 'create_test_plan'
        assert generate_cli_command.name == 'generate_cli_command'


class TestSolutionEngineerAgent:
    """Tests for the SolutionEngineerAgent."""
    
    def test_solution_engineer_module_imports(self) -> None:
        """SolutionEngineerAgent can be imported."""
        from src.agents.solution_engineer import SolutionEngineerAgent, get_solution_engineer_agent
        assert SolutionEngineerAgent is not None
        assert callable(get_solution_engineer_agent)

    def test_solution_engineer_has_sub_agents(self) -> None:
        """SolutionEngineerAgent creates sub-agents."""
        with patch.dict('os.environ', {
            'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
            'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
        }):
            from src.agents.solution_engineer import SolutionEngineerAgent
            
            agent = SolutionEngineerAgent()
            assert hasattr(agent, 'researcher')
            assert hasattr(agent, 'architect')
            assert hasattr(agent, 'ghcp_coding')
            assert hasattr(agent, 'agent')

    def test_solution_engineer_has_run_method(self) -> None:
        """SolutionEngineerAgent has async run method."""
        with patch.dict('os.environ', {
            'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
            'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
        }):
            from src.agents.solution_engineer import SolutionEngineerAgent
            import inspect
            
            agent = SolutionEngineerAgent()
            assert hasattr(agent, 'run')
            assert inspect.iscoroutinefunction(agent.run)


class TestAgentsInit:
    """Tests for agents package __init__."""
    
    def test_agents_package_exports(self) -> None:
        """Agents package exports all agents."""
        from src.agents import (
            ResearcherAgent,
            ArchitectAgent,
            GHCPCodingAgent,
            SolutionEngineerAgent,
        )
        
        assert ResearcherAgent is not None
        assert ArchitectAgent is not None
        assert GHCPCodingAgent is not None
        assert SolutionEngineerAgent is not None

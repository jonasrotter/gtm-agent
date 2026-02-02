"""
Azure OpenAI chat client for agent-framework integration.

Implements the ChatClientProtocol from agent_framework to enable
ChatAgent instances to communicate with Azure OpenAI.
"""

from collections.abc import AsyncGenerator, MutableSequence, Sequence
from typing import Any, Literal

from azure.identity import DefaultAzureCredential
from openai import AsyncAzureOpenAI

from agent_framework._clients import BaseChatClient
from agent_framework._types import (
    ChatMessage,
    ChatOptions,
    ChatResponse,
    Content,
    Role,
)
from agent_framework import use_function_invocation

from src.config import get_settings
from src.utils.logging import get_logger


logger = get_logger(__name__)


@use_function_invocation
class AzureOpenAIChatClient(BaseChatClient):
    """
    Azure OpenAI chat client implementing agent_framework.BaseChatClient.
    
    Uses Azure OpenAI Service via the openai SDK with Azure AD authentication.
    Implements the required _inner_get_response and _inner_get_streaming_response
    abstract methods from BaseChatClient.
    
    The @use_function_invocation decorator enables automatic tool/function calling
    support, allowing the agent framework to execute tools and return results.
    """
    
    def __init__(
        self,
        endpoint: str | None = None,
        deployment: str | None = None,
        api_version: str | None = None,
    ) -> None:
        """
        Initialize Azure OpenAI chat client.
        
        Args:
            endpoint: Azure OpenAI endpoint URL. Defaults to settings.
            deployment: Model deployment name. Defaults to settings.
            api_version: API version. Defaults to settings.
        """
        super().__init__()  # Initialize BaseChatClient
        
        settings = get_settings()
        
        self._endpoint = endpoint or settings.azure_openai_endpoint
        self._deployment = deployment or settings.azure_openai_deployment
        self._api_version = api_version or settings.azure_openai_api_version
        
        # Initialize Azure OpenAI client with DefaultAzureCredential
        self._credential = DefaultAzureCredential()
        self._client: AsyncAzureOpenAI | None = None
        
        # Track tool calls for external access
        self._last_tool_calls: list[str] = []
        
        logger.info(
            "AzureOpenAIChatClient initialized",
            endpoint=self._endpoint[:50] + "..." if len(self._endpoint) > 50 else self._endpoint,
            deployment=self._deployment,
            api_version=self._api_version,
        )
    
    def clear_tool_call_tracking(self) -> None:
        """Clear the tracked tool calls. Call this before starting a new conversation turn."""
        self._last_tool_calls = []
    
    @property
    def client(self) -> AsyncAzureOpenAI:
        """Lazy-initialize and return the Azure OpenAI client."""
        if self._client is None:
            self._client = AsyncAzureOpenAI(
                azure_endpoint=self._endpoint,
                azure_ad_token_provider=self._get_token,
                api_version=self._api_version,
            )
        return self._client
    
    def _get_token(self) -> str:
        """Get Azure AD token for authentication."""
        token = self._credential.get_token("https://cognitiveservices.azure.com/.default")
        return token.token
    
    def _convert_messages(
        self,
        messages: str | ChatMessage | list[str] | list[ChatMessage],
    ) -> list[dict[str, Any]]:
        """
        Convert agent_framework messages to OpenAI format.
        
        Handles text messages, function calls, and function results.
        
        Args:
            messages: Input messages in various formats.
            
        Returns:
            List of message dicts in OpenAI format.
        """
        if isinstance(messages, str):
            return [{"role": "user", "content": messages}]
        
        if isinstance(messages, ChatMessage):
            messages = [messages]
        
        result = []
        for msg in messages:
            if isinstance(msg, str):
                result.append({"role": "user", "content": msg})
            elif isinstance(msg, ChatMessage):
                role = self._normalize_role(msg.role)
                
                # Check if message has contents with function calls or results
                # Using content.type attribute to identify content types
                if msg.contents:
                    has_function_calls = any(
                        getattr(c, "type", None) == "function_call" for c in msg.contents
                    )
                    has_function_results = any(
                        getattr(c, "type", None) == "function_result" for c in msg.contents
                    )
                    
                    if has_function_calls:
                        # Assistant message with tool calls
                        tool_calls = []
                        text_content = ""
                        for c in msg.contents:
                            if getattr(c, "type", None) == "function_call":
                                tool_calls.append({
                                    "id": c.call_id,
                                    "type": "function",
                                    "function": {
                                        "name": c.name,
                                        "arguments": c.arguments if isinstance(c.arguments, str) else str(c.arguments),
                                    },
                                })
                            elif getattr(c, "type", None) == "text":
                                text_content += getattr(c, "text", "") or ""
                        
                        msg_dict: dict[str, Any] = {"role": "assistant"}
                        if text_content:
                            msg_dict["content"] = text_content
                        if tool_calls:
                            msg_dict["tool_calls"] = tool_calls
                        result.append(msg_dict)
                        
                    elif has_function_results:
                        # Tool result messages - each result is a separate message
                        for c in msg.contents:
                            if getattr(c, "type", None) == "function_result":
                                result.append({
                                    "role": "tool",
                                    "tool_call_id": c.call_id,
                                    "content": str(c.result) if c.result is not None else "",
                                })
                    else:
                        # Regular message with contents
                        content = msg.text or ""
                        result.append({"role": role, "content": content})
                else:
                    # Simple text message
                    content = msg.text or ""
                    result.append({"role": role, "content": content})
            else:
                # Assume it's already a dict
                result.append(msg)
        
        return result
    
    def _normalize_role(self, role: Role | str | dict[str, Any]) -> str:
        """Normalize role to string format for OpenAI API."""
        if isinstance(role, str):
            return role
        if isinstance(role, dict):
            return role.get("role", "user")
        # Role enum or similar
        return str(role.value if hasattr(role, "value") else role)
    
    def _convert_tools(
        self,
        tools: Any,
    ) -> list[dict[str, Any]] | None:
        """Convert agent_framework tools to OpenAI function format."""
        if tools is None:
            return None
        
        if not isinstance(tools, (list, tuple)):
            tools = [tools]
        
        converted = []
        for tool in tools:
            if hasattr(tool, "to_dict"):
                # agent_framework tool with to_dict method
                tool_dict = tool.to_dict()
                # Extract OpenAI-compatible fields from agent_framework format
                # agent_framework uses 'input_model' but OpenAI expects 'parameters'
                parameters = tool_dict.get("input_model") or tool_dict.get("parameters") or {"type": "object", "properties": {}}
                converted.append({
                    "type": "function",
                    "function": {
                        "name": tool_dict.get("name", "unknown"),
                        "description": tool_dict.get("description", ""),
                        "parameters": parameters,
                    },
                })
            elif hasattr(tool, "__name__") and hasattr(tool, "__doc__"):
                # Function decorated with @ai_function
                converted.append({
                    "type": "function",
                    "function": {
                        "name": tool.__name__,
                        "description": tool.__doc__ or "",
                        "parameters": getattr(tool, "parameters", {"type": "object", "properties": {}}),
                    },
                })
            elif isinstance(tool, dict):
                converted.append(tool)
        
        return converted if converted else None
    
    async def _inner_get_response(
        self,
        *,
        messages: MutableSequence[ChatMessage],
        chat_options: ChatOptions | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        """
        Internal method called by BaseChatClient.get_response().
        
        This is the abstract method that must be implemented.
        
        Args:
            messages: List of ChatMessage objects.
            chat_options: Chat configuration options (ChatOptions object or dict).
            **kwargs: Additional parameters (includes 'options' from agent_framework).
            
        Returns:
            ChatResponse with the model's response.
        """
        # Merge options from different sources:
        # 1. chat_options parameter (if provided)
        # 2. kwargs['options'] (from agent_framework ChatAgent)
        merged_options: dict[str, Any] = {}
        
        # First apply kwargs['options'] (framework default options)
        if "options" in kwargs and kwargs["options"]:
            merged_options.update(kwargs["options"])
        
        # Then overlay chat_options (explicit options)
        if chat_options:
            merged_options.update(chat_options)
        
        openai_messages = self._convert_messages(list(messages))
        openai_tools = self._convert_tools(merged_options.get("tools"))
        
        # Build request kwargs
        request_kwargs: dict[str, Any] = {
            "model": merged_options.get("model_id") or self._deployment,
            "messages": openai_messages,
        }
        
        # Apply chat options
        if merged_options.get("temperature") is not None:
            request_kwargs["temperature"] = merged_options["temperature"]
        if merged_options.get("max_tokens") is not None:
            request_kwargs["max_tokens"] = merged_options["max_tokens"]
        if merged_options.get("frequency_penalty") is not None:
            request_kwargs["frequency_penalty"] = merged_options["frequency_penalty"]
        if merged_options.get("presence_penalty") is not None:
            request_kwargs["presence_penalty"] = merged_options["presence_penalty"]
        if merged_options.get("top_p") is not None:
            request_kwargs["top_p"] = merged_options["top_p"]
        if merged_options.get("stop") is not None:
            request_kwargs["stop"] = merged_options["stop"]
        if merged_options.get("seed") is not None:
            request_kwargs["seed"] = merged_options["seed"]
        if merged_options.get("user") is not None:
            request_kwargs["user"] = merged_options["user"]
        
        if openai_tools:
            request_kwargs["tools"] = openai_tools
            if merged_options.get("tool_choice"):
                # Convert ToolMode to OpenAI format (just the string "auto", "required", "none")
                tool_choice = merged_options["tool_choice"]
                request_kwargs["tool_choice"] = str(tool_choice)
        
        # Debug logging
        logger.debug("OpenAI request", tools_count=len(openai_tools) if openai_tools else 0)
        
        try:
            response = await self.client.chat.completions.create(**request_kwargs)
            
            # Extract response content
            choice = response.choices[0] if response.choices else None
            message = choice.message if choice else None
            content = message.content if message else ""
            
            # Track tool calls for external access (e.g., by SolutionEngineerAgent)
            # Append to list rather than replace, so we keep history of all tool calls in a session
            if message and message.tool_calls:
                new_tools = [tc.function.name for tc in message.tool_calls]
                self._last_tool_calls.extend(new_tools)
                logger.debug("Tool calls received", count=len(message.tool_calls), tools=new_tools)
            
            # Build contents list - include text and/or tool calls
            contents: list[Any] = []
            
            # Add text content if present
            if content:
                contents.append(Content.from_text(content))
            
            # Add function calls if present (tool calls from the LLM)
            if message and message.tool_calls:
                for tool_call in message.tool_calls:
                    contents.append(
                        Content.from_function_call(
                            call_id=tool_call.id,
                            name=tool_call.function.name,
                            arguments=tool_call.function.arguments,
                        )
                    )
            
            # Build ChatResponse
            return ChatResponse(
                messages=[
                    ChatMessage(
                        role="assistant",
                        contents=contents if contents else None,
                        text=content or "",
                    )
                ],
            )
            
        except Exception as e:
            logger.error("Azure OpenAI _inner_get_response failed", error=str(e))
            raise
    
    async def _inner_get_streaming_response(
        self,
        *,
        messages: MutableSequence[ChatMessage],
        chat_options: ChatOptions | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> AsyncGenerator[Any, None]:
        """
        Internal streaming method called by BaseChatClient.get_streaming_response().
        
        This is the abstract method that must be implemented.
        
        Args:
            messages: List of ChatMessage objects.
            chat_options: Chat configuration options (ChatOptions object or dict).
            **kwargs: Additional parameters (includes 'options' from agent_framework).
            
        Yields:
            ChatResponseUpdate chunks as they are generated.
        """
        from agent_framework._types import ChatResponseUpdate
        
        # Merge options from different sources
        merged_options: dict[str, Any] = {}
        if "options" in kwargs and kwargs["options"]:
            merged_options.update(kwargs["options"])
        if chat_options:
            merged_options.update(chat_options)
        
        openai_messages = self._convert_messages(list(messages))
        openai_tools = self._convert_tools(merged_options.get("tools"))
        
        request_kwargs: dict[str, Any] = {
            "model": merged_options.get("model_id") or self._deployment,
            "messages": openai_messages,
            "stream": True,
        }
        
        if merged_options.get("temperature") is not None:
            request_kwargs["temperature"] = merged_options["temperature"]
        if merged_options.get("max_tokens") is not None:
            request_kwargs["max_tokens"] = merged_options["max_tokens"]
        
        if openai_tools:
            request_kwargs["tools"] = openai_tools
        
        try:
            stream = await self.client.chat.completions.create(**request_kwargs)
            
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        yield ChatResponseUpdate(
                            contents=[Content.from_text(delta.content)],
                            role="assistant",
                        )
                        
        except Exception as e:
            logger.error("Azure OpenAI _inner_get_streaming_response failed", error=str(e))
            raise


def create_azure_openai_client(
    endpoint: str | None = None,
    deployment: str | None = None,
    api_version: str | None = None,
) -> AzureOpenAIChatClient:
    """
    Factory function to create an Azure OpenAI chat client.
    
    Args:
        endpoint: Azure OpenAI endpoint URL. Defaults to settings.
        deployment: Model deployment name. Defaults to settings.
        api_version: API version. Defaults to settings.
        
    Returns:
        AzureOpenAIChatClient instance.
    """
    return AzureOpenAIChatClient(
        endpoint=endpoint,
        deployment=deployment,
        api_version=api_version,
    )


# Global client instance (lazy-initialized)
_azure_chat_client: AzureOpenAIChatClient | None = None


def get_azure_chat_client() -> AzureOpenAIChatClient:
    """
    Get the global Azure OpenAI chat client instance.
    
    Returns:
        AzureOpenAIChatClient singleton instance.
    """
    global _azure_chat_client
    if _azure_chat_client is None:
        _azure_chat_client = create_azure_openai_client()
    return _azure_chat_client

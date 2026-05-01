"""MCP Server implementation."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ServerConfig:
    """Configuration for MCP server."""

    name: str = "pheno-mcp"
    version: str = "0.1.0"


@dataclass
class Tool:
    """Represents an MCP tool."""

    name: str
    description: str
    input_schema: dict[str, Any] = field(default_factory=dict)
    handler: Callable[..., Coroutine[Any, Any, Any]] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert tool to dictionary format."""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema,
        }


@dataclass
class Resource:
    """Represents an MCP resource."""

    uri: str
    name: str
    description: str = ""
    mime_type: str = "text/plain"

    def to_dict(self) -> dict[str, Any]:
        """Convert resource to dictionary format."""
        return {
            "uri": self.uri,
            "name": self.name,
            "description": self.description,
            "mimeType": self.mime_type,
        }


@dataclass
class Prompt:
    """Represents an MCP prompt."""

    name: str
    description: str
    arguments: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert prompt to dictionary format."""
        return {
            "name": self.name,
            "description": self.description,
            "arguments": self.arguments,
        }


class Server:
    """MCP server implementation."""

    def __init__(self, config: ServerConfig | None = None) -> None:
        """Initialize the MCP server.

        Args:
            config: Server configuration. Uses defaults if not provided.
        """
        self._config = config or ServerConfig()
        self._tools: dict[str, Tool] = {}
        self._resources: dict[str, Resource] = {}
        self._prompts: dict[str, Prompt] = {}

    @property
    def name(self) -> str:
        """Get server name."""
        return self._config.name

    @property
    def version(self) -> str:
        """Get server version."""
        return self._config.version

    def register_tool(self, tool: Tool) -> None:
        """Register a tool with the server.

        Args:
            tool: Tool to register.
        """
        self._tools[tool.name] = tool

    def register_resource(self, resource: Resource) -> None:
        """Register a resource with the server.

        Args:
            resource: Resource to register.
        """
        self._resources[resource.uri] = resource

    def register_prompt(self, prompt: Prompt) -> None:
        """Register a prompt with the server.

        Args:
            prompt: Prompt to register.
        """
        self._prompts[prompt.name] = prompt

    def list_tools(self) -> list[dict[str, Any]]:
        """List all registered tools."""
        return [tool.to_dict() for tool in self._tools.values()]

    def list_resources(self) -> list[dict[str, Any]]:
        """List all registered resources."""
        return [resource.to_dict() for resource in self._resources.values()]

    def list_prompts(self) -> list[dict[str, Any]]:
        """List all registered prompts."""
        return [prompt.to_dict() for prompt in self._prompts.values()]

    async def handle_request(self, method: str, params: dict[str, Any] | None = None) -> Any:
        """Handle an MCP request.

        Args:
            method: Request method name.
            params: Request parameters.

        Returns:
            Response data.
        """
        params = params or {}

        if method == "tools/list":
            return {"tools": self.list_tools()}
        elif method == "resources/list":
            return {"resources": self.list_resources()}
        elif method == "prompts/list":
            return {"prompts": self.list_prompts()}
        elif method == "tools/call":
            tool_name = params.get("name")
            if not tool_name:
                return None
            arguments = params.get("arguments", {})
            if tool_name not in self._tools:
                msg = f"Unknown tool: {tool_name}"
                raise ValueError(msg)
            tool = self._tools[tool_name]
            if tool.handler:
                return await tool.handler(arguments)
            return None
        else:
            msg = f"Unknown method: {method}"
            raise ValueError(msg)

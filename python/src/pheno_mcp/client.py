"""MCP Client implementation."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ClientConfig:
    """Configuration for MCP client."""

    server_command: list[str] = field(default_factory=list)
    server_env: dict[str, str] = field(default_factory=dict)
    timeout: float = 30.0


class Client:
    """MCP client for connecting to Model Context Protocol servers."""

    def __init__(self, config: ClientConfig | None = None) -> None:
        """Initialize the MCP client.

        Args:
            config: Client configuration. Uses defaults if not provided.
        """
        self._config = config or ClientConfig()
        self._connected = False
        self._tools: dict[str, Callable[..., Coroutine[Any, Any, Any]]] = {}
        self._resources: dict[str, Any] = {}

    @property
    def is_connected(self) -> bool:
        """Check if client is connected to a server."""
        return self._connected

    async def connect(self) -> None:
        """Connect to the MCP server."""
        if self._connected:
            return

        if not self._config.server_command:
            msg = "No server command configured"
            raise RuntimeError(msg)

        self._connected = True

    async def disconnect(self) -> None:
        """Disconnect from the MCP server."""
        self._connected = False
        self._tools.clear()
        self._resources.clear()

    async def call_tool(
        self, name: str, arguments: dict[str, Any] | None = None
    ) -> Any:
        """Call a tool on the MCP server.

        Args:
            name: Name of the tool to call.
            arguments: Arguments to pass to the tool.

        Returns:
            Result of the tool call.
        """
        if not self._connected:
            msg = "Not connected to server"
            raise RuntimeError(msg)

        if name not in self._tools:
            msg = f"Unknown tool: {name}"
            raise ValueError(msg)

        return await self._tools[name](arguments or {})

    async def list_tools(self) -> list[dict[str, Any]]:
        """List available tools from the server."""
        if not self._connected:
            msg = "Not connected to server"
            raise RuntimeError(msg)

        return []

    async def list_resources(self) -> list[dict[str, Any]]:
        """List available resources from the server."""
        if not self._connected:
            msg = "Not connected to server"
            raise RuntimeError(msg)

        return []

    async def read_resource(self, uri: str) -> Any:
        """Read a resource from the server.

        Args:
            uri: URI of the resource to read.

        Returns:
            Resource contents.
        """
        if not self._connected:
            msg = "Not connected to server"
            raise RuntimeError(msg)

        if uri not in self._resources:
            msg = f"Unknown resource: {uri}"
            raise ValueError(msg)

        return self._resources[uri]

    async def __aenter__(self) -> Client:
        """Enter async context manager."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context manager."""
        await self.disconnect()

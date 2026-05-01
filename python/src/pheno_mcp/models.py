"""MCP data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Tool:
    """Represents an MCP tool definition."""

    name: str
    description: str
    input_schema: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary format."""
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
    contents: Any = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "uri": self.uri,
            "name": self.name,
            "description": self.description,
            "mimeType": self.mime_type,
        }


@dataclass
class Prompt:
    """Represents an MCP prompt definition."""

    name: str
    description: str
    arguments: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "name": self.name,
            "description": self.description,
            "arguments": self.arguments,
        }


@dataclass
class CallToolResult:
    """Result of a tool call."""

    content: list[dict[str, Any]]
    is_error: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "content": self.content,
            "isError": self.is_error,
        }


@dataclass
class ListResourcesResult:
    """Result of listing resources."""

    resources: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary format."""
        return {"resources": self.resources}

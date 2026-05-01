"""Tests for pheno_mcp models module."""

import pytest

from pheno_mcp.models import (
    Tool,
    Resource,
    Prompt,
    CallToolResult,
    ListResourcesResult,
)


class TestToolModel:
    """Test Tool model."""

    def test_tool_creation(self):
        """Test creating a tool."""
        tool = Tool(name="search", description="Search resources")
        assert tool.name == "search"
        assert tool.description == "Search resources"
        assert tool.input_schema == {}

    def test_tool_with_input_schema(self):
        """Test creating a tool with input schema."""
        schema = {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "limit": {"type": "integer", "description": "Max results"},
            },
            "required": ["query"],
        }
        tool = Tool(name="search", description="Search resources", input_schema=schema)
        assert tool.input_schema == schema
        assert "properties" in tool.input_schema

    def test_tool_to_dict(self):
        """Test tool serialization."""
        tool = Tool(
            name="greet",
            description="Greet a user",
            input_schema={"type": "object"},
        )
        result = tool.to_dict()
        assert result["name"] == "greet"
        assert result["description"] == "Greet a user"
        assert result["inputSchema"]["type"] == "object"


class TestResourceModel:
    """Test Resource model."""

    def test_resource_creation_defaults(self):
        """Test creating a resource with defaults."""
        resource = Resource(uri="file:///data.txt", name="data")
        assert resource.uri == "file:///data.txt"
        assert resource.name == "data"
        assert resource.description == ""
        assert resource.mime_type == "text/plain"
        assert resource.contents is None

    def test_resource_creation_full(self):
        """Test creating a resource with all fields."""
        contents = {"key": "value"}
        resource = Resource(
            uri="memory://cache/test",
            name="cache",
            description="Memory cache resource",
            mime_type="application/json",
            contents=contents,
        )
        assert resource.contents == contents

    def test_resource_to_dict(self):
        """Test resource serialization."""
        resource = Resource(
            uri="https://api.example.com/users",
            name="users",
            description="User API endpoint",
            mime_type="application/json",
        )
        result = resource.to_dict()
        assert result["uri"] == "https://api.example.com/users"
        assert result["name"] == "users"
        assert result["description"] == "User API endpoint"
        assert result["mimeType"] == "application/json"
        assert "contents" not in result  # contents not serialized

    def test_resource_mime_types(self):
        """Test various MIME types."""
        test_cases = [
            ("text/plain", "file:///readme.txt"),
            ("application/json", "file:///data.json"),
            ("image/png", "file:///image.png"),
            ("text/html", "file:///index.html"),
        ]
        for mime_type, uri in test_cases:
            resource = Resource(uri=uri, name=uri.split("/")[-1], mime_type=mime_type)
            assert resource.mime_type == mime_type


class TestPromptModel:
    """Test Prompt model."""

    def test_prompt_creation(self):
        """Test creating a prompt."""
        prompt = Prompt(name="summarize", description="Summarize text")
        assert prompt.name == "summarize"
        assert prompt.description == "Summarize text"
        assert prompt.arguments == []

    def test_prompt_with_arguments(self):
        """Test creating a prompt with arguments."""
        arguments = [
            {"name": "text", "description": "Text to summarize", "required": True},
            {"name": "length", "description": "Summary length", "required": False},
        ]
        prompt = Prompt(
            name="summarize",
            description="Summarize text",
            arguments=arguments,
        )
        assert len(prompt.arguments) == 2
        assert prompt.arguments[0]["name"] == "text"
        assert prompt.arguments[1]["name"] == "length"

    def test_prompt_to_dict(self):
        """Test prompt serialization."""
        prompt = Prompt(
            name="code_review",
            description="Review code changes",
            arguments=[
                {"name": "diff", "description": "Code diff", "required": True},
            ],
        )
        result = prompt.to_dict()
        assert result["name"] == "code_review"
        assert result["description"] == "Review code changes"
        assert len(result["arguments"]) == 1


class TestCallToolResult:
    """Test CallToolResult model."""

    def test_result_creation_default(self):
        """Test creating a result with defaults."""
        result = CallToolResult(content=[{"type": "text", "text": "hello"}])
        assert result.content[0]["text"] == "hello"
        assert result.is_error is False

    def test_result_creation_error(self):
        """Test creating an error result."""
        result = CallToolResult(
            content=[{"type": "text", "text": "error message"}],
            is_error=True,
        )
        assert result.is_error is True

    def test_result_to_dict(self):
        """Test result serialization."""
        result = CallToolResult(
            content=[
                {"type": "text", "text": "success"},
            ],
            is_error=False,
        )
        data = result.to_dict()
        assert data["content"] == [{"type": "text", "text": "success"}]
        assert data["isError"] is False

    def test_result_to_dict_error(self):
        """Test error result serialization."""
        result = CallToolResult(
            content=[{"type": "text", "text": "error"}],
            is_error=True,
        )
        data = result.to_dict()
        assert data["isError"] is True


class TestListResourcesResult:
    """Test ListResourcesResult model."""

    def test_empty_resources(self):
        """Test listing with no resources."""
        result = ListResourcesResult(resources=[])
        assert result.resources == []

    def test_with_resources(self):
        """Test listing with resources."""
        resources = [
            {"uri": "file:///a.txt", "name": "a"},
            {"uri": "file:///b.txt", "name": "b"},
        ]
        result = ListResourcesResult(resources=resources)
        assert len(result.resources) == 2

    def test_to_dict(self):
        """Test serialization."""
        resources = [{"uri": "file:///test.txt", "name": "test"}]
        result = ListResourcesResult(resources=resources)
        data = result.to_dict()
        assert "resources" in data
        assert data["resources"] == resources


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

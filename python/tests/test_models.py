"""Tests for MCP data models."""

from __future__ import annotations

from pheno_mcp.models import (
    CallToolResult,
    ListResourcesResult,
    Prompt,
    Resource,
    Tool,
)


class TestTool:
    """Tests for Tool model."""

    def test_tool_to_dict(self) -> None:
        """Test tool serialization."""
        tool = Tool(
            name="search",
            description="Search for items",
            input_schema={"type": "object"},
        )
        result = tool.to_dict()
        assert result["name"] == "search"
        assert result["description"] == "Search for items"
        assert "inputSchema" in result


class TestResource:
    """Tests for Resource model."""

    def test_resource_to_dict(self) -> None:
        """Test resource serialization."""
        resource = Resource(
            uri="file://data.csv",
            name="CSV Data",
            description="CSV data file",
            mime_type="text/csv",
        )
        result = resource.to_dict()
        assert result["uri"] == "file://data.csv"
        assert result["name"] == "CSV Data"
        assert result["mimeType"] == "text/csv"

    def test_resource_defaults(self) -> None:
        """Test resource has correct defaults."""
        resource = Resource(uri="test://file", name="Test")
        assert resource.description == ""
        assert resource.mime_type == "text/plain"


class TestPrompt:
    """Tests for Prompt model."""

    def test_prompt_to_dict(self) -> None:
        """Test prompt serialization."""
        prompt = Prompt(
            name="summarize",
            description="Summarize text",
            arguments=[{"name": "text", "description": "Text to summarize"}],
        )
        result = prompt.to_dict()
        assert result["name"] == "summarize"
        assert result["description"] == "Summarize text"
        assert len(result["arguments"]) == 1


class TestCallToolResult:
    """Tests for CallToolResult model."""

    def test_call_tool_result_to_dict(self) -> None:
        """Test call tool result serialization."""
        result = CallToolResult(
            content=[{"type": "text", "text": "Hello"}],
            is_error=False,
        )
        output = result.to_dict()
        assert output["content"] == [{"type": "text", "text": "Hello"}]
        assert output["isError"] is False

    def test_call_tool_result_error(self) -> None:
        """Test call tool result with error."""
        result = CallToolResult(
            content=[{"type": "text", "text": "Error occurred"}],
            is_error=True,
        )
        output = result.to_dict()
        assert output["isError"] is True


class TestListResourcesResult:
    """Tests for ListResourcesResult model."""

    def test_list_resources_result_to_dict(self) -> None:
        """Test list resources result serialization."""
        result = ListResourcesResult(
            resources=[
                {"uri": "file://a.txt", "name": "A"},
                {"uri": "file://b.txt", "name": "B"},
            ],
        )
        output = result.to_dict()
        assert len(output["resources"]) == 2

    def test_list_resources_result_empty(self) -> None:
        """Test empty list resources result."""
        result = ListResourcesResult(resources=[])
        output = result.to_dict()
        assert output["resources"] == []


class TestToolEdgeCases:
    """Tests for Tool model edge cases."""

    def test_tool_with_complex_input_schema(self) -> None:
        """Test tool with complex input schema."""
        tool = Tool(
            name="complex_tool",
            description="Tool with complex schema",
            input_schema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "active": {"type": "boolean"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "metadata": {"type": "object"},
                },
                "required": ["name"],
            },
        )
        result = tool.to_dict()
        assert result["inputSchema"]["type"] == "object"
        assert "name" in result["inputSchema"]["properties"]
        assert "required" in result["inputSchema"]

    def test_tool_with_empty_description(self) -> None:
        """Test tool with empty description."""
        tool = Tool(name="minimal", description="")
        result = tool.to_dict()
        assert result["description"] == ""

    def test_tool_with_empty_input_schema(self) -> None:
        """Test tool with empty input schema."""
        tool = Tool(name="minimal", description="A minimal tool")
        result = tool.to_dict()
        assert result["inputSchema"] == {}


class TestResourceEdgeCases:
    """Tests for Resource model edge cases."""

    def test_resource_with_all_fields(self) -> None:
        """Test resource with all fields populated."""
        resource = Resource(
            uri="https://example.com/data.json",
            name="Example Data",
            description="Example JSON data",
            mime_type="application/json",
            contents={"key": "value"},
        )
        result = resource.to_dict()
        assert result["uri"] == "https://example.com/data.json"
        assert result["name"] == "Example Data"
        assert result["mimeType"] == "application/json"

    def test_resource_with_special_uri_schemes(self) -> None:
        """Test resource with various URI schemes."""
        schemes = [
            "file://",
            "https://",
            "s3://",
            "memory://",
            "data:text/plain;base64,",
        ]
        for i, scheme in enumerate(schemes):
            resource = Resource(uri=f"{scheme}resource{i}", name=f"Resource {i}")
            result = resource.to_dict()
            assert result["uri"].startswith(scheme)


class TestPromptEdgeCases:
    """Tests for Prompt model edge cases."""

    def test_prompt_with_no_arguments(self) -> None:
        """Test prompt with no arguments."""
        prompt = Prompt(name="simple", description="Simple prompt")
        result = prompt.to_dict()
        assert result["arguments"] == []

    def test_prompt_with_multiple_arguments(self) -> None:
        """Test prompt with multiple arguments."""
        prompt = Prompt(
            name="complex",
            description="Complex prompt",
            arguments=[
                {"name": "arg1", "description": "First", "required": True},
                {"name": "arg2", "description": "Second", "type": "string"},
                {"name": "arg3", "description": "Third", "type": "integer"},
            ],
        )
        result = prompt.to_dict()
        assert len(result["arguments"]) == 3

    def test_prompt_with_empty_arguments_list(self) -> None:
        """Test prompt with explicitly empty arguments."""
        prompt = Prompt(
            name="explicit_empty",
            description="Prompt with empty args",
            arguments=[],
        )
        result = prompt.to_dict()
        assert result["arguments"] == []


class TestCallToolResultEdgeCases:
    """Tests for CallToolResult model edge cases."""

    def test_call_tool_result_with_text_content(self) -> None:
        """Test call tool result with text content."""
        result = CallToolResult(
            content=[
                {"type": "text", "text": "Hello, World!"},
            ],
        )
        output = result.to_dict()
        assert len(output["content"]) == 1
        assert output["content"][0]["type"] == "text"

    def test_call_tool_result_with_image_content(self) -> None:
        """Test call tool result with image content."""
        result = CallToolResult(
            content=[
                {
                    "type": "image",
                    "data": "base64encodeddata",
                    "mimeType": "image/png",
                },
            ],
        )
        output = result.to_dict()
        assert output["content"][0]["type"] == "image"

    def test_call_tool_result_with_embedded_content(self) -> None:
        """Test call tool result with embedded resource content."""
        result = CallToolResult(
            content=[
                {
                    "type": "resource",
                    "resource": {
                        "uri": "file://data.json",
                        "mimeType": "application/json",
                        "text": '{"key": "value"}',
                    },
                },
            ],
        )
        output = result.to_dict()
        assert output["content"][0]["type"] == "resource"

    def test_call_tool_result_multiple_content_items(self) -> None:
        """Test call tool result with multiple content items."""
        result = CallToolResult(
            content=[
                {"type": "text", "text": "First item"},
                {"type": "text", "text": "Second item"},
            ],
        )
        output = result.to_dict()
        assert len(output["content"]) == 2

    def test_call_tool_result_is_error_defaults_false(self) -> None:
        """Test is_error defaults to False."""
        result = CallToolResult(content=[{"type": "text", "text": "OK"}])
        output = result.to_dict()
        assert output["isError"] is False


class TestModelImmutability:
    """Tests for model field immutability patterns."""

    def test_tool_fields_are_accessible(self) -> None:
        """Test tool fields can be accessed."""
        tool = Tool(name="test", description="desc")
        assert tool.name == "test"
        assert tool.description == "desc"

    def test_resource_fields_are_accessible(self) -> None:
        """Test resource fields can be accessed."""
        resource = Resource(uri="file://test", name="Test")
        assert resource.uri == "file://test"
        assert resource.name == "Test"

    def test_prompt_fields_are_accessible(self) -> None:
        """Test prompt fields can be accessed."""
        prompt = Prompt(name="test", description="desc")
        assert prompt.name == "test"
        assert prompt.description == "desc"

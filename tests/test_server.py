"""Tests for pheno_mcp server module."""

import pytest

from pheno_mcp.server import (
    Server,
    ServerConfig,
    Tool,
    Resource,
    Prompt,
)


class TestServerConfig:
    """Test ServerConfig dataclass."""

    def test_default_config(self):
        """Test default configuration values."""
        config = ServerConfig()
        assert config.name == "pheno-mcp"
        assert config.version == "0.1.0"

    def test_custom_config(self):
        """Test custom configuration values."""
        config = ServerConfig(name="custom-server", version="1.2.3")
        assert config.name == "custom-server"
        assert config.version == "1.2.3"


class TestTool:
    """Test Tool dataclass."""

    def test_tool_creation(self):
        """Test creating a basic tool."""
        tool = Tool(name="test_tool", description="A test tool")
        assert tool.name == "test_tool"
        assert tool.description == "A test tool"
        assert tool.input_schema == {}
        assert tool.handler is None

    def test_tool_with_schema(self):
        """Test creating a tool with input schema."""
        schema = {"type": "object", "properties": {"query": {"type": "string"}}}
        tool = Tool(name="search", description="Search resources", input_schema=schema)
        assert tool.input_schema == schema
        assert tool.input_schema["type"] == "object"

    def test_tool_to_dict(self):
        """Test tool serialization to dictionary."""
        tool = Tool(name="echo", description="Echo input", input_schema={"type": "object"})
        result = tool.to_dict()
        assert result["name"] == "echo"
        assert result["description"] == "Echo input"
        assert result["inputSchema"] == {"type": "object"}


class TestResource:
    """Test Resource dataclass."""

    def test_resource_creation(self):
        """Test creating a basic resource."""
        resource = Resource(uri="file:///test.txt", name="test")
        assert resource.uri == "file:///test.txt"
        assert resource.name == "test"
        assert resource.description == ""
        assert resource.mime_type == "text/plain"

    def test_resource_full_creation(self):
        """Test creating a resource with all fields."""
        resource = Resource(
            uri="https://example.com/data.json",
            name="data",
            description="JSON data file",
            mime_type="application/json",
        )
        assert resource.uri == "https://example.com/data.json"
        assert resource.description == "JSON data file"
        assert resource.mime_type == "application/json"

    def test_resource_to_dict(self):
        """Test resource serialization to dictionary."""
        resource = Resource(
            uri="memory://cache/test",
            name="cache",
            description="Memory cache",
            mime_type="application/octet-stream",
        )
        result = resource.to_dict()
        assert result["uri"] == "memory://cache/test"
        assert result["name"] == "cache"
        assert result["description"] == "Memory cache"
        assert result["mimeType"] == "application/octet-stream"


class TestPrompt:
    """Test Prompt dataclass."""

    def test_prompt_creation(self):
        """Test creating a basic prompt."""
        prompt = Prompt(name="greet", description="Generate greeting")
        assert prompt.name == "greet"
        assert prompt.description == "Generate greeting"
        assert prompt.arguments == []

    def test_prompt_with_arguments(self):
        """Test creating a prompt with arguments."""
        args = [
            {"name": "name", "description": "Person to greet", "required": True},
            {"name": "style", "description": "Greeting style", "required": False},
        ]
        prompt = Prompt(name="greet", description="Generate greeting", arguments=args)
        assert len(prompt.arguments) == 2
        assert prompt.arguments[0]["name"] == "name"
        assert prompt.arguments[1]["name"] == "style"

    def test_prompt_to_dict(self):
        """Test prompt serialization to dictionary."""
        prompt = Prompt(
            name="summarize",
            description="Summarize text",
            arguments=[{"name": "text", "description": "Text to summarize"}],
        )
        result = prompt.to_dict()
        assert result["name"] == "summarize"
        assert result["description"] == "Summarize text"
        assert len(result["arguments"]) == 1


class TestServer:
    """Test Server class."""

    def test_server_default_initialization(self):
        """Test server initializes with defaults."""
        server = Server()
        assert server.name == "pheno-mcp"
        assert server.version == "0.1.0"

    def test_server_custom_initialization(self):
        """Test server initializes with custom config."""
        config = ServerConfig(name="test-server", version="2.0.0")
        server = Server(config=config)
        assert server.name == "test-server"
        assert server.version == "2.0.0"

    def test_register_tool(self):
        """Test registering a tool."""
        server = Server()
        tool = Tool(name="test", description="Test tool")
        server.register_tool(tool)
        tools = server.list_tools()
        assert len(tools) == 1
        assert tools[0]["name"] == "test"

    def test_register_multiple_tools(self):
        """Test registering multiple tools."""
        server = Server()
        server.register_tool(Tool(name="tool1", description="First"))
        server.register_tool(Tool(name="tool2", description="Second"))
        server.register_tool(Tool(name="tool3", description="Third"))
        tools = server.list_tools()
        assert len(tools) == 3

    def test_register_resource(self):
        """Test registering a resource."""
        server = Server()
        resource = Resource(uri="file:///data.txt", name="data")
        server.register_resource(resource)
        resources = server.list_resources()
        assert len(resources) == 1
        assert resources[0]["uri"] == "file:///data.txt"

    def test_register_prompt(self):
        """Test registering a prompt."""
        server = Server()
        prompt = Prompt(name="greet", description="Generate greeting")
        server.register_prompt(prompt)
        prompts = server.list_prompts()
        assert len(prompts) == 1
        assert prompts[0]["name"] == "greet"

    def test_list_tools_empty(self):
        """Test listing tools when none registered."""
        server = Server()
        assert server.list_tools() == []

    def test_list_resources_empty(self):
        """Test listing resources when none registered."""
        server = Server()
        assert server.list_resources() == []

    def test_list_prompts_empty(self):
        """Test listing prompts when none registered."""
        server = Server()
        assert server.list_prompts() == []

    @pytest.mark.asyncio
    async def test_handle_request_tools_list(self):
        """Test handling tools/list request."""
        server = Server()
        server.register_tool(Tool(name="test", description="Test"))
        result = await server.handle_request("tools/list")
        assert "tools" in result
        assert len(result["tools"]) == 1

    @pytest.mark.asyncio
    async def test_handle_request_resources_list(self):
        """Test handling resources/list request."""
        server = Server()
        server.register_resource(Resource(uri="file:///test", name="test"))
        result = await server.handle_request("resources/list")
        assert "resources" in result
        assert len(result["resources"]) == 1

    @pytest.mark.asyncio
    async def test_handle_request_prompts_list(self):
        """Test handling prompts/list request."""
        server = Server()
        server.register_prompt(Prompt(name="greet", description="Hello"))
        result = await server.handle_request("prompts/list")
        assert "prompts" in result
        assert len(result["prompts"]) == 1

    @pytest.mark.asyncio
    async def test_handle_request_tools_call(self):
        """Test handling tools/call request with handler."""
        server = Server()

        async def handler(args):
            return {"result": args.get("query", "default")}

        tool = Tool(name="search", description="Search", handler=handler)
        server.register_tool(tool)

        result = await server.handle_request("tools/call", {"name": "search", "arguments": {"query": "test"}})
        assert result["result"] == "test"

    @pytest.mark.asyncio
    async def test_handle_request_tools_call_no_handler(self):
        """Test handling tools/call request without handler."""
        server = Server()
        server.register_tool(Tool(name="search", description="Search"))
        result = await server.handle_request("tools/call", {"name": "search"})
        assert result is None

    @pytest.mark.asyncio
    async def test_handle_request_unknown_tool(self):
        """Test handling request for unknown tool."""
        server = Server()
        with pytest.raises(ValueError, match="Unknown tool"):
            await server.handle_request("tools/call", {"name": "nonexistent"})

    @pytest.mark.asyncio
    async def test_handle_request_unknown_method(self):
        """Test handling unknown request method."""
        server = Server()
        with pytest.raises(ValueError, match="Unknown method"):
            await server.handle_request("unknown/method")

    @pytest.mark.asyncio
    async def test_handle_request_no_params(self):
        """Test handling request without params."""
        server = Server()
        server.register_tool(Tool(name="test", description="Test"))
        result = await server.handle_request("tools/list")
        assert "tools" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

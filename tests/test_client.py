"""Tests for pheno_mcp client module."""

import pytest

from pheno_mcp.client import Client, ClientConfig


class TestClientConfig:
    """Test ClientConfig dataclass."""

    def test_default_config(self):
        """Test default configuration values."""
        config = ClientConfig()
        assert config.server_command == []
        assert config.server_env == {}
        assert config.timeout == 30.0

    def test_custom_config(self):
        """Test custom configuration values."""
        config = ClientConfig(
            server_command=["python", "server.py"],
            server_env={"DEBUG": "1"},
            timeout=60.0,
        )
        assert config.server_command == ["python", "server.py"]
        assert config.server_env == {"DEBUG": "1"}
        assert config.timeout == 60.0


class TestClient:
    """Test Client class."""

    def test_client_default_initialization(self):
        """Test client initializes with defaults."""
        client = Client()
        assert not client.is_connected

    def test_client_custom_initialization(self):
        """Test client initializes with custom config."""
        config = ClientConfig(
            server_command=["cargo", "run", "--bin", "pheno-mcp"],
            timeout=120.0,
        )
        client = Client(config=config)
        assert not client.is_connected
        assert client._config.timeout == 120.0

    def test_is_connected_property(self):
        """Test is_connected property."""
        client = Client()
        assert client.is_connected is False

    @pytest.mark.asyncio
    async def test_connect_without_command_raises(self):
        """Test connecting without server command raises error."""
        client = Client()
        with pytest.raises(RuntimeError, match="No server command configured"):
            await client.connect()

    @pytest.mark.asyncio
    async def test_connect_with_command(self):
        """Test connecting with server command succeeds."""
        config = ClientConfig(server_command=["echo", "test"])
        client = Client(config=config)
        await client.connect()
        assert client.is_connected

    @pytest.mark.asyncio
    async def test_connect_twice_is_idempotent(self):
        """Test connecting twice is idempotent."""
        config = ClientConfig(server_command=["echo", "test"])
        client = Client(config=config)
        await client.connect()
        await client.connect()
        assert client.is_connected

    @pytest.mark.asyncio
    async def test_disconnect(self):
        """Test disconnecting from server."""
        config = ClientConfig(server_command=["echo", "test"])
        client = Client(config=config)
        await client.connect()
        assert client.is_connected
        await client.disconnect()
        assert not client.is_connected

    @pytest.mark.asyncio
    async def test_disconnect_clears_tools(self):
        """Test disconnecting clears registered tools."""
        config = ClientConfig(server_command=["echo", "test"])
        client = Client(config=config)
        await client.connect()
        await client.disconnect()
        assert len(client._tools) == 0

    @pytest.mark.asyncio
    async def test_disconnect_clears_resources(self):
        """Test disconnecting clears cached resources."""
        config = ClientConfig(server_command=["echo", "test"])
        client = Client(config=config)
        await client.connect()
        await client.disconnect()
        assert len(client._resources) == 0

    @pytest.mark.asyncio
    async def test_call_tool_not_connected(self):
        """Test calling tool without connection raises error."""
        client = Client()
        with pytest.raises(RuntimeError, match="Not connected to server"):
            await client.call_tool("test_tool")

    @pytest.mark.asyncio
    async def test_call_tool_unknown(self):
        """Test calling unknown tool raises error."""
        config = ClientConfig(server_command=["echo", "test"])
        client = Client(config=config)
        await client.connect()
        with pytest.raises(ValueError, match="Unknown tool"):
            await client.call_tool("nonexistent")

    @pytest.mark.asyncio
    async def test_call_tool_success(self):
        """Test calling a registered tool succeeds."""
        config = ClientConfig(server_command=["echo", "test"])
        client = Client(config=config)
        await client.connect()

        async def mock_handler(args):
            return {"input": args}

        client._tools["test"] = mock_handler
        result = await client.call_tool("test", {"key": "value"})
        assert result["input"]["key"] == "value"

    @pytest.mark.asyncio
    async def test_call_tool_no_arguments(self):
        """Test calling tool with no arguments."""
        config = ClientConfig(server_command=["echo", "test"])
        client = Client(config=config)
        await client.connect()

        async def mock_handler(args):
            return {"args": args}

        client._tools["test"] = mock_handler
        result = await client.call_tool("test")
        assert result["args"] == {}

    @pytest.mark.asyncio
    async def test_list_tools_not_connected(self):
        """Test listing tools without connection raises error."""
        client = Client()
        with pytest.raises(RuntimeError, match="Not connected to server"):
            await client.list_tools()

    @pytest.mark.asyncio
    async def test_list_tools_connected(self):
        """Test listing tools when connected."""
        config = ClientConfig(server_command=["echo", "test"])
        client = Client(config=config)
        await client.connect()
        tools = await client.list_tools()
        assert tools == []

    @pytest.mark.asyncio
    async def test_list_resources_not_connected(self):
        """Test listing resources without connection raises error."""
        client = Client()
        with pytest.raises(RuntimeError, match="Not connected to server"):
            await client.list_resources()

    @pytest.mark.asyncio
    async def test_list_resources_connected(self):
        """Test listing resources when connected."""
        config = ClientConfig(server_command=["echo", "test"])
        client = Client(config=config)
        await client.connect()
        resources = await client.list_resources()
        assert resources == []

    @pytest.mark.asyncio
    async def test_read_resource_not_connected(self):
        """Test reading resource without connection raises error."""
        client = Client()
        with pytest.raises(RuntimeError, match="Not connected to server"):
            await client.read_resource("file:///test")

    @pytest.mark.asyncio
    async def test_read_resource_unknown(self):
        """Test reading unknown resource raises error."""
        config = ClientConfig(server_command=["echo", "test"])
        client = Client(config=config)
        await client.connect()
        with pytest.raises(ValueError, match="Unknown resource"):
            await client.read_resource("file:///nonexistent")

    @pytest.mark.asyncio
    async def test_read_resource_success(self):
        """Test reading a registered resource."""
        config = ClientConfig(server_command=["echo", "test"])
        client = Client(config=config)
        await client.connect()
        client._resources["file:///test"] = {"content": "Hello"}
        result = await client.read_resource("file:///test")
        assert result["content"] == "Hello"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

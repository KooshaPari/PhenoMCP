"""Tests for create_configured_server factory and tools __init__ exports.

Mirrors the ledger_query wiring pattern:
  - schema present in tools.__init__
  - all register_* symbols exported
  - create_configured_server registers all 8 tools end-to-end
  - handle_request round-trip for each tool bundle via factory server
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import pheno_mcp
from pheno_mcp import create_configured_server
from pheno_mcp.server import Server, ServerConfig
from pheno_mcp.tools import (
    # governance
    GOVERNANCE_TOOLS,
    TOOL_LEDGER_QUERY,
    TOOL_LEDGER_VERIFY,
    handle_ledger_query,
    handle_ledger_verify,
    register_governance_tools,
    # session
    SESSION_TOOLS,
    TOOL_SESSION_SUSPEND,
    TOOL_SESSION_RESUME,
    handle_session_suspend,
    handle_session_resume,
    register_session_tools,
    # workflow
    WORKFLOW_TOOLS,
    TOOL_WORKFLOW_EXECUTE,
    TOOL_WORKFLOW_STATUS,
    TOOL_WORKFLOW_CANCEL,
    TOOL_WORKFLOW_LIST,
    handle_workflow_execute,
    handle_workflow_status,
    handle_workflow_cancel,
    handle_workflow_list,
    register_workflow_tools,
)


# ---------------------------------------------------------------------------
# tools.__init__ exports
# ---------------------------------------------------------------------------


class TestToolsInitExports:
    """All register_* and schema constants are importable from pheno_mcp.tools."""

    def test_governance_exports_present(self) -> None:
        assert TOOL_LEDGER_QUERY["name"] == "ledger_query"
        assert TOOL_LEDGER_VERIFY["name"] == "ledger_verify"
        assert len(GOVERNANCE_TOOLS) == 2
        assert callable(handle_ledger_query)
        assert callable(handle_ledger_verify)
        assert callable(register_governance_tools)

    def test_session_exports_present(self) -> None:
        assert TOOL_SESSION_SUSPEND["name"] == "session_suspend"
        assert TOOL_SESSION_RESUME["name"] == "session_resume"
        assert len(SESSION_TOOLS) == 2
        assert callable(handle_session_suspend)
        assert callable(handle_session_resume)
        assert callable(register_session_tools)

    def test_workflow_exports_present(self) -> None:
        assert TOOL_WORKFLOW_EXECUTE["name"] == "workflow_execute"
        assert TOOL_WORKFLOW_STATUS["name"] == "workflow_status"
        assert TOOL_WORKFLOW_CANCEL["name"] == "workflow_cancel"
        assert TOOL_WORKFLOW_LIST["name"] == "workflow_list"
        assert len(WORKFLOW_TOOLS) == 4
        assert callable(handle_workflow_execute)
        assert callable(handle_workflow_status)
        assert callable(handle_workflow_cancel)
        assert callable(handle_workflow_list)
        assert callable(register_workflow_tools)


# ---------------------------------------------------------------------------
# top-level package export
# ---------------------------------------------------------------------------


class TestTopLevelExport:
    """create_configured_server is importable from pheno_mcp top-level."""

    def test_create_configured_server_in_package(self) -> None:
        assert hasattr(pheno_mcp, "create_configured_server")
        assert callable(pheno_mcp.create_configured_server)

    def test_create_configured_server_in_all(self) -> None:
        assert "create_configured_server" in pheno_mcp.__all__


# ---------------------------------------------------------------------------
# create_configured_server factory
# ---------------------------------------------------------------------------


class TestCreateConfiguredServer:
    """create_configured_server wires all 8 tools end-to-end."""

    def test_returns_server_instance(self) -> None:
        server = create_configured_server()
        assert isinstance(server, Server)

    def test_accepts_custom_config(self) -> None:
        cfg = ServerConfig(name="test-server", port=9999)
        server = create_configured_server(cfg)
        assert server.name == "test-server"

    def test_registers_all_eight_tools(self) -> None:
        server = create_configured_server()
        tools = server.list_tools()
        assert len(tools) == 8

    def test_all_expected_tool_names_present(self) -> None:
        server = create_configured_server()
        names = {t["name"] for t in server.list_tools()}
        expected = {
            "ledger_query",
            "ledger_verify",
            "session_suspend",
            "session_resume",
            "workflow_execute",
            "workflow_status",
            "workflow_cancel",
            "workflow_list",
        }
        assert names == expected

    def test_all_tools_have_descriptions(self) -> None:
        server = create_configured_server()
        for tool in server.list_tools():
            assert "description" in tool
            assert len(tool["description"]) > 0

    def test_all_tools_have_input_schemas(self) -> None:
        server = create_configured_server()
        for tool in server.list_tools():
            assert "inputSchema" in tool
            assert isinstance(tool["inputSchema"], dict)

    @pytest.mark.asyncio
    async def test_tools_list_via_handle_request(self) -> None:
        server = create_configured_server()
        result = await server.handle_request("tools/list")
        assert "tools" in result
        assert len(result["tools"]) == 8


# ---------------------------------------------------------------------------
# handle_request round-trips through factory server
# ---------------------------------------------------------------------------


class TestConfiguredServerRoundTrip:
    """Full Server.handle_request round-trips for every tool bundle."""

    # -- governance ----------------------------------------------------------

    @pytest.mark.asyncio
    async def test_ledger_query_round_trip(self) -> None:
        server = create_configured_server()
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"entries": [{"id": "e1"}]}
        mock_resp.raise_for_status.return_value = None
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_resp
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        with patch("pheno_mcp.tools.governance_tools._client", return_value=mock_client):
            result = await server.handle_request(
                "tools/call",
                {"name": "ledger_query", "arguments": {"limit": 5}},
            )
        assert result["entries"][0]["id"] == "e1"

    @pytest.mark.asyncio
    async def test_ledger_verify_round_trip(self) -> None:
        server = create_configured_server()
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"valid": True, "chain_length": 3}
        mock_resp.raise_for_status.return_value = None
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_resp
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        with patch("pheno_mcp.tools.governance_tools._client", return_value=mock_client):
            result = await server.handle_request(
                "tools/call",
                {"name": "ledger_verify", "arguments": {"from_entry": "e1", "to_entry": "e3"}},
            )
        assert result["valid"] is True

    # -- session -------------------------------------------------------------

    @pytest.mark.asyncio
    async def test_session_suspend_round_trip(self) -> None:
        server = create_configured_server()
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"bundle_ref": "bref-1", "status": "SUSPENDED"}
        mock_resp.raise_for_status.return_value = None
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_resp
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        with patch("pheno_mcp.tools.session_tools._client", return_value=mock_client):
            result = await server.handle_request(
                "tools/call",
                {"name": "session_suspend", "arguments": {"session_id": "sid-1"}},
            )
        assert result["bundle_ref"] == "bref-1"
        assert result["status"] == "SUSPENDED"

    @pytest.mark.asyncio
    async def test_session_resume_round_trip(self) -> None:
        server = create_configured_server()
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"session_id": "sid-new", "bundle_ref": "bref-1"}
        mock_resp.raise_for_status.return_value = None
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_resp
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        with patch("pheno_mcp.tools.session_tools._client", return_value=mock_client):
            result = await server.handle_request(
                "tools/call",
                {"name": "session_resume", "arguments": {"bundle_ref": "bref-1"}},
            )
        assert result["session_id"] == "sid-new"

    # -- workflow ------------------------------------------------------------

    @pytest.mark.asyncio
    async def test_workflow_execute_round_trip(self) -> None:
        server = create_configured_server()
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"execution_id": "exec-1", "status": "RUNNING"}
        mock_resp.raise_for_status.return_value = None
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_resp
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        with patch("pheno_mcp.tools.workflow_tools._client", return_value=mock_client):
            result = await server.handle_request(
                "tools/call",
                {"name": "workflow_execute", "arguments": {"workflow_id": "wf-1"}},
            )
        assert result["execution_id"] == "exec-1"

    @pytest.mark.asyncio
    async def test_workflow_status_round_trip(self) -> None:
        server = create_configured_server()
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"workflow_id": "wf-1", "status": "COMPLETED"}
        mock_resp.raise_for_status.return_value = None
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_resp
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        with patch("pheno_mcp.tools.workflow_tools._client", return_value=mock_client):
            result = await server.handle_request(
                "tools/call",
                {"name": "workflow_status", "arguments": {"workflow_id": "wf-1"}},
            )
        assert result["status"] == "COMPLETED"

    @pytest.mark.asyncio
    async def test_workflow_cancel_round_trip(self) -> None:
        server = create_configured_server()
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"workflow_id": "wf-1", "status": "CANCELLED"}
        mock_resp.raise_for_status.return_value = None
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_resp
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        with patch("pheno_mcp.tools.workflow_tools._client", return_value=mock_client):
            result = await server.handle_request(
                "tools/call",
                {"name": "workflow_cancel", "arguments": {"workflow_id": "wf-1"}},
            )
        assert result["status"] == "CANCELLED"

    @pytest.mark.asyncio
    async def test_workflow_list_round_trip(self) -> None:
        server = create_configured_server()
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"workflows": [{"id": "wf-1"}, {"id": "wf-2"}]}
        mock_resp.raise_for_status.return_value = None
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_resp
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        with patch("pheno_mcp.tools.workflow_tools._client", return_value=mock_client):
            result = await server.handle_request(
                "tools/call",
                {"name": "workflow_list", "arguments": {}},
            )
        assert len(result["workflows"]) == 2

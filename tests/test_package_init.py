"""Tests for pheno_mcp package initialization."""

import pytest


class TestPackageInit:
    """Test package initialization and exports."""

    def test_version_exists(self):
        """Test version is defined."""
        from pheno_mcp import __version__
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert len(__version__) > 0

    def test_version_format(self):
        """Test version follows semver format."""
        from pheno_mcp import __version__
        parts = __version__.split(".")
        assert len(parts) >= 2
        assert parts[0].isdigit()

    def test_client_exported(self):
        """Test Client is exported."""
        from pheno_mcp import Client
        assert Client is not None

    def test_server_exported(self):
        """Test Server is exported."""
        from pheno_mcp import Server
        assert Server is not None

    def test_tool_exported(self):
        """Test Tool is exported."""
        from pheno_mcp import Tool
        assert Tool is not None

    def test_resource_exported(self):
        """Test Resource is exported."""
        from pheno_mcp import Resource
        assert Resource is not None

    def test_prompt_exported(self):
        """Test Prompt is exported."""
        from pheno_mcp import Prompt
        assert Prompt is not None

    def test_all_list(self):
        """Test __all__ is defined and contains expected items."""
        from pheno_mcp import __all__
        assert isinstance(__all__, list)
        assert "Client" in __all__
        assert "Server" in __all__
        assert "Tool" in __all__
        assert "Resource" in __all__
        assert "Prompt" in __all__


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

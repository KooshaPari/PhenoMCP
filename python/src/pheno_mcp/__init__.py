"""PhenoMCP - Model Context Protocol Client Library.

A Python client library for interacting with MCP servers in the Phenotype ecosystem.
"""

from pheno_mcp.client import Client
from pheno_mcp.models import Prompt, Resource, Tool
from pheno_mcp.server import Server

__version__ = "0.1.0"
__all__ = ["__version__", "Client", "Server", "Tool", "Resource", "Prompt"]

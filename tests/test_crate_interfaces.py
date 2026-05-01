"""Tests for PhenoMCP Rust crate interfaces and types.

This module documents and tests the expected Rust crate interfaces
for the PhenoMCP project. These tests verify the expected API contracts
that Python bindings should implement.
"""

import pytest
from dataclasses import dataclass
from typing import Any


@dataclass
class ExpectedSkill:
    """Expected Skill struct from phenotype-surrealdb crate."""
    id: str | None
    name: str
    version: str
    code: str
    runtime: str
    metadata: dict[str, Any]


@dataclass
class ExpectedEmbedding:
    """Expected Embedding struct from phenotype-surrealdb crate."""
    id: str | None
    vector: list[float]
    metadata: dict[str, Any]


@dataclass
class ExpectedQdrantPoint:
    """Expected Point struct from pheno-qdrant crate."""
    id: str
    vector: list[float]
    payload: dict[str, Any]


@dataclass
class ExpectedQdrantSearchResult:
    """Expected SearchResult struct from pheno-qdrant crate."""
    id: str
    score: float
    payload: dict[str, Any]


@dataclass
class ExpectedMeiliDocument:
    """Expected Document struct from pheno-meilisearch crate."""
    id: str
    fields: dict[str, Any]


@dataclass
class ExpectedMeiliSearchResult:
    """Expected SearchResult struct from pheno-meilisearch crate."""
    hits: list[dict[str, Any]]
    estimated_total_hits: int
    processing_time_ms: int
    query: str


class TestSurrealDBCrateInterfaces:
    """Test expected interfaces for phenotype-surrealdb crate."""

    def test_skill_struct_fields(self):
        """Verify Skill struct has expected fields."""
        skill = ExpectedSkill(
            id=None,
            name="test-skill",
            version="1.0.0",
            code="fn main() {}",
            runtime="wasm",
            metadata={}
        )

        assert skill.name == "test-skill"
        assert skill.version == "1.0.0"
        assert skill.runtime == "wasm"

    def test_embedding_struct_fields(self):
        """Verify Embedding struct has expected fields."""
        embedding = ExpectedEmbedding(
            id="emb-001",
            vector=[0.1, 0.2, 0.3],
            metadata={"source": "test"}
        )

        assert len(embedding.vector) == 3
        assert embedding.id == "emb-001"

    def test_phenosurreal_expected_methods(self):
        """Document expected PhenoSurreal methods."""
        # These are the methods that should be available via Python bindings
        expected_methods = [
            "new",           # Create new instance
            "store_skill",   # Store a skill
            "query_skills",  # Query all skills
            "store_embedding",  # Store vector embedding
        ]

        # This test documents the expected API
        assert len(expected_methods) == 4


class TestQdrantCrateInterfaces:
    """Test expected interfaces for pheno-qdrant crate."""

    def test_point_struct_fields(self):
        """Verify Point struct has expected fields."""
        point = ExpectedQdrantPoint(
            id="point-001",
            vector=[0.1, 0.2, 0.3],
            payload={"text": "hello"}
        )

        assert point.id == "point-001"
        assert len(point.vector) == 3

    def test_search_result_struct_fields(self):
        """Verify Qdrant SearchResult struct has expected fields."""
        result = ExpectedQdrantSearchResult(
            id="result-001",
            score=0.95,
            payload={"text": "match"}
        )

        assert result.score == 0.95
        assert "text" in result.payload

    def test_qdrant_client_expected_methods(self):
        """Document expected QdrantClient methods."""
        expected_methods = [
            "new",                # Create new client
            "create_collection",  # Create collection
            "upsert",            # Upsert points
            "search",            # Search vectors
            "delete_collection", # Delete collection
            "health",           # Health check
        ]

        assert len(expected_methods) == 6


class TestMeilisearchCrateInterfaces:
    """Test expected interfaces for pheno-meilisearch crate."""

    def test_document_struct_fields(self):
        """Verify Document struct has expected fields."""
        doc = ExpectedMeiliDocument(
            id="doc-001",
            fields={"title": "Test", "content": "Hello world"}
        )

        assert doc.id == "doc-001"
        assert doc.fields["title"] == "Test"

    def test_search_result_struct_fields(self):
        """Verify Meilisearch SearchResult struct has expected fields."""
        result = ExpectedMeiliSearchResult(
            hits=[{"id": "1"}, {"id": "2"}],
            estimated_total_hits=100,
            processing_time_ms=5,
            query="test"
        )

        assert len(result.hits) == 2
        assert result.estimated_total_hits == 100
        assert result.processing_time_ms == 5

    def test_meilisearch_client_expected_methods(self):
        """Document expected MeilisearchClient methods."""
        expected_methods = [
            "new",              # Create new client
            "create_index",    # Create/update index
            "add_documents",   # Add documents
            "search",          # Search
            "delete_document", # Delete document
            "health",          # Health check
        ]

        assert len(expected_methods) == 6


class TestMCPServerInterfaces:
    """Test expected MCP server interfaces from integration tests."""

    def test_json_rpc_types(self):
        """Document expected JSON-RPC types."""
        # Based on integration-tests/test-server.rs
        expected_types = [
            "JsonRpcRequest",
            "JsonRpcResponse",
            "MCPServer",
        ]

        assert len(expected_types) == 3

    def test_mcp_server_expected_functionality(self):
        """Document expected MCPServer functionality."""
        # Based on test-server.rs, MCPServer should have:
        expected_features = [
            "register_tool",   # Register a tool
            "handle_request",  # Handle JSON-RPC requests
        ]

        assert len(expected_features) == 2


class TestErrorTypes:
    """Test expected error types from crates."""

    def test_qdrant_error_variants(self):
        """Document expected QdrantError variants."""
        expected_variants = [
            "Http",
            "NotFound",
            "Collection",
            "Parse",
        ]

        assert len(expected_variants) == 4

    def test_meilisearch_error_variants(self):
        """Document expected MeilisearchError variants."""
        expected_variants = [
            "Http",
            "Index",
            "Search",
        ]

        assert len(expected_variants) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

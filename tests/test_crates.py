"""Tests for PhenoMCP Rust crate configurations."""

from pathlib import Path
import tomllib


def test_meilisearch_crate_exists():
    """Verify pheno-meilisearch crate exists."""
    project_root = Path(__file__).parent.parent
    crate = project_root / "crates" / "pheno-meilisearch"
    assert crate.exists(), "pheno-meilisearch crate should exist"


def test_qdrant_crate_exists():
    """Verify pheno-qdrant crate exists."""
    project_root = Path(__file__).parent.parent
    crate = project_root / "crates" / "pheno-qdrant"
    assert crate.exists(), "pheno-qdrant crate should exist"


def test_surrealdb_crate_exists():
    """Verify phenotype-surrealdb crate exists."""
    project_root = Path(__file__).parent.parent
    crate = project_root / "crates" / "phenotype-surrealdb"
    assert crate.exists(), "phenotype-surrealdb crate should exist"


def test_meilisearch_crate_toml():
    """Verify pheno-meilisearch has valid Cargo.toml."""
    project_root = Path(__file__).parent.parent
    cargo_toml = project_root / "crates" / "pheno-meilisearch" / "Cargo.toml"

    with open(cargo_toml, "rb") as f:
        data = tomllib.load(f)

    assert "package" in data
    assert "dependencies" in data
    assert "reqwest" in data["dependencies"]


def test_qdrant_crate_toml():
    """Verify pheno-qdrant has valid Cargo.toml."""
    project_root = Path(__file__).parent.parent
    cargo_toml = project_root / "crates" / "pheno-qdrant" / "Cargo.toml"

    with open(cargo_toml, "rb") as f:
        data = tomllib.load(f)

    assert "package" in data
    assert "dependencies" in data
    assert "reqwest" in data["dependencies"]


def test_surrealdb_crate_toml():
    """Verify phenotype-surrealdb has valid Cargo.toml."""
    project_root = Path(__file__).parent.parent
    cargo_toml = project_root / "crates" / "phenotype-surrealdb" / "Cargo.toml"

    with open(cargo_toml, "rb") as f:
        data = tomllib.load(f)

    assert "package" in data


def test_crates_have_lib_rs():
    """Verify each crate has a lib.rs file."""
    project_root = Path(__file__).parent.parent
    crates_dir = project_root / "crates"

    for crate_dir in crates_dir.iterdir():
        if crate_dir.is_dir():
            lib_rs = crate_dir / "src" / "lib.rs"
            assert lib_rs.exists(), f"{crate_dir.name} should have src/lib.rs"

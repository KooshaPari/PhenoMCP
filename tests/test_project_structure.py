"""Tests for PhenoMCP project structure and configuration files."""

from pathlib import Path


def test_version_file_exists():
    """Verify VERSION file exists at project root."""
    project_root = Path(__file__).parent.parent
    version_file = project_root / "VERSION"
    assert version_file.exists(), "VERSION file should exist"


def test_version_file_not_empty():
    """Verify VERSION file has content."""
    project_root = Path(__file__).parent.parent
    version_file = project_root / "VERSION"
    content = version_file.read_text().strip()
    assert len(content) > 0, "VERSION file should not be empty"


def test_cargo_toml_exists():
    """Verify Cargo.toml exists (Rust project)."""
    project_root = Path(__file__).parent.parent
    cargo_toml = project_root / "Cargo.toml"
    assert cargo_toml.exists(), "Cargo.toml should exist"


def test_cargo_toml_is_valid_toml():
    """Verify Cargo.toml is valid TOML format."""
    import tomllib

    project_root = Path(__file__).parent.parent
    cargo_toml = project_root / "Cargo.toml"
    with open(cargo_toml, "rb") as f:
        data = tomllib.load(f)
    assert "package" in data
    assert "name" in data["package"]


def test_crates_directory_exists():
    """Verify Rust crates directory exists."""
    project_root = Path(__file__).parent.parent
    crates_dir = project_root / "crates"
    assert crates_dir.exists(), "crates/ directory should exist"


def test_rust_crates_are_modules():
    """Verify each crate has a Cargo.toml."""
    project_root = Path(__file__).parent.parent
    crates_dir = project_root / "crates"

    for crate_dir in crates_dir.iterdir():
        if crate_dir.is_dir():
            crate_toml = crate_dir / "Cargo.toml"
            assert crate_toml.exists(), f"{crate_dir.name} should have Cargo.toml"


def test_readme_exists():
    """Verify README.md exists."""
    project_root = Path(__file__).parent.parent
    readme = project_root / "README.md"
    assert readme.exists(), "README.md should exist"


def test_readme_has_content():
    """Verify README.md has substantial content."""
    project_root = Path(__file__).parent.parent
    readme = project_root / "README.md"
    content = readme.read_text()
    assert len(content) > 100, "README.md should have substantial content"


def test_integration_tests_directory_exists():
    """Verify integration tests directory exists."""
    project_root = Path(__file__).parent.parent
    integration_dir = project_root / "integration-tests"
    assert integration_dir.exists(), "integration-tests/ directory should exist"

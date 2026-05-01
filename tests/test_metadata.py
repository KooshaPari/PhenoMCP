"""Tests for PhenoMCP package metadata and configuration."""

import importlib.metadata
import tomllib
from pathlib import Path


def _get_local_pyproject():
    """Read pyproject.toml directly from source."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    return tomllib.loads(pyproject_path.read_text())


def test_package_name_in_metadata():
    """Verify package name is correctly registered."""
    try:
        dist = importlib.metadata.distribution("pheno-mcp")
        name = dist.metadata["Name"]
        assert name == "pheno-mcp"
    except importlib.metadata.PackageNotFoundError:
        # Fallback: check pyproject.toml
        data = _get_local_pyproject()
        assert data["project"]["name"] == "pheno-mcp"


def test_package_version_exists():
    """Verify package version is defined."""
    try:
        version = importlib.metadata.version("pheno-mcp")
        assert version is not None
        assert isinstance(version, str)
        assert len(version) > 0
    except importlib.metadata.PackageNotFoundError:
        # Fallback: check pyproject.toml
        data = _get_local_pyproject()
        assert data["project"]["version"] == "0.1.0"


def test_package_has_license():
    """Verify package has license information in pyproject.toml."""
    # Always check pyproject.toml for this project
    data = _get_local_pyproject()
    assert "license" in data["project"], "License should be in pyproject.toml"
    # License can be a string or a table with 'text' key
    license_val = data["project"]["license"]
    if isinstance(license_val, dict):
        # TOML table format: license = { text = "MIT OR Apache-2.0" }
        assert "text" in license_val, "License should have 'text' field"
        assert len(license_val["text"]) > 0
    else:
        # String format: license = "MIT OR Apache-2.0"
        assert isinstance(license_val, str)
        assert len(license_val) > 0


def test_version_format():
    """Verify version follows semver format."""
    try:
        version = importlib.metadata.version("pheno-mcp")
    except importlib.metadata.PackageNotFoundError:
        data = _get_local_pyproject()
        version = data["project"]["version"]

    parts = version.split(".")
    assert len(parts) >= 2, "Version should have at least major.minor"
    assert parts[0].isdigit(), "Major version should be numeric"


def test_package_description_exists():
    """Verify package has a description."""
    try:
        dist = importlib.metadata.distribution("pheno-mcp")
        description = dist.metadata.get("Description") or dist.metadata.get("Summary")
        assert description is not None
        assert len(description) > 0
    except importlib.metadata.PackageNotFoundError:
        # Fallback: check pyproject.toml
        data = _get_local_pyproject()
        assert "description" in data["project"]


def test_python_requirement():
    """Verify Python version requirement is specified."""
    try:
        dist = importlib.metadata.distribution("pheno-mcp")
        requires_python = dist.metadata.get("Requires-Python")
        assert requires_python is not None
        assert len(requires_python) > 0
        # Verify it's a valid Python version specifier
        assert ">=" in requires_python or "~" in requires_python or ">" in requires_python
    except importlib.metadata.PackageNotFoundError:
        # Fallback: check pyproject.toml
        data = _get_local_pyproject()
        assert "requires-python" in data["project"]

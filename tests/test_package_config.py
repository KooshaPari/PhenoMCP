"""Tests for pheno-mcp package configuration and structure."""

import pytest


class TestPackageConfiguration:
    """Test package configuration."""

    def test_pyproject_exists(self):
        """Verify pyproject.toml exists and is valid."""
        import tomllib
        from pathlib import Path

        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        assert pyproject_path.exists(), "pyproject.toml should exist"

        content = pyproject_path.read_text()
        data = tomllib.loads(content)

        assert data["project"]["name"] == "pheno-mcp"
        assert data["project"]["version"] == "0.1.0"
        assert ">=3.11" in data["project"]["requires-python"]

    def test_pytest_configured(self):
        """Verify pytest is configured."""
        import tomllib
        from pathlib import Path

        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        data = tomllib.loads(pyproject_path.read_text())

        # Check that pytest>=8.0 is in the dev dependencies
        dev_deps = data["project"]["optional-dependencies"]["dev"]
        pytest_dep = next((d for d in dev_deps if d.startswith("pytest")), None)
        assert pytest_dep is not None, "pytest should be in dev dependencies"
        assert ">=8.0" in pytest_dep
        # Check pytest config in pyproject.toml
        assert "pytest" in data["tool"]
        assert "ini_options" in data["tool"]["pytest"]
        assert data["tool"]["pytest"]["ini_options"]["testpaths"] == ["python/tests"]

    def test_ruff_configured(self):
        """Verify ruff linter is configured."""
        import tomllib
        from pathlib import Path

        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        data = tomllib.loads(pyproject_path.read_text())

        assert data["tool"]["ruff"]["target-version"] == "py311"
        assert data["tool"]["ruff"]["line-length"] == 100


class TestPackageStructure:
    """Test package directory structure."""

    def test_python_directory_exists(self):
        """Verify python/ directory exists as placeholder."""
        from pathlib import Path

        python_dir = Path(__file__).parent.parent / "python"
        assert python_dir.exists(), "python/ directory should exist"

    def test_bindings_directory_exists(self):
        """Verify bindings/ directory exists."""
        from pathlib import Path

        bindings_dir = Path(__file__).parent.parent / "bindings"
        assert bindings_dir.exists(), "bindings/ directory should exist"

    def test_tests_init_exists(self):
        """Verify tests/__init__.py exists."""
        from pathlib import Path

        init_path = Path(__file__).parent / "__init__.py"
        assert init_path.exists(), "tests/__init__.py should exist"


class TestRustWorkspace:
    """Test Rust workspace configuration."""

    def test_cargo_toml_exists(self):
        """Verify Cargo.toml exists."""
        from pathlib import Path

        cargo_path = Path(__file__).parent.parent / "Cargo.toml"
        assert cargo_path.exists(), "Cargo.toml should exist"

    def test_crates_exist(self):
        """Verify workspace crates are defined."""
        import tomllib
        from pathlib import Path

        cargo_path = Path(__file__).parent.parent / "Cargo.toml"
        data = tomllib.loads(cargo_path.read_text())

        # Workspace uses members list
        assert "workspace" in data
        assert "members" in data["workspace"]
        # Members can be glob patterns like "crates/*"
        members = data["workspace"]["members"]
        assert any("crates" in m for m in members), "Should have crates directory in workspace"

    def test_cargo_lock_exists(self):
        """Verify Cargo.lock exists (dependencies locked)."""
        from pathlib import Path

        lock_path = Path(__file__).parent.parent / "Cargo.lock"
        assert lock_path.exists(), "Cargo.lock should exist for reproducible builds"


class TestProjectMetadata:
    """Test project metadata files."""

    def test_readme_exists(self):
        """Verify README.md exists."""
        from pathlib import Path

        readme = Path(__file__).parent.parent / "README.md"
        assert readme.exists(), "README.md should exist"

    def test_license_exists(self):
        """Verify license files exist."""
        from pathlib import Path

        apache_license = Path(__file__).parent.parent / "LICENSE-APACHE"
        mit_license = Path(__file__).parent.parent / "LICENSE-MIT"

        assert apache_license.exists(), "LICENSE-APACHE should exist"
        assert mit_license.exists(), "LICENSE-MIT should exist"

    def test_version_file_exists(self):
        """Verify VERSION file exists."""
        from pathlib import Path

        version_file = Path(__file__).parent.parent / "VERSION"
        assert version_file.exists(), "VERSION file should exist"

    def test_version_content(self):
        """Verify VERSION file has content."""
        from pathlib import Path

        version_file = Path(__file__).parent.parent / "VERSION"
        version = version_file.read_text().strip()
        assert len(version) > 0, "VERSION file should not be empty"


class TestDevelopmentTools:
    """Test development tooling configuration."""

    def test_pre_commit_config_exists(self):
        """Verify pre-commit configuration exists."""
        from pathlib import Path

        precommit = Path(__file__).parent.parent / ".pre-commit-config.yaml"
        assert precommit.exists(), ".pre-commit-config.yaml should exist"

    def test_justfile_exists(self):
        """Verify justfile exists for task automation."""
        from pathlib import Path

        justfile = Path(__file__).parent.parent / "justfile"
        assert justfile.exists(), "justfile should exist"

    def test_taskfile_exists(self):
        """Verify Taskfile.yml exists for task automation."""
        from pathlib import Path

        taskfile = Path(__file__).parent.parent / "Taskfile.yml"
        assert taskfile.exists(), "Taskfile.yml should exist"

    def test_editorconfig_exists(self):
        """Verify .editorconfig exists."""
        from pathlib import Path

        editorconfig = Path(__file__).parent.parent / ".editorconfig"
        assert editorconfig.exists(), ".editorconfig should exist"


class TestMCPIntegration:
    """Test MCP-related integration files."""

    def test_integration_tests_exist(self):
        """Verify integration tests directory exists."""
        from pathlib import Path

        int_tests = Path(__file__).parent.parent / "integration-tests"
        assert int_tests.exists(), "integration-tests/ directory should exist"

    def test_docs_exist(self):
        """Verify documentation directory exists."""
        from pathlib import Path

        docs = Path(__file__).parent.parent / "docs"
        assert docs.exists(), "docs/ directory should exist"

    def test_examples_exist(self):
        """Verify examples directory exists."""
        from pathlib import Path

        examples = Path(__file__).parent.parent / "examples"
        assert examples.exists(), "examples/ directory should exist"


class TestCIConfiguration:
    """Test CI/CD configuration."""

    def test_github_workflows_exist(self):
        """Verify GitHub workflows directory exists."""
        from pathlib import Path

        workflows = Path(__file__).parent.parent / ".github" / "workflows"
        assert workflows.exists(), ".github/workflows/ directory should exist"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

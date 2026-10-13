"""Regression tests for the public ``trentorch`` package version."""

from pathlib import Path

import trentorch


def test_package_version_matches_project_metadata():
    """The package and project metadata must expose the same version."""
    project_root = Path(__file__).parents[3]
    pyproject_content = (project_root / "pyproject.toml").read_text(encoding="utf-8")
    project_version = next(
        line.split("=", 1)[1].strip().strip('"').strip("'")
        for line in pyproject_content.splitlines()
        if line.strip().startswith("version")
    )

    assert trentorch.__version__ == project_version


def test_project_version_ignores_unrelated_parent_pyproject(tmp_path):
    """A parent project's version must not be mistaken for TrenTorch's."""
    decoy = tmp_path / "pyproject.toml"
    decoy.write_text('[project]\nname = "unrelated-project"\nversion = "9.9.9"\n', encoding="utf-8")

    assert trentorch._read_project_version(decoy) is None


def test_version_prefers_installed_distribution_metadata(monkeypatch):
    """Installed wheels expose their version through standard metadata."""
    monkeypatch.setattr(trentorch._metadata, "version", lambda package: "2.3.4")

    assert trentorch._get_version() == "2.3.4"

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


def test_get_version_skips_decoy_parent_and_finds_trentorch_project(tmp_path, monkeypatch):
    """The source-checkout walk must ignore a nested project's metadata."""
    package_init = tmp_path / "venv" / "lib" / "site-packages" / "trentorch" / "__init__.py"
    package_init.parent.mkdir(parents=True)
    package_init.write_text("", encoding="utf-8")

    decoy = package_init.parents[3] / "pyproject.toml"
    decoy.write_text('[project]\nname = "unrelated-project"\nversion = "9.9.9"\n', encoding="utf-8")
    project = tmp_path / "pyproject.toml"
    project.write_text('[project]\nname = "trentorch"\nversion = "1.2.3"\n', encoding="utf-8")

    def missing_distribution(_package):
        raise trentorch._metadata.PackageNotFoundError(_package)

    monkeypatch.setattr(trentorch, "__file__", str(package_init))
    monkeypatch.setattr(trentorch._metadata, "version", missing_distribution)

    assert trentorch._get_version() == "1.2.3"


def test_project_version_ignores_version_outside_project_table(tmp_path):
    """Only the matching project's version field is used."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '[tool.other]\nversion = "9.9.9"\n\n[project]\nname = "trentorch"\nversion = "1.2.3"\n',
        encoding="utf-8",
    )

    assert trentorch._read_project_version(pyproject) == "1.2.3"


def test_version_prefers_installed_distribution_metadata(monkeypatch):
    """Installed wheels expose their version through standard metadata."""
    monkeypatch.setattr(trentorch._metadata, "version", lambda package: "2.3.4")

    assert trentorch._get_version() == "2.3.4"

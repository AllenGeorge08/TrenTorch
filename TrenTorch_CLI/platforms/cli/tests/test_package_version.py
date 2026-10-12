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

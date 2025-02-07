from pathlib import Path

import pytest


@pytest.fixture
def test_project() -> Path:
    """Fixture to obtain a directory with a very basic mkdocs project."""
    return Path(__file__).parent / "project"

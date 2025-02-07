"""Unit test for mkdocstrings_handlers.python_betterrefs.handler module."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from griffe import Docstring, Module, Object
from mkdocstrings.handlers.base import CollectorItem

from mkdocstrings_handlers.python.config import PythonConfig, PythonOptions
from mkdocstrings_handlers.python.handler import PythonHandler
from mkdocstrings_handlers.python_betterrefs.config import PythonBetterRefsOptions
from mkdocstrings_handlers.python_betterrefs.handler import PythonBetterRefsHandler


def test_init(test_project: Path) -> None:
    """Test the initialization of the custom handler.

    This is primarily to make sure that the inheritance works.
    """
    handler = PythonBetterRefsHandler(
        config=PythonConfig.from_data(
            options={"better_crossrefs": True, "check_crossrefs": False, "show_source": True},
        ),
        base_dir=test_project,
        theme="material",
        mdx=[],
        mdx_config={},
    )

    # Custom name for our handler
    assert handler.name == "python_betterrefs"

    # Template dirs should be redirected to python handler ones
    assert handler.get_templates_dir(handler.name) == handler.get_templates_dir("python")


@pytest.mark.parametrize(
    ("input_opts", "expected_global_opts", "expected_betterrefs_opts"),
    [
        pytest.param(
            {},
            {},
            {},
            id="empty-opts",
        ),
        pytest.param(
            {"show_source": True, "docstring_style": "google"},
            {"show_source": True, "docstring_style": "google"},
            {},
            id="external-opts",
        ),
        pytest.param(
            {"better_crossrefs": True, "check_crossrefs": True},
            {},
            {"better_crossrefs": True, "check_crossrefs": True},
            id="internal-opts",
        ),
        pytest.param(
            {"show_source": True, "docstring_style": "google", "better_crossrefs": True, "check_crossrefs": True},
            {"show_source": True, "docstring_style": "google"},
            {"better_crossrefs": True, "check_crossrefs": True},
            id="mix",
        ),
    ],
)
def test_options(
    test_project: Path,
    input_opts: dict[str, Any],
    expected_global_opts: dict[str, Any],
    expected_betterrefs_opts: dict[str, Any],
) -> None:
    """Test whether the options are parsed successfully.

    This makes sure the custom options for this handler aren't being propagated to
    the original handler, where they'd cause issues and are instead correctly extracted.
    """
    handler = PythonBetterRefsHandler(
        config=PythonConfig.from_data(options=input_opts),
        base_dir=test_project,
        theme="material",
        mdx=[],
        mdx_config={},
    )

    assert handler.global_options == expected_global_opts
    assert handler.better_refs_opts == expected_betterrefs_opts


@pytest.mark.parametrize(
    ("input_opts", "local_opts", "expected_merged_opts"),
    [
        pytest.param(
            {
                "better_crossrefs": True,
                "check_crossrefs": False,
                "show_source": True,
            },
            {},
            PythonBetterRefsOptions.from_data(
                better_crossrefs=True,
                check_crossrefs=False,
                show_source=True,
            ),
            id="only-global-opts",
        ),
        pytest.param(
            {
                "better_crossrefs": True,
                "check_crossrefs": False,
                "show_source": True,
            },
            {"show_source": True},
            PythonBetterRefsOptions.from_data(
                better_crossrefs=True,
                check_crossrefs=False,
                show_source=True,
            ),
            id="external-local-opt-unchanged",
        ),
        pytest.param(
            {
                "better_crossrefs": True,
                "check_crossrefs": False,
                "show_source": True,
            },
            {"show_source": False},
            PythonBetterRefsOptions.from_data(
                better_crossrefs=True,
                check_crossrefs=False,
                show_source=False,
            ),
            id="external-local-opt-changed",
        ),
        pytest.param(
            {
                "better_crossrefs": True,
                "check_crossrefs": False,
                "show_source": True,
            },
            {"check_crossrefs": False},
            PythonBetterRefsOptions.from_data(
                better_crossrefs=True,
                check_crossrefs=False,
                show_source=True,
            ),
            id="internal-local-opt-unchanged",
        ),
        pytest.param(
            {
                "better_crossrefs": True,
                "check_crossrefs": False,
                "show_source": True,
            },
            {"check_crossrefs": True},
            PythonBetterRefsOptions.from_data(
                better_crossrefs=True,
                check_crossrefs=True,
                show_source=True,
            ),
            id="internal-local-opt-changed",
        ),
        pytest.param(
            {
                "better_crossrefs": True,
                "check_crossrefs": False,
                "show_source": True,
            },
            {"check_crossrefs": True, "show_source": True},
            PythonBetterRefsOptions.from_data(
                better_crossrefs=True,
                check_crossrefs=True,
                show_source=True,
            ),
            id="mix",
        ),
    ],
)
def test_options_merging(
    input_opts: dict[str, Any],
    local_opts: dict[str, Any],
    expected_merged_opts: PythonBetterRefsOptions,
    test_project: Path,
) -> None:
    """Test the logic for local opts merging was overwritten correctly."""
    handler = PythonBetterRefsHandler(
        config=PythonConfig.from_data(options=input_opts),
        base_dir=test_project,
        theme="material",
        mdx=[],
        mdx_config={},
    )

    merged_opts = handler.get_options(local_opts)
    assert type(merged_opts) is PythonBetterRefsOptions
    assert merged_opts == expected_merged_opts


@pytest.mark.parametrize(
    ("griffe_obj", "options", "checkref_result", "expected_rendered", "expected_error"),
    [
        pytest.param(
            Module(name="mod", filepath=Path("mod."), docstring=Docstring("[foo][.foo]")),
            {"better_crossrefs": False, "check_crossrefs": False},
            True,
            "[foo][.foo]",
            False,
            id="rel-ref-but-disabled",
        ),
        pytest.param(
            Module(name="mod", filepath=Path("mod."), docstring=Docstring("[foo][.foo]")),
            {"better_crossrefs": True, "check_crossrefs": False},
            True,
            "[foo][mod.foo]",
            False,
            id="rel-ref-enabled",
        ),
        pytest.param(
            Module(name="mod", filepath=Path("mod."), docstring=Docstring("[bar][.]")),
            {"better_crossrefs": True, "check_crossrefs": False},
            True,
            "[bar][mod.bar]",
            False,
            id="rel-ref-enabled2",
        ),
        pytest.param(
            Module(name="mod", filepath=Path("mod."), docstring=Docstring("[foo][mod.foo]")),
            {"better_crossrefs": True, "check_crossrefs": True},
            True,
            "[foo][mod.foo]",
            False,
            id="abs-ref-check-crossrefs-pass",
        ),
        pytest.param(
            Module(name="mod", filepath=Path("mod."), docstring=Docstring("[foo][mod.foo]")),
            {"better_crossrefs": True, "check_crossrefs": True},
            False,
            "[foo][mod.foo]",
            True,
            id="abs-ref-check-crossrefs-fail",
        ),
        pytest.param(
            Module(name="mod", filepath=Path("mod."), docstring=Docstring("[foo][.foo]")),
            {"better_crossrefs": True, "check_crossrefs": True},
            True,
            "[foo][mod.foo]",
            False,
            id="rel-ref-check-crossrefs-pass",
        ),
        pytest.param(
            Module(name="mod", filepath=Path("mod."), docstring=Docstring("[foo][.foo]")),
            {"better_crossrefs": True, "check_crossrefs": True},
            False,
            "[foo][mod.foo]",
            True,
            id="rel-ref-check-crossrefs-fail",
        ),
        pytest.param(
            Module(name="mod", filepath=Path("mod."), docstring=Docstring("[foo][mod.foo]")),
            {"better_crossrefs": False, "check_crossrefs": True},
            False,
            "[foo][mod.foo]",
            False,
            id="abs-ref-check-crossrefs-nofail-without-betterrefs",
        ),
        pytest.param(
            Module(name="mod", filepath=Path("mod."), docstring=Docstring("[foo][.foo]")),
            {"better_crossrefs": False, "check_crossrefs": True},
            False,
            "[foo][.foo]",
            False,
            id="rel-ref-check-crossrefs-nofail-without-betterrefs",
        ),
        pytest.param(
            Module(name="mod", filepath=Path("mod."), docstring=Docstring("[foo][.foo] [bar][.]")),
            {"better_crossrefs": True, "check_crossrefs": False},
            True,
            "[foo][mod.foo] [bar][mod.bar]",
            False,
            id="rel-refs-enabled-multiple",
        ),
    ],
)
def test_render(
    griffe_obj: Object,
    options: dict[str, Any],
    checkref_result: bool,
    expected_rendered: str,
    expected_error: bool,
    test_project: Path,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that the rendering was overwritten correctly.

    Note that the goal of this test isn't necessarily to test the better ref logic,
    rather, it is to test that the handler is using this logic properly and applying
    it accordingly to the passed options.
    """
    handler = PythonBetterRefsHandler(
        config=PythonConfig(),
        base_dir=test_project,
        theme="material",
        mdx=[],
        mdx_config={},
    )

    # patch the render method of the parent class to only return the docstring,
    # we don't need/want to see the full template here
    def fake_render(_self: PythonHandler, data: CollectorItem, options: PythonOptions) -> str:
        return data.docstring.value

    monkeypatch.setattr(PythonHandler, "render", fake_render)

    # Patch check-ref according to the test parameters
    monkeypatch.setattr(PythonBetterRefsHandler, "_check_ref", lambda self, ref: checkref_result)

    # Test if rendering works as expected
    rendered = handler.render(griffe_obj, PythonBetterRefsOptions.from_data(**options))
    assert rendered == expected_rendered

    # Check whether a log was produced (when a reference wasn't found)
    if expected_error:
        assert len(caplog.records) >= 1
        assert "Cannot load reference" in caplog.messages[0]
    else:
        assert len(caplog.records) == 0

"""Unit tests for relative crossref expansion."""

from __future__ import annotations

import inspect
import logging
import re
from collections.abc import Callable
from pathlib import Path

import pytest
from griffe import Class, Docstring, Function, Module, Object

# noinspection PyProtectedMember
from mkdocstrings_handlers.python_betterrefs.crossref import (
    _RE_CROSSREF,  # pyright: ignore[reportPrivateUsage]
    _RE_REL_CROSSREF,  # pyright: ignore[reportPrivateUsage]
    _RelativeCrossrefProcessor,  # pyright: ignore[reportPrivateUsage]
    substitute_relative_crossrefs,
)


def test_RelativeCrossrefProcessor(caplog: pytest.LogCaptureFixture) -> None:  # noqa: N802
    """Unit test for internal _RelativeCrossrefProcessor class.

    Arguments:
        caplog: fixture
    """
    mod1 = Module(name="mod1", filepath=Path("mod1.py"))
    mod2 = Module(name="mod2", parent=mod1, filepath=Path("mod2.py"))
    mod1.members.update(mod2=mod2)
    cls1 = Class(name="Class1", parent=mod2)
    mod2.members.update(Class1=cls1)
    meth1 = Function(name="meth1", parent=cls1)
    cls1.members.update(meth1=meth1)

    def assert_sub(
        parent: Object,
        title: str,
        ref: str,
        expected: str = "",
        *,
        warning: str = "",
        relative: bool = True,
        checkref: Callable[[str], bool] | None = None,
    ) -> None:
        """Tests a relative crossref substitution.

        Arguments:
            parent: assumed parent object for docstring
            title: the title portion of the cross-reference expression
            ref: the reference path section of the cross-reference expression
            expected: the expected new value for the cross-reference
            warning: if specified, is regexp matching expected warning message
            relative: true if relative reference is expected
            checkref: reference checking function
        """
        if not expected:
            expected = ref
        crossref = f"[{title}][{ref}]"
        doc = Docstring(parent=parent, value=f"subject\n\n{crossref}\n", lineno=42)
        match = _RE_REL_CROSSREF.search(doc.value)
        if relative:
            assert match is not None
        else:
            assert match is None
            match = _RE_CROSSREF.search(doc.value)
            assert match is not None
        caplog.clear()
        actual = _RelativeCrossrefProcessor(doc, checkref=checkref)(match)
        if warning:
            assert len(caplog.records) == 1
            _, level, msg = caplog.record_tuples[0]
            assert level == logging.WARNING
            assert re.search(warning, msg)
            assert f"{parent.filepath}:44:" in msg
        else:
            assert not caplog.records
        assert actual == f"[{title}][{expected}]"

    assert_sub(cls1, "foo", ".", "mod1.mod2.Class1.foo")
    assert_sub(meth1, "foo", "^", "mod1.mod2.Class1")
    assert_sub(meth1, "foo", "^.", "mod1.mod2.Class1.foo")
    assert_sub(meth1, "foo", "..", "mod1.mod2.Class1.foo")
    assert_sub(meth1, "foo", "^.bar", "mod1.mod2.Class1.bar")
    assert_sub(meth1, "foo", "(c)", "mod1.mod2.Class1")
    assert_sub(meth1, "foo", "(c).", "mod1.mod2.Class1.foo")
    assert_sub(meth1, "foo", "(C).baz", "mod1.mod2.Class1.baz")
    assert_sub(meth1, "foo", "(c).baz.", "mod1.mod2.Class1.baz.foo")
    assert_sub(meth1, "foo", "(m).", "mod1.mod2.foo")
    assert_sub(meth1, "foo", "mod3.", "mod3.foo")
    assert_sub(meth1, "foo", "^^.", "mod1.mod2.foo", checkref=lambda x: True)
    assert_sub(meth1, "foo", "...", "mod1.mod2.foo", checkref=lambda x: True)
    assert_sub(meth1, "Class1", "(p).mod2.", "mod1.mod2.Class1")
    assert_sub(mod1, "Class1", "(P).mod2.Class1", "mod1.mod2.Class1")

    # disable checking

    def assert_nocheck(val: str) -> bool:
        pytest.fail(f"unexpected check of '{val}'")
        return False

    assert_sub(cls1, "foo", "?.", "mod1.mod2.Class1.foo", checkref=assert_nocheck)
    assert_sub(cls1, "foo", "?mod1.mod2.Class1.foo", "mod1.mod2.Class1.foo", checkref=assert_nocheck, relative=False)

    # Error cases

    assert_sub(meth1, "foo", ".", ".", warning="Cannot use '.'")
    assert_sub(meth1, "foo", ".bar", ".bar", warning="Cannot use '.'")
    assert_sub(meth1, "foo", ".bad+syntax", warning="Bad syntax")
    assert_sub(meth1, "bad id", "..", warning="not a qualified identifier")
    assert_sub(mod2, "foo", "(c)", warning="not in a class")
    assert_sub(meth1, "foo", "^^^^", warning="too many levels")
    assert_sub(
        meth1,
        "foo",
        "..",
        "mod1.mod2.Class1.foo",
        warning="Cannot load reference 'mod1.mod2.Class1.foo'",
        checkref=lambda x: False,
    )
    assert_sub(
        meth1,
        "foo",
        "mod1.mod2.Class1.foo",
        "mod1.mod2.Class1.foo",
        warning="Cannot load reference 'mod1.mod2.Class1.foo'",
        relative=False,
        checkref=lambda x: False,
    )


def test_substitute_relative_crossrefs(caplog: pytest.LogCaptureFixture) -> None:
    """Unit test for substitute_relative_crossrefs.

    Arguments:
        caplog: fixture
    """
    caplog.clear()

    mod1 = Module(name="mod1", filepath=Path("mod1.py"))
    mod2 = Module(name="mod2", parent=mod1, filepath=Path("mod2.py"))
    mod1.members["mod2"] = mod2
    cls1 = Class(name="Class1", parent=mod2)
    mod2.members["Class1"] = cls1
    meth1 = Function(name="meth1", parent=cls1)
    cls1.members["meth1"] = meth1

    meth1.docstring = Docstring(
        """
    [foo][..]
    [bar][(m).]
    """,
        parent=meth1,
        lineno=42,
    )

    mod1.docstring = Docstring(
        """
    [mod2.Class1][.]
    """,
        parent=mod1,
        lineno=23,
    )

    substitute_relative_crossrefs(mod1)

    assert meth1.docstring.value == inspect.cleandoc(
        """
    [foo][mod1.mod2.Class1.foo]
    [bar][mod1.mod2.bar]
    """,
    )

    assert len(caplog.records) == 0

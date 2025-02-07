"""Integration test for python_betterrefs handler."""

import re
import subprocess as sp
from collections.abc import Mapping
from os import PathLike
from pathlib import Path
from typing import cast

import bs4


def run_test_project_mkdocs(test_project: Path, site_dir: Path) -> sp.CompletedProcess[str]:
    """Run mkdocs command on a tiny sample project (contained in the same dir as this file)."""
    mkdocs_cmd = [
        "mkdocs",
        "build",
        "-f",
        str(test_project / "mkdocs.yml"),
        "-d",
        str(site_dir),
    ]
    return sp.run(mkdocs_cmd, capture_output=True, encoding="utf8", check=False)  # noqa: S603 # input is trusted


def check_autorefs(html_file: Path, cases: Mapping[tuple[str, str], str]) -> None:
    """Verify given HTML file contains all of the expected autorefs.

    Note:
        If the HTML file contains some additional autorefs, an AssertionError will be raised.

    Args:
        html_file: HTML file to check for autorefs.
        cases: mapping from (<location>,<title>) to generated reference link (<href>)
            where <location> is the qualified name of the object whose doc string
            contains the cross-reference, and <title> is the text in the cross-reference.
    """
    html = html_file.read_text()
    soup = bs4.BeautifulSoup(html, "html.parser")
    autorefs = soup.find_all("a", class_=["autorefs"])

    cases = dict(cases)
    for autoref in autorefs:
        # This is for typing purposes only, the find_all filter shouldn't ever find non-tags
        if not isinstance(autoref, bs4.Tag):
            raise TypeError("Autorefs contained non-tag")

        cur_id = cast(bs4.Tag, autoref.find_previous(id=True)).attrs["id"]
        text = autoref.string
        href = autoref.attrs["href"]
        expected_href = cases.get((cur_id, text))  # pyright: ignore[reportArgumentType]

        if expected_href:
            assert href == expected_href
            _ = cases.pop((cur_id, text))  # pyright: ignore[reportArgumentType]
        else:
            raise AssertionError(f"Skipping ref: {cur_id=},{text=} -> {href!r} ({autoref!s}")

    assert len(cases) == 0


def test_integration(test_project: Path, tmpdir: PathLike[str]) -> None:
    """An integration test that runs mkdocs on a tiny sample project.

    This then grovels the generated HTML to see that the links were resolved.
    """
    site_dir = Path(tmpdir).joinpath("site")
    result = run_test_project_mkdocs(test_project, site_dir)

    # Make sure the command succeeded
    try:
        result.check_returncode()
    except sp.CalledProcessError:
        print(result.stderr)  # noqa: T201
        raise

    # There is a single intentional bad reference in the bar.py file
    # make sure it was reported (check_crossrefs).
    m = re.search(
        r"WARNING.*file://(.*[/\\]myproj[/\\]bar\.py):(\d+):\s*\n\s*Cannot load reference '(.*)'",
        result.stderr,
    )
    assert m is not None, result.stderr
    assert m[1] == str(test_project.joinpath("src", "myproj", "bar.py"))
    assert m[2] == "3"
    assert m[3] == "myproj.bar.bad"

    # The original error for invalid references from autorefs should still be present too
    m = re.search(
        (
            r"WARNING.*mkdocs_autorefs: bar\.md: from (.*[/\\]myproj[/\\]bar.py):(\d+): \(myproj\.bar\) "
            r"Could not find cross-reference target '(.*)'"
        ),
        result.stderr,
    )
    assert m is not None, result.stderr
    assert m[1] == str(test_project.joinpath("src", "myproj", "bar.py"))
    assert m[2] == "1"  # line numbers aren't supported by mkdocs_autorefs, this is always 1
    assert m[3] == "myproj.bar.bad"

    # Verify the references (autorefs anchor tags) in the generated documentation HTML
    check_autorefs(
        site_dir.joinpath("bar", "index.html"),
        {
            ("myproj.bar.Bar", "Foo"): "../foo/#myproj.foo.Foo",  # from bases (parent class)
            ("myproj.bar.Bar", "bar"): "#myproj.bar.Bar.bar",
            ("myproj.bar.Bar.bar", "Bar"): "#myproj.bar.Bar",
            ("myproj.bar.Bar.bar", "foo"): "#myproj.bar.Bar.foo",
            ("myproj.bar.Bar.bar", "func"): "#myproj.bar.func",
            ("myproj.bar.Bar.foo", "Foo.foo"): "../foo/#myproj.foo.Foo.foo",
            ("myproj.bar.func", "bar"): "#myproj.bar",
        },
    )
    check_autorefs(
        site_dir.joinpath("pkg-baz", "index.html"),
        {
            ("myproj.pkg.baz", "func"): "../pkg/#myproj.pkg.func",
        },
    )

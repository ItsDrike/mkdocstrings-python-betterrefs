# Installation

!!! note "Installing alongside `mkdocstrings-python`"

    You don't need to explicitly specify [`mkdocstrings-python`][mkdocstrings-python] as a dependency, as this package
    already lists it as it's internal dependency, which means installing `mkdocstrings-python-betterrefs` will also
    install `mkdocstrings-python` for you.

## PyPI (stable) version

`mkdocstrings-python-betterrefs` is available on [PyPI] and can be installed like any other python library with:

=== ":simple-python: pip"

    ```bash
    pip install mkdocstrings-python-betterrefs
    ```

    <div class="result" markdown>

    [pip](https://pip.pypa.io/en/stable/) is the main package installer for Python.

    </div>

=== ":simple-poetry: poetry"

    ```bash
    poetry add mkdocstrings-python-betterrefs
    ```

    <div class="result" markdown>

    [Poetry](https://python-poetry.org/) is an all-in-one solution for Python project management.

    </div>

=== ":simple-rye: rye"

    ```bash
    rye add mkdocstrings-python-betterrefs
    ```

    <div class="result" markdown>

    [Rye](https://rye.astral.sh/) is an all-in-one solution for Python project management, written in Rust.

    </div>

=== ":simple-ruff: uv"

    ```bash
    uv pip install mkdocstrings-python-betterrefs
    ```

    <div class="result" markdown>

    [uv](https://github.com/astral-sh/uv) is an ultra fast dependency resolver and package installer, written in Rust.

    </div>

=== ":simple-pdm: pdm"

    ```bash
    pdm add mkdocstrings-python-betterrefs
    ```

    <div class="result" markdown>

    [PDM](https://pdm-project.org/en/latest/) is an all-in-one solution for Python project management.

    </div>

## Latest (git) version

!!! warning "We don't guarantee stability with method of installing"

If you wish to install the latest available version (the one you currently see in the `main` git branch), you may
instead choose this method of installing.

This kind of installation should only be done if you wish to test some new unreleased features and it's likely that you
will encounter bugs.

That said, this library is still in development, and there may be some features that you might wish to try, even
though they're not yet available in the latest release. This method of installation allows you to do just that.

To install the latest version of `mkdocstrings-python-betterrefs` directly from the `main` git branch, use:

=== ":simple-python: pip"

    ```bash
    pip install 'mkdocstrings-python-betterrefs@git+https://github.com/ItsDrike/mkdocstrings-python-betterrefs@main'
    ```

    <div class="result" markdown>

    [pip](https://pip.pypa.io/en/stable/) is the main package installer for Python.

    </div>

=== ":simple-poetry: poetry"

    ```bash
    poetry add 'git+https://github.com/ItsDrike/mkdocstrings-python-betterrefs#main'
    ```

    <div class="result" markdown>

    [Poetry](https://python-poetry.org/) is an all-in-one solution for Python project management.

    </div>

=== ":simple-rye: rye"

    ```bash
    rye add mkdocstrings-python-betterrefs --git='https://github.com/ItsDrike/mkdocstrings-python-betterrefs' --branch main
    ```

    <div class="result" markdown>

    [Rye](https://rye.astral.sh/) is an all-in-one solution for Python project management, written in Rust.

    </div>

=== ":simple-ruff: uv"

    ```bash
    uv pip install 'mkdocstrings-python-betterrefs@git+https://github.com/ItsDrike/mkdocstrings-python-betterrefs@main'
    ```

    <div class="result" markdown>

    [uv](https://github.com/astral-sh/uv) is an ultra fast dependency resolver and package installer, written in Rust.

    </div>

=== ":simple-pdm: pdm"

    ```bash
    pdm add "git+https://github.com/ItsDrike/mkdocstrings-python-betterrefs@main"
    ```

    <div class="result" markdown>

    [PDM](https://pdm-project.org/en/latest/) is an all-in-one solution for Python project management.

    </div>

[PyPI]: https://pypi.org/project/mkdocstrings-python-betterrefs
[mkdocstrings-python]: https://github.com/mkdocstrings/python

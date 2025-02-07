# Fork notice

This project is a fork of the excellent [mkdocstrings-python-xref] project. The primary reason for forking was personal
curiosity with how this project worked, though another reason was also that the original project was somewhat slow at
addressing some issues and used fairly uncommon packaging practices when it comes to modern python, which IMO made it
harder to contribute to.

At its core, this fork retains the original functionality while addressing compatibility issues that arose as its
dependencies (namely: mkdocstrings, mkdocstrings-python, mkdocstrings-autorefs, and griffe) were updated.

In addition, significant improvements have been made to the codebase, including cleanup and updates to follow modern
packaging practices. For example, this project moved away from Conda in favor of [uv].

We’ve also placed a greater emphasis on properly managing project dependencies. Stricter version requirements have been
applied to ensure stability, meaning that new versions of dependencies will only be supported once they’ve been properly
tested. The goal is to automate this process with GitHub workflows that will periodically check for new versions, run
tests, and publish a new PyPI release if all tests pass. This is particularly important given this library's reliance on
internal features of [mkdocstrings-python], which means breakages are common when dependencies are updated.

It's important to note that this is a "hard fork," meaning future updates to the original mkdocstrings-python-xref will
not necessarily be merged back here. This is mainly because the code-base of this project has become sufficiently
different to make that task pretty hard. However, if a relevant feature from the original project is introduced, we may
consider porting it to this fork. That said, considering this project haven't released a new feature in quite a while
now, this likely won't be a concern.

!!! note

    Due to technical reasons, this project is not marked as a "fork" on GitHub, even though it is one. Forked repositories
    come with limitations, such as disappearing if the original repo is made private, or creating confusion by suggesting
    this project is still work-in-progress aimed at contributing back to the original. Using a standalone repository helps
    avoid these issues and makes it clear that this is an independent continuation of the original project.

## Acknowledgements

This project would not exist without the original mkdocstrings-python-xref project, created by Christopher Barber and
the Analog Devices, Inc. We owe a huge thanks to them for their work, which laid the foundation for this fork and also
suggested the original idea of the improved syntax for cross-references.

## Legal notice

The purpose of this page is to acknowledge the original author and clarify the reasons behind this fork, as well as the
changes that have been made since. For the legal information required for derivative works under the Apache 2.0 license,
please refer to the [license page][license-page] instead.

[mkdocstrings-python-xref]: https://github.com/analog-garage/mkdocstrings-python-xref
[mkdocstrings-python]: https://github.com/mkdocstrings/python
[uv]: https://docs.astral.sh/uv
[license-page]: ./license.md

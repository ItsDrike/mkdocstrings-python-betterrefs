# mkdocstrings-python-betterrefs

![Supported python versions](https://img.shields.io/pypi/pyversions/mkdocstrings-python-betterrefs.svg)
[![Current PyPI version](https://img.shields.io/pypi/v/mkdocstrings-python-betterrefs.svg)](https://pypi.org/project/mkdocstrings-python-betterrefs/)
![License](https://img.shields.io/github/license/ItsDrike/mkdocstrings-python-betterrefs)
[![CI](https://github.com/ItsDrike/mkdocstrings-python-betterrefs/actions/workflows/main.yml/badge.svg)](https://github.com/ItsDrike/mkdocstrings-python-betterrefs/actions/workflows/main.yml)
[![Docs](https://github.com/ItsDrike/mkdocstrings-python-betterrefs/actions/workflows/mkdocs.yml/badge.svg)](https://itsdrike.github.io/mkdocstrings-python-betterrefs)

Python handler for [mkdocstrings] with improved handling for cross-references, including relative ones.

[mkdocstrings] is an awesome plugin for [MkDocs] that can generate Markdown API documentation from comments in code. The
standard [python handler][mkdocstrings-python] allows you to create cross-reference links using the syntax
`[<title>][<path>]` where the path must either be the fully qualified name of the referent or is empty, in which case
the path is taken from the title.

[mkdocstrings-python] does already have support for cross-references, however, it is currently only available in the
insiders edition, which is limited to their sponsors. Additionally, this implementation is fairly limited in comparison
to what this project offers.

> [!TIP]
> For more information on the [mkdocstrings-python] official support of relative cross-references, check out the feature
> request proposing them: [here][official-xrefs-issue], and the docs detailing the configuration option:
> [here][official-xrefs-docs].
>
> It is expected that relative cross-references will make it into the open-source version once a funding goal of $2,000
> is reached. You can see the current progress towards this goal [here][official-xrefs-funding-goal].

This package extends [mkdocstrings-python] to support an improved cross-reference syntax, that allows you to write
doc-strings with relative cross-references like:

```python
class MyClass:
    def this_method(self):
        """
        See [other_method][..] from [MyClass][(c)]
        """
```

rather than:

```python
class MyClass:
    def this_method(self):
        """
        See [other_method][mypkg.mymod.MyClass.other_method]
        from [MyClass][mypkg.mymod.Myclass]
        """
```

Relative references are especially useful for larger codebases with deeply nested package structure, where writing out
the absolute paths each time gets very burdensome.

Another benefit of this extension is that it will report source locations for bad references so that errors are easier
to find and fix. For example:

```bash
$ mkdocs build
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /home/jdoe/my-project/site
WARNING -  mkdocstrings_handlers: file:///home/jdoe/my-project/src/myproj/bar.py:16:
           Cannot load reference 'myproj.bar.bad'
```

For further details, please see the [Documentation](https://itsdrike.github.io/mkdocstrings-python-betterrefs)

[MkDocs]: https://mkdocs.readthedocs.io/
[mkdocstrings]: https://github.com/mkdocstrings/mkdocstrings
[mkdocstrings-python]: https://github.com/mkdocstrings/python
[official-xrefs-issue]: https://github.com/mkdocstrings/python/issues/27
[official-xrefs-docs]: https://mkdocstrings.github.io/python/usage/configuration/docstrings/?h=relative#relative_crossrefs
[official-xrefs-funding-goal]: https://mkdocstrings.github.io/python/insiders/#funding

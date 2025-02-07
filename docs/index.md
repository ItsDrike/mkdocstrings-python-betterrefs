---
hide:
    - navigation
---

# mkdocstrings-python-betterrefs

Python handler for [mkdocstrings] with improved handling for cross-references, including relative ones.

[mkdocstrings] is an awesome plugin for [MkDocs] that can generate Markdown API documentation from comments in code. The
standard [python handler (mkdomkdocstrings-python)][mkdocstrings-python] allows you to create cross-reference links
using the syntax `[<title>][<path>]` where the path must either be the fully qualified name of the referent or is empty,
in which case the path is taken from the title.

mkdocstrings-python does already have support for cross-references, however, it is currently only available in the
insiders edition, which is limited to their sponsors. Additionally, this implementation is fairly limited in comparison
to what this project offers.

!!! tip

    For more information on the mkdocstrings-python official support of relative cross-references, check out the
    feature request proposing them: [here][official-xrefs-issue], and the docs detailing the configuration option:
    [here][official-xrefs-docs].

    Even though the issue proposed the syntax similar to that used by this handler, the official relative crossrefs
    support ended up being a very limited version of it.

    It is expected that relative cross-references will make it into the open-source version once a funding goal of
    $2,000 is reached. You can see the current progress towards this goal [here][official-xrefs-funding-goal].

This package extends [mkdocstrings-python] to support an improved cross-reference syntax, that allows you to write
your doc-strings with these nicer cross-references. The primary goal is making cross-references shorter and less
repetitive.

Do note that this project is a fork of the original [mkdocstrings-python-xref]. For more info, see our [fork
notice][fork-notice] section

[MkDocs]: https://mkdocs.readthedocs.io/
[mkdocstrings]: https://github.com/mkdocstrings/mkdocstrings
[mkdocstrings-python]: https://github.com/mkdocstrings/python
[official-xrefs-issue]: https://github.com/mkdocstrings/python/issues/27
[official-xrefs-docs]: https://mkdocstrings.github.io/python/usage/configuration/docstrings/?h=relative#relative_crossrefs
[official-xrefs-funding-goal]: https://mkdocstrings.github.io/python/insiders/#funding
[mkdocstrings-python-xref]: https://github.com/analog-garage/mkdocstrings-python-xref
[fork-notice]: ./meta/fork.md

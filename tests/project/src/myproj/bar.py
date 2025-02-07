"""This is another module.

This is a [bad][.] reference.
"""

from typing_extensions import override

from .foo import Foo


class Bar(Foo):
    """See [bar][.] method."""

    def bar(self) -> None:
        """This is in the [Bar][(c)] class.

        Also see the [foo][^.] method and the [func][(m).] function.
        """

    @override
    def foo(self) -> None:
        """Overrides [Foo.foo][^^^.foo.]."""


def func() -> None:
    """This is a function in the [bar][(m)] module."""

"""Implementation of python_betterrefs handler."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path
from typing import Any, ClassVar

from mkdocstrings.handlers.base import CollectionError, CollectorItem, HandlerOptions
from mkdocstrings.loggers import get_logger
from typing_extensions import override

from mkdocstrings_handlers.python.config import PythonConfig, PythonOptions
from mkdocstrings_handlers.python.handler import PythonHandler
from mkdocstrings_handlers.python_betterrefs.config import PythonBetterRefsOptions

from .crossref import substitute_relative_crossrefs

__all__ = ["PythonBetterRefsHandler"]

logger = get_logger(__name__)


class PythonBetterRefsHandler(PythonHandler):
    """Extended version of mkdocstrings Python handler.

    * Converts custom cross-reference syntax into full (absolute) references.
    * Checks cross-references early in order to produce errors with source location.
    """

    name: ClassVar[str] = "python_betterrefs"
    """The handler's name."""

    @override
    def __init__(self, config: PythonConfig, base_dir: Path, **kwargs: Any) -> None:
        # Extract our custom options before thy're passed into PythonHandler init,
        # preventing complains about unknown options
        self.better_refs_opts, remaining_opts = PythonBetterRefsOptions.extract_betterrefs(config.options)
        config = replace(config, options=remaining_opts)  # pyright: ignore[reportArgumentType]  # PythonConfig is a dataclass

        super().__init__(config, base_dir, **kwargs)

    @override
    def get_options(self, local_options: Mapping[str, Any]) -> HandlerOptions:
        local_better_refs_opts, local_remaining_opts = PythonBetterRefsOptions.extract_betterrefs(local_options)
        python_opts: PythonOptions = super().get_options(local_remaining_opts)

        better_refs_opts = self.better_refs_opts.copy()
        better_refs_opts.update(local_better_refs_opts)

        return PythonBetterRefsOptions.merge_python(python_opts, better_refs_opts)

    @override
    def render(  # pyright: ignore[reportIncompatibleMethodOverride] # we use our type for options
        self,
        data: CollectorItem,
        options: PythonBetterRefsOptions,
    ) -> str:
        if options.better_crossrefs:
            checkref = self._check_ref if options.check_crossrefs else None
            substitute_relative_crossrefs(data, checkref=checkref)

        try:
            return super().render(data, options)
        except Exception:  # pragma: no cover
            print(f"{data.path=}")  # noqa: T201
            raise

    @override
    def get_templates_dir(self, handler: str | None = None) -> Path:
        # Return the python handler templates dir
        if handler == self.name:
            handler = "python"
        return super().get_templates_dir(handler)

    def _check_ref(self, ref: str) -> bool:
        """Check for existence of reference."""
        # Try to collect the reference normally and see if it fails
        try:
            self.collect(ref, PythonOptions())
        except CollectionError:
            return False
        else:
            return True

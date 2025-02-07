from collections.abc import Mapping
from dataclasses import dataclass, fields
from typing import Annotated, Any

from typing_extensions import Self

from mkdocstrings_handlers.python.config import (
    Field,
    PythonOptions,
    _dataclass_options,  # pyright: ignore[reportPrivateUsage]
)


@dataclass(**_dataclass_options)
class PythonBetterRefsOptions(PythonOptions):
    """Accepted input options."""

    better_crossrefs: Annotated[
        bool,
        Field(group="docstrings", description="Whether to enable better crossrefs syntax."),
    ] = True

    check_crossrefs: Annotated[
        bool,
        Field(
            group="docstrings",
            description="""Whether to produce improved warnings for invalid cross-references.

            This will only take effect if `better_crossrefs` is also enabled.
            """,
        ),
    ] = True

    @staticmethod
    def extract_betterrefs(data: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        """Extract the options specific to better-refs, leaving the rest untouched.

        Returns:
            A tuple of (better-refs specific options, remaining options).
        """
        better_refs_fields = {"better_crossrefs", "check_crossrefs"}
        copy = dict(data)
        return {name: copy.pop(name) for name in data if name in better_refs_fields}, copy

    @classmethod
    def merge_python(cls, python_opts: PythonOptions, extra_data: Mapping[str, Any]) -> Self:
        """Create a better-refs options from an existing PythonOptions instance and the extra data.

        Note that the passed extra_data is expected to already be coerced.
        """
        if type(python_opts) is not PythonOptions:
            raise TypeError("This function can only work directly with PythonOptions instances, not any descendents.")

        orig_fields = fields(PythonOptions)  # pyright: ignore[reportArgumentType] # PythonOptions is a dataclass
        field_names = {field.name for field in orig_fields}
        orig_data = {name: getattr(python_opts, name) for name in field_names}

        return cls(**orig_data, **extra_data)

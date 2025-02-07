"""Expose the extended mkdocstrings python handler."""

from collections.abc import MutableMapping
from pathlib import Path
from typing import Any
from warnings import warn

from mkdocs.config.defaults import MkDocsConfig

from mkdocstrings_handlers.python.config import PythonConfig

from .handler import PythonBetterRefsHandler

__all__ = ["get_handler"]


def get_handler(
    handler_config: MutableMapping[str, Any],
    tool_config: MkDocsConfig,
    **kwargs: Any,
) -> PythonBetterRefsHandler:
    """Return an instance of PythonBetterRefsHandler handler.

    This function essentially mimics the same function from mkdocstrings-python,
    just returning our extended handler instead of the Python one.

    Arguments:
        handler_config: The handler configuration.
        tool_config: The tool (SSG) configuration.

    Returns:
        An instance of `PythonHandler`.
    """
    base_dir = Path(tool_config.config_file_path or "./mkdocs.yml").parent
    if "inventories" not in handler_config and "import" in handler_config:
        warn("The 'import' key is renamed 'inventories' for the Python handler", FutureWarning, stacklevel=1)
        handler_config["inventories"] = handler_config.pop("import", [])

    # PythonConfig will actually store all of the options in a dict without doing any
    # checking during this initialization. That means we can just re-use it here, our
    # custom options will be stored and we can handle them from __init__.
    config = PythonConfig.from_data(**handler_config)

    return PythonBetterRefsHandler(
        config=config,
        base_dir=base_dir,
        **kwargs,
    )

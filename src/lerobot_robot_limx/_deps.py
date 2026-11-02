#!/usr/bin/env python
"""Dependency guards for the LimX LeRobot plugin.

The in-tree drivers used ``lerobot.utils.import_utils.require_package``, whose error
message points at ``pip install 'lerobot[<extra>]'``.  That hint is wrong once the
drivers ship as their own distribution, so this module keeps the same call signature
but points at the plugin's own extras.
"""

import importlib


def require_package(pkg_name: str, extra: str | None = None, import_name: str | None = None) -> None:
    """Raise an informative `ImportError` if `pkg_name` is not importable.

    Args:
        pkg_name (`str`):
            Distribution name, used in the message.
        extra (`str | None`):
            Extra of this plugin that installs it, if any.
        import_name (`str | None`):
            Module to import; defaults to `pkg_name`.

    Raises:
        ImportError: If the module cannot be imported.

    """
    module = import_name or pkg_name
    try:
        importlib.import_module(module)
    except ImportError as exc:
        hint = f"pip install 'lerobot_robot_limx[{extra}]'" if extra else f"pip install {pkg_name}"
        raise ImportError(
            f"'{pkg_name}' is required by this LimX driver but is not installed.\nInstall it with: {hint}"
        ) from exc

"""Stub configger for standalone repo.

In the original DPD repo, this reads from config.ini.
In the standalone repo, exporters read from bundled JSON source files instead.
"""

from typing import Optional


def config_read(
    section: str, option: str, default_value: Optional[str] = None
) -> str | None:
    """Return None for all config reads in standalone mode."""
    return default_value

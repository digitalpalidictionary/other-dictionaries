#!/usr/bin/env python3
"""Calculate next incremental version from git tags."""

import subprocess
import re


def get_latest_tag() -> str | None:
    """Get the latest release tag from git (semantic version only)."""
    try:
        result = subprocess.run(
            ["git", "tag", "--list", "v*"],
            capture_output=True,
            text=True,
            check=True,
        )
        tags = result.stdout.strip().split("\n")
        # Only match semantic version tags: v1.0.0, v1.2.3, etc.
        tags = [t for t in tags if t and re.match(r"^v\d+\.\d+\.\d+$", t)]
        if not tags:
            return None

        tags.sort(key=lambda x: [int(p) for p in x[1:].split(".")])
        return tags[-1]
    except subprocess.CalledProcessError:
        return None


def increment_version(tag: str) -> str:
    """Increment patch version."""
    major, minor, patch = [int(p) for p in tag[1:].split(".")]
    return f"v{major}.{minor}.{patch + 1}"


def get_next_version() -> str:
    """Get next version (v1.0.0 if no tags exist)."""
    latest = get_latest_tag()
    if latest is None:
        return "v1.0.0"
    return increment_version(latest)


if __name__ == "__main__":
    version = get_next_version()
    print(f"version={version}")

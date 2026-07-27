#!/usr/bin/env python3
"""Materialize all dictionary source files needed by downstream exporters.

Usage:
    uv run python scripts/prepare_sources.py

Restores scraped sources (CPD, BHS, Cone, DPPN, ...) from tracked .tar.zst
archives, then builds MW's mw.json and Apte's apte.json from fresh Cologne
data. MW falls back to its tracked mwweb1.zip when Cologne is unreachable;
Apte's ap90web1.zip is not tracked, so a fresh clone has no fallback and the
build fails if Cologne is down.

Run this before exporting the mobile DB — locally or in CI. Exits
non-zero if any mobile-critical source file is missing afterwards.
"""

import sys
from pathlib import Path

from dictionaries.apte.apte_from_cologne import build_apte_json
from dictionaries.mw.mw_from_cologne import build_mw_json
from scripts.decompress_sources import decompress_sources
from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr


def prepare_sources() -> bool:
    """Prepare all sources. Returns True when every mobile-critical file exists."""
    pth = RepoPaths()

    decompress_sources()

    build_mw_json(pth)

    build_apte_json(pth)

    mobile_critical: dict[str, Path] = {
        "cpd": pth.cpd_source_path,
        "bhs": pth.bhs_source_path,
        "mw": pth.mw_json_path,
        "apte": pth.apte_json_path,
        "dppn": pth.dppn_source_path,
        "nyanatiloka": pth.nyanatiloka_source_path,
    }

    pr.title("mobile-critical source files")
    all_present = True
    for name, path in mobile_critical.items():
        pr.green(name)
        if path.exists() and path.stat().st_size > 0:
            pr.yes(f"{path.stat().st_size / 1_000_000:.1f} MB")
        else:
            pr.no(f"MISSING: {path}")
            all_present = False

    return all_present


def main() -> None:
    if not prepare_sources():
        pr.error("source preparation incomplete — see MISSING entries above")
        sys.exit(1)


if __name__ == "__main__":
    main()

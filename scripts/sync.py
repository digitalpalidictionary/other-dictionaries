#!/usr/bin/env python3
"""Sync vendor tools and source data from DPD repository."""

import argparse
import shutil
from pathlib import Path

from vendor.dpd_tools.printer import printer as pr

VENDOR_TOOLS = [
    "goldendict_exporter.py",
    "mdict_exporter.py",
    "niggahitas.py",
    "printer.py",
    "pali_sort_key.py",
    "sanskrit_translit.py",
    "date_and_time.py",
]

WRITEMDICT_FILES = [
    "writemdict.py",
    "ripemd128.py",
    "pureSalsa20.py",
    "LICENSE",
]


def sync_vendor_tools(dpd_path: Path, dry_run: bool = False) -> None:
    """Copy DPD tools into vendor/dpd_tools/."""
    pr.green_title("syncing vendor tools")

    vendor_dir = Path(__file__).parent.parent / "vendor" / "dpd_tools"
    dpd_tools_dir = dpd_path / "tools"

    if not dpd_tools_dir.exists():
        pr.red(f"DPD tools directory not found: {dpd_tools_dir}")
        return

    for tool in VENDOR_TOOLS:
        src = dpd_tools_dir / tool
        dst = vendor_dir / tool
        if src.exists():
            pr.white(f"  {tool}")
            if not dry_run:
                shutil.copy2(src, dst)
            pr.yes("ok")
        else:
            pr.no(f"not found: {src}")

    pr.white("  writemdict/")
    writemdict_src = dpd_tools_dir / "writemdict"
    writemdict_dst = vendor_dir / "writemdict"
    if writemdict_src.exists():
        if not dry_run:
            writemdict_dst.mkdir(parents=True, exist_ok=True)
            for f in WRITEMDICT_FILES:
                src_file = writemdict_src / f
                if src_file.exists():
                    shutil.copy2(src_file, writemdict_dst / f)
        pr.yes("ok")
    else:
        pr.no(f"not found: {writemdict_src}")


def main():
    parser = argparse.ArgumentParser(description="Sync vendor tools from DPD repo")
    parser.add_argument(
        "--dpd-path",
        type=Path,
        required=True,
        help="Path to DPD repository root",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    args = parser.parse_args()

    sync_vendor_tools(args.dpd_path, args.dry_run)
    pr.green_title("sync complete")


if __name__ == "__main__":
    main()

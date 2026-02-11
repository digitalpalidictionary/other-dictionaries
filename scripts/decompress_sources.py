#!/usr/bin/env python3
"""Decompress all .tar.zst archives in dictionaries/*/ to restore source files.

Usage:
    uv run python scripts/decompress_sources.py

This extracts all .tar.zst archives (e.g., mw.tar.zst) to restore
the source directories (e.g., dictionaries/mw/source/).
"""

import subprocess
import tarfile
from pathlib import Path
from vendor.dpd_tools.printer import printer as pr


def decompress_sources():
    """Decompress all .tar.zst archives to restore source directories."""
    base_dir = Path(__file__).resolve().parent.parent
    dictionaries_dir = base_dir / "dictionaries"

    pr.title("decompressing source archives")

    decompressed_count = 0

    # Find all .tar.zst archives
    for archive_path in sorted(dictionaries_dir.glob("*/*.tar.zst")):
        dict_name = archive_path.stem.split(".")[0]  # Remove .tar.zst
        source_dir = archive_path.parent / "source"

        # Check if already decompressed
        if source_dir.exists() and any(source_dir.iterdir()):
            pr.green(f"{dict_name}: already decompressed")
            continue

        pr.green_title(f"decompressing {dict_name}")

        # Create source directory if needed
        source_dir.mkdir(parents=True, exist_ok=True)

        # Decompress with zstd
        pr.white("  decompressing with zstd...")
        tar_path = archive_path.with_suffix("")  # Remove .zst
        result = subprocess.run(
            ["zstd", "-d", "-f", str(archive_path), "-o", str(tar_path)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            pr.no("failed")
            pr.error(f"  failed to decompress {dict_name}")
            if result.stderr:
                pr.error(f"    error: {result.stderr}")
            continue
        # Extract tar archive
        pr.white("  extracting tar archive...")
        try:
            with tarfile.open(tar_path, "r") as tar:
                tar.extractall(path=source_dir)

            # Remove intermediate tar file
            tar_path.unlink(missing_ok=True)

            # Count extracted files
            extracted_files = list(source_dir.iterdir())
            pr.yes("ok")
            pr.info(f"  {len(extracted_files)} files extracted")
            decompressed_count += 1

        except Exception as e:
            pr.no("failed")
            pr.error(f"  failed to extract {dict_name}: {e}")
            tar_path.unlink(missing_ok=True)

    pr.green_title("decompression complete")
    if decompressed_count > 0:
        pr.info(f"{decompressed_count} dictionaries decompressed")
    else:
        pr.info("all dictionaries already decompressed")

    return decompressed_count


if __name__ == "__main__":
    decompress_sources()

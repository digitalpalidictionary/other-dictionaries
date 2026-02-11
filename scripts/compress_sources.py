#!/usr/bin/env python3
"""Compress all source files in dictionaries/*/source/ to single .tar.zst archives.

Usage:
    uv run python scripts/compress_sources.py

This creates one compressed archive per dictionary containing all source files.
Example: dictionaries/whitney/whitney.tar.zst (contains all source files)
"""

import subprocess
import tarfile
from pathlib import Path
from vendor.dpd_tools.printer import printer as pr


def compress_sources():
    """Compress all source directories to single .tar.zst archives."""
    base_dir = Path(__file__).resolve().parent.parent
    dictionaries_dir = base_dir / "dictionaries"

    pr.title("compressing source directories to .tar.zst")

    total_original = 0
    total_compressed = 0
    compressed_count = 0

    # Find all source directories
    for source_dir in sorted(dictionaries_dir.glob("*/source")):
        dict_dir = source_dir.parent
        dict_name = dict_dir.name
        archive_path = dict_dir / f"{dict_name}.tar.zst"
        tar_path = dict_dir / f"{dict_name}.tar"

        # Get total size of files to compress
        files_to_compress = [
            f for f in source_dir.iterdir() if f.is_file() and f.suffix != ".zst"
        ]
        if not files_to_compress:
            pr.white(f"{dict_name}: no files to compress")
            continue

        original_size = sum(f.stat().st_size for f in files_to_compress)
        pr.green(
            f"{dict_name} {len(files_to_compress)} files, {original_size / 1024 / 1024:.1f}MB"
        )
        # Create tar archive
        with tarfile.open(tar_path, "w") as tar:
            for file_path in files_to_compress:
                tar.add(file_path, arcname=file_path.name)

        # Compress with zstd level 19
        result = subprocess.run(
            ["zstd", "-19", "-f", str(tar_path), "-o", str(archive_path)],
            capture_output=True,
            text=True,
        )

        # Remove intermediate tar file
        tar_path.unlink(missing_ok=True)

        if result.returncode == 0:
            compressed_size = archive_path.stat().st_size
            ratio = (1 - compressed_size / original_size) * 100

            total_original += original_size
            total_compressed += compressed_size
            compressed_count += 1

            pr.yes("ok")
            pr.info(
                f"    {original_size / 1024 / 1024:.1f}MB → {compressed_size / 1024 / 1024:.1f}MB ({ratio:.0f}% reduction)"
            )
        else:
            pr.no("failed")
            pr.error(f"    failed to compress {dict_name}")
            if result.stderr:
                pr.error(f"    error: {result.stderr}")

    if compressed_count > 0:
        pr.info(f"{compressed_count} dictionaries compressed")
        pr.info(
            f"total size: {total_original / 1024 / 1024:.1f}MB → {total_compressed / 1024 / 1024:.1f}MB"
        )
        pr.info(f"space saved: {(1 - total_compressed / total_original) * 100:.0f}%")
    else:
        pr.info("all dictionaries already compressed")

    return compressed_count


if __name__ == "__main__":
    compress_sources()

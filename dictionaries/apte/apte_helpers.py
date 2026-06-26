"""Apte helper functions for Cologne source processing."""

import re
import sqlite3
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import requests

from vendor.dpd_tools.goldendict_exporter import DictEntry
from vendor.dpd_tools.niggahitas import add_niggahitas
from vendor.dpd_tools.sanskrit_sort_key import sanskrit_sort_key
from vendor.dpd_tools.sanskrit_translit import slp1_translit

from vendor.dpd_tools.printer import printer as pr


@dataclass
class ApteEntry:
    """A single sub-entry from ap90.sqlite."""

    key: str
    lnum: float
    data: str


@dataclass
class ApteData:
    """All Apte data loaded from SQLite databases."""

    abbreviations: dict[str, str] = field(default_factory=dict)
    author_tooltips: dict[str, str] = field(default_factory=dict)
    entries: dict[str, list[ApteEntry]] = field(default_factory=dict)


APTE_ZIP_URL = "https://www.sanskrit-lexicon.uni-koeln.de/scans/AP90Scan/2020/downloads/ap90web1.zip"

# Cologne's server rejects python-requests' default User-Agent (403/500).
REQUEST_HEADERS = {"User-Agent": "dpd-other-dictionaries-build/1.0"}


def _local_zip_is_valid(zip_path: Path) -> bool:
    return zip_path.exists() and zipfile.is_zipfile(zip_path)


def _unpack_if_missing(zip_path: Path, source_dir: Path) -> None:
    if not (source_dir / "web" / "sqlite").exists():
        _unpack_zip(zip_path, source_dir)


def _fall_back_to_local_zip(zip_path: Path, source_dir: Path, reason: str) -> None:
    if _local_zip_is_valid(zip_path):
        pr.red(f"{reason} — using local ap90web1.zip")
        _unpack_if_missing(zip_path, source_dir)
        return
    raise RuntimeError(f"{reason} and no valid local ap90web1.zip to fall back to")


def download_fresh_source(zip_path: Path, source_dir: Path) -> None:
    """Download ap90web1.zip from Cologne if remote size differs from local.

    Compares Content-Length header against local file size. Downloads when
    they differ or the local file is missing. Falls back to a valid local
    zip when Cologne is unreachable or returns invalid data. Unpacks
    whenever the extracted sqlite directory is missing.
    """
    pr.green("checking cologne server for updates")

    try:
        response = requests.head(APTE_ZIP_URL, timeout=30, headers=REQUEST_HEADERS)
        response.raise_for_status()
        remote_size = int(response.headers.get("Content-Length", 0))
    except requests.RequestException as e:
        _fall_back_to_local_zip(zip_path, source_dir, f"cologne unreachable ({e})")
        return

    local_size = zip_path.stat().st_size if zip_path.exists() else 0

    if local_size == remote_size and local_size > 0:
        pr.yes("up to date")
        _unpack_if_missing(zip_path, source_dir)
        return

    pr.no("downloading")
    pr.green(f"downloading ap90web1.zip ({remote_size / 1_000_000:.1f} MB)")

    try:
        response = requests.get(APTE_ZIP_URL, timeout=300, headers=REQUEST_HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        _fall_back_to_local_zip(zip_path, source_dir, f"download failed ({e})")
        return

    zip_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = zip_path.with_suffix(".zip.tmp")
    tmp_path.write_bytes(response.content)

    if not zipfile.is_zipfile(tmp_path):
        tmp_path.unlink(missing_ok=True)
        _fall_back_to_local_zip(
            zip_path, source_dir, "downloaded file is not a valid zip"
        )
        return

    tmp_path.replace(zip_path)
    pr.yes("done")

    _unpack_zip(zip_path, source_dir)


def _unpack_zip(zip_path: Path, source_dir: Path) -> None:
    """Extract zip contents into source directory."""
    pr.green("unpacking ap90web1.zip")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(source_dir)
    pr.yes("done")


def load_apte_data(sqlite_dir: Path) -> ApteData:
    """Load SQLite databases into ApteData dataclass."""
    data = ApteData()

    pr.green("loading ap90ab.sqlite")
    data.abbreviations = _load_abbreviations(sqlite_dir / "ap90ab.sqlite")
    pr.yes(str(len(data.abbreviations)))

    pr.green("loading ap90authtooltips.sqlite")
    data.author_tooltips = _load_author_tooltips(sqlite_dir / "ap90authtooltips.sqlite")
    pr.yes(str(len(data.author_tooltips)))

    pr.green("loading ap90.sqlite")
    data.entries = _load_entries(sqlite_dir / "ap90.sqlite")
    pr.yes(str(len(data.entries)))

    return data


def _load_abbreviations(db_path: Path) -> dict[str, str]:
    """Load abbreviations from ap90ab.sqlite → {id: display_text}."""
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT id, data FROM ap90ab").fetchall()
    conn.close()

    result: dict[str, str] = {}
    for ab_id, raw_data in rows:
        match = re.search(r"<disp>(.*?)</disp>", raw_data)
        result[ab_id] = match.group(1) if match else raw_data
    return result


def _load_author_tooltips(db_path: Path) -> dict[str, str]:
    """Load author/literature tooltips → {key: full_name}."""
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT key, data FROM ap90authtooltips").fetchall()
    conn.close()

    return {key: data for key, data in rows}


def _load_entries(db_path: Path) -> dict[str, list[ApteEntry]]:
    """Load ap90.sqlite, grouping sub-entries by headword key.

    Returns dict of slp1_key → [ApteEntry, ...] sorted by lnum.
    Non-consecutive same-key entries (e.g. alternate spellings scattered
    across the db) are collected together then sorted by first lnum.
    """
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT key, lnum, data FROM ap90 ORDER BY lnum").fetchall()
    conn.close()

    grouped: dict[str, list[ApteEntry]] = {}
    for key, lnum, data in rows:
        entry = ApteEntry(key=key, lnum=float(lnum), data=data)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(entry)

    return grouped


def generate_synonyms(slp1_key: str) -> list[str]:
    """Generate synonyms: IAST + niggahita variants + original SLP1."""
    iast = slp1_translit(slp1_key)
    synonyms = [iast, slp1_key]
    synonyms = add_niggahitas(synonyms)
    return list(set(synonyms))


def build_apte_entries(data: ApteData) -> list[DictEntry]:
    """Build GoldenDict DictEntry list from loaded Apte data.

    Keys are sorted in Sanskrit alphabetical order using slp1→IAST conversion
    and the sanskrit_sort_key function.
    """
    from dictionaries.apte.apte_renderer import preprocess_xml, render_xml_to_html

    pr.green_title("building apte entries")

    sorted_keys = sorted(
        data.entries.keys(),
        key=lambda k: sanskrit_sort_key(slp1_translit(k)),
    )

    entries: list[DictEntry] = []
    total = len(sorted_keys)

    for i, key in enumerate(sorted_keys):
        iast_word = slp1_translit(key)

        if i % 10000 == 0:
            pr.counter(i, total, iast_word)

        html_parts: list[str] = []
        for entry in data.entries[key]:
            processed = preprocess_xml(
                entry.data, data.abbreviations, data.author_tooltips
            )
            rendered = render_xml_to_html(processed)
            html_parts.append(f"<p>{rendered}</p>")

        body = "\n".join(html_parts)
        definition_html = (
            '<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<link href="apte.css" rel="stylesheet">'
            "</head><body>"
            f"{body}"
            "</body></html>"
        )
        synonyms = generate_synonyms(key)

        entries.append(
            DictEntry(
                word=iast_word,
                definition_html=definition_html,
                definition_plain="",
                synonyms=synonyms,
            )
        )

    return entries

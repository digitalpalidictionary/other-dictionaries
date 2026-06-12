"""MW2 helper functions for Cologne source processing."""

import bisect
import re
import sqlite3
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import requests

from vendor.dpd_tools.goldendict_exporter import DictEntry
from vendor.dpd_tools.niggahitas import add_niggahitas
from vendor.dpd_tools.sanskrit_translit import slp1_translit

from vendor.dpd_tools.printer import printer as pr


@dataclass
class MwEntry:
    """A single sub-entry from mw.sqlite."""

    key: str
    lnum: float
    data: str


@dataclass
class MwKeyEntry:
    """A grouped headword from mwkeys.sqlite."""

    key: str
    lnum: float
    data: str


@dataclass
class MwData:
    """All MW data loaded from SQLite databases."""

    abbreviations: dict[str, str] = field(default_factory=dict)
    author_tooltips: dict[str, str] = field(default_factory=dict)
    entries: dict[float, MwEntry] = field(default_factory=dict)
    keys: dict[float, MwKeyEntry] = field(default_factory=dict)


MW_ZIP_URL = (
    "https://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2020/downloads/mwweb1.zip"
)

# Cologne's server rejects python-requests' default User-Agent (403/500).
REQUEST_HEADERS = {"User-Agent": "dpd-other-dictionaries-build/1.0"}


def _local_zip_is_valid(zip_path: Path) -> bool:
    return zip_path.exists() and zipfile.is_zipfile(zip_path)


def _unpack_if_missing(zip_path: Path, source_dir: Path) -> None:
    if not (source_dir / "web" / "sqlite").exists():
        _unpack_zip(zip_path, source_dir)


def _fall_back_to_local_zip(
    zip_path: Path, source_dir: Path, reason: str
) -> None:
    if _local_zip_is_valid(zip_path):
        pr.red(f"{reason} — using local mwweb1.zip")
        _unpack_if_missing(zip_path, source_dir)
        return
    raise RuntimeError(f"{reason} and no valid local mwweb1.zip to fall back to")


def download_fresh_source(zip_path: Path, source_dir: Path) -> None:
    """Download mwweb1.zip from Cologne if remote size differs from local.

    Compares Content-Length header against local file size. Downloads when
    they differ or the local file is missing. Falls back to a valid local
    zip when Cologne is unreachable or returns invalid data. Unpacks
    whenever the extracted sqlite directory is missing.
    """
    pr.green("checking cologne server for updates")

    try:
        response = requests.head(MW_ZIP_URL, timeout=30, headers=REQUEST_HEADERS)
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
    pr.green(f"downloading mwweb1.zip ({remote_size / 1_000_000:.1f} MB)")

    try:
        response = requests.get(MW_ZIP_URL, timeout=300, headers=REQUEST_HEADERS)
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
    pr.green("unpacking mwweb1.zip")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(source_dir)
    pr.yes("done")


def load_mw_data(sqlite_dir: Path) -> MwData:
    """Load all 4 SQLite databases into MwData dataclass."""
    data = MwData()

    pr.green("loading mwab.sqlite")
    data.abbreviations = _load_abbreviations(sqlite_dir / "mwab.sqlite")
    pr.yes(str(len(data.abbreviations)))

    pr.green("loading mwauthtooltips.sqlite")
    data.author_tooltips = _load_author_tooltips(sqlite_dir / "mwauthtooltips.sqlite")
    pr.yes(str(len(data.author_tooltips)))

    pr.green("loading mw.sqlite")
    data.entries = _load_entries(sqlite_dir / "mw.sqlite")
    pr.yes(str(len(data.entries)))

    pr.green("loading mwkeys.sqlite")
    data.keys = _load_keys(sqlite_dir / "mwkeys.sqlite")
    pr.yes(str(len(data.keys)))

    return data


def _load_abbreviations(db_path: Path) -> dict[str, str]:
    """Load abbreviations from mwab.sqlite → {id: display_text}."""
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT id, data FROM mwab").fetchall()
    conn.close()

    result: dict[str, str] = {}
    for ab_id, raw_data in rows:
        match = re.search(r"<disp>(.*?)</disp>", raw_data)
        result[ab_id] = match.group(1) if match else raw_data
    return result


def _load_author_tooltips(db_path: Path) -> dict[str, str]:
    """Load author/literature tooltips → {key: full_name}."""
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT key, data FROM mwauthtooltips").fetchall()
    conn.close()

    return {key: data for key, data in rows}


def _load_entries(db_path: Path) -> dict[float, MwEntry]:
    """Load all sub-entries from mw.sqlite → {lnum: MwEntry}."""
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT key, lnum, data FROM mw").fetchall()
    conn.close()

    return {
        float(lnum): MwEntry(key=key, lnum=float(lnum), data=data)
        for key, lnum, data in rows
    }


def _load_keys(db_path: Path) -> dict[float, MwKeyEntry]:
    """Load grouped headwords from mwkeys.sqlite → {lnum: MwKeyEntry}."""
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT key, lnum, data FROM mwkeys").fetchall()
    conn.close()

    return {
        float(lnum): MwKeyEntry(key=key, lnum=float(lnum), data=data)
        for key, lnum, data in rows
    }


def parse_key_ranges(data: str) -> list[tuple[str, float, float]]:
    """Parse mwkeys data format: 'H1,startL,endL;H1A,startL2,endL2;...'

    Returns list of (h_type, start_lnum, end_lnum) tuples.
    """
    ranges: list[tuple[str, float, float]] = []
    for segment in data.split(";"):
        parts = segment.strip().split(",")
        if len(parts) == 3:
            h_type = parts[0]
            start = float(parts[1])
            end = float(parts[2])
            ranges.append((h_type, start, end))
    return ranges


def generate_synonyms(slp1_key: str) -> list[str]:
    """Generate synonyms: IAST + niggahita variants + original SLP1."""
    iast = slp1_translit(slp1_key)
    synonyms = [iast, slp1_key]
    synonyms = add_niggahitas(synonyms)
    return list(set(synonyms))


def build_mw_entries(data: MwData) -> list[DictEntry]:
    """Build GoldenDict DictEntry list from loaded MW data."""
    from dictionaries.mw.mw_renderer import preprocess_entry, render_xml_to_html

    pr.green_title("building mw entries")

    sorted_lnums = sorted(data.entries.keys())
    sorted_keys = sorted(data.keys.values(), key=lambda k: k.lnum)
    entries: list[DictEntry] = []

    for i, key_entry in enumerate(sorted_keys):
        iast_word = slp1_translit(key_entry.key)

        if i % 10000 == 0:
            pr.counter(i, len(sorted_keys), iast_word)
        ranges = parse_key_ranges(key_entry.data)

        html_parts: list[str] = []
        for _h_type, start, end in ranges:
            lo = bisect.bisect_left(sorted_lnums, start)
            hi = bisect.bisect_right(sorted_lnums, end)
            for idx in range(lo, hi):
                lnum = sorted_lnums[idx]
                entry = data.entries[lnum]
                processed = preprocess_entry(
                    entry.data, data.abbreviations, data.author_tooltips
                )
                rendered = render_xml_to_html(processed)
                html_parts.append(f"<p>{rendered}</p>")

        body = "\n".join(html_parts)
        definition_html = (
            '<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<link href="mw.css" rel="stylesheet">'
            "</head><body>"
            f"{body}"
            "</body></html>"
        )
        synonyms = generate_synonyms(key_entry.key)

        entries.append(
            DictEntry(
                word=iast_word,
                definition_html=definition_html,
                definition_plain="",
                synonyms=synonyms,
            )
        )

    return entries

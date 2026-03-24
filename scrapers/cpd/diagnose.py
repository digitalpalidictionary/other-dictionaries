"""
CPD Database Diagnostic

Scans data/cpd.db (read-only) and reports problem characters per field.
Writes detailed offender log to data/diagnose_report.txt.
"""

import re
import sqlite3
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

from cleanup_rules import HEADWORD_ALLOW_EXTRA, WEBKEYWORD_ALLOW_EXTRA

SOURCE_DB = Path("data/cpd_clean.db")
REPORT_PATH = Path("diagnose_report.txt")

PALI_ALPHABET = [
    "a", "ā", "i", "ī", "u", "ū", "e", "o",
    "k", "kh", "g", "gh", "ṅ",
    "c", "ch", "j", "jh", "ñ",
    "ṭ", "ṭh", "ḍ", "ḍh", "ṇ",
    "t", "th", "d", "dh", "n",
    "p", "ph", "b", "bh", "m",
    "y", "r", "l", "s", "v", "h", "ḷ", "ṃ",
]

ROOT_SIGN = ["√"]
HYPHEN = ["\\-"]

headword_allowed   = PALI_ALPHABET + ROOT_SIGN + HEADWORD_ALLOW_EXTRA
webkeyword_allowed = PALI_ALPHABET + HYPHEN + ROOT_SIGN + WEBKEYWORD_ALLOW_EXTRA


def join_allowed(chars: list[str]) -> str:
    return f"({'|'.join(chars)})"


class _HTMLErrorTracker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.errors: list[str] = []

    def error(self, message: str):
        self.errors.append(message)


def check_integers(rows: list, report_file) -> None:
    bad_id, bad_article_id = [], []
    for row in rows:
        if not isinstance(row["id"], int):
            bad_id.append(row["id"])
        if not isinstance(row["article_id"], int):
            bad_article_id.append(row["article_id"])

    for field, bad in (("id", bad_id), ("article_id", bad_article_id)):
        status = "[ok]" if not bad else f"[!!] {len(bad)} non-int values"
        print(f"  {field:<20} {status}")
        if bad:
            report_file.write(f"\n=== {field} — non-integer values ===\n")
            for v in bad:
                report_file.write(f"  {v!r}\n")


def _char_name(c: str) -> str:
    try:
        return unicodedata.name(c)
    except ValueError:
        return "?"


def check_field(rows: list, field: str, allowed_chars: list[str], report_file) -> None:
    pattern = join_allowed(allowed_chars)
    remainder_chars: set[str] = set()
    offenders: list[tuple] = []  # (id, article_id, value, leftovers)

    for row in rows:
        text = row[field] or ""
        oops = re.sub(pattern, "", text)
        if oops:
            remainder_chars.update(oops)
            offenders.append((row["id"], row["article_id"], text, oops))

    char_list = sorted(remainder_chars)

    if not char_list:
        print(f"  {field:<20} [ok]")
        return

    print(f"  {field:<20} [!!] {len(offenders)} rows — {len(char_list)} bad chars:")
    for c in char_list:
        print(f"    {c:<8} \\u{ord(c):04x}   {_char_name(c)}")

    # build first-example index: char → first value containing it
    first_example: dict[str, str] = {}
    for _row_id, _art_id, value, oops in offenders:
        for c in set(oops):
            if c not in first_example:
                first_example[c] = value

    report_file.write(f"\n{'='*70}\n{field} — {len(offenders)} offending rows\n{'='*70}\n")
    report_file.write(f"  {'char':<8} {'code':<12} {'unicode name':<40} example\n")
    report_file.write(f"  {'-'*8} {'-'*12} {'-'*40} {'-'*30}\n")
    for c in char_list:
        report_file.write(
            f"  {c:<8} \\u{ord(c):04x}     {_char_name(c):<40} {first_example[c]!r}\n"
        )


def check_html(rows: list, report_file) -> None:
    null_html, error_rows = [], []

    for row in rows:
        html = row["html"]
        if html is None:
            null_html.append(row["article_id"])
            continue
        tracker = _HTMLErrorTracker()
        try:
            tracker.feed(html)
        except Exception as e:
            error_rows.append((row["article_id"], [str(e)]))
            continue
        if tracker.errors:
            error_rows.append((row["article_id"], tracker.errors))

    parts = []
    if null_html:
        parts.append(f"{len(null_html)} null")
    if error_rows:
        parts.append(f"{len(error_rows)} parse errors")
    status = "[ok]" if not parts else "[!!] " + ", ".join(parts)
    print(f"  {'html':<20} {status}")

    if null_html:
        report_file.write(f"\n=== html — {len(null_html)} null rows ===\n")
        for art_id in null_html[:50]:
            report_file.write(f"  article_id={art_id}\n")
        if len(null_html) > 50:
            report_file.write(f"  ... and {len(null_html) - 50} more\n")

    if error_rows:
        report_file.write(f"\n=== html — {len(error_rows)} rows with parse errors ===\n")
        for art_id, errors in error_rows[:50]:
            report_file.write(f"  article_id={art_id}: {errors}\n")
        if len(error_rows) > 50:
            report_file.write(f"  ... and {len(error_rows) - 50} more\n")


def main():
    if not SOURCE_DB.exists():
        print(f"Source DB not found: {SOURCE_DB}")
        return

    con = sqlite3.connect(f"file:{SOURCE_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    rows = con.execute("SELECT id, article_id, headword, webkeyword, html FROM entries").fetchall()
    con.close()

    print(f"Loaded {len(rows):,} rows from {SOURCE_DB}\n")
    print(f"  {'Field':<20} Status")
    print(f"  {'-'*20} {'-'*40}")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_PATH.open("w", encoding="utf-8") as report:
        report.write(f"CPD Diagnostic Report — {len(rows):,} rows\n{'='*70}\n")
        check_integers(rows, report)
        check_field(rows, "headword",  headword_allowed,  report)
        check_field(rows, "webkeyword", webkeyword_allowed, report)
        check_html(rows, report)

    print(f"\nDetailed report written to {REPORT_PATH}")


if __name__ == "__main__":
    main()

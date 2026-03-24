"""
CPD Database Cleaner

Reads data/cpd.db (source — never modified).
Applies cleanup rules from cleanup_rules.py.
Writes cleaned data to data/cpd_clean.db.

Run: uv run python clean.py
Then: just diagnose-clean  to see what remains
"""

import re
import sqlite3
from pathlib import Path

from cleanup_rules import (
    CHAR_SUBSTITUTIONS,
    HEADWORD_DELETE,
    HEADWORD_WORD_FIXES,
    WEBKEYWORD_DELETE,
    WEBKEYWORD_WORD_FIXES,
)

SOURCE_DB = Path("data/cpd.db")
CLEAN_DB = Path("data/cpd_clean.db")

SLASH_PATTERN = re.compile(r"\[([^/\]]+)/([^/\]]+)\]")
HTML_TAG = re.compile(r"<[^>]+>")


# ---------------------------------------------------------------------------
# Transformation steps
# ---------------------------------------------------------------------------

def apply_word_fixes(text: str, fixes: dict[str, str]) -> str:
    for old, new in fixes.items():
        text = text.replace(old, new)
    return text


def apply_char_substitutions(text: str) -> str:
    for old, new in CHAR_SUBSTITUTIONS.items():
        text = text.replace(old, new)
    return text


def apply_deletes(text: str, delete_list: list[str]) -> str:
    for token in delete_list:
        text = text.replace(token, "")
    return text


def strip_html_tags(text: str) -> str:
    return HTML_TAG.sub("", text)


def slash_split(headword: str, webkeyword: str) -> list[tuple[str, str]]:
    """Expand [x/y] into two (headword, webkeyword) pairs.

    Matches the pattern [x/y] anywhere in the string.
    Everything before the bracket is the prefix, everything after is the suffix.

    e.g. āyāsan[ā/a]   → āyāsanā   / āyāsana
         [[ā/a]guṇḍita] → [āguṇḍita] / [aguṇḍita]  (outer [ ] deleted in step 4)
    """
    hw_match = SLASH_PATTERN.search(headword)
    if not hw_match:
        return [(headword, webkeyword)]

    def expand(text: str, match: re.Match) -> tuple[str, str]:
        x, y = match.group(1), match.group(2)
        prefix, suffix = text[:match.start()], text[match.end():]
        return prefix + x + suffix, prefix + y + suffix

    hw1, hw2 = expand(headword, hw_match)

    wk_match = SLASH_PATTERN.search(webkeyword)
    if wk_match:
        wk1, wk2 = expand(webkeyword, wk_match)
    else:
        wk1 = wk2 = webkeyword

    return [(hw1, wk1), (hw2, wk2)]


# ---------------------------------------------------------------------------
# Row processing — applies all steps in order
# ---------------------------------------------------------------------------

def process_row(row: sqlite3.Row) -> list[dict]:
    """Apply all cleaning rules to one source row.

    Returns a list of dicts — normally one, two if a slash split occurred.

    Order:
        0. Strip HTML tags from webkeyword (headword was already stripped by scraper)
        1. Word-level fixes
        2. Char substitutions
        3. Slash split  (must precede delete: delete removes [ ] chars)
        4. Delete chars
        5. Lowercase
    """
    hw = row["headword"] or ""
    wk = row["webkeyword"] or ""

    # 0. Strip HTML tags from webkeyword
    wk = strip_html_tags(wk)

    # 1. Word fixes
    hw = apply_word_fixes(hw, HEADWORD_WORD_FIXES)
    wk = apply_word_fixes(wk, WEBKEYWORD_WORD_FIXES)

    # 2. Char substitutions
    hw = apply_char_substitutions(hw)
    wk = apply_char_substitutions(wk)

    # 3. Slash split
    pairs = slash_split(hw, wk)

    results = []
    for hw_out, wk_out in pairs:
        # 4. Delete
        hw_out = apply_deletes(hw_out, HEADWORD_DELETE)
        wk_out = apply_deletes(wk_out, WEBKEYWORD_DELETE)

        # 5. Lowercase
        hw_out = hw_out.lower()
        wk_out = wk_out.lower()

        results.append({
            "article_id": row["article_id"],
            "headword":   hw_out,
            "webkeyword": wk_out,
            "html":       row["html"],
            "failed":     row["failed"],
        })

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not SOURCE_DB.exists():
        print(f"Source DB not found: {SOURCE_DB}")
        return

    con = sqlite3.connect(f"file:{SOURCE_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT id, article_id, headword, webkeyword, html, failed FROM entries"
    ).fetchall()
    con.close()

    print(f"Source rows: {len(rows):,}")

    CLEAN_DB.unlink(missing_ok=True)
    out = sqlite3.connect(CLEAN_DB)
    out.execute("""
        CREATE TABLE entries (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL,
            headword   TEXT NOT NULL,
            webkeyword TEXT NOT NULL,
            html       TEXT,
            failed     TEXT
        )
    """)

    split_count = 0
    out_rows = []
    for row in rows:
        cleaned = process_row(row)
        if len(cleaned) == 2:
            split_count += 1
        out_rows.extend(cleaned)

    out.executemany(
        "INSERT INTO entries (article_id, headword, webkeyword, html, failed) "
        "VALUES (:article_id, :headword, :webkeyword, :html, :failed)",
        out_rows,
    )
    out.commit()
    out.close()

    print(f"Slash splits:  {split_count:,}")
    print(f"Output rows:   {len(out_rows):,}")
    print(f"Written to:    {CLEAN_DB}")


if __name__ == "__main__":
    main()

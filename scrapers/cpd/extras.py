"""
CPD Extras Injector

Reads supplementary intro pages from data/intro/ and injects them into
data/cpd_clean.db as 3 combined entries (one per website section).

Run: uv run python extras.py
"""

import re
import sqlite3
from pathlib import Path

CLEAN_DB = Path("data/cpd_clean.db")
INTRO_DIR = Path("data/intro")
EXTRAS_ID_OFFSET = 90000

GROUPS = [
    ("cpd prefaces", "cpd-prefaces", [
        "trenckner.html",
        "preface_vol1.html",
        "preface_vol2.html",
        "preface_vol3.html",
        "contributors_vol2.html",
        "vol3_list_of_contributors.html",
        "vol1_on_critics_and_new_texts.html",
        "vol3_notice_about_development.html",
        "vol3_concluding_remarks.html",
    ]),
    ("cpd obituaries", "cpd-obituaries", [
        "ludwig_alsdorf_obituary.html",
        "dines_andersen_obituary.html",
        "wilhelm_geiger_obituary.html",
        "klas_hagren_obituary.html",
        "elof_olesen_obituary.html",
        "else_margrethe_pauly_obituary.html",
        "helmer_smith_obituary.html",
    ]),
    ("cpd bibliography", "cpd-bibliography", [
        "vol1_epileg_abbrev_texts.html",
        "vol3_consolidated_list_of_abbreviations.html",
        "vol1_epileg_bibliography.html",
        "vol1_epileg_concordances.html",
        "vol1_epileg_general_index.html",
        "vol1_epileg_terms_and_signs.html",
        "how_to_use.html",
    ]),
]

DIV_OPEN = re.compile(r"<div\b")
DIV_CLOSE = "</div>"
CONTENTS_START = re.compile(r'<div\s+id="contents"[^>]*>')


def extract_contents(text: str) -> str:
    """Return the inner HTML of <div id="contents">...</div>."""
    m = CONTENTS_START.search(text)
    if not m:
        return ""
    pos = m.end()
    depth = 1
    while depth > 0 and pos < len(text):
        next_open = DIV_OPEN.search(text, pos)
        next_close = text.find(DIV_CLOSE, pos)
        if next_close == -1:
            break
        open_pos = next_open.start() if next_open else len(text)
        if open_pos < next_close:
            depth += 1
            pos = next_open.end()
        else:
            depth -= 1
            if depth == 0:
                return text[m.end():next_close]
            pos = next_close + len(DIV_CLOSE)
    return ""


def build_html(article_id: int, filenames: list[str]) -> str:
    sections = []
    for filename in filenames:
        path = INTRO_DIR / filename
        if not path.exists():
            print(f"  warning: {filename} not found, skipping")
            continue
        inner = extract_contents(path.read_text(encoding="utf-8"))
        if inner.strip():
            sections.append(f'<section class="intro-page">{inner}</section>')
        else:
            print(f"  warning: no contents found in {filename}")

    body = "\n<hr/>\n".join(sections)
    return f'<article data-id="{article_id}" class="intro">\n{body}\n</article>'


def main():
    if not CLEAN_DB.exists():
        print(f"Database not found: {CLEAN_DB}")
        return

    db = sqlite3.connect(CLEAN_DB)

    extra_ids = [EXTRAS_ID_OFFSET + i + 1 for i in range(len(GROUPS))]
    db.execute(
        f"DELETE FROM entries WHERE article_id IN ({','.join('?' * len(extra_ids))})",
        extra_ids,
    )

    rows = []
    for i, (headword, webkeyword, filenames) in enumerate(GROUPS):
        article_id = EXTRAS_ID_OFFSET + i + 1
        html = build_html(article_id, filenames)
        rows.append({
            "article_id": article_id,
            "headword":   headword,
            "webkeyword": webkeyword,
            "html":       html,
            "failed":     None,
        })
        print(f"  {article_id}  {headword}  ({len(filenames)} pages, {len(html):,} bytes)")

    db.executemany(
        "INSERT INTO entries (article_id, headword, webkeyword, html, failed) "
        "VALUES (:article_id, :headword, :webkeyword, :html, :failed)",
        rows,
    )
    db.commit()
    db.close()

    print(f"{len(rows)} intro entries written to {CLEAN_DB}")


if __name__ == "__main__":
    main()

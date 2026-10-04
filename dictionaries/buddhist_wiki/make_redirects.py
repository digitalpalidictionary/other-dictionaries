# -*- coding: utf-8 -*-
"""Add every enwiki redirect that points at a listed article to redirects.json.

Streams the `redirect` SQL dump, keeps mainspace redirects whose target is
in article_list.txt, resolves each redirect's own title through the `page`
table already loaded in catgraph.sqlite3 (by make_article_list.py), and
merges the result into source/redirects.json. Redirect titles become
synonyms, and links written with them resolve to the article.

Never run it while fetch_wikitext.py runs: the fetcher reads redirects.json
once at start and rewrites it after every batch, so it would overwrite
redirects added in the meantime.

Usage:
    uv run python dictionaries/buddhist_wiki/make_redirects.py
"""

import gzip
import sqlite3
from pathlib import Path

from dictionaries.buddhist_wiki.dump_rows import iter_dump_rows
from dictionaries.buddhist_wiki.fetch_wikitext import (
    load_redirects,
    read_title_list,
    save_redirects,
)
from dictionaries.buddhist_wiki.make_article_list import _indices, read_columns
from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr

NS_MAIN = 0


def redirect_ids_to_targets(gz_path: Path, wanted: set[str]) -> dict[int, str]:
    """Map redirect page id → target title, for mainspace targets in `wanted`."""
    columns = read_columns(gz_path, "redirect")
    i_from, i_ns, i_title, i_iw = _indices(
        columns, ["rd_from", "rd_namespace", "rd_title", "rd_interwiki"], gz_path.name
    )
    found: dict[int, str] = {}
    rows = 0
    with gzip.open(gz_path, "rt", encoding="utf-8", errors="replace") as fh:
        for row in iter_dump_rows(fh, "redirect"):
            rows += 1
            if row[i_ns] != NS_MAIN or row[i_iw]:
                continue
            target = row[i_title].replace("_", " ")
            if target in wanted:
                found[row[i_from]] = target
    if rows == 0:
        raise RuntimeError(f"parsed 0 rows from {gz_path.name}; dump format changed?")
    return found


def redirect_titles(db_path: Path, targets: dict[int, str]) -> dict[str, str]:
    """Resolve redirect page ids to titles: {redirect title: target title}."""
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    ids = sorted(targets)
    result: dict[str, str] = {}
    for start in range(0, len(ids), 500):
        chunk = ids[start : start + 500]
        ph = ",".join("?" * len(chunk))
        for page_id, title in conn.execute(
            f"SELECT id, title FROM ppage WHERE id IN ({ph}) AND ns = ?",
            (*chunk, NS_MAIN),
        ):
            result[title.replace("_", " ")] = targets[page_id]
    conn.close()
    return result


def main() -> None:
    pr.tic()
    pr.title("adding dump redirects to redirects.json")
    pth = RepoPaths()
    dumps = pth.buddhist_wiki_source_dir / "dumps"
    wanted = set(read_title_list(pth.buddhist_wiki_article_list_path))
    targets = redirect_ids_to_targets(dumps / "enwiki-latest-redirect.sql.gz", wanted)
    pr.white(f"{len(targets)} redirects point at listed articles")
    found = redirect_titles(dumps / "catgraph.sqlite3", targets)

    redirects = load_redirects(pth.buddhist_wiki_redirects_path)
    before = len(redirects)
    redirects.update(found)
    save_redirects(pth.buddhist_wiki_redirects_path, redirects)
    pr.yes(f"{before} → {len(redirects)} redirects")
    pr.toc()


if __name__ == "__main__":
    main()

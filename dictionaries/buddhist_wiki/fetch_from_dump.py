# -*- coding: utf-8 -*-
"""Extract wikitext for the article list from the pages-articles dump.

Stream-parses enwiki-latest-pages-articles.xml.bz2 and appends
{title, wikitext} rows to source/wikitext.jsonl for every title in
article_list.txt that isn't checkpointed yet. Fully resumable: the
checkpoint file from the API fetcher is shared, so Phase 1 articles are
never re-extracted, and an interrupted run re-parses the dump but only
writes the missing rows.

The same pass collects every mainspace redirect whose target is in the
article list and merges it into source/redirects.json, so links to
alternative titles resolve and redirects become synonyms. Redirects are
only complete after a full pass, which `dump_redirects.done` records.

Usage:
    uv run python dictionaries/buddhist_wiki/fetch_from_dump.py
"""

import bz2
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from dictionaries.buddhist_wiki.fetch_wikitext import (
    append_checkpoint,
    append_jsonl,
    load_checkpoint,
    load_redirects,
    read_title_list,
    save_redirects,
)
from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr

# ElementTree needs `{*}` to match a tag in any namespace; the dump's tags
# all carry the export-0.11 namespace
TITLE_TAG = "{*}title"
NS_TAG = "{*}ns"
REDIRECT_TAG = "{*}redirect"
TEXT_PATH = "{*}revision/{*}text"


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def extract_from_dump(
    dump_path: Path,
    list_path: Path,
    jsonl_path: Path,
    checkpoint_path: Path,
    redirects_path: Path,
) -> dict[str, Any]:
    """Parse the pages-articles dump, writing rows for pending titles."""
    wanted = set(read_title_list(list_path))
    completed = load_checkpoint(checkpoint_path)
    pending = wanted - completed
    pr.white(f"{len(wanted)} titles in list, {len(completed)} checkpointed")

    redirects_done = jsonl_path.parent / "dump_redirects.done"
    if not pending and redirects_done.exists():
        pr.yes("all titles and redirects already extracted — nothing to do")
        return {"found": 0, "missing": 0, "redirects": 0, "scanned_pages": 0}

    found: set[str] = set()
    redirects: dict[str, str] = {}
    scanned = 0
    batch: list[dict[str, str]] = []

    with bz2.open(dump_path, "rb") as fh:
        context = ET.iterparse(fh, events=("start", "end"))
        _, root = next(context)
        for event, elem in context:
            if event != "end" or _local(elem.tag) != "page":
                continue
            scanned += 1
            title = elem.findtext(TITLE_TAG)
            redirect_elem = elem.find(REDIRECT_TAG)
            if title is None:
                pass
            elif redirect_elem is not None:
                target = (redirect_elem.get("title") or "").split("#", 1)[0]
                if elem.findtext(NS_TAG) == "0" and target in wanted:
                    redirects[title] = target
            elif title in pending:
                wikitext = elem.findtext(TEXT_PATH)
                if wikitext:
                    batch.append({"title": title, "wikitext": wikitext})
                    found.add(title)
                if len(batch) >= 5_000:
                    append_jsonl(jsonl_path, batch)
                    append_checkpoint(checkpoint_path, [r["title"] for r in batch])
                    pr.counter(len(found), len(pending), "articles extracted")
                    batch = []
            elem.clear()
            root.clear()
            if scanned % 1_000_000 == 0:
                pr.counter(scanned, 0, "pages scanned")

    if batch:
        append_jsonl(jsonl_path, batch)
        append_checkpoint(checkpoint_path, [r["title"] for r in batch])

    merged = load_redirects(redirects_path)
    merged.update(redirects)
    save_redirects(redirects_path, merged)
    redirects_done.touch()

    missing = sorted(pending - found)
    if missing:
        missing_path = jsonl_path.parent / "missing_dump.txt"
        with open(missing_path, "a", encoding="utf-8") as f:
            for title in missing:
                f.write(f"{title}\n")

    return {
        "found": len(found),
        "missing": len(missing),
        "redirects": len(redirects),
        "scanned_pages": scanned,
    }


def main() -> None:
    pr.tic()
    pr.title("extracting wikitext from pages-articles dump")
    pth = RepoPaths()
    dump_path = (
        pth.buddhist_wiki_source_dir / "dumps" / "enwiki-latest-pages-articles.xml.bz2"
    )
    if not dump_path.exists():
        pr.no(f"dump not found: {dump_path}")
        return
    result = extract_from_dump(
        dump_path,
        pth.buddhist_wiki_article_list_path,
        pth.buddhist_wiki_wikitext_path,
        pth.buddhist_wiki_fetch_checkpoint_path,
        pth.buddhist_wiki_redirects_path,
    )
    pr.summary("articles extracted", result["found"])
    pr.summary("missing from dump", result["missing"])
    pr.summary("redirects found", result["redirects"])
    pr.toc()


if __name__ == "__main__":
    main()

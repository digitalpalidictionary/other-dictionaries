# -*- coding: utf-8 -*-
"""Resumable API fetch of Wikipedia article wikitext.

Fetches the raw wikitext of every title in seed_articles.txt (or a list file
passed with --list) via the MediaWiki action API, resolving redirects, and
appends to source/wikitext.jsonl. Safe to interrupt and re-run: completed
titles are tracked in a checkpoint file and skipped on the next run.

Usage:
    uv run python dictionaries/buddhist_wiki/fetch_wikitext.py
    uv run python dictionaries/buddhist_wiki/fetch_wikitext.py --list path.txt
"""

import argparse
import json
import time
from pathlib import Path
from typing import Any

import httpx

from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr

API_URL = "https://en.wikipedia.org/w/api.php"
USER_AGENT = (
    "dpd-other-dictionaries/0.1 "
    "(https://github.com/digitalpalidictionary/dpd-db; "
    "digitalpalidictionary@gmail.com)"
)
BATCH_SIZE = 20
MAX_ATTEMPTS = 8
BACKOFF_BASE_SECONDS = 2.0


def read_title_list(list_path: Path) -> list[str]:
    """Read one title per line, skipping blanks and # comments.

    Underscores are converted to spaces: enwiki canonical titles use spaces,
    and the checkpoint/redirect stores match that form.
    """
    titles: list[str] = []
    with open(list_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip().replace("_", " ")
            if line and not line.startswith("#"):
                titles.append(line)
    return titles


def load_checkpoint(checkpoint_path: Path) -> set[str]:
    """Load the set of completed titles (canonical form) from the checkpoint."""
    if not checkpoint_path.exists():
        return set()
    with open(checkpoint_path, encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def append_checkpoint(checkpoint_path: Path, titles: list[str]) -> None:
    with open(checkpoint_path, "a", encoding="utf-8") as f:
        for title in titles:
            f.write(f"{title}\n")


def append_jsonl(jsonl_path: Path, rows: list[dict[str, Any]]) -> None:
    with open(jsonl_path, "a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_redirects(redirects_path: Path) -> dict[str, str]:
    if not redirects_path.exists():
        return {}
    with open(redirects_path, encoding="utf-8") as f:
        return dict(json.load(f))


def save_redirects(redirects_path: Path, redirects: dict[str, str]) -> None:
    with open(redirects_path, "w", encoding="utf-8") as f:
        json.dump(redirects, f, ensure_ascii=False, sort_keys=True, indent=0)


def api_get(client: httpx.Client, params: dict[str, str]) -> dict[str, Any]:
    """One action-API GET with exponential backoff on 429/5xx and network errors."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = client.get(API_URL, params=params)
            if response.status_code == 429 or response.status_code >= 500:
                raise httpx.HTTPStatusError(
                    f"status {response.status_code}",
                    request=response.request,
                    response=response,
                )
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, httpx.StreamError) as e:
            if attempt == MAX_ATTEMPTS:
                raise RuntimeError(
                    f"giving up after {MAX_ATTEMPTS} attempts: {params.get('titles', '')}"
                ) from e
            delay = BACKOFF_BASE_SECONDS * (2 ** (attempt - 1))
            pr.warning(f"attempt {attempt} failed ({e}); retrying in {delay:.0f}s")
            time.sleep(delay)
    raise AssertionError("unreachable")


def fetch_batch(
    client: httpx.Client, titles: list[str]
) -> tuple[list[dict[str, Any]], dict[str, str], dict[str, str], list[str]]:
    """Fetch one batch of titles.

    Returns (rows, redirects, normalized, missing):
    - rows: {"title": canonical_title, "wikitext": str}
    - redirects: {redirect_title: canonical_title} for this batch
    - normalized: {requested_title: canonical_title} for this batch
    - missing: requested titles that do not exist
    """
    params: dict[str, str] = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
        "redirects": "1",
        "titles": "|".join(titles),
    }
    data = api_get(client, params)
    query = data.get("query", {})

    canonical: dict[str, str] = {t: t for t in titles}
    for item in query.get("normalized", []):
        canonical[item["from"]] = item["to"]
    redirects: dict[str, str] = {}
    for item in query.get("redirects", []):
        canonical[item["from"]] = item["to"]
        redirects[item["from"]] = item["to"]

    rows: list[dict[str, Any]] = []
    missing: list[str] = []
    for page in query.get("pages", []):
        if "missing" in page:
            missing.append(page["title"])
            continue
        revisions = page.get("revisions", [])
        if not revisions:
            # an existing page without revisions means the API cut the batch
            # short (result-size limit); leave it unchecked so a re-run retries
            pr.warning(f"no content returned for {page['title']}; will retry")
            continue
        slots = revisions[0].get("slots", {})
        # formatversion=2 puts content under "content"; v1 used "*"
        wikitext = slots.get("main", {}).get("content", "")
        if not wikitext:
            missing.append(page["title"])
            continue
        rows.append({"title": page["title"], "wikitext": wikitext})

    normalized = {t: canonical.get(t, t) for t in titles if canonical.get(t, t) != t}
    return rows, redirects, normalized, missing


def fetch_all(
    list_path: Path,
    jsonl_path: Path,
    checkpoint_path: Path,
    redirects_path: Path,
    missing_path: Path,
) -> None:
    """Fetch every not-yet-fetched title, appending to the jsonl store."""
    titles = read_title_list(list_path)
    pr.white(f"{len(titles)} titles in list")

    completed = load_checkpoint(checkpoint_path)
    redirects = load_redirects(redirects_path)
    pr.white(f"{len(completed)} already fetched (checkpoint)")

    # resolve list titles through known redirects so resume works cleanly
    todo: list[str] = []
    for title in titles:
        canonical = redirects.get(title, title)
        if canonical not in completed:
            todo.append(title)
    # dedupe, keep order
    seen: set[str] = set()
    todo = [t for t in todo if not (t in seen or seen.add(t))]

    pr.green(f"{len(todo)} titles to fetch")
    if not todo:
        pr.yes("nothing to fetch")
        return

    batches = [todo[i : i + BATCH_SIZE] for i in range(0, len(todo), BATCH_SIZE)]
    fetched = 0
    with httpx.Client(
        headers={"User-Agent": USER_AGENT},
        timeout=httpx.Timeout(60.0),
        follow_redirects=True,
    ) as client:
        for i, batch in enumerate(batches, 1):
            rows, batch_redirects, normalized, missing = fetch_batch(client, batch)
            append_jsonl(jsonl_path, rows)

            redirects.update(batch_redirects)
            save_redirects(redirects_path, redirects)

            checkpoint_titles = [row["title"] for row in rows]
            if missing:
                with open(missing_path, "a", encoding="utf-8") as f:
                    for title in missing:
                        f.write(f"{title}\n")
                # record a canonical miss in the checkpoint so a re-run
                # doesn't retry permanently missing titles
                for title in missing:
                    canonical = redirects.get(title, title)
                    if canonical not in checkpoint_titles:
                        checkpoint_titles.append(canonical)
            append_checkpoint(checkpoint_path, checkpoint_titles)

            fetched += len(rows)
            pr.counter(fetched, len(todo), f"batch {i}/{len(batches)}")
            # polite: 1 req / ~2s keeps well under the anonymous rate limit
            if i < len(batches):
                time.sleep(2.0)

    pr.yes(f"fetched {fetched} articles, {len(redirects)} redirects known")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--list",
        type=Path,
        default=None,
        help="title list file (default: seed_articles.txt)",
    )
    args = parser.parse_args()

    pr.tic()
    pr.title("fetching Wikipedia wikitext")
    pth = RepoPaths()

    list_path = args.list or pth.buddhist_wiki_seed_articles_path
    fetch_all(
        list_path=list_path,
        jsonl_path=pth.buddhist_wiki_wikitext_path,
        checkpoint_path=pth.buddhist_wiki_fetch_checkpoint_path,
        redirects_path=pth.buddhist_wiki_redirects_path,
        missing_path=pth.buddhist_wiki_source_dir / "missing.txt",
    )
    pr.toc()


if __name__ == "__main__":
    main()

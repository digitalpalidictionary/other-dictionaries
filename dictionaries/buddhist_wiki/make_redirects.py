# -*- coding: utf-8 -*-
"""Add every enwiki redirect that points at a listed article to redirects.json.

Asks the action API for each article's mainspace redirects
(`prop=redirects`, 50 titles per request, following `continue`) and merges
them into source/redirects.json. Redirect titles become synonyms, and links
written with them resolve to the article. The API needs no dump, so the
redirect map can be rebuilt from the committed article list alone.

Never run it while fetch_wikitext.py runs: the fetcher reads redirects.json
once at start and rewrites it after every batch, so it would overwrite
redirects added in the meantime.

Usage:
    uv run python dictionaries/buddhist_wiki/make_redirects.py
"""

import time

import httpx

from dictionaries.buddhist_wiki.fetch_wikitext import (
    USER_AGENT,
    api_get,
    load_redirects,
    read_title_list,
    save_redirects,
)
from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr

BATCH_SIZE = 50


def fetch_redirect_batch(client: httpx.Client, titles: list[str]) -> dict[str, str]:
    """Return {redirect title: article title} for one batch of titles."""
    params: dict[str, str] = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "redirects",
        "rdnamespace": "0",
        "rdprop": "title",
        "rdlimit": "max",
        # a listed title renamed since the dump resolves to its new page
        "redirects": "1",
        "titles": "|".join(titles),
    }
    found: dict[str, str] = {}
    while True:
        data = api_get(client, params)
        query = data.get("query", {})
        for item in query.get("redirects", []):
            found[item["from"]] = item["to"]
        for page in query.get("pages", []):
            for redirect in page.get("redirects", []):
                found[redirect["title"]] = page["title"]
        if "continue" not in data:
            return found
        params = {**params, **data["continue"]}


def main() -> None:
    pr.tic()
    pr.title("adding API redirects to redirects.json")
    pth = RepoPaths()
    titles = read_title_list(pth.buddhist_wiki_article_list_path)
    redirects = load_redirects(pth.buddhist_wiki_redirects_path)
    before = len(redirects)

    batches = [titles[i : i + BATCH_SIZE] for i in range(0, len(titles), BATCH_SIZE)]
    with httpx.Client(
        headers={"User-Agent": USER_AGENT}, timeout=httpx.Timeout(60.0)
    ) as client:
        for i, batch in enumerate(batches, 1):
            redirects.update(fetch_redirect_batch(client, batch))
            pr.counter(i, len(batches), "batches")
            # polite: well under the anonymous rate limit
            time.sleep(1.0)

    save_redirects(pth.buddhist_wiki_redirects_path, redirects)
    pr.yes(f"{before} → {len(redirects)} redirects")
    pr.toc()


if __name__ == "__main__":
    main()

"""Tests for the Wikipedia API wikitext fetcher (faked responses)."""

import httpx

from dictionaries.buddhist_wiki.fetch_wikitext import fetch_batch

# shape of a real formatversion=2 action=query&prop=revisions response
API_RESPONSE = {
    "batchcomplete": True,
    "query": {
        "redirects": [{"from": "Kamma", "to": "Karma"}],
        "pages": [
            {
                "pageid": 16864,
                "ns": 0,
                "title": "Karma",
                "revisions": [
                    {
                        "slots": {
                            "main": {
                                "contentmodel": "wikitext",
                                "contentformat": "text/x-wiki",
                                "content": "'''Karma''' is a concept.",
                            }
                        }
                    }
                ],
            },
            {"ns": 0, "title": "No such article xyz", "missing": True},
            {"pageid": 11393, "ns": 0, "title": "Four Noble Truths"},
        ],
    },
}


def _client() -> httpx.Client:
    return httpx.Client(
        transport=httpx.MockTransport(lambda _: httpx.Response(200, json=API_RESPONSE))
    )


def test_fetch_batch_returns_content_and_redirects() -> None:
    rows, redirects, _, _ = fetch_batch(
        _client(), ["Kamma", "No such article xyz", "Four Noble Truths"]
    )
    assert rows == [{"title": "Karma", "wikitext": "'''Karma''' is a concept."}]
    assert redirects == {"Kamma": "Karma"}


def test_fetch_batch_cut_off_page_is_not_missing() -> None:
    _, _, _, missing = fetch_batch(
        _client(), ["Kamma", "No such article xyz", "Four Noble Truths"]
    )
    # a page that exists but came back without content must be retried,
    # never recorded as permanently missing
    assert missing == ["No such article xyz"]

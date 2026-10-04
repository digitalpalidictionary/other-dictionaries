"""Tests for the API redirect step of the Buddhist Wiki dictionary.

Responses are copied from the live action API (2026-10-05) for
titles=Karma|Avidyā (Buddhism), cut to a few redirects per page.
"""

import httpx

from dictionaries.buddhist_wiki.make_redirects import fetch_redirect_batch

FIRST_PAGE = {
    "continue": {"rdcontinue": "Karma|210588", "continue": "||"},
    "query": {
        "redirects": [{"from": "Avidyā (Buddhism)", "to": "Avidyā"}],
        "pages": [
            {"pageid": 16864, "ns": 0, "title": "Karma"},
            {
                "pageid": 36640701,
                "ns": 0,
                "title": "Avidyā",
                "redirects": [
                    {"ns": 0, "title": "Avidyā (Hinduism)"},
                    {"ns": 0, "title": "Avidya"},
                ],
            },
        ],
    },
}
SECOND_PAGE = {
    "batchcomplete": True,
    "query": {
        "pages": [
            {
                "pageid": 16864,
                "ns": 0,
                "title": "Karma",
                "redirects": [{"ns": 0, "title": "Karmic"}],
            },
            {"pageid": 36640701, "ns": 0, "title": "Avidyā"},
        ],
    },
}


def test_follows_continue_and_maps_redirects_to_articles() -> None:
    seen: list[dict[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(dict(request.url.params))
        page = SECOND_PAGE if "rdcontinue" in request.url.params else FIRST_PAGE
        return httpx.Response(200, json=page)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    found = fetch_redirect_batch(client, ["Karma", "Avidyā (Buddhism)"])

    assert found == {
        "Avidyā (Buddhism)": "Avidyā",
        "Avidyā (Hinduism)": "Avidyā",
        "Avidya": "Avidyā",
        "Karmic": "Karma",
    }
    # the second request carried the continue token
    assert len(seen) == 2
    assert seen[1]["rdcontinue"] == "Karma|210588"

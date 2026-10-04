"""Tests for the Category:Buddhism walk of the Buddhist Wiki dictionary.

Ids and titles are real rows from the enwiki-20261001 page, linktarget and
categorylinks dumps: Buddhism → Buddhist_terminology →
Buddhist_philosophical_concepts → Karma. Categories link to their parent
by the parent's linktarget id, never its page id. The edge from Buddhism to
the hidden category and its member page 1 are added for the test.
"""

import sqlite3
from pathlib import Path

import pytest

from dictionaries.buddhist_wiki.make_article_list import (
    _create_tables,
    live_seed_titles,
    member_titles,
    walk_categories,
)

ROOT_LT = 20316599  # Category:Buddhism
TERMINOLOGY_LT = 20586335  # Category:Buddhist_terminology
CONCEPTS_LT = 26939709  # Category:Buddhist_philosophical_concepts
HIDDEN_LT = 1  # Category:Articles_containing_Pali-language_text (test id)

PAGES = [
    # (id, title, is_redirect, ns)
    (693801, "Buddhism", 0, 14),
    (44452918, "Buddhist_terminology", 0, 14),
    (742369, "Buddhist_philosophical_concepts", 0, 14),
    (56039551, "Articles_containing_Pali-language_text", 0, 14),
    (16864, "Karma", 0, 0),
    (13352172, "Kamma", 1, 0),
    (1, "Only_in_hidden", 0, 0),
]
LINKTARGETS = [
    (ROOT_LT, "Buddhism"),
    (TERMINOLOGY_LT, "Buddhist_terminology"),
    (CONCEPTS_LT, "Buddhist_philosophical_concepts"),
    (HIDDEN_LT, "Articles_containing_Pali-language_text"),
]
CATLINKS = [
    # (cl_from page id, cl_target lt_id, cl_type)
    (44452918, ROOT_LT, "subcat"),
    (742369, TERMINOLOGY_LT, "subcat"),
    (16864, CONCEPTS_LT, "page"),
    (16864, HIDDEN_LT, "page"),
    (56039551, ROOT_LT, "subcat"),
    (1, HIDDEN_LT, "page"),
]


@pytest.fixture()
def conn() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    _create_tables(db)
    db.executemany("INSERT INTO ppage VALUES (?,?,?,?)", PAGES)
    db.executemany("INSERT INTO lt VALUES (?,?)", LINKTARGETS)
    db.executemany("INSERT INTO catlink VALUES (?,?,?)", CATLINKS)
    db.execute("INSERT INTO props VALUES (56039551, 'hiddencat')")
    db.execute(
        "INSERT INTO catmap SELECT p.id, l.id FROM ppage p"
        " JOIN lt l ON l.title = p.title WHERE p.ns = 14"
    )
    return db


def test_walk_follows_linktarget_ids_to_max_depth(conn: sqlite3.Connection) -> None:
    assert walk_categories(conn, "Buddhism", 1) == {ROOT_LT, TERMINOLOGY_LT}
    assert walk_categories(conn, "Buddhism", 2) == {
        ROOT_LT,
        TERMINOLOGY_LT,
        CONCEPTS_LT,
    }


def test_walk_skips_hidden_categories(conn: sqlite3.Connection) -> None:
    assert HIDDEN_LT not in walk_categories(conn, "Buddhism", 5)


def test_members_are_live_articles_with_spaces(conn: sqlite3.Connection) -> None:
    assert member_titles(conn, walk_categories(conn, "Buddhism", 2)) == {"Karma"}
    assert member_titles(conn, walk_categories(conn, "Buddhism", 1)) == set()


def test_seed_titles_drop_redirects_and_dead_titles(
    conn: sqlite3.Connection, tmp_path: Path
) -> None:
    seed = tmp_path / "seed_articles.txt"
    seed.write_text("Karma\nKamma\nAkusala\n", encoding="utf-8")
    assert live_seed_titles(conn, seed) == {"Karma"}

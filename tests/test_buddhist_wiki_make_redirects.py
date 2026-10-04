"""Tests for the redirect-dump step of the Buddhist Wiki dictionary.

Header and rows are copied from enwiki-20261001-redirect.sql.gz; page
titles for those ids are from enwiki-20261001-page.sql.gz.
"""

import gzip
import sqlite3
from pathlib import Path

from dictionaries.buddhist_wiki.make_redirects import (
    redirect_ids_to_targets,
    redirect_titles,
)

REDIRECT_DUMP = """\
CREATE TABLE `redirect` (
  `rd_from` int(8) unsigned NOT NULL DEFAULT 0,
  `rd_namespace` int(11) NOT NULL DEFAULT 0,
  `rd_title` varbinary(255) NOT NULL DEFAULT '',
  `rd_interwiki` varbinary(32) DEFAULT NULL,
  `rd_fragment` varbinary(255) DEFAULT NULL,
  PRIMARY KEY (`rd_from`),
  KEY `rd_ns_title` (`rd_namespace`,`rd_title`,`rd_from`)
) ENGINE=InnoDB DEFAULT CHARSET=binary ROW_FORMAT=COMPRESSED;
INSERT INTO `redirect` VALUES
(10,0,'Computer_accessibility','',''),
(13,0,'History_of_Afghanistan','',''),
(50760,14,'Wikipedia','',''),
(51868,0,'Bodhisattva','','');
"""

# (id, title, is_redirect, ns) as in the catgraph `ppage` table
PAGES = [
    (10, "AccessibleComputing", 1, 0),
    (13, "AfghanistanHistory", 1, 0),
    (50760, "Wikidex", 1, 4),
    (51868, "Bodhisattvas", 1, 0),
]


def _dump(tmp_path: Path) -> Path:
    gz = tmp_path / "redirect.sql.gz"
    with gzip.open(gz, "wt", encoding="utf-8") as f:
        f.write(REDIRECT_DUMP)
    return gz


def _catgraph(tmp_path: Path) -> Path:
    db = tmp_path / "catgraph.sqlite3"
    conn = sqlite3.connect(db)
    conn.execute(
        "CREATE TABLE ppage (id INTEGER PRIMARY KEY, title TEXT,"
        " is_redirect INTEGER, ns INTEGER)"
    )
    conn.executemany("INSERT INTO ppage VALUES (?,?,?,?)", PAGES)
    conn.commit()
    conn.close()
    return db


def test_keeps_only_mainspace_redirects_to_listed_articles(tmp_path: Path) -> None:
    targets = redirect_ids_to_targets(
        _dump(tmp_path), {"Bodhisattva", "History of Afghanistan", "Wikipedia"}
    )
    # 50760 points at Category:Wikipedia (ns 14), not the article
    assert targets == {13: "History of Afghanistan", 51868: "Bodhisattva"}


def test_resolves_redirect_titles_with_spaces(tmp_path: Path) -> None:
    found = redirect_titles(
        _catgraph(tmp_path), {13: "History of Afghanistan", 51868: "Bodhisattva"}
    )
    assert found == {
        "AfghanistanHistory": "History of Afghanistan",
        "Bodhisattvas": "Bodhisattva",
    }

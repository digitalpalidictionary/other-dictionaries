# -*- coding: utf-8 -*-
"""Build the full article list for the enwiki Category:Buddhism subtree.

Reads the dumps.wikimedia.org SQL dumps (categorylinks, linktarget, page,
page_props), loads them into a SQLite database kept next to the dumps,
walks the category graph from Category:Buddhism breadth-first (descending
through subcategories, skipping hidden categories), and writes every
mainspace non-redirect member page to article_list.txt. Dumps and the
SQLite db are never deleted.

Column order is read from each dump's CREATE TABLE header — never
hardcoded. Since MediaWiki 1.45 `categorylinks` has no `cl_to` title
column: `cl_target_id` is a `linktarget.lt_id`, NOT a page id. A
subcategory row's `cl_from` is the subcategory's page id, so each step of
the walk maps page id → title (`page`) → lt_id (`linktarget`).

Usage:
    uv run python dictionaries/buddhist_wiki/make_article_list.py
"""

import gzip
import re
import sqlite3
from collections.abc import Callable
from pathlib import Path

from dictionaries.buddhist_wiki.dump_rows import iter_dump_rows
from dictionaries.buddhist_wiki.fetch_wikitext import read_title_list
from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr

ROOT_CATEGORY = "Buddhism"
# measured 2026-10-04: below depth 5 the tree drifts into the general
# history and culture of Buddhist countries (footballers, film, politics)
MAX_DEPTH = 5
NS_MAIN = 0
NS_CATEGORY = 14
SQL_BATCH = 50_000


def _dumps_dir(pth: RepoPaths) -> Path:
    return pth.buddhist_wiki_source_dir / "dumps"


def read_columns(gz_path: Path, table: str) -> list[str]:
    """Read the column order of `table` from the dump's CREATE TABLE."""
    with gzip.open(gz_path, "rt", encoding="utf-8", errors="replace") as f:
        in_table = False
        cols: list[str] = []
        for line in f:
            if not in_table:
                if line.startswith(f"CREATE TABLE `{table}`"):
                    in_table = True
                continue
            stripped = line.strip()
            if stripped.startswith(")"):
                return cols
            m = re.match(r"`([^`]+)`", stripped)
            if m:
                cols.append(m.group(1))
    raise ValueError(f"CREATE TABLE for `{table}` not found in {gz_path.name}")


def _indices(columns: list[str], wanted: list[str], gz_name: str) -> list[int]:
    idx = {c: i for i, c in enumerate(columns)}
    missing = [c for c in wanted if c not in idx]
    if missing:
        raise ValueError(f"{gz_name}: columns {missing} not in schema {columns}")
    return [idx[c] for c in wanted]


def load_table(
    conn: sqlite3.Connection,
    gz_path: Path,
    table: str,
    insert_sql: str,
    row_fn,
) -> int:
    """Stream one sql.gz dump into SQLite. The dump file is kept."""
    count = 0
    batch: list = []
    with gzip.open(gz_path, "rt", encoding="utf-8", errors="replace") as fh:
        for row in iter_dump_rows(fh, table):
            batch.append(row_fn(row))
            if len(batch) >= SQL_BATCH:
                conn.executemany(insert_sql, batch)
                count += len(batch)
                batch = []
                if count % 1_000_000 < SQL_BATCH:
                    pr.counter(count, 0, f"{table} rows")
    if batch:
        conn.executemany(insert_sql, batch)
        count += len(batch)
    conn.commit()
    if count == 0:
        # never treat an unparseable dump as "consumed" — keep the file
        raise RuntimeError(
            f"parsed 0 rows from {gz_path.name}; dump format changed? "
            "file kept for inspection"
        )
    # NEVER delete dumps: re-downloading costs the user hours. Disk is
    # cheaper than bandwidth.
    return count


def _load_categorylinks(conn: sqlite3.Connection, gz_path: Path) -> int:
    columns = read_columns(gz_path, "categorylinks")
    i_from, i_type, i_target = _indices(
        columns, ["cl_from", "cl_type", "cl_target_id"], gz_path.name
    )
    return load_table(
        conn,
        gz_path,
        "categorylinks",
        "INSERT INTO catlink VALUES (?,?,?)",
        lambda r: (r[i_from], r[i_target], r[i_type]),
    )


def _load_linktarget(conn: sqlite3.Connection, gz_path: Path) -> int:
    columns = read_columns(gz_path, "linktarget")
    i_id, i_ns, i_title = _indices(
        columns, ["lt_id", "lt_namespace", "lt_title"], gz_path.name
    )
    count = 0
    batch: list[tuple[int, str]] = []
    with gzip.open(gz_path, "rt", encoding="utf-8", errors="replace") as fh:
        for row in iter_dump_rows(fh, "linktarget"):
            # only category targets are reachable from categorylinks
            if row[i_ns] != NS_CATEGORY:
                continue
            batch.append((row[i_id], row[i_title]))
            if len(batch) >= SQL_BATCH:
                conn.executemany("INSERT INTO lt VALUES (?,?)", batch)
                count += len(batch)
                batch = []
                pr.counter(count, 0, "category linktarget rows")
    if batch:
        conn.executemany("INSERT INTO lt VALUES (?,?)", batch)
        count += len(batch)
    conn.commit()
    if count == 0:
        raise RuntimeError(
            f"parsed 0 category rows from {gz_path.name}; dump format changed?"
        )
    return count


def _load_page(conn: sqlite3.Connection, gz_path: Path) -> int:
    columns = read_columns(gz_path, "page")
    i_id, i_ns, i_title, i_red = _indices(
        columns,
        ["page_id", "page_namespace", "page_title", "page_is_redirect"],
        gz_path.name,
    )
    return load_table(
        conn,
        gz_path,
        "page",
        "INSERT INTO ppage VALUES (?,?,?,?)",
        lambda r: (r[i_id], r[i_title], r[i_red], r[i_ns]),
    )


def _load_page_props(conn: sqlite3.Connection, gz_path: Path) -> int:
    columns = read_columns(gz_path, "page_props")
    i_page, i_prop = _indices(columns, ["pp_page", "pp_propname"], gz_path.name)
    return load_table(
        conn,
        gz_path,
        "page_props",
        "INSERT INTO props VALUES (?,?)",
        lambda r: (r[i_page], r[i_prop]),
    )


def _create_tables(conn: sqlite3.Connection) -> None:
    # catlink: cl_from = member/subcat page id, cl_target = category lt_id
    conn.execute(
        "CREATE TABLE IF NOT EXISTS catlink (cl_from INTEGER, cl_target INTEGER, cl_type TEXT)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS ppage (id INTEGER PRIMARY KEY, title TEXT,"
        " is_redirect INTEGER, ns INTEGER)"
    )
    conn.execute("CREATE TABLE IF NOT EXISTS props (pp_page INTEGER, prop TEXT)")
    # lt: category linktargets only (lt_namespace = 14)
    conn.execute("CREATE TABLE IF NOT EXISTS lt (id INTEGER PRIMARY KEY, title TEXT)")
    # catmap: category page id → its lt_id, joined on title
    conn.execute(
        "CREATE TABLE IF NOT EXISTS catmap (page_id INTEGER PRIMARY KEY, lt_id INTEGER)"
    )
    # one row per load step that finished; a row count cannot tell a
    # finished load from one killed halfway (journal_mode is OFF)
    conn.execute("CREATE TABLE IF NOT EXISTS loaded (step TEXT PRIMARY KEY)")


def _load_once(
    conn: sqlite3.Connection, step: str, tables: list[str], load: Callable[[], None]
) -> bool:
    """Run `load` unless `step` already finished; clear partial rows first.
    Returns True when the step ran now."""
    if conn.execute("SELECT 1 FROM loaded WHERE step = ?", (step,)).fetchone():
        pr.green(f"reusing {step} from catgraph db")
        return False
    for table in tables:
        conn.execute(f"DELETE FROM {table}")
    load()
    conn.execute("INSERT INTO loaded VALUES (?)", (step,))
    conn.commit()
    return True


def _load_graph(conn: sqlite3.Connection, dumps: Path) -> None:
    def load_base() -> None:
        pr.title("loading categorylinks dump")
        n = _load_categorylinks(conn, dumps / "enwiki-latest-categorylinks.sql.gz")
        pr.yes(f"{n} categorylinks rows")
        pr.title("loading page dump")
        n = _load_page(conn, dumps / "enwiki-latest-page.sql.gz")
        pr.yes(f"{n} page rows")
        pr.title("loading page_props dump")
        n = _load_page_props(conn, dumps / "enwiki-latest-page_props.sql.gz")
        pr.yes(f"{n} page_props rows")

    def load_lt() -> None:
        pr.title("loading linktarget dump")
        n = _load_linktarget(conn, dumps / "enwiki-latest-linktarget.sql.gz")
        pr.yes(f"{n} category linktarget rows")

    def load_catmap() -> None:
        pr.title("mapping category pages to linktargets")
        conn.execute(
            "INSERT INTO catmap SELECT p.id, l.id FROM ppage p"
            " JOIN lt l ON l.title = p.title WHERE p.ns = ?",
            (NS_CATEGORY,),
        )

    base_ran = _load_once(conn, "base", ["catlink", "ppage", "props"], load_base)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_catlink_target ON catlink (cl_target)")
    lt_ran = _load_once(conn, "linktarget", ["lt"], load_lt)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_lt_title ON lt (title)")
    # catmap joins ppage and lt, so a reload of either makes it stale
    if base_ran or lt_ran:
        conn.execute("DELETE FROM loaded WHERE step = 'catmap'")
    _load_once(conn, "catmap", ["catmap"], load_catmap)


def walk_categories(
    conn: sqlite3.Connection, root_title: str, max_depth: int
) -> set[int]:
    """Breadth-first walk of the category graph from `root_title`, down to
    `max_depth` levels, skipping hidden categories. Returns category lt_ids."""
    root_rows = conn.execute(
        "SELECT id FROM lt WHERE title = ?", (root_title,)
    ).fetchall()
    if not root_rows:
        raise RuntimeError(f"linktarget `{root_title}` (ns14) not found in dump")
    root_lt = root_rows[0][0]

    # hidden category page ids (flagged hiddencat in page_props)
    hidden = {
        r[0] for r in conn.execute("SELECT pp_page FROM props WHERE prop = 'hiddencat'")
    }
    pr.white(f"{len(hidden)} hidden categories")

    subtree: set[int] = {root_lt}
    frontier: list[int] = [root_lt]
    depth = 0
    while frontier and depth < max_depth:
        next_frontier: set[int] = set()
        for start in range(0, len(frontier), 500):
            chunk = frontier[start : start + 500]
            ph = ",".join("?" * len(chunk))
            child_rows = conn.execute(
                "SELECT DISTINCT m.page_id, m.lt_id FROM catlink c"
                " JOIN catmap m ON m.page_id = c.cl_from"
                f" WHERE c.cl_type = 'subcat' AND c.cl_target IN ({ph})",
                chunk,
            )
            for page_id, lt_id in child_rows:
                if page_id not in hidden and lt_id not in subtree:
                    next_frontier.add(lt_id)
        depth += 1
        frontier = sorted(next_frontier)
        subtree.update(frontier)
        pr.white(f"depth {depth}: {len(frontier)} new categories")
    return subtree


def member_titles(conn: sqlite3.Connection, categories: set[int]) -> set[str]:
    """Mainspace non-redirect articles directly in any of `categories`."""
    titles: set[str] = set()
    cat_list = sorted(categories)
    for chunk_start in range(0, len(cat_list), 500):
        chunk = cat_list[chunk_start : chunk_start + 500]
        ph = ",".join("?" * len(chunk))
        member_rows = conn.execute(
            "SELECT cl_from FROM catlink WHERE cl_type = 'page'"
            f" AND cl_target IN ({ph})",
            chunk,
        )
        member_ids = [r[0] for r in member_rows]
        for id_start in range(0, len(member_ids), 500):
            ids = member_ids[id_start : id_start + 500]
            iph = ",".join("?" * len(ids))
            rows = conn.execute(
                f"SELECT title FROM ppage WHERE id IN ({iph})"
                f" AND ns = ? AND is_redirect = 0",
                (*ids, NS_MAIN),
            )
            # the page dump stores titles with underscores; the seed list,
            # checkpoint and API all use spaces
            titles.update(r[0].replace("_", " ") for r in rows)
        pr.counter(len(titles), 0, "articles found")
    return titles


def live_seed_titles(conn: sqlite3.Connection, seed_path: Path) -> set[str]:
    """Seed titles that are live mainspace articles in the page dump.

    Checked against the dump rather than a local redirects file, so the
    list is the same on a fresh checkout; dead and redirect titles drop out.
    """
    seeds = [t.replace(" ", "_") for t in read_title_list(seed_path)]
    live: set[str] = set()
    for start in range(0, len(seeds), 500):
        chunk = seeds[start : start + 500]
        ph = ",".join("?" * len(chunk))
        rows = conn.execute(
            f"SELECT title FROM ppage WHERE title IN ({ph})"
            " AND ns = ? AND is_redirect = 0",
            (*chunk, NS_MAIN),
        )
        live.update(r[0].replace("_", " ") for r in rows)
    return live


def build_article_list(pth: RepoPaths) -> list[str]:
    dumps = _dumps_dir(pth)
    conn = sqlite3.connect(dumps / "catgraph.sqlite3")
    conn.execute("PRAGMA journal_mode=OFF")
    conn.execute("PRAGMA synchronous=OFF")
    _create_tables(conn)
    # the graph db is kept between runs: loading it takes hours and no
    # download is involved in redoing it
    _load_graph(conn, dumps)

    subtree = walk_categories(conn, ROOT_CATEGORY, MAX_DEPTH)
    pr.green(f"{len(subtree)} categories in subtree (hidden excluded)")
    titles = member_titles(conn, subtree)
    # merge the Phase 1 seed list so nothing already curated is lost
    titles |= live_seed_titles(conn, pth.buddhist_wiki_seed_articles_path)
    conn.close()

    sorted_titles = sorted(titles)
    with open(pth.buddhist_wiki_article_list_path, "w", encoding="utf-8") as f:
        for title in sorted_titles:
            f.write(f"{title}\n")
    return sorted_titles


def main() -> None:
    pr.tic()
    pr.title("building Buddhism subtree article list")
    pth = RepoPaths()
    titles = build_article_list(pth)
    pr.yes(f"{len(titles)} articles written to article_list.txt")
    pr.toc()


if __name__ == "__main__":
    main()

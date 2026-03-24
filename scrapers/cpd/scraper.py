"""
CPD (Critical Pāli Dictionary) Scraper

Scrapes the entire dictionary from cpd.uni-koeln.de using its /query API.
Stores everything in SQLite, downloads CSS/fonts/images/intro pages.
Supports resume — safe to interrupt and restart.
"""

import re
import sqlite3
import time
from pathlib import Path

import httpx
from tqdm import tqdm

BASE_URL = "https://cpd.uni-koeln.de"
DATA_DIR = Path("data")
DB_PATH = DATA_DIR / "cpd.db"
HEADWORD_BATCH = 500

BATCH_SIZE = 30   # requests per batch
BATCH_PAUSE = 60  # seconds to pause between batches


def _ts() -> str:
    return time.strftime('%H:%M:%S')


INTRO_PAGES = [
    "trenckner",
    "preface_vol1",
    "preface_vol2",
    "preface_vol3",
    "vol3_list_of_contributors",
    "contributors_vol2",
    "vol1_on_critics_and_new_texts",
    "vol3_notice_about_development",
    "vol3_concluding_remarks",
    "ludwig_alsdorf_obituary",
    "dines_andersen_obituary",
    "wilhelm_geiger_obituary",
    "klas_hagren_obituary",
    "elof_olesen_obituary",
    "else_margrethe_pauly_obituary",
    "helmer_smith_obituary",
    "vol1_epileg_abbrev_texts",
    "vol3_consolidated_list_of_abbreviations",
    "vol1_epileg_bibliography",
    "vol1_epileg_concordances",
    "vol1_epileg_general_index",
    "vol1_epileg_terms_and_signs",
    "how_to_use",
]

STATIC_ASSETS = [
    "css/pali.css",
    "css/webfonts/webfonts.css",
    "images/kammavaca1.jpg",
    "images/kammavaca2.jpg",
    "images/cceh-32x32.png",
    "images/clarin-400x400.png",
    "images/front_vol1_1200w_high.jpg",
    "images/front_vol2_1200w_high.jpg",
    "images/front_vol3_1200w_high.jpg",
    "images/translitt_98ret1_auto_high_.jpg",
    "images/translitt_98ret1_bitmap.pdf",
    "images/translitt_99ret1_auto_high_.jpg",
    "images/translitt_99ret1_bitmap.pdf",
]

FONT_FILES = [
    "GenBasBI",
    "GenBasB",
    "GenBasI",
    "GenBasR",
    "GenBkBasBI",
    "GenBkBasB",
    "GenBkBasI",
    "GenBkBasR",
]
FONT_EXTS = ["woff2", "woff", "ttf", "eot"]


def clean_headword(webkeyword: str) -> str:
    # webkeyword is the server's hyphenated breakdown form with HTML, e.g. "<sup>1</sup>a-kata"
    # We strip it down to a plain searchable headword, e.g. "akata"
    text = re.sub(r"<[^>]+>", "", webkeyword)
    text = re.sub(r"^\d+", "", text)  # leading digits come from <sup>N</sup> homonym markers
    text = text.replace("-", "")      # hyphens mark syllable boundaries, not part of the word
    return text.strip()


def init_db(db: sqlite3.Connection):
    db.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL,
            headword   TEXT NOT NULL,
            webkeyword TEXT NOT NULL,
            html       TEXT,
            failed     TEXT,
            UNIQUE(article_id, webkeyword)
        )
    """)
    db.commit()


def _download_file(client: httpx.Client, url: str, dest: Path) -> None:
    if dest.exists():
        print(f"  [skip] {dest.relative_to(DATA_DIR)}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    resp = client.get(url)
    if resp.status_code == 200:
        dest.write_bytes(resp.content)
        print(f"  [ok]   {dest.relative_to(DATA_DIR)} ({len(resp.content)} bytes)")
    else:
        print(f"  [FAIL] {dest.relative_to(DATA_DIR)} (HTTP {resp.status_code})")


def download_static_assets(client: httpx.Client):
    print("\n=== Downloading static assets ===")
    for asset in STATIC_ASSETS:
        _download_file(client, f"{BASE_URL}/{asset}", DATA_DIR / asset)

    print("\n=== Downloading fonts ===")
    font_dir = DATA_DIR / "css" / "webfonts"
    font_dir.mkdir(parents=True, exist_ok=True)
    for name in FONT_FILES:
        for ext in FONT_EXTS:
            fname = f"{name}.{ext}"
            dest = font_dir / fname
            if dest.exists():
                continue
            resp = client.get(f"{BASE_URL}/css/webfonts/{fname}")
            if resp.status_code == 200:
                dest.write_bytes(resp.content)
                print(f"  [ok]   {fname} ({len(resp.content)} bytes)")


def download_intro_pages(client: httpx.Client):
    print("\n=== Downloading intro pages ===")
    intro_dir = DATA_DIR / "intro"
    for page in INTRO_PAGES:
        _download_file(client, f"{BASE_URL}/intro/{page}", intro_dir / f"{page}.html")
        time.sleep(0.2)


def fetch_all_headwords(client: httpx.Client, db: sqlite3.Connection):
    print("\n=== Fetching headwords ===")
    existing = db.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
    if existing >= 29716:
        print(f"  Already have {existing} headword rows, skipping")
        return
    if existing > 0:
        # Partial headword fetch means the DB is incomplete — safer to restart than patch
        print(f"  Only have {existing}/29716 rows — re-fetching all headwords")
        db.execute("DELETE FROM entries")
        db.commit()

    offset = 0
    total = None
    pbar = None
    while True:
        for attempt in range(5):
            try:
                resp = client.get(
                    f"{BASE_URL}/query",
                    params={
                        "action": "search",
                        "mode": "entries",
                        "query": "*",
                        "limit": HEADWORD_BATCH,
                        "offset": offset,
                    },
                )
                if resp.status_code != 200 or not resp.text.strip():
                    raise ValueError(
                        f"HTTP {resp.status_code}, empty={not resp.text.strip()}"
                    )
                data = resp.json()
                break
            except Exception as e:
                if attempt < 4:
                    wait = 2**attempt
                    print(
                        f"\n  Retry {attempt + 1}/5 at offset {offset}: {e} (waiting {wait}s)"
                    )
                    time.sleep(wait)
                else:
                    raise
        if total is None:
            total = data["records"]
            pbar = tqdm(total=total, desc="Headwords", unit="hw")
            pbar.update(offset)
        entries = data["entries"]
        if not entries:
            break
        # INSERT OR IGNORE because spelling variants share the same article_id —
        # the server returns duplicate IDs for different webkeyword forms of the same entry
        db.executemany(
            "INSERT OR IGNORE INTO entries (article_id, webkeyword, headword) VALUES (?, ?, ?)",
            [
                (e["no"], e["webkeyword"], clean_headword(e["webkeyword"]))
                for e in entries
            ],
        )
        db.commit()
        pbar.update(len(entries))
        offset += HEADWORD_BATCH
        time.sleep(0.2)
    if pbar:
        pbar.close()
    count = db.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
    print(f"  Total headwords in DB: {count}")


def fetch_all_articles(client: httpx.Client, db: sqlite3.Connection):
    print("\n=== Fetching articles ===")
    # html IS NULL covers both never-fetched and previously failed articles — retry everything
    to_fetch = [
        r[0]
        for r in db.execute("""
            SELECT DISTINCT article_id FROM entries
            WHERE html IS NULL
            ORDER BY article_id
        """).fetchall()
    ]
    total_rows = db.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
    total_articles = db.execute("SELECT COUNT(DISTINCT article_id) FROM entries").fetchone()[0]
    w = 7
    print(f"  {'Total headword rows:':<22} {total_rows:>{w},}")
    print(f"  {'Distinct articles:':<22} {total_articles:>{w},}")
    print(f"  {'Already fetched:':<22} {total_articles - len(to_fetch):>{w},}")
    print(f"  {'Remaining:':<22} {len(to_fetch):>{w},}")
    print()

    if not to_fetch:
        print("  All articles already fetched!")
        return

    already_fetched = total_articles - len(to_fetch)
    errors = 0
    done = 0
    pbar = tqdm(total=total_articles, initial=already_fetched, unit="art", smoothing=0,
                bar_format="{desc}: {percentage:.0f}%|{bar}| [{elapsed}<{remaining}, {rate_fmt}]")

    for i, article_id in enumerate(to_fetch):
        # Pause after every batch of 30 before firing the next batch
        if i > 0 and i % BATCH_SIZE == 0:
            batch_start = to_fetch[i - BATCH_SIZE]
            batch_end = to_fetch[i - 1]
            tqdm.write(f"  [pause] {_ts()}  {batch_start} - {batch_end}, pausing {BATCH_PAUSE}s")
            time.sleep(BATCH_PAUSE)

        success = False
        last_error = ""
        for attempt in range(3):
            try:
                resp = client.get(
                    f"{BASE_URL}/query",
                    params={"action": "article", "article_id": article_id},
                )
                if resp.status_code == 200 and resp.text.strip():
                    # UPDATE covers all spelling variants sharing this article_id in one shot
                    db.execute(
                        "UPDATE entries SET html = ?, failed = NULL WHERE article_id = ?",
                        (resp.text, article_id),
                    )
                    done += 1
                    db.commit()
                    success = True
                    pbar.set_description(f"{done} ({already_fetched + done}) / {total_articles} [{(already_fetched + done) / total_articles:.1%}]")
                    pbar.update(1)
                    break
                elif resp.status_code == 403:
                    tqdm.write(f"  [rate]  {_ts()}  {article_id}  403, skipping, pausing 60s")
                    time.sleep(60)
                    break
                elif resp.status_code == 429:
                    tqdm.write(f"  [rate]  {_ts()}  {article_id}  429, pausing 5min")
                    time.sleep(300)
                else:
                    last_error = f"HTTP {resp.status_code}"
                    tqdm.write(f"  [block] {_ts()}  {article_id}  {last_error}, retry {attempt+1}/3")
            except Exception as e:
                last_error = str(e)
                # Connection refused = IP block; pause long enough for it to lift before retrying
                tqdm.write(f"  [err]   {_ts()}  {article_id}  {last_error}, retry {attempt+1}/3, pausing 5min")
                time.sleep(300)

        if not success:
            errors += 1
            tqdm.write(f"  [fail]  {_ts()}  {article_id}  gave up — {last_error}")
            db.execute(
                "UPDATE entries SET failed = ? WHERE article_id = ?", (last_error, article_id)
            )
            db.commit()
            pbar.update(1)

    pbar.close()
    db.commit()
    fetched = db.execute(
        "SELECT COUNT(DISTINCT article_id) FROM entries WHERE html IS NOT NULL"
    ).fetchone()[0]
    failed = db.execute(
        "SELECT COUNT(DISTINCT article_id) FROM entries WHERE failed IS NOT NULL"
    ).fetchone()[0]
    print(f"  Articles in DB: {fetched}/{total_articles}")
    if errors:
        print(f"  Errors this run: {errors}")
    if failed:
        print(f"  Total failures: {failed}")


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    init_db(db)

    client = httpx.Client(
        timeout=30,
        follow_redirects=True,
        headers={"User-Agent": "CPD-Scraper/1.0 (academic research)"},
    )

    print("=== Checking server connectivity ===")
    for attempt in range(10):
        try:
            resp = client.get(BASE_URL, timeout=10)
            print(f"  Server is up (HTTP {resp.status_code})")
            break
        except Exception as e:
            print(f"  Attempt {attempt + 1}/10: {e}")
            print("  Retrying in 60s...")
            time.sleep(60)
    else:
        print("  Server unreachable after 10 attempts. Your IP may be blocked.")
        print("  Options: restart router for new IP, use VPN, or wait longer.")
        client.close()
        db.close()
        return

    try:
        download_static_assets(client)
        download_intro_pages(client)
        fetch_all_headwords(client, db)
        fetch_all_articles(client, db)
    except KeyboardInterrupt:
        print("\n\n=== Interrupted — saving progress ===")
        for attempt in range(10):
            try:
                db.commit()
                break
            except sqlite3.OperationalError as e:
                print(f"  Database locked, retrying in 5s... ({e})")
                time.sleep(5)
    finally:
        client.close()
        db.close()

    db2 = sqlite3.connect(DB_PATH)
    total = db2.execute("SELECT COUNT(DISTINCT article_id) FROM entries").fetchone()[0]
    fetched = db2.execute(
        "SELECT COUNT(DISTINCT article_id) FROM entries WHERE html IS NOT NULL"
    ).fetchone()[0]
    db2.close()
    print(f"Progress: {fetched}/{total} articles saved")
    print("Run again to resume.")


if __name__ == "__main__":
    main()

# CPD Scraper

Scrapes the [Critical Pāli Dictionary](https://cpd.uni-koeln.de) and produces a clean SQLite database for import into other projects.

## What it does

- Fetches all ~29,716 dictionary entries via the site's `/query` API
- Downloads CSS, fonts, images, and supplementary intro pages
- Stores everything in `data/cpd.db` (source — never modified after scraping)
- Cleans and normalises headwords and webkeywords into `data/cpd_clean.db`

Safe to interrupt and restart — already-fetched articles are skipped.

## Rate limiting

Requests are sent in batches of 30 with a 60-second pause between batches. On a 403 the scraper pauses 60s; on a 429 it pauses 5 minutes; on a connection error it pauses 5 minutes before retrying.

## Commands

```
just run       # run the scraper
just db        # browse the source database in visidata
just clean     # apply cleanup rules → data/cpd_clean.db
just diagnose  # validate clean DB, write diagnose_report.txt
just extras    # inject supplementary intro pages into cpd_clean.db
```

## Cleanup pipeline

The source database is kept raw. Cleaning is a separate step:

- **`cleanup_rules.py`** — all transformation rules in one place: word-level OCR fixes, character substitutions, delete lists, and allowed character sets. Fully commented — the authoritative record of every decision made.
- **`clean.py`** — reads `cpd.db`, applies rules in order (word fixes → char subs → slash split → delete → lowercase), writes `cpd_clean.db`.
- **`diagnose.py`** — scans `cpd_clean.db` and reports any remaining problem characters per field.
- **`extras.py`** — reads intro pages from `data/intro/`, injects them into `cpd_clean.db` as combined entries (prefaces, obituaries, bibliography).
- **`cleanup.md`** — human-readable spec that `cleanup_rules.py` is derived from.

## Output

```
data/
├── cpd.db          source database — raw scrape, never modified
├── cpd_clean.db    cleaned database — headwords and webkeywords normalised
├── css/            stylesheets and fonts
├── images/         dictionary images
└── intro/          supplementary pages (prefaces, obituaries, etc.)
```

## Dependencies

[uv](https://docs.astral.sh/uv/) manages Python and packages:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For the database browser:

```
uv tool install visidata
```

For the task runner:

```
brew install just        # macOS
apt install just         # Ubuntu/Debian
```

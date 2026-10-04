#!/usr/bin/env bash
# Overnight pipeline for the Buddhist Wiki, Phase 2.
# Fully resumable: every step is idempotent, downloads use curl -C -,
# the API fetch keeps a checkpoint. Re-running this script after an
# interruption picks up where it stopped.
#
# Article text comes from the Wikipedia API, not the 25 GB pages-articles
# dump: at depth <= 5 the list is ~24k articles, ~100 MB over the API.
# fetch_from_dump.py stays as the fallback for a much larger list.
#
# Usage: ./dictionaries/buddhist_wiki/run_overnight.sh
set -uo pipefail
cd "$(dirname "$0")/../.."

DUMP_DIR="dictionaries/buddhist_wiki/source/dumps"
# pinned to one dump run: "latest" moves on the 1st/20th of each month, and
# curl -C - would then splice bytes of a new file onto a partial old one
DUMP_URL="https://dumps.wikimedia.org/enwiki/20261001/enwiki-20261001"
LOG="$DUMP_DIR/overnight.log"
mkdir -p "$DUMP_DIR"
exec &> >(tee -a "$LOG")

stamp() { date +"%Y-%m-%d %H:%M:%S"; }
step() { echo; echo "[$(stamp)] === $1 ==="; }

dl() {
    local url="$1" out="$2"
    # MAX_RATE: curl bandwidth cap, e.g. 300k = 300 KB/s (default), 2M = unlimited-ish
    if [ -f "$out.done" ]; then echo "[$(stamp)] $out already downloaded"; return 0; fi
    echo "[$(stamp)] downloading $url (rate limit: ${MAX_RATE:-300k})"
    curl -fL --retry 20 --retry-all-errors --retry-delay 15 -C - \
        --limit-rate "${MAX_RATE:-300k}" -o "$out" "$url" \
        && touch "$out.done"
}

step "1/6 SQL dumps: categorylinks, linktarget, page, page_props, redirect"
dl "$DUMP_URL-categorylinks.sql.gz" "$DUMP_DIR/enwiki-latest-categorylinks.sql.gz"
dl "$DUMP_URL-linktarget.sql.gz" "$DUMP_DIR/enwiki-latest-linktarget.sql.gz"
dl "$DUMP_URL-page.sql.gz" "$DUMP_DIR/enwiki-latest-page.sql.gz"
dl "$DUMP_URL-page_props.sql.gz" "$DUMP_DIR/enwiki-latest-page_props.sql.gz"
dl "$DUMP_URL-redirect.sql.gz" "$DUMP_DIR/enwiki-latest-redirect.sql.gz"
for f in categorylinks linktarget page page_props redirect; do
    [ -f "$DUMP_DIR/enwiki-latest-$f.sql.gz.done" ] \
        || { echo "[$(stamp)] DOWNLOAD FAILED: $f"; exit 1; }
done

step "2/6 build article list (parses the SQL dumps)"
uv run python dictionaries/buddhist_wiki/make_article_list.py || { echo "[$(stamp)] ARTICLE LIST FAILED"; exit 1; }

step "3/6 fetch article wikitext from the Wikipedia API"
uv run python dictionaries/buddhist_wiki/fetch_wikitext.py \
    --list dictionaries/buddhist_wiki/source/article_list.txt \
    || { echo "[$(stamp)] API FETCH FAILED"; exit 1; }

# never alongside the fetch: both rewrite redirects.json
step "4/6 add dump redirects to redirects.json"
uv run python dictionaries/buddhist_wiki/make_redirects.py || { echo "[$(stamp)] REDIRECTS FAILED"; exit 1; }

step "5/6 build GoldenDict + MDict"
uv run python dictionaries/buddhist_wiki/buddhist_wiki.py || { echo "[$(stamp)] BUILD FAILED"; exit 1; }

step "6/6 done — dumps kept on disk (deleting them would force re-downloads)"
echo "[$(stamp)] OVERNIGHT RUN COMPLETE"

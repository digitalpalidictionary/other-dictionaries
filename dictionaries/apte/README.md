# Apte Practical Sanskrit-English Dictionary

Vaman Shivram Apte's Practical Sanskrit-English Dictionary (1890), built directly from the Cologne Sanskrit Lexicon raw source data.

## Source

- `source/ap90web1.zip` - Auto-downloaded from Cologne server on each run
- `source/web/sqlite/ap90.sqlite` - Sub-entries
- `source/web/sqlite/ap90keys.sqlite` - Grouped headwords
- `source/web/sqlite/ap90ab.sqlite` - Abbreviations
- `source/web/sqlite/ap90authtooltips.sqlite` - Literature tooltips

## Run

```bash
uv run python -m dictionaries.apte.apte_from_cologne
```

## Output

- `build/goldendict/apte.zip`
- `build/mdict/apte.mdx.zip`
- `source/apte.json` - Intermediate JSON

## Architecture

- `apte_helpers.py` - Data loading (`load_apte_data`), entry building (`build_apte_entries`), download logic
- `apte_renderer.py` - XML-to-HTML rendering (pre-processing + tag conversion)
- `apte.css` - CSS derived from Cologne's main.css + font.css
- `apte_from_cologne.py` - Main export orchestrator

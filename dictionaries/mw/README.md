# MW Monier-Williams Sanskrit-English Dictionary (Cologne)

Monier-Williams' Sanskrit-English dictionary (1899), built directly from the Cologne Sanskrit Lexicon raw source data.

## Source

- `source/mwweb1.zip` - Auto-downloaded from Cologne server on each run
- `source/web/sqlite/mw.sqlite` - 286,554 sub-entries
- `source/web/sqlite/mwkeys.sqlite` - 194,083 grouped headwords
- `source/web/sqlite/mwab.sqlite` - 424 abbreviations
- `source/web/sqlite/mwauthtooltips.sqlite` - 871 literature tooltips

## Run

```bash
uv run python -m dictionaries.mw.mw_from_cologne
```

## Output

- `build/goldendict/mw.zip`
- `build/mdict/mw.mdx.zip`
- `source/mw.json` - Intermediate JSON for mobile export

## Architecture

- `mw_helpers.py` - Data loading (`load_mw_data`), entry building (`build_mw_entries`), download logic
- `mw_renderer.py` - XML-to-HTML rendering (pre-processing + tag conversion)
- `mw.css` - CSS derived from Cologne's main.css + font.css
- `mw_from_cologne.py` - Main export orchestrator

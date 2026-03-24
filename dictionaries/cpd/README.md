# Critical Pāli Dictionary (CPD)

Exports the [Critical Pāli Dictionary](https://cpd.uni-koeln.de) into GoldenDict and MDict formats.

## Source

The source is `cpd_clean.db` — a cleaned SQLite database scraped from the CPD website, produced by the [cpd-scraper](https://github.com/digitalpalidictionary/cpd-scraper) project.

- 29,734 dictionary entries
- 3 supplementary entries (prefaces, obituaries, bibliography)
- Headwords normalised and cleaned; HTML preserved from the original site

## Output

- `build/goldendict/cpd-goldendict.zip`
- `build/mdict/cpd-mdict.zip`

## Run

From the project root:

```
just cpd
```

Or directly:

```
cd resources/other-dictionaries/
uv run python dictionaries/cpd/cpd.py
```

## Notes

- CPD uses `ṁ` (dot above) for the niggahita. Synonyms with `ṃ` (dot below) and `ŋ` are generated automatically so all three variants are searchable.
- The source archive `cpd.tar.zst` is decompressed automatically by `scripts/decompress_sources.py` before export.

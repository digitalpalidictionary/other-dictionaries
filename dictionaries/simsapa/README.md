# Simsapa Combined Dictionary

Combined Pali-English dictionary from Simsapa Dhamma Reader:
- Nyanatiloka's Buddhist Dictionary
- Dictionary of Pali Proper Names (DPPN)
- New Concise Pali-English Dictionary (NCPED)
- Pali Text Society Pali-English Dictionary (PTS)

## Source

- `source/simsapa.json` - JSON dictionary data (extracted from Simsapa dictionary database)

## Run

```bash
uv run python -m dictionaries.simsapa.simsapa_combined
```

## Output

- `build/goldendict/simsapa.zip`
- `build/mdict/simsapa.mdx.zip`

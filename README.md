# Other Dictionaries

Auxiliary dictionary exporters for Pāḷi, Sanskrit, and Sinhala languages, producing GoldenDict and MDict formats.

## Dictionaries

| Abbreviation | Full name |
|---|---|
| apte | Apte Practical Sanskrit-English Dictionary, 1890 |
| bhs | Edgerton's Buddhist Hybrid Sanskrit Dictionary, 1953 |
| bold_definitions | CST Bold Definitions |
| cone | Dictionary of Pāli by Margaret Cone |
| cpd | Critical Pāli Dictionary |
| cped | Concise Pali English Dictionary (Ancient Buddhist Texts) |
| dppn | Dictionary of Pāli Proper Names |
| dpr | DPR Analysis |
| mw | Monier-Williams Sanskrit-English Dictionary, 1899 |
| nyanatiloka | Buddhist Dictionary: Manual of Buddhist Terms and Doctrines |
| peu | Pali English Ultimate |
| si-en-si | Sinhala-English English-Sinhala Dictionary |
| simsapa | Simsapa Combined Pali-English Dictionary |
| whitney | Whitney Sanskrit Roots |

## Quick Start

```bash
# Sync vendor tools from DPD repo
uv run python scripts/sync.py --dpd-path /path/to/dpd-db

# Build all dictionaries
uv run python scripts/export_all.py
```

## Build Outputs

- `build/goldendict/` - GoldenDict .zip files
- `build/mdict/` - MDict .zip files

## Development

```bash
# Run tests
uv run pytest tests/ -v

# Lint and format
uv run ruff check .
uv run ruff format .
```

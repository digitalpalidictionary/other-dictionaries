# Other Dictionaries

Auxiliary dictionary exporters for Pāḷi, Sanskrit, and Sinhala languages, producing GoldenDict and MDict formats.

## Dictionaries

| Code | Name | Description |
|------|------|-------------|
| abt | Ancient Buddhist Texts Glossary | CPED glossary from Ancient Buddhist Texts |
| bhs | Buddhist Hybrid Sanskrit | Edgerton's BHS dictionary |
| bold_def | CST Bold Definitions | Bold definitions from CST texts |
| cone | Margaret Cone | Dictionary of Pāḷi (partial) |
| cpd | Critical Pāḷi Dictionary | CPD from Copenhagen |
| dhammika | Dhammika | Data only (no exporter yet) |
| dppn | DPPN | Dictionary of Pāḷi Proper Names |
| dpr | DPR Analysis | Digital Pali Reader analysis data |
| mw | Monier-Williams | Sanskrit-English dictionary |
| peu | Pali English Ultimate | Combined Pāḷi-English dictionary |
| simsapa | Simsapa Combined | Combined dictionary from Simsapa |
| sin_eng_sin | Sinhala-English-Sinhala | Trilingual dictionary |
| vri | VRI | Vipassana Research Institute (data only) |
| whitney | Whitney Roots | Sanskrit roots dictionary |
| wordnet | WordNet | Pāḷi WordNet (incomplete) |

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

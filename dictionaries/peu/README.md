# Pali English Ultimate (PEU)

Pali Myanmar Abhidhan - the world's largest Pali dictionary (23 volumes).

## Source

- `source/peu_dump.js` - JSON data dump from https://pm12e.pali.tools/dump

To update source data:
```bash
# Download latest dump
curl -o dictionaries/peu/source/peu_dump.js https://pm12e.pali.tools/dump
```

## Run

```bash
uv run python -m dictionaries.peu.peu
```

## Output

- `build/goldendict/peu.zip`
- `build/mdict/peu.mdx.zip`

# Open English WordNet (English–English dictionary)

An English lexical dictionary of common words, integrated into the DPD mobile app
as an optional external dictionary (`dict_id = "wordnet"`).

## Source

- **Open English WordNet 2025** — https://en-word.net/
- Loaded via the `wn` Python library as `oewn:2025`.
- **License:** CC BY 4.0 (attribution required). Attribution is provided by the
  dictionary name **"Open English WordNet"** shown in the app's dictionary list and on
  each result card. Note: the app does not currently render the `author` field, so the
  attribution must live in the `name`.

## Scope

- Common-word senses only. **Proper nouns are excluded** (any headword whose first
  character is uppercase is skipped), so English place/person/brand names do not
  appear.
- Each headword's senses are grouped by part of speech, with gloss, synonyms, and
  usage examples.

## Build

```bash
uv run --with wn resources/other-dictionaries/dictionaries/wordnet/wordnet_to_json.py
```

## Output

- `source/wordnet_dict.json` — `{headword: definition_html}`, consumed by the mobile
  exporter's `include_wordnet` block (mirrors the Cone dictionary pattern).

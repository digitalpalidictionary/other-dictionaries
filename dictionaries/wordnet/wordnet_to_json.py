#!/usr/bin/env python3
"""Convert Open English WordNet (oewn:2025) into wordnet_dict.json.

Produces {headword: definition_html} in the shape the mobile exporter's
include_wordnet block expects (mirrors cone_dict.json).

Run standalone with the wn library available:

    uv run --with wn resources/other-dictionaries/dictionaries/wordnet/wordnet_to_json.py

Proper nouns are excluded: any headword whose first character is uppercase is
skipped. Senses are grouped by part of speech, each showing gloss, synonyms, and
usage examples.
"""

import html
import json
from pathlib import Path

import wn

OEWN = "oewn:2025"

SOURCE_DIR = Path(__file__).parent / "source"
# LMF source kept at the dictionary-folder root, not in source/, so
# compress_sources.py (which archives everything under source/) never bundles
# the 11 MB gz into wordnet.tar.zst — the build only needs the generated JSON.
LOCAL_LMF = Path(__file__).parent / "english-wordnet-2025.xml.gz"
OUTPUT = SOURCE_DIR / "wordnet_dict.json"

POS_ORDER = ["n", "v", "a", "r"]
POS_LABEL = {"n": "noun", "v": "verb", "a": "adjective", "r": "adverb"}
# Adjective satellites render as plain adjectives.
POS_CANON = {"n": "n", "v": "v", "a": "a", "s": "a", "r": "r"}


def _pos_of(word: "wn.Word") -> str:
    pos = word.pos
    if callable(pos):
        pos = pos()
    return POS_CANON.get(pos, pos)


def _load_wordnet() -> "wn.Wordnet":
    try:
        return wn.Wordnet(OEWN)
    except Exception:
        pass
    # Prefer a locally-downloaded LMF file (robust against flaky downloads);
    # fall back to wn's own downloader only if it is absent.
    if LOCAL_LMF.exists():
        wn.add(str(LOCAL_LMF))
    else:
        wn.download(OEWN)
    return wn.Wordnet(OEWN)


def _collect() -> dict[str, dict[str, list[dict]]]:
    """headword_lower -> pos -> list of {gloss, synonyms, examples}."""
    en = _load_wordnet()
    entries: dict[str, dict[str, list[dict]]] = {}

    for word in en.words():
        lemma = word.lemma()
        if not lemma or lemma[0].isupper():
            continue
        pos = _pos_of(word)
        key = lemma.lower()

        senses_out: list[dict] = []
        for sense in word.senses():
            synset = sense.synset()
            gloss = synset.definition() or ""
            examples = list(synset.examples() or [])
            synonyms = [
                syn
                for syn in synset.lemmas()
                if syn.lower() != key and not syn[0].isupper()
            ]
            if not gloss and not examples:
                continue
            senses_out.append(
                {"gloss": gloss, "synonyms": synonyms, "examples": examples}
            )

        if not senses_out:
            continue

        entries.setdefault(key, {}).setdefault(pos, []).extend(senses_out)

    return entries


def _render_html(pos_map: dict[str, list[dict]]) -> str:
    ordered_pos = [p for p in POS_ORDER if p in pos_map]
    ordered_pos += [p for p in pos_map if p not in POS_ORDER]

    parts: list[str] = ['<div class="wordnet">']
    for pos in ordered_pos:
        label = POS_LABEL.get(pos, pos)
        parts.append(f"<b>{html.escape(label)}</b>")
        parts.append("<ol>")
        for sense in pos_map[pos]:
            line = html.escape(sense["gloss"])
            if sense["synonyms"]:
                syns = ", ".join(html.escape(s) for s in sense["synonyms"])
                line += f' <i>(syn: {syns})</i>'
            for ex in sense["examples"]:
                line += f'<br><i>"{html.escape(ex)}"</i>'
            parts.append(f"<li>{line}</li>")
        parts.append("</ol>")
    parts.append("</div>")
    return "".join(parts)


def main() -> None:
    print(f"loading {OEWN} ...")
    entries = _collect()
    print(f"collected {len(entries)} headwords (proper nouns excluded)")

    out = {word: _render_html(pos_map) for word, pos_map in sorted(entries.items())}

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)

    size_mb = OUTPUT.stat().st_size / 1_000_000
    print(f"wrote {OUTPUT} ({len(out)} entries, {size_mb:.1f} MB)")


if __name__ == "__main__":
    main()

# PTS Pāḷi-English Dictionary

*The Pali Text Society's Pali-English Dictionary* by T. W. Rhys Davids and
William Stede, Pali Text Society, 1921–25.

## Licence

The licence is taken from the BuddhaDust page, which states: "Corrected
reprint Copyright The Pāḷi Text Society. Commercial Rights Reserved", with a
CC BY-NC badge and a link to its Terms of Use. BuddhaDust's text follows the
2015 "Reprint with corrections" by K. R. Norman, William Pruitt and Peter
Jackson. This dictionary is therefore shipped as © Pāḷi Text Society,
CC BY-NC (non-commercial, with attribution).

## Source

- `source/ped.htm` — the BuddhaDust edition, one page holding the whole
  dictionary, downloaded once on 2026-10-02 from
  <https://obo.genaud.net/backmatter/glossology/ped/pts_ped/ped.htm>.
  8,976,003 bytes. The server reports it as last changed on 9 December 2025.
- `source/pts.json` — built from `ped.htm` by `pts_from_buddhadust.py`.
  16,421 rows, 15,739 distinct words. Each row is an object with the keys
  `word` and `definition_html`.
- Both files are packed in `pts.tar.zst`. Re-pack it whenever the converter
  changes, or `scripts/decompress_sources.py` restores the old `pts.json`.

### Why this copy

Five copies were compared in October 2026:

| Copy | Entries | Verdict |
|---|---|---|
| Tipitaka Pali Reader database | 13,497 | About 3,000 headwords missing, `ṅ` flattened to `n`, no bold or italic. |
| Simsapa (2019) | 16,106 | A 2019 copy of SuttaCentral's; superscripts lost. |
| SuttaCentral `pli2en_pts.json` | 16,100 | Clean, but entries are restructured (etymology moved, homonyms merged). |
| Digital Pali Reader `ped.xml` | 16,282 | Closest to the 1925 print, but uses `ŋ`, ` -- ` and has stray `;`. |
| **BuddhaDust** | 16,415 anchors | **Chosen.** Pāḷi in italics, references in bold, homonym numbers kept, short reference names. |

## Conversion

`pts_from_buddhadust.py` does all the cleaning, so GoldenDict, MDict and the
DPD app get the same text.

1. Keep the region from the first headword to the Afterword.
2. Split the page into 16,407 entries, one per headword anchor that starts a
   paragraph (`Yena`, typed as bold italic, is turned into one). Compound
   paragraphs (`<p class="in1">`, 1,482) stay with their headword. The other
   9 anchors are variant headwords inside an entry.
3. Remove BuddhaDust's page furniture: images (including the audio-link
   icons), printed-page markers (`{58}` and two older `[Page N]` forms),
   letter-heading images, section dividers, the `[SUTTA SEARCH] [GLOSSOLOGY]`
   links, and the side boxes that define English words. Unwrap every link.
4. Remove text that is not from PTS. BuddhaDust adds its own notes
   (`[BD]`, 148) and text merged from Childers (`[DPL]`, 62), CPD (3) and
   DOP (3). All 216 removals were printed and read.
5. Drop 61 headwords: 52 whose body has no words left once the merged text
   is gone, and 9 anchors (8 headwords) that BuddhaDust added and that have
   no entry in the print edition (checked against the Digital Pali Reader
   copy), such as `Sūpatiṭṭha` from the New Concise PED.
6. Fix two errors in the BuddhaDust text:
   - 106 `-fullness` misspellings (`mindfullness`, `watchfullness`, …)
     become `-fulness`. The word `fullness` on its own is not touched.
   - The lost commentary abbreviation in `as 121` is restored to `DhsA 121`
     (Atthasālinī), 1,001 times. Each one was checked against the Digital
     Pali Reader copy: 994 match `DhsA` in the same entry, 7 elsewhere.
     `ENGLISH_AS` lists 26 places left alone: 25 uses of the English word
     "as", and `vyāyāma` (see below).
7. Words: drop the `:: ` prefix and the homonym number, fold `ṁ` to `ṃ`,
   lower-case. Prefix and suffix marks (`pa°`, `an-`, `-da`) are dropped.
   Spaces inside a word (`upa kappati`) are removed. Bracketed letters are
   indexed both ways (`jap(p)aka` → `jappaka`, `japaka`), and hyphenated
   compounds also without the hyphen (`paṭiccasamuppāda`). A variant
   headword inside another entry (`Amha and Amhan`) gets its own row.
   Duplicate rows are skipped.
8. Bodies: a homonym starts with `<sup>N</sup>`, and `ṁ` is folded to `ṃ`.

### Known problems left as they are

- Some Greek is garbled (e.g. `δἓμα`). There is no reliable source to
  correct it against.
- BuddhaDust edited a few places without a tag. For example, `Brahma` reads
  "see Mayrhofer 1994" where the print cites Osthoff. These cannot be found
  by rule.
- A few words in the bodies keep a stray space inside them, as the
  headwords did (`bha vati`). Only the headwords are fixed.
- `vyāyāma` reads "= vāyāma as 146". It is probably `DhsA 146`, but the
  Digital Pali Reader copy has no entry to confirm it, so it is left alone.

## Run

```bash
uv run python -m dictionaries.pts.pts_from_buddhadust
uv run python -m dictionaries.pts.pts
```

## Output

- `build/goldendict/pts.zip`
- `build/mdict/pts.zip`

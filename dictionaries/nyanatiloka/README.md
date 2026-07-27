# Nyanatiloka's Buddhist Dictionary

*Buddhist Dictionary: Manual of Buddhist Terms and Doctrines* by Nyanatiloka
Mahathera, 4th revised edition, edited by Nyanaponika Mahathera, Buddhist
Publication Society (Kandy), 1980, ISBN 955-24-0019-8.

## Source

- `source/nyanatiloka.json` — 1,406 entries, scraped 2026-07-27 from
  <https://www.dhammatalks.net/Buddhist.Dictionary/> (per-letter pages
  `dic3_a.htm` … `dic3_y.htm`, per the site's own index at
  `index_dict.n2.htm`). That site's own footer records the page content as
  last saved 05 November 2005. Nyanatiloka died in 1957 and no further
  edition has appeared since the 1980 4th revision, so this is treated as a
  one-off acquisition, not a live/re-run source — not a verified claim that
  the page itself has been byte-for-byte unchanged since 2005.
- The HTML across the 22 pages is hand-edited and inconsistent (at least
  three different tag-nesting shapes for the same logical entry). See
  `kamma/threads/20260727_nyanatiloka_dictionary/spec.md` in the main
  `dpd-db` repo for the full extraction-rule writeup.
- Licensing: the source page carries only a bare `© 1980 by Buddhist
  Publication Society` notice — no explicit reuse terms were found on the
  page, but that is an absence of a stated restriction, not a confirmed
  redistribution license. Shipped here with full author/editor/publisher
  attribution, the same posture DPD already takes for DPPN/CPD/MW/Apte
  (none of which carry a verified open license either); rights status
  should be treated as unresolved rather than cleared.

## Run

```bash
uv run python -m dictionaries.nyanatiloka.nyanatiloka
```

## Output

- `build/goldendict/nyanatiloka.zip`
- `build/mdict/nyanatiloka.zip`

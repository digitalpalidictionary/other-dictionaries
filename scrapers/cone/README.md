# Cone Scraper

Scrapes [A Dictionary of Pāli by Margaret Cone](https://gandhari.org/dictionary?section=dop) from the gandhari.org website and produces JSON files for the cone dictionary exporter.

## What it does

- Scrapes all headwords by iterating through the Pāli alphabet via the site's search box
- Fetches the HTML definition for each headword using Selenium
- Outputs `cone_dict.json` (all entries) and `front_matter.json` (abbreviations and front matter)

Uses Selenium with Chrome — requires Chrome and ChromeDriver to be installed.

## Commands

```
just cone-scrape-headwords   # scrape headwords → headwords.tsv
just cone-scrape-entries     # scrape entries   → cone_dict.json
just cone-front-matter       # generate front matter → front_matter.json
```

## Output

```
scrapers/cone/
├── headwords.tsv       scraped headword list (intermediate)
├── cone_dict.json      main dictionary data
└── front_matter.json   abbreviations and front matter
```

## After scraping

Copy outputs to the cone source directory and re-compress:

```
cp cone_dict.json ../../dictionaries/cone/source/cone_dict.json
cp front_matter.json ../../dictionaries/cone/source/cone_front_matter.json
```

Then re-run `just cpd` (or the full export) to rebuild the dictionary.

## Notes

- `scrape_entries.py` is resumable — already-fetched entries are skipped on restart.
- Safe to interrupt; progress is saved every 100 entries.

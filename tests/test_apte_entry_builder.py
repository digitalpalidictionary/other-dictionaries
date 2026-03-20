"""Test apte entry builder — headword assembly.

Tests verify:
- Sub-entries wrapped in <p> tags
- Full HTML document wrapper present with apte.css link
- CSS filename is apte.css
- Synonym generation includes IAST + SLP1 variants
- build_apte_entries returns list of DictEntry objects
- Headwords sorted in Sanskrit alphabetical order
"""

import pytest

from dictionaries.apte.apte_helpers import (
    ApteData,
    ApteEntry,
    build_apte_entries,
    generate_synonyms,
)


class TestSynonymGeneration:
    def test_basic_synonym(self):
        syns = generate_synonyms("agni")
        assert "agni" in syns

    def test_iast_synonym(self):
        syns = generate_synonyms("saMskfta")
        assert "saṃskṛta" in syns

    def test_slp1_included(self):
        syns = generate_synonyms("saMskfta")
        assert "saMskfta" in syns

    def test_niggahita_variants(self):
        syns = generate_synonyms("saMskfta")
        iast_forms = [s for s in syns if "ṃ" in s or "ṁ" in s]
        assert len(iast_forms) >= 1


@pytest.fixture
def sample_data() -> ApteData:
    data = ApteData()
    data.entries = {
        "a": [
            ApteEntry(
                key="a",
                lnum=1.0,
                data="<H1><body>first</body><tail><pc>1,1</pc></tail></H1>",
            ),
            ApteEntry(
                key="a",
                lnum=1.1,
                data="<H1><body>sub</body><tail><pc>1,1</pc></tail></H1>",
            ),
        ],
    }
    data.abbreviations = {}
    data.author_tooltips = {}
    return data


class TestEntryWrapping:
    def test_sub_entries_wrapped_in_p_tags(self, sample_data: ApteData):
        entries = build_apte_entries(sample_data)
        assert "<p>" in entries[0].definition_html

    def test_full_html_wrapper_present(self, sample_data: ApteData):
        entries = build_apte_entries(sample_data)
        html = entries[0].definition_html
        assert "<!DOCTYPE html>" in html
        assert "<html>" in html
        assert '<meta charset="utf-8">' in html

    def test_css_link_is_apte_css(self, sample_data: ApteData):
        entries = build_apte_entries(sample_data)
        html = entries[0].definition_html
        assert 'href="apte.css"' in html

    def test_entry_word_is_iast(self, sample_data: ApteData):
        entries = build_apte_entries(sample_data)
        assert entries[0].word == "a"

    def test_entry_has_synonyms(self, sample_data: ApteData):
        entries = build_apte_entries(sample_data)
        assert len(entries[0].synonyms) >= 1

    def test_all_sub_entries_rendered(self, sample_data: ApteData):
        entries = build_apte_entries(sample_data)
        html = entries[0].definition_html
        assert "first" in html
        assert "sub" in html


class TestSanskritSorting:
    def test_headwords_sorted_in_sanskrit_order(self):
        """Entries sorted by Sanskrit alphabet, not ASCII."""
        data = ApteData()
        data.entries = {
            "ga": [ApteEntry(key="ga", lnum=3.0, data="<H1><body>ga</body></H1>")],
            "a": [ApteEntry(key="a", lnum=1.0, data="<H1><body>a</body></H1>")],
            "ka": [ApteEntry(key="ka", lnum=2.0, data="<H1><body>ka</body></H1>")],
        }
        data.abbreviations = {}
        data.author_tooltips = {}
        entries = build_apte_entries(data)
        words = [e.word for e in entries]
        assert words.index("a") < words.index("ka")
        assert words.index("ka") < words.index("ga")

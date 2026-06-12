"""Test mw entry builder — headword assembly.

Tests verify:
- mwkeys data format parsing (H1,startL,endL;H1A,startL2,endL2;...)
- Sub-entry grouping by lnum range
- Entry HTML assembly
- Page-column reference rendering
- Synonym generation (IAST + niggahita variants + SLP1)
"""

from pathlib import Path

import pytest

from dictionaries.mw.mw_helpers import (
    MwData,
    MwEntry,
    MwKeyEntry,
    build_mw_entries,
    generate_synonyms,
    parse_key_ranges,
)


class TestKeyRangeParsing:
    """Task 5.1: Parse mwkeys data format."""

    def test_single_range(self):
        result = parse_key_ranges("H1,8,8")
        assert result == [("H1", 8.0, 8.0)]

    def test_multiple_ranges(self):
        result = parse_key_ranges("H1,1,1.1;H1,3,3.1;H1,4,4.7")
        assert len(result) == 3
        assert result[0] == ("H1", 1.0, 1.1)
        assert result[1] == ("H1", 3.0, 3.1)
        assert result[2] == ("H1", 4.0, 4.7)

    def test_h2_type(self):
        result = parse_key_ranges("H2,264901,264901")
        assert result == [("H2", 264901.0, 264901.0)]


class TestSubEntryGrouping:
    """Task 5.2: Group sub-entries by lnum range."""

    @pytest.fixture
    def sample_data(self) -> MwData:
        data = MwData()
        data.entries = {
            1.0: MwEntry(
                key="a",
                lnum=1.0,
                data="<H1><body>first</body><tail><pc>1,1</pc></tail></H1>",
            ),
            1.1: MwEntry(
                key="a",
                lnum=1.1,
                data="<H1A><body>sub</body><tail><pc>1,1</pc></tail></H1A>",
            ),
            3.0: MwEntry(
                key="a",
                lnum=3.0,
                data="<H1><body>second</body><tail><pc>1,1</pc></tail></H1>",
            ),
            3.1: MwEntry(
                key="a",
                lnum=3.1,
                data="<H1A><body>sub2</body><tail><pc>1,1</pc></tail></H1A>",
            ),
        }
        data.keys = {
            1.0: MwKeyEntry(key="a", lnum=1.0, data="H1,1,1.1;H1,3,3.1"),
        }
        data.abbreviations = {}
        data.author_tooltips = {}
        return data

    def test_builds_correct_entry_count(self, sample_data: MwData):
        entries = build_mw_entries(sample_data)
        assert len(entries) == 1

    def test_entry_word_is_iast(self, sample_data: MwData):
        entries = build_mw_entries(sample_data)
        assert entries[0].word == "a"

    def test_entry_html_contains_all_sub_entries(self, sample_data: MwData):
        entries = build_mw_entries(sample_data)
        assert "first" in entries[0].definition_html
        assert "sub" in entries[0].definition_html
        assert "second" in entries[0].definition_html


class TestPageColumnReference:
    """Task 5.4: Page-column references in output."""

    @pytest.fixture
    def data_with_pc(self) -> MwData:
        data = MwData()
        data.entries = {
            890.0: MwEntry(
                key="agni",
                lnum=890.0,
                data="<H1><body><s>agni</s> fire</body><tail><pc>5,1</pc></tail></H1>",
            ),
        }
        data.keys = {
            707.0: MwKeyEntry(key="agni", lnum=707.0, data="H1,890,890"),
        }
        data.abbreviations = {}
        data.author_tooltips = {}
        return data

    def test_page_ref_in_html(self, data_with_pc: MwData):
        entries = build_mw_entries(data_with_pc)
        html = entries[0].definition_html
        assert "Printed book page" in html
        assert "pcol-ref" in html


class TestSynonymGeneration:
    """Task 5.5: Synonym generation (IAST + niggahita variants + SLP1)."""

    def test_basic_synonym(self):
        syns = generate_synonyms("agni")
        assert "agni" in syns

    def test_iast_synonym(self):
        syns = generate_synonyms("saMskfta")
        assert "saṃskṛta" in syns

    def test_niggahita_variants(self):
        syns = generate_synonyms("saMskfta")
        iast_forms = [s for s in syns if "ṃ" in s or "ṁ" in s]
        assert len(iast_forms) >= 1

    def test_slp1_included(self):
        syns = generate_synonyms("saMskfta")
        assert "saMskfta" in syns


class TestBuildMwEntriesIntegration:
    """Task 5.3/5.6: Full integration with real data."""

    def test_real_data_produces_entries(self):
        sqlite_dir = (
            Path(__file__).parent.parent
            / "dictionaries"
            / "mw"
            / "source"
            / "web"
            / "sqlite"
        )
        from dictionaries.mw.mw_helpers import load_mw_data

        data = load_mw_data(sqlite_dir)
        entries = build_mw_entries(data)
        # Cologne updates upstream data; assert a floor, not an exact pin.
        assert len(entries) >= 194_083

    def test_first_entry_is_a(self):
        sqlite_dir = (
            Path(__file__).parent.parent
            / "dictionaries"
            / "mw"
            / "source"
            / "web"
            / "sqlite"
        )
        from dictionaries.mw.mw_helpers import load_mw_data

        data = load_mw_data(sqlite_dir)
        entries = build_mw_entries(data)
        assert entries[0].word == "a"
        assert entries[0].definition_html
        assert len(entries[0].synonyms) >= 1

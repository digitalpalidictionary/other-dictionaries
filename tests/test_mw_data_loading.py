"""Test mw data loading from SQLite databases.

Tests verify that load_mw_data() correctly reads:
- mwab.sqlite: 424 abbreviations → dict[str, str] (key → tooltip text)
- mwauthtooltips.sqlite: 871 tooltips → dict[str, str] (key → full name)
- mw.sqlite: 286,554 sub-entries → dict[float, MwEntry]
- mwkeys.sqlite: 194,083 headwords → dict[float, MwKeyEntry]
"""

from pathlib import Path

import pytest

from dictionaries.mw.mw_helpers import MwData, load_mw_data

SQLITE_DIR = (
    Path(__file__).parent.parent / "dictionaries" / "mw" / "source" / "web" / "sqlite"
)


@pytest.fixture(scope="module")
def mw_data() -> MwData:
    """Load all MW data once for the module."""
    return load_mw_data(SQLITE_DIR)


class TestAbbreviationLoading:
    """Task 2.1: Test abbreviation loading from mwab.sqlite."""

    def test_abbreviations_count(self, mw_data: MwData):
        assert len(mw_data.abbreviations) == 424

    def test_abbreviation_is_dict(self, mw_data: MwData):
        assert isinstance(mw_data.abbreviations, dict)

    def test_known_abbreviation_exists(self, mw_data: MwData):
        assert "f." in mw_data.abbreviations

    def test_abbreviation_value_is_display_text(self, mw_data: MwData):
        assert mw_data.abbreviations["f."] == "feminine"

    def test_abbreviation_ind(self, mw_data: MwData):
        assert mw_data.abbreviations["ind."] == "indeclinable"


class TestAuthorTooltipLoading:
    """Task 2.2: Test author tooltip loading from mwauthtooltips.sqlite."""

    def test_tooltips_count(self, mw_data: MwData):
        assert len(mw_data.author_tooltips) == 868

    def test_tooltips_is_dict(self, mw_data: MwData):
        assert isinstance(mw_data.author_tooltips, dict)

    def test_known_tooltip_exists(self, mw_data: MwData):
        assert "Abhinav." in mw_data.author_tooltips

    def test_tooltip_value_is_full_name(self, mw_data: MwData):
        assert mw_data.author_tooltips["Abhinav."] == "Abhinava-gupta"


class TestEntryLoading:
    """Task 2.3: Test entry loading from mw.sqlite."""

    def test_entries_count(self, mw_data: MwData):
        assert len(mw_data.entries) == 286_554

    def test_entries_is_dict(self, mw_data: MwData):
        assert isinstance(mw_data.entries, dict)

    def test_entry_keyed_by_lnum(self, mw_data: MwData):
        entry = mw_data.entries[1.0]
        assert entry.key == "a"
        assert "<H1>" in entry.data

    def test_entry_has_key_and_data(self, mw_data: MwData):
        entry = mw_data.entries[1.1]
        assert entry.key == "a"
        assert "short vowel" in entry.data


class TestHeadwordKeyLoading:
    """Task 2.4: Test headword key parsing from mwkeys.sqlite."""

    def test_keys_count(self, mw_data: MwData):
        assert len(mw_data.keys) == 194_083

    def test_keys_is_dict(self, mw_data: MwData):
        assert isinstance(mw_data.keys, dict)

    def test_key_entry_has_key_and_data(self, mw_data: MwData):
        key_entry = mw_data.keys[1.0]
        assert key_entry.key == "a"
        assert "H1,1,1.1" in key_entry.data

    def test_key_entry_simple(self, mw_data: MwData):
        key_entry = mw_data.keys[2.0]
        assert key_entry.key == "afRin"
        assert key_entry.data == "H1,8,8"

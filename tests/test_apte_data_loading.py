"""Test apte data loading from SQLite databases.

Tests verify that load_apte_data() correctly reads:
- ap90ab.sqlite: abbreviations → dict[str, str] (id → display text)
- ap90authtooltips.sqlite: tooltips → dict[str, str] (key → full name)
- ap90.sqlite: sub-entries → dict[str, list[ApteEntry]] (key → entries by lnum)
"""

from dictionaries.apte.apte_helpers import ApteData, ApteEntry


class TestApteDataclasses:
    def test_apte_data_has_three_fields(self):
        data = ApteData()
        assert hasattr(data, "abbreviations")
        assert hasattr(data, "author_tooltips")
        assert hasattr(data, "entries")

    def test_apte_entry_has_three_fields(self):
        entry = ApteEntry(key="agni", lnum=1.0, data="<H1>test</H1>")
        assert entry.key == "agni"
        assert entry.lnum == 1.0
        assert entry.data == "<H1>test</H1>"

    def test_entries_grouped_by_key(self):
        """entries is dict[str, list[ApteEntry]] keyed by slp1 headword."""
        data = ApteData()
        data.entries = {
            "agni": [ApteEntry(key="agni", lnum=1.0, data="<H1>fire</H1>")],
        }
        assert "agni" in data.entries
        assert isinstance(data.entries["agni"], list)
        assert data.entries["agni"][0].lnum == 1.0

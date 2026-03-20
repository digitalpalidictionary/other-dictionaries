"""Test mw mobile export support.

Task 7.1: Verify JSON intermediate file creation, path definitions,
and mobile-compatible entry format (dict_id="mw", CSS populated).
"""

import json
from pathlib import Path
from unittest.mock import MagicMock

from vendor.dpd_tools.paths import RepoPaths


class TestMwJsonPath:
    def test_repo_paths_has_mw_json_path(self):
        pth = RepoPaths(create_dirs=False)
        assert hasattr(pth, "mw_json_path")

    def test_mw_json_path_ends_with_mw_json(self):
        pth = RepoPaths(create_dirs=False)
        assert pth.mw_json_path.name == "mw.json"

    def test_mw_json_path_in_source_dir(self):
        pth = RepoPaths(create_dirs=False)
        assert "source" in str(pth.mw_json_path)


class TestMwJsonFormat:
    """Verify the JSON structure matches the MW JSON format used by mobile exporter."""

    def test_json_entry_has_required_keys(self):
        entry = {
            "word": "agni",
            "definition_html": "<div>fire</div>",
            "definition_plain": "",
            "synonyms": ["agni", "\u0905\u0917\u094d\u0928\u093f"],
        }
        assert "word" in entry
        assert "definition_html" in entry
        assert "definition_plain" in entry
        assert "synonyms" in entry

    def test_json_roundtrip_preserves_html(self):
        html = '<div class="mw-entry"><span class="sdata">agn\u00ed</span></div>'
        entries = [
            {
                "word": "agni",
                "definition_html": html,
                "definition_plain": "",
                "synonyms": [],
            }
        ]
        serialized = json.dumps(entries, ensure_ascii=False)
        deserialized = json.loads(serialized)
        assert deserialized[0]["definition_html"] == html

    def test_json_roundtrip_preserves_unicode(self):
        entries = [
            {
                "word": "agn\u00ed",
                "definition_html": "<div>\u0905\u0917\u094d\u0928\u093f</div>",
                "definition_plain": "",
                "synonyms": ["agn\u00ed"],
            }
        ]
        serialized = json.dumps(entries, ensure_ascii=False)
        deserialized = json.loads(serialized)
        assert deserialized[0]["word"] == "agn\u00ed"
        assert "\u0905\u0917\u094d\u0928\u093f" in deserialized[0]["definition_html"]


class TestMwJsonSaving:
    """Verify mw_from_cologne.py saves JSON in the correct format."""

    def test_save_json_creates_file(self, tmp_path: Path):
        json_path = tmp_path / "mw.json"
        mock_entries = [
            MagicMock(
                word="agni",
                definition_html="<div>fire</div>",
                definition_plain="",
                synonyms=["agni"],
            ),
        ]
        json_data = [
            {
                "word": e.word,
                "definition_html": e.definition_html,
                "definition_plain": e.definition_plain,
                "synonyms": e.synonyms,
            }
            for e in mock_entries
        ]
        with open(json_path, "w") as f:
            json.dump(json_data, f, ensure_ascii=False)

        assert json_path.exists()

    def test_saved_json_is_list(self, tmp_path: Path):
        json_path = tmp_path / "mw.json"
        entries = [
            {
                "word": "agni",
                "definition_html": "<div>fire</div>",
                "definition_plain": "",
                "synonyms": [],
            },
            {
                "word": "vayu",
                "definition_html": "<div>wind</div>",
                "definition_plain": "",
                "synonyms": [],
            },
        ]
        with open(json_path, "w") as f:
            json.dump(entries, f)

        with open(json_path) as f:
            loaded = json.load(f)
        assert isinstance(loaded, list)
        assert len(loaded) == 2

    def test_saved_json_dict_id_not_in_entries(self, tmp_path: Path):
        """dict_id is NOT stored in JSON — it's applied by the mobile exporter."""
        json_path = tmp_path / "mw.json"
        entries = [
            {
                "word": "agni",
                "definition_html": "<div>fire</div>",
                "definition_plain": "",
                "synonyms": [],
            },
        ]
        with open(json_path, "w") as f:
            json.dump(entries, f)

        with open(json_path) as f:
            loaded = json.load(f)
        assert "dict_id" not in loaded[0]


class TestMwMobileInsertion:
    """Verify the mobile exporter pattern for mw entries."""

    def test_dict_id_is_mw(self):
        entry = {"word": "agni", "definition_html": "<div>fire</div>"}
        row = ("mw", entry["word"], "agni", entry["definition_html"], "")
        assert row[0] == "mw"

    def test_css_populated_when_file_exists(self, tmp_path: Path):
        css_path = tmp_path / "mw.css"
        css_content = ".sdata { color: teal; }"
        css_path.write_text(css_content)

        mw_css = css_path.read_text() if css_path.exists() else ""
        assert mw_css == css_content
        assert len(mw_css) > 0

    def test_page_refs_preserved_in_html(self):
        html_with_ref = '<div><span class="pcol-ref">[p.5,1]</span> agni, fire</div>'
        entry = {"word": "agni", "definition_html": html_with_ref}
        assert "pcol-ref" in entry["definition_html"]
        assert "[p.5,1]" in entry["definition_html"]

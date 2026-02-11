"""Test that source data files have valid schema."""

import csv
from pathlib import Path

import pytest

SOURCE_DIR = Path(__file__).parent.parent / "dictionaries"


class TestBoldDefSource:
    """Test bold_definitions source TSV schema."""

    @pytest.fixture
    def source_path(self):
        return SOURCE_DIR / "bold_def" / "source" / "bold_definitions.tsv"

    def test_file_exists(self, source_path):
        assert source_path.exists(), f"Missing: {source_path}"

    def test_valid_tsv(self, source_path):
        with open(source_path) as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)
        assert len(rows) > 0

    def test_entry_schema(self, source_path):
        with open(source_path) as f:
            reader = csv.DictReader(f, delimiter="\t")
            row = next(reader)
        assert "bold" in row, "Missing 'bold' field"
        assert "commentary" in row, "Missing 'commentary' field"


class TestPeuSource:
    """Test PEU source JS/JSON schema (downloaded from pm12e.pali.tools/dump)."""

    @pytest.fixture
    def source_path(self):
        return SOURCE_DIR / "peu" / "source" / "peu_dump.js"

    def test_file_exists(self, source_path):
        assert source_path.exists(), f"Missing: {source_path}"

    def test_valid_structure(self, source_path):
        content = source_path.read_text()
        assert "var pm12e" in content or content.startswith("{"), "File should contain var pm12e or start with {"
        assert "'a':" in content, "Should contain headword 'a'"


class TestSimsapaSource:
    """Test Simsapa source TSV schema.

    Simsapa data is extracted from the Simsapa appdata.sqlite3 database.
    Requires update_source.py to be run with access to the Simsapa DB.
    """

    @pytest.fixture
    def source_path(self):
        return SOURCE_DIR / "simsapa" / "source" / "simsapa.tsv"

    @pytest.mark.skip(reason="Requires Simsapa DB extraction")
    def test_file_exists(self, source_path):
        assert source_path.exists(), f"Missing: {source_path}"

    @pytest.mark.skip(reason="Requires Simsapa DB extraction")
    def test_valid_tsv(self, source_path):
        with open(source_path) as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)
        assert len(rows) > 0


class TestMwSource:
    """Test MW source TSV schema.

    MW data is extracted from the Simsapa appdata.sqlite3 database.
    Requires update_source.py to be run with access to the Simsapa DB.
    """

    @pytest.fixture
    def source_path(self):
        return SOURCE_DIR / "mw" / "source" / "mw.tsv"

    @pytest.mark.skip(reason="Requires Simsapa DB extraction")
    def test_file_exists(self, source_path):
        assert source_path.exists(), f"Missing: {source_path}"

    @pytest.mark.skip(reason="Requires Simsapa DB extraction")
    def test_valid_tsv(self, source_path):
        with open(source_path) as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)
        assert len(rows) > 0

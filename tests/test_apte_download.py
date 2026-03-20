"""Test apte auto-download logic (download, compare, unpack).

Tests verify that download_fresh_source():
- Downloads ap90web1.zip when no local copy exists
- Skips download when remote size matches local zip
- Re-downloads and unpacks when remote size differs
- Extracts SQLite files into source/web/sqlite/
"""

import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from dictionaries.apte.apte_helpers import APTE_ZIP_URL, download_fresh_source


@pytest.fixture
def tmp_apte_dir(tmp_path: Path) -> Path:
    """Create a temporary apte source directory structure."""
    source_dir = tmp_path / "source"
    sqlite_dir = source_dir / "web" / "sqlite"
    sqlite_dir.mkdir(parents=True)
    return tmp_path


@pytest.fixture
def fake_zip(tmp_path: Path) -> Path:
    """Create a small valid zip file with a dummy SQLite file inside."""
    zip_path = tmp_path / "test.zip"
    dummy_sqlite = tmp_path / "web" / "sqlite" / "ap90.sqlite"
    dummy_sqlite.parent.mkdir(parents=True)
    dummy_sqlite.write_bytes(b"fake-sqlite-data")
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(dummy_sqlite, "web/sqlite/ap90.sqlite")
    return zip_path


class TestDownloadUrl:
    def test_url_points_to_cologne_server(self):
        assert "sanskrit-lexicon.uni-koeln.de" in APTE_ZIP_URL

    def test_url_ends_with_ap90web1_zip(self):
        assert APTE_ZIP_URL.endswith("ap90web1.zip")


class TestDownloadFreshSource:
    @patch("dictionaries.apte.apte_helpers.requests.head")
    @patch("dictionaries.apte.apte_helpers.requests.get")
    def test_downloads_when_no_local_zip(
        self,
        mock_get: MagicMock,
        mock_head: MagicMock,
        tmp_apte_dir: Path,
        fake_zip: Path,
    ):
        """Should download and unpack when no local zip exists."""
        zip_path = tmp_apte_dir / "source" / "ap90web1.zip"
        assert not zip_path.exists()

        mock_head.return_value = MagicMock(
            headers={"Content-Length": str(fake_zip.stat().st_size)},
            status_code=200,
        )
        mock_get.return_value = MagicMock(
            content=fake_zip.read_bytes(),
            status_code=200,
        )

        download_fresh_source(zip_path=zip_path, source_dir=tmp_apte_dir / "source")

        assert zip_path.exists()
        assert (tmp_apte_dir / "source" / "web" / "sqlite" / "ap90.sqlite").exists()

    @patch("dictionaries.apte.apte_helpers.requests.head")
    def test_skips_when_size_matches(
        self, mock_head: MagicMock, tmp_apte_dir: Path, fake_zip: Path
    ):
        """Should skip download when remote size matches local zip."""
        zip_path = tmp_apte_dir / "source" / "ap90web1.zip"
        zip_path.write_bytes(fake_zip.read_bytes())
        local_size = zip_path.stat().st_size

        mock_head.return_value = MagicMock(
            headers={"Content-Length": str(local_size)},
            status_code=200,
        )

        download_fresh_source(zip_path=zip_path, source_dir=tmp_apte_dir / "source")

        mock_head.assert_called_once()

    @patch("dictionaries.apte.apte_helpers.requests.head")
    @patch("dictionaries.apte.apte_helpers.requests.get")
    def test_redownloads_when_size_differs(
        self,
        mock_get: MagicMock,
        mock_head: MagicMock,
        tmp_apte_dir: Path,
        fake_zip: Path,
    ):
        """Should re-download when remote size differs from local."""
        zip_path = tmp_apte_dir / "source" / "ap90web1.zip"
        zip_path.write_bytes(b"old-smaller-zip")

        mock_head.return_value = MagicMock(
            headers={"Content-Length": str(fake_zip.stat().st_size)},
            status_code=200,
        )
        mock_get.return_value = MagicMock(
            content=fake_zip.read_bytes(),
            status_code=200,
        )

        download_fresh_source(zip_path=zip_path, source_dir=tmp_apte_dir / "source")

        mock_get.assert_called_once()
        assert zip_path.stat().st_size == fake_zip.stat().st_size

    @patch("dictionaries.apte.apte_helpers.requests.head")
    @patch("dictionaries.apte.apte_helpers.requests.get")
    def test_unpacks_sqlite_files(
        self, mock_get: MagicMock, mock_head: MagicMock, tmp_apte_dir: Path
    ):
        """Should extract zip contents into source directory."""
        zip_path = tmp_apte_dir / "source" / "ap90web1.zip"
        sqlite_dir = tmp_apte_dir / "source" / "web" / "sqlite"

        test_zip = tmp_apte_dir / "build.zip"
        dummy = tmp_apte_dir / "web" / "sqlite" / "ap90keys.sqlite"
        dummy.parent.mkdir(parents=True)
        dummy.write_bytes(b"keys-data")
        with zipfile.ZipFile(test_zip, "w") as zf:
            zf.write(dummy, "web/sqlite/ap90keys.sqlite")

        mock_head.return_value = MagicMock(
            headers={"Content-Length": "999"},
            status_code=200,
        )
        mock_get.return_value = MagicMock(
            content=test_zip.read_bytes(),
            status_code=200,
        )

        download_fresh_source(zip_path=zip_path, source_dir=tmp_apte_dir / "source")

        assert (sqlite_dir / "ap90keys.sqlite").exists()
        assert (sqlite_dir / "ap90keys.sqlite").read_bytes() == b"keys-data"

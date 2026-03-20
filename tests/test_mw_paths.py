"""Test mw path configuration in RepoPaths (vendor/dpd_tools/paths.py).

Verifies that RepoPaths has mw attributes pointing to:
- mw_source_dir: SQLite databases (mw.sqlite, mwkeys.sqlite, etc.)
- mw_zip_path: downloaded mwweb1.zip archive
- mw_css_path: generated CSS file for mw dictionary
- mw_gd_path: GoldenDict output directory
- mw_mdict_path: MDict output directory
"""

from vendor.dpd_tools.paths import RepoPaths


class TestRepoPathsMw:
    """Test mw paths in the standalone other-dictionaries RepoPaths."""

    def test_mw_source_dir_exists_and_points_to_sqlite(self):
        pth = RepoPaths(create_dirs=False)
        assert hasattr(pth, "mw_source_dir")
        expected = pth.dictionaries_dir / "mw" / "source" / "web" / "sqlite"
        assert pth.mw_source_dir == expected

    def test_mw_zip_path_points_to_mwweb1(self):
        pth = RepoPaths(create_dirs=False)
        assert hasattr(pth, "mw_zip_path")
        expected = pth.dictionaries_dir / "mw" / "source" / "mwweb1.zip"
        assert pth.mw_zip_path == expected

    def test_mw_css_path_points_to_mw_css(self):
        pth = RepoPaths(create_dirs=False)
        assert hasattr(pth, "mw_css_path")
        expected = pth.dictionaries_dir / "mw" / "mw.css"
        assert pth.mw_css_path == expected

    def test_mw_gd_path_is_goldendict_dir(self):
        pth = RepoPaths(create_dirs=False)
        assert hasattr(pth, "mw_gd_path")
        assert pth.mw_gd_path == pth.goldendict_path

    def test_mw_mdict_path_is_mdict_dir(self):
        pth = RepoPaths(create_dirs=False)
        assert hasattr(pth, "mw_mdict_path")
        assert pth.mw_mdict_path == pth.mdict_path

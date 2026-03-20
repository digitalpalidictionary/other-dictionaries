"""Test apte path configuration in RepoPaths (vendor/dpd_tools/paths.py).

Verifies that RepoPaths has apte attributes pointing to:
- apte_source_dir: SQLite databases (ap90.sqlite, ap90keys.sqlite, etc.)
- apte_zip_path: downloaded ap90web1.zip archive
- apte_json_path: intermediate JSON file
- apte_css_path: generated CSS file for apte dictionary
- apte_gd_path: GoldenDict output directory
- apte_mdict_path: MDict output directory
"""

from vendor.dpd_tools.paths import RepoPaths


class TestRepoPathsApte:
    """Test apte paths in the standalone other-dictionaries RepoPaths."""

    def test_apte_has_all_six_path_attributes(self):
        pth = RepoPaths(create_dirs=False)
        for attr in [
            "apte_source_dir",
            "apte_zip_path",
            "apte_json_path",
            "apte_css_path",
            "apte_gd_path",
            "apte_mdict_path",
        ]:
            assert hasattr(pth, attr), f"RepoPaths missing attribute: {attr}"

    def test_apte_source_dir_points_to_sqlite(self):
        pth = RepoPaths(create_dirs=False)
        expected = pth.dictionaries_dir / "apte" / "source" / "web" / "sqlite"
        assert pth.apte_source_dir == expected

    def test_apte_css_path_filename_is_apte_css(self):
        pth = RepoPaths(create_dirs=False)
        assert pth.apte_css_path.name == "apte.css"

    def test_apte_zip_path_filename_is_ap90web1_zip(self):
        pth = RepoPaths(create_dirs=False)
        assert pth.apte_zip_path.name == "ap90web1.zip"

    def test_apte_gd_path_is_goldendict_dir(self):
        pth = RepoPaths(create_dirs=False)
        assert pth.apte_gd_path == pth.goldendict_path

    def test_apte_mdict_path_is_mdict_dir(self):
        pth = RepoPaths(create_dirs=False)
        assert pth.apte_mdict_path == pth.mdict_path

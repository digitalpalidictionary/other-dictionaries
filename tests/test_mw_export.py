"""Test mw GoldenDict export integration.

Task 6.1: Verify dict name is 'mw' and export_all includes mw.
"""


class TestExportAllIncludesMw:
    def test_mw_imported_in_export_all(self):
        from scripts.export_all import mw

        assert callable(mw)

    def test_mw_exporter_importable(self):
        from dictionaries.mw.mw_from_cologne import main

        assert callable(main)

    def test_dict_name_is_mw(self):
        from vendor.dpd_tools.goldendict_exporter import DictVariables
        from vendor.dpd_tools.paths import RepoPaths

        pth = RepoPaths(create_dirs=False)
        dv = DictVariables(
            css_paths=[pth.mw_css_path],
            js_paths=None,
            gd_path=pth.mw_gd_path,
            md_path=pth.mw_mdict_path,
            dict_name="mw",
            icon_path=None,
        )
        assert "mw" in str(dv.gd_zip_path)
        assert "mw" in str(dv.mdict_mdx_path)

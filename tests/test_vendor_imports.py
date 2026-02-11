"""Test that all vendored tools are importable and functional."""



class TestVendorImports:
    def test_import_dict_entry(self):
        from vendor.dpd_tools.goldendict_exporter import DictEntry

        entry = DictEntry(word="test", definition_html="<b>test</b>", definition_plain="", synonyms=[])
        assert entry.word == "test"

    def test_import_dict_info(self):
        from vendor.dpd_tools.goldendict_exporter import DictInfo

        info = DictInfo(
            bookname="Test",
            author="Test Author",
            description="Test Description",
            website="test.com",
            source_lang="pi",
            target_lang="en",
        )
        assert info.bookname == "Test"

    def test_import_dict_variables(self):
        from pathlib import Path
        from vendor.dpd_tools.goldendict_exporter import DictVariables

        var = DictVariables(
            css_paths=None,
            js_paths=None,
            gd_path=Path("build/goldendict"),
            md_path=Path("build/mdict"),
            dict_name="test",
            icon_path=None,
        )
        assert var.gd_zip_path.name == "test.zip"

    def test_import_goldendict_export_function(self):
        from vendor.dpd_tools.goldendict_exporter import export_to_goldendict_with_pyglossary

        assert callable(export_to_goldendict_with_pyglossary)

    def test_import_mdict_exporter(self):
        from vendor.dpd_tools.mdict_exporter import export_to_mdict

        assert callable(export_to_mdict)

    def test_import_niggahitas(self):
        from vendor.dpd_tools.niggahitas import add_niggahitas

        result = add_niggahitas(["saṃsāra"])
        assert "saṃsāra" in result
        assert "saṁsāra" in result

    def test_import_printer(self):
        from vendor.dpd_tools.printer import printer as pr

        assert hasattr(pr, "tic")
        assert hasattr(pr, "toc")

    def test_import_pali_sort_key(self):
        from vendor.dpd_tools.pali_sort_key import pali_sort_key

        result = pali_sort_key("dhamma")
        assert isinstance(result, str)

    def test_import_sanskrit_translit(self):
        from vendor.dpd_tools.sanskrit_translit import slp1_translit

        result = slp1_translit("A")
        assert result == "ā"

    def test_import_paths(self):
        from vendor.dpd_tools.paths import RepoPaths

        pth = RepoPaths(create_dirs=False)
        assert pth.goldendict_path.name == "goldendict"
        assert pth.mdict_path.name == "mdict"
        assert pth.bhs_source_path.name == "bhs.xml"

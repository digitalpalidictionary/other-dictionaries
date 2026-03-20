"""Test apte export configuration.

Tests verify:
- main() function exists and is callable
- DictInfo uses correct bookname and author
- DictVariables uses dict_name="apte"
"""

import inspect

import dictionaries.apte.apte_from_cologne as apte_module
from vendor.dpd_tools.goldendict_exporter import DictInfo, DictVariables


class TestMainFunctionExists:
    def test_main_function_exists(self):
        assert hasattr(apte_module, "main")
        assert callable(apte_module.main)

    def test_main_is_a_function(self):
        assert inspect.isfunction(apte_module.main)


class TestDictInfo:
    def test_dict_info_bookname(self):
        info = DictInfo(
            bookname="Apte Practical Sanskrit-English Dictionary, 1890",
            author="Vaman Shivram Apte",
            description="test",
            website="https://www.sanskrit-lexicon.uni-koeln.de",
            source_lang="sa",
            target_lang="en",
        )
        assert "Apte" in info.bookname
        assert "1890" in info.bookname

    def test_dict_info_author(self):
        info = DictInfo(
            bookname="Apte Practical Sanskrit-English Dictionary, 1890",
            author="Vaman Shivram Apte",
            description="test",
            website="https://www.sanskrit-lexicon.uni-koeln.de",
            source_lang="sa",
            target_lang="en",
        )
        assert info.author == "Vaman Shivram Apte"


class TestDictVariables:
    def test_dict_name_is_apte(self):
        from pathlib import Path

        vars_ = DictVariables(
            css_paths=[Path("apte.css")],
            js_paths=None,
            gd_path=Path("build/goldendict"),
            md_path=Path("build/mdict"),
            dict_name="apte",
            icon_path=None,
            zip_up=True,
            delete_original=True,
        )
        assert "apte" in str(vars_.gd_path)

# -*- coding: utf-8 -*-
import csv

from jinja2 import Template

from vendor.dpd_tools.goldendict_exporter import (
    DictEntry,
    DictInfo,
    DictVariables,
    export_to_goldendict_with_pyglossary,
)
from vendor.dpd_tools.mdict_exporter import export_to_mdict
from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr


class BoldDefinitions:
    """Export CST Bold Definitions to Goldendict and MDict"""

    def __init__(self):
        self.pth = RepoPaths()
        self.template = self._load_template()

    def _load_template(self) -> Template:
        with open(self.pth.bold_def_template_path, encoding="utf-8") as f:
            return Template(f.read())

    def run(self):
        pr.tic()
        pr.title("exporting bold definitions")
        pr.green("loading data from TSV")

        dict_info = self._get_dict_info()
        dict_vars = self._get_dict_vars()

        bd_data = self._load_tsv_data()
        pr.yes(len(bd_data))

        dict_data = self.make_dict_data(bd_data)

        export_to_goldendict_with_pyglossary(dict_info, dict_vars, dict_data)
        export_to_mdict(dict_info, dict_vars, dict_data)

        pr.toc()

    def _load_tsv_data(self) -> list[dict]:
        data = []
        with open(self.pth.bold_def_source_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                data.append(row)
        return data

    def _get_dict_info(self) -> DictInfo:
        return DictInfo(
            bookname="CST Bold Definitions",
            author="Bodhirasa Bhikkhu",
            description="Extracted from Chaṭṭha Saṅgāyana Tipiṭaka",
            website="dpdict.net/?tab=bd&q1=&q2=&option=regex",
            source_lang="pi",
            target_lang="pi",
        )

    def _get_dict_vars(self) -> DictVariables:
        return DictVariables(
            css_paths=None,
            js_paths=None,
            gd_path=self.pth.bold_def_gd_path,
            md_path=self.pth.bold_def_mdict_path,
            dict_name="bold-def",
            icon_path=None,
            zip_up=True,
            delete_original=True,
        )

    def make_dict_data(self, bd_data: list[dict]) -> list[DictEntry]:
        pr.green_title("making dict data")
        dict_data = []
        total = len(bd_data)

        for counter, bd_entry in enumerate(bd_data):
            dict_entry = self.make_dict_entry(bd_entry)
            dict_data.append(dict_entry)
            if counter % 50000 == 0:
                pr.counter(counter, total, bd_entry.get("bold", ""))
        return dict_data

    def make_dict_entry(self, bd_entry: dict) -> DictEntry:
        word = bd_entry.get("bold", "")
        definition_html = self.template.render(bd=bd_entry)
        return DictEntry(
            word=word,
            definition_html=definition_html,
            definition_plain="",
            synonyms=[],
        )


if __name__ == "__main__":
    bd = BoldDefinitions()
    bd.run()

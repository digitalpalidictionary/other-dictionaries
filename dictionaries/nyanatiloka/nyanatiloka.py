# -*- coding: utf-8 -*-
import json

from vendor.dpd_tools.goldendict_exporter import (
    DictEntry,
    DictInfo,
    DictVariables,
    export_to_goldendict_with_pyglossary,
)
from vendor.dpd_tools.mdict_exporter import export_to_mdict
from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr


def main():
    """Export Nyanatiloka's Buddhist Dictionary to Goldendict and MDict"""

    pr.tic()
    pr.title("exporting Nyanatiloka's Buddhist Dictionary")

    pr.green("preparing data")
    pth = RepoPaths()
    dict_data: list[DictEntry] = []

    with open(pth.nyanatiloka_source_path, encoding="utf-8") as f:
        nyanatiloka_json = json.load(f)

    for i in nyanatiloka_json:
        dict_entry = DictEntry(
            word=i["word"],
            definition_html=i["definition_html"],
            definition_plain="",
            synonyms=[],
        )
        dict_data.append(dict_entry)

    dict_info = DictInfo(
        bookname="Buddhist Dictionary: Manual of Buddhist Terms and Doctrines",
        author="Nyanatiloka Mahathera",
        description="4th revised edition, ed. Nyanaponika Mahathera, Buddhist Publication Society, 1980",
        website="https://www.dhammatalks.net/Buddhist.Dictionary/",
        source_lang="pi",
        target_lang="en",
    )

    dict_vars = DictVariables(
        css_paths=[pth.nyanatiloka_css_path],
        js_paths=None,
        gd_path=pth.nyanatiloka_gd_path,
        md_path=pth.nyanatiloka_mdict_path,
        dict_name="nyanatiloka",
        icon_path=None,
        zip_up=True,
        delete_original=True,
    )

    pr.yes(len(dict_data))

    export_to_goldendict_with_pyglossary(
        dict_info,
        dict_vars,
        dict_data,
    )

    export_to_mdict(
        dict_info,
        dict_vars,
        dict_data,
    )

    pr.toc()


if __name__ == "__main__":
    main()

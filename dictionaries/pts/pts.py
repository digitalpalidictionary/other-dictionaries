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
    """Export the PTS Pāli-English Dictionary to Goldendict and MDict"""

    pr.tic()
    pr.title("exporting PTS")

    pr.green("preparing data")
    pth = RepoPaths()
    dict_data: list[DictEntry] = []

    with open(pth.pts_source_path, encoding="utf-8") as f:
        pts_json = json.load(f)

    for i in pts_json:
        dict_entry = DictEntry(
            word=i["word"],
            definition_html=i["definition_html"],
            definition_plain="",
            synonyms=[],
        )
        dict_data.append(dict_entry)

    dict_info = DictInfo(
        bookname="PTS Pāḷi-English Dictionary",
        author="T. W. Rhys Davids & William Stede",
        description="The Pali Text Society's Pali-English Dictionary, 1921–25. Text from the BuddhaDust edition (obo.genaud.net), revised to the PTS 2015 corrected reprint. Corrected reprint © The Pāḷi Text Society, CC BY-NC, commercial rights reserved (as stated by BuddhaDust).",
        website="https://obo.genaud.net/backmatter/glossology/ped/pts_ped/ped.htm",
        source_lang="pi",
        target_lang="en",
    )

    dict_vars = DictVariables(
        css_paths=[pth.pts_css_path],
        js_paths=None,
        gd_path=pth.pts_gd_path,
        md_path=pth.pts_mdict_path,
        dict_name="pts",
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

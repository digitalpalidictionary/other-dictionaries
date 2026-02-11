# -*- coding: utf-8 -*-
import csv
import re
from vendor.dpd_tools.goldendict_exporter import DictEntry, DictInfo, DictVariables
from vendor.dpd_tools.goldendict_exporter import export_to_goldendict_with_pyglossary
from vendor.dpd_tools.mdict_exporter import export_to_mdict
from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr


def main():
    """Export Ven. Ānandajoti's Ancient Buddhist Texts Glossary to Goldendict"""

    pr.tic()
    pr.title("exporting ancient buddhist texts glossary")

    pr.white("processing csv")

    dict_data: list[DictEntry] = []
    pth = RepoPaths()

    with open(pth.abt_source_path, newline="") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter="|")
        for i in csv_reader:
            word = i[0].strip()
            if ": " in i[1]:
                pos, english = re.split(":", i[1].strip(), 1)
                definition = f"{pos.rstrip('.')}. <b>{english}</b>"
            else:
                english = i[1].strip()
                definition = f"<b>{english}</b>"

            dict_entry = DictEntry(
                word=word, definition_html=definition, definition_plain="", synonyms=[]
            )
            dict_data.append(dict_entry)

    dict_info = DictInfo(
        bookname="Concise Pali English Dictionary",
        author="Ven. A. P. Buddhadatta",
        description="Modified from the Original",
        website="ancient-buddhist-texts.net",
        source_lang="pi",
        target_lang="en",
    )

    dict_vars = DictVariables(
        css_paths=None,
        js_paths=None,
        gd_path=pth.abt_gd_path,
        md_path=pth.abt_mdict_path,
        dict_name="abt",
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

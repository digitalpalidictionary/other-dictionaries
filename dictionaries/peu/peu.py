# -*- coding: utf-8 -*-
"""Export PEU into Goldendict, MDict and JSON formats."""

import json
import re

from rich import print

from vendor.dpd_tools.goldendict_exporter import (
    DictEntry,
    DictInfo,
    DictVariables,
    export_to_goldendict_with_pyglossary,
)
from vendor.dpd_tools.mdict_exporter import export_to_mdict
from vendor.dpd_tools.niggahitas import add_niggahitas
from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr


def extract_peu_from_data_dump(pth: RepoPaths) -> list | None:
    """Load PEU data from dump file"""

    if not pth.peu_source_path.exists():
        print("[red]PEU source file not found")
        return None

    with open(pth.peu_source_path) as f:
        raw_data = f.read()

    # Strip JavaScript wrapper: var pm12e = {...};
    match = re.search(r"var\s+\w+\s*=\s*(\{.*\})\s*;?\s*$", raw_data, re.DOTALL)
    if match:
        raw_data = match.group(1)

    # Clean control characters
    raw_data = re.sub(r"[\x00-\x1F\x7F-\x9F]", "", raw_data)

    # Convert JS single quotes to JSON double quotes
    raw_data = raw_data.replace('"', "^^^")
    raw_data = raw_data.replace("'", '"')
    raw_data = raw_data.replace("^^^", "'")

    data_dict = json.loads(raw_data)

    # Convert dict to list of tuples (headword, html, book_id)
    data_list = [(k, v, 8) for k, v in data_dict.items()]
    return data_list


def main():
    pr.tic()
    print("[bright_yellow]exporting PEU from data dump")

    pth = RepoPaths()
    peu_data = extract_peu_from_data_dump(pth)

    if peu_data is None:
        print("[red]No PEU data available")
        pr.toc()
        return

    dict_data: list[DictEntry] = []

    for i in peu_data:
        headword, html, book_id = i
        headword = headword.replace("ṁ", "ṃ")
        html = html.replace("ṁ", "ṃ")

        if "ṃ" in headword:
            synonyms = add_niggahitas([headword])
        else:
            synonyms = []

        dict_entry = DictEntry(
            word=headword, definition_html=html, definition_plain="", synonyms=synonyms
        )
        dict_data.append(dict_entry)

    print("[green]saving goldendict")

    dict_info = DictInfo(
        bookname="Pali English Ultimate",
        author="Pali Myanmar Abhidhan",
        description="""<h3>Pali Myanmar Abhidhan</h3><p>Pali Myanmar Abhidhan is the world's largest Pali dictionary, a massive 23 volumes, with more than 200 000 words, a complete reference guide to the language of the root texts and commentaries.</p><p>There is a project underway to translate this into English, currently at about 80% human translated, the remainder is by Google.</p><p><a href='https://pm12e.pali.tools/'>Project Website</a></p><p>This dictionary can be found in the Tipitaka Pali Projector project on <a href='https://github.com/bksubhuti/Tipitaka-Pali-Projector'>GitHub</a></p><p>Encoded by Bodhirasa 2024.</p>""",
        website="https://pm12e.pali.tools/",
        source_lang="pa",
        target_lang="en",
    )

    dict_vars = DictVariables(
        css_paths=None,
        js_paths=None,
        gd_path=pth.peu_gd_path,
        md_path=pth.peu_mdict_path,
        dict_name="peu",
        icon_path=None,
        zip_up=True,
        delete_original=True,
    )

    export_to_goldendict_with_pyglossary(
        dict_info,
        dict_vars,
        dict_data,
    )

    print("[green]saving mdict")

    export_to_mdict(dict_info, dict_vars, dict_data)

    pr.toc()


if __name__ == "__main__":
    main()

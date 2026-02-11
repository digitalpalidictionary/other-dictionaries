"""Export Simsapa Combined from JSON to GoldenDict, MDict."""

import json

from bs4 import BeautifulSoup

from vendor.dpd_tools.goldendict_exporter import (
    DictEntry,
    DictInfo,
    DictVariables,
    export_to_goldendict_with_pyglossary,
)
from vendor.dpd_tools.mdict_exporter import export_to_mdict
from vendor.dpd_tools.niggahitas import add_niggahitas
from vendor.dpd_tools.pali_sort_key import pali_sort_key
from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr


class GlobalVars:
    pth = RepoPaths()
    simsapa_data: list[dict]
    dict_data: list[DictEntry]


def load_simsapa_data(g: GlobalVars):
    """Load Simsapa data from JSON file"""

    pr.green("loading simsapa data from json")

    if not g.pth.simsapa_source_path.exists():
        pr.red("Simsapa source file not found")
        g.simsapa_data = []
        return

    with open(g.pth.simsapa_source_path, encoding="utf-8") as f:
        data = json.load(f)

    g.simsapa_data = sorted(data, key=lambda x: pali_sort_key(x.get("word", "")))
    pr.yes(len(g.simsapa_data))


def make_data_list(g: GlobalVars):
    pr.green("making data list")
    dict_data: list[DictEntry] = []
    processed_headwords = set()

    index = 0
    for index, entry in enumerate(g.simsapa_data):
        headword = entry.get("word", "")
        html = entry.get("definition_html", "")
        synonyms = entry.get("synonyms", [])

        if headword not in processed_headwords:
            processed_headwords.add(headword)

            html_comp = html
            if synonyms:
                if isinstance(synonyms, list):
                    synonyms_comp = set(synonyms)
                else:
                    synonyms_comp = set([synonyms])
            else:
                synonyms_comp = set()
            next_index = index + 1
            if next_index < len(g.simsapa_data):
                next_headword = g.simsapa_data[next_index].get("word", "")
            else:
                next_headword = "fin"

            while headword == next_headword and next_index < len(g.simsapa_data):
                entry = g.simsapa_data[next_index]
                headword = entry.get("word", "")
                html = entry.get("definition_html", "")
                synonyms = entry.get("synonyms", [])
                html_comp += html
                if synonyms:
                    if isinstance(synonyms, list):
                        synonyms_comp.update(synonyms)
                    else:
                        synonyms_comp.add(synonyms)
                next_index = next_index + 1
                if next_index < len(g.simsapa_data):
                    next_headword = g.simsapa_data[next_index].get("word", "")
                else:
                    next_headword = "fin"

            soup = BeautifulSoup(html_comp, "html.parser")
            ays = soup.find_all("a")
            for ay in ays:
                if hasattr(ay, "unwrap"):
                    ay.unwrap()

            html_comp = str(soup)
            html_comp = html_comp.replace("ṁ", "ṃ")

            headword = headword.replace("ṁ", "ṃ")
            if "ṃ" in headword:
                synonyms_comp.update(add_niggahitas([headword], all=False))

            dict_entry = DictEntry(
                word=headword,
                definition_html=html_comp,
                definition_plain="",
                synonyms=list(synonyms_comp),
            )
            dict_data.append(dict_entry)

    g.dict_data = dict_data
    pr.yes(len(dict_data))


def save_goldendict_and_mdict(g: GlobalVars):
    """Save as Goldendict"""

    dict_info = DictInfo(
        bookname="Simsapa Combined Pali-English Dictionary",
        author="",
        description="<h3>Simsapa Combined Pali-English Dictionary</h3><p>Nyanatiloka's Buddhist Dictionary</p><p>Dictionary of Pali Proper Names (DPPN)</p><p>New Concise Pali - English Dictionary (NCPED)</p><p>Pali Text Society Pali - English Dictionary (PTS)</p><p>Reformatted for the <a href='https://github.com/simsapa/simsapa'>Simsapa Dhamma Reader.</a></p><p>Encoded by Bodhirasa 2024.</p>",
        website="https://simsapa.github.io/",
        source_lang="pa",
        target_lang="en",
    )

    dict_vars = DictVariables(
        css_paths=None,
        js_paths=None,
        gd_path=g.pth.simsapa_gd_path,
        md_path=g.pth.simsapa_mdict_path,
        dict_name="simsapa",
        icon_path=None,
        zip_up=True,
        delete_original=True,
    )

    export_to_goldendict_with_pyglossary(
        dict_info,
        dict_vars,
        g.dict_data,
    )

    export_to_mdict(dict_info, dict_vars, g.dict_data)


def main():
    pr.tic()
    pr.title("exporting Simsapa Combined to GoldenDict and MDict")
    g = GlobalVars()
    load_simsapa_data(g)
    if g.simsapa_data:
        make_data_list(g)
        save_goldendict_and_mdict(g)
    else:
        pr.red("No data to export")
    pr.toc()


if __name__ == "__main__":
    main()

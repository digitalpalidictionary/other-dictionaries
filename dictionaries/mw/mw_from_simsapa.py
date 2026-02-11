"""Export MW from JSON to GoldenDict and MDict."""

import json

from vendor.dpd_tools.goldendict_exporter import DictEntry, DictInfo, DictVariables
from vendor.dpd_tools.goldendict_exporter import export_to_goldendict_with_pyglossary
from vendor.dpd_tools.mdict_exporter import export_to_mdict

from vendor.dpd_tools.niggahitas import add_niggahitas
from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr


class GlobalVars:
    pth: RepoPaths = RepoPaths()
    mw_data: list[dict]
    dict_data: list[DictEntry] = []


def load_mw_from_json(g: GlobalVars):
    """Load MW data from JSON file."""
    pr.green("loading mw data from json")

    if not g.pth.mw_source_path.exists():
        pr.red("MW source file not found")
        g.mw_data = []
        return

    with open(g.pth.mw_source_path, encoding="utf-8") as f:
        g.mw_data = json.load(f)

    pr.yes(len(g.mw_data))


def make_dict_data(g: GlobalVars):
    pr.green("making data list")

    for entry in g.mw_data:
        headword = entry.get("word", "").replace("ṁ", "ṃ")
        html = entry.get("definition_html", "").replace("ṁ", "ṃ")

        if "ṃ" in headword:
            synonyms = add_niggahitas([headword])
        else:
            synonyms = []

        dict_entry = DictEntry(
            word=headword, definition_html=html, definition_plain="", synonyms=synonyms
        )
        g.dict_data.append(dict_entry)
    pr.yes(len(g.dict_data))


def save_goldendict_and_mdict(g: GlobalVars):
    dict_info = DictInfo(
        bookname="Monier Williams Sanskrit English Dictionary 1899",
        author="Sir Monier Monier Williams",
        description="""<h3>Monier-Williams' Sanskrit-English dictionary 1899</h3><p>Etymologically and philologically arranged with special reference to cognate Indo-European languages, by Sir Monier Monier-Williams, M.A., K.C.I.E. Boden Professor of Sanskṛit, Hon. D.C.L. Oxon, Hon. L.L.D. Calcutta, Hon. Ph.D. Göttingen, Hon. fellow of University College and sometime fellow of Balliol College, Oxford.</p><p>New edition, greatly enlarged and improved with the collaboration of Professor E. Leumann, Ph.D. of the University of Strassburg, Professor C. Cappeller, Ph.D. of the University of Jena, and other scholars.</p><p>Published by Oxford at the the Clarendon Press, 1899.</p><p>For more Sanskrit dicitonaries please visit <a href="http://www.sanskrit-lexicon.uni-koeln.de">Cologne Sanskrit Lexicon</a> website.</p><p>Encoded by Bodhirasa 2024</p>""",
        website="https://www.sanskrit-lexicon.uni-koeln.de",
        source_lang="sa",
        target_lang="en",
    )

    dict_vars = DictVariables(
        css_paths=None,
        js_paths=None,
        gd_path=g.pth.mw_gd_path,
        md_path=g.pth.mw_mdict_path,
        dict_name="mw",
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
    pr.title("exporting mw to GoldenDict, MDict")
    g = GlobalVars()
    load_mw_from_json(g)
    if g.mw_data:
        make_dict_data(g)
        save_goldendict_and_mdict(g)
    else:
        pr.red("No data to export")
    pr.toc()


if __name__ == "__main__":
    main()

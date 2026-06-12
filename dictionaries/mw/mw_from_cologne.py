"""Export MW from Cologne SQLite source to GoldenDict and MDict."""

import json

from vendor.dpd_tools.goldendict_exporter import DictEntry, DictInfo, DictVariables
from vendor.dpd_tools.goldendict_exporter import export_to_goldendict_with_pyglossary
from vendor.dpd_tools.mdict_exporter import export_to_mdict
from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr

from dictionaries.mw.mw_helpers import (
    build_mw_entries,
    download_fresh_source,
    load_mw_data,
)


def build_mw_json(pth: RepoPaths) -> list[DictEntry]:
    """Fetch fresh Cologne source data and write source/mw.json.

    Returns the built entries so main() can reuse them for the
    GoldenDict/MDict exports.
    """
    pr.green_title("downloading fresh source data")
    download_fresh_source(zip_path=pth.mw_zip_path, source_dir=pth.mw_zip_path.parent)

    pr.green_title("loading sqlite databases")
    data = load_mw_data(pth.mw_source_dir)

    dict_data = build_mw_entries(data)

    pr.green_title("saving mw.json for mobile export")
    json_data = [
        {
            "word": e.word,
            "definition_html": e.definition_html,
            "definition_plain": e.definition_plain,
            "synonyms": e.synonyms,
        }
        for e in dict_data
    ]
    with open(pth.mw_json_path, "w") as f:
        json.dump(json_data, f, ensure_ascii=False)
    pr.green(f"saved {len(json_data)} entries")
    pr.yes("ok")

    return dict_data


def main() -> None:
    pr.tic()
    pr.title("exporting mw (cologne source) to GoldenDict, MDict")

    pth = RepoPaths()

    dict_data = build_mw_json(pth)

    dict_info = DictInfo(
        bookname="Monier-Williams Sanskrit-English Dictionary, 1899",
        author="Sir Monier Monier-Williams",
        description=(
            "<h3>Monier-Williams Sanskrit-English Dictionary 1899</h3>"
            "<p>Built from the Cologne Sanskrit Lexicon raw source data.</p>"
            "<p>Encoded by Bodhirasa 2024</p>"
        ),
        website="https://www.sanskrit-lexicon.uni-koeln.de",
        source_lang="sa",
        target_lang="en",
    )

    dict_vars = DictVariables(
        css_paths=[pth.mw_css_path],
        js_paths=None,
        gd_path=pth.mw_gd_path,
        md_path=pth.mw_mdict_path,
        dict_name="mw",
        icon_path=None,
        zip_up=True,
        delete_original=True,
    )

    export_to_goldendict_with_pyglossary(dict_info, dict_vars, dict_data)
    export_to_mdict(dict_info, dict_vars, dict_data)

    pr.toc()


if __name__ == "__main__":
    main()

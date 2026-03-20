"""Export Apte from Cologne SQLite source to GoldenDict and MDict."""

import json

from vendor.dpd_tools.goldendict_exporter import DictInfo, DictVariables
from vendor.dpd_tools.goldendict_exporter import export_to_goldendict_with_pyglossary
from vendor.dpd_tools.mdict_exporter import export_to_mdict
from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr

from dictionaries.apte.apte_helpers import (
    build_apte_entries,
    download_fresh_source,
    load_apte_data,
)


def main() -> None:
    pr.tic()
    pr.title("exporting apte (cologne source) to GoldenDict, MDict")

    pth = RepoPaths()

    pr.green_title("downloading fresh source data")
    download_fresh_source(
        zip_path=pth.apte_zip_path, source_dir=pth.apte_zip_path.parent
    )

    pr.green_title("loading sqlite databases")
    data = load_apte_data(pth.apte_source_dir)

    dict_data = build_apte_entries(data)

    dict_info = DictInfo(
        bookname="Apte Practical Sanskrit-English Dictionary, 1890",
        author="Vaman Shivram Apte",
        description=(
            "<h3>Apte Practical Sanskrit-English Dictionary 1890</h3>"
            "<p>Built from the Cologne Sanskrit Lexicon raw source data.</p>"
            "<p>Encoded by Bodhirasa 2026</p>"
        ),
        website="https://www.sanskrit-lexicon.uni-koeln.de",
        source_lang="sa",
        target_lang="en",
    )

    dict_vars = DictVariables(
        css_paths=[pth.apte_css_path],
        js_paths=None,
        gd_path=pth.apte_gd_path,
        md_path=pth.apte_mdict_path,
        dict_name="apte",
        icon_path=None,
        zip_up=True,
        delete_original=True,
    )

    pr.green_title("saving apte.json")
    json_data = [
        {
            "word": e.word,
            "definition_html": e.definition_html,
            "definition_plain": e.definition_plain,
            "synonyms": e.synonyms,
        }
        for e in dict_data
    ]
    with open(pth.apte_json_path, "w") as f:
        json.dump(json_data, f, ensure_ascii=False)
    pr.green(f"saved {len(json_data)} entries")
    pr.yes("ok")

    export_to_goldendict_with_pyglossary(dict_info, dict_vars, dict_data)
    export_to_mdict(dict_info, dict_vars, dict_data)

    pr.toc()


if __name__ == "__main__":
    main()

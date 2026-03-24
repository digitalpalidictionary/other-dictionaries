"""Export Critical Pāḷi Dictionary from SQLite into GoldenDict and MDict formats."""

import re
import sqlite3

from vendor.dpd_tools.goldendict_exporter import DictEntry, DictInfo, DictVariables
from vendor.dpd_tools.goldendict_exporter import export_to_goldendict_with_pyglossary
from vendor.dpd_tools.mdict_exporter import export_to_mdict
from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr


def make_niggahita_synonyms(headword: str) -> list[str]:
    """Generate ṃ and ŋ variants for CPD headwords that use ṁ."""
    if "ṁ" not in headword:
        return []
    synonyms: set[str] = set()
    synonyms.add(headword.replace("ṁ", "ṃ"))
    synonyms.add(headword.replace("ṁ", "ŋ"))
    return list(synonyms)


def main() -> None:
    pr.tic()
    pr.title("exporting CPD for GoldenDict and MDict")

    pth = RepoPaths()

    pr.green("loading cpd_clean.db")
    conn = sqlite3.connect(pth.cpd_source_path)
    rows = conn.execute(
        "SELECT headword, html FROM entries ORDER BY id"
    ).fetchall()
    conn.close()
    pr.yes(str(len(rows)))

    pr.green("making dict entries")
    dict_data: list[DictEntry] = []
    for headword, html in rows:
        html = re.sub(r"<img[^>]*>", "", html)
        synonyms = make_niggahita_synonyms(headword)
        html = (
            "<!DOCTYPE html>"
            "<html lang='en'>"
            "<head>"
            "<meta charset='utf-8'>"
            "<link href='cpd.css' rel='stylesheet'>"
            "</head>"
            "<body>"
            f"{html}"
            "</body></html>"
        )
        dict_data.append(
            DictEntry(
                word=headword,
                definition_html=html,
                definition_plain="",
                synonyms=synonyms,
            )
        )
    pr.yes("ok")

    dict_info = DictInfo(
        bookname="Critical Pāli Dictionary",
        author="V. Trenckner et al.",
        description=(
            "<h3>A Critical Pāli Dictionary</h3>"
            "<p>by V. Trenckner, et al. Published by the Royal Danish Academy "
            "of Science and Letters, Copenhagen, 1925–2011.</p>"
            "<p>The dictionary can be found online on the "
            "<a href='https://cpd.uni-koeln.de'>Cologne University</a> "
            "website.</p>"
            "<p>Encoded by Bodhirasa 2024.</p>"
        ),
        website="https://cpd.uni-koeln.de",
        source_lang="pi",
        target_lang="en",
    )

    dict_vars = DictVariables(
        css_paths=[pth.cpd_css_path],
        js_paths=None,
        gd_path=pth.cpd_gd_path,
        md_path=pth.cpd_mdict_path,
        dict_name="cpd",
        icon_path=None,
        zip_up=True,
        delete_original=True,
    )

    export_to_goldendict_with_pyglossary(dict_info, dict_vars, dict_data)
    export_to_mdict(dict_info, dict_vars, dict_data)

    pr.toc()


if __name__ == "__main__":
    main()

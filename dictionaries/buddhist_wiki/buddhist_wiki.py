# -*- coding: utf-8 -*-
"""Export the Buddhist Wiki (text from English Wikipedia)
to GoldenDict and MDict."""

from datetime import date

from dictionaries.buddhist_wiki.entry_builder import (
    ABOUT_WORD,
    BOOKNAME,
    LICENSE,
    LICENSE_URL,
    build_store_entries,
)
from vendor.dpd_tools.goldendict_exporter import (
    DictEntry,
    DictInfo,
    DictVariables,
    export_to_goldendict_with_pyglossary,
)
from vendor.dpd_tools.mdict_exporter import export_to_mdict
from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr

WEBSITE = "https://en.wikipedia.org/wiki/Category:Buddhism"


def make_description() -> str:
    return (
        f"A reading selection of articles on Buddhism, with text adapted from "
        f"English Wikipedia ({WEBSITE}) and licensed under {LICENSE} "
        f"({LICENSE_URL}). Built {date.today().isoformat()}. "
        f"See the '{ABOUT_WORD}' entry for terms."
    )


def scheme_substitute(html: str, scheme: str) -> str:
    """Replace neutral wiki:// anchors with the target dictionary's scheme."""
    return html.replace("wiki://", scheme)


def to_dict_entries(store_entries: list[dict], scheme: str) -> list[DictEntry]:
    """Convert builder dicts to vendor DictEntry with the link scheme applied."""
    dict_entries: list[DictEntry] = []
    for entry in store_entries:
        dict_entries.append(
            DictEntry(
                word=entry["word"],
                definition_html=scheme_substitute(entry["definition_html"], scheme),
                definition_plain="",
                synonyms=entry["synonyms"],
            )
        )
    return dict_entries


def make_dict_info() -> DictInfo:
    return DictInfo(
        bookname=BOOKNAME,
        author="English Wikipedia contributors",
        description=make_description(),
        website=WEBSITE,
        source_lang="en",
        target_lang="en",
    )


def make_dict_vars(pth: RepoPaths) -> DictVariables:
    return DictVariables(
        css_paths=[pth.buddhist_wiki_css_path],
        js_paths=None,
        gd_path=pth.buddhist_wiki_gd_path,
        md_path=pth.buddhist_wiki_mdict_path,
        dict_name="buddhist-wiki",
        icon_path=None,
        zip_up=True,
        delete_original=True,
    )


def main() -> None:
    """Export the Buddhist Wiki to GoldenDict and MDict."""
    pr.tic()
    pr.title(f"exporting {BOOKNAME}")

    pth = RepoPaths()
    store_entries = build_store_entries(pth)
    dict_info = make_dict_info()
    dict_vars = make_dict_vars(pth)

    pr.yes(len(store_entries))

    pr.green("exporting GoldenDict")
    export_to_goldendict_with_pyglossary(
        dict_info,
        dict_vars,
        to_dict_entries(store_entries, "bword://"),
    )

    pr.green("exporting MDict")
    export_to_mdict(
        dict_info,
        dict_vars,
        to_dict_entries(store_entries, "Entry://"),
    )

    pr.toc()


if __name__ == "__main__":
    main()

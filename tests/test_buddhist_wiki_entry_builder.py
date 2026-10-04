# -*- coding: utf-8 -*-
"""Tests for the Buddhist Wiki entry builder (dictionaries/buddhist_wiki)."""

import re
from pathlib import Path

import pytest

from dictionaries.buddhist_wiki.entry_builder import (
    BOOKNAME,
    about_entry_html,
    attribution_footer,
    build_entries,
    clean_punctuation,
    convert_links,
    normalize_title,
    paragraphs_to_html,
    remove_blocks,
    wikitext_to_html,
)

REDIRECTS = {
    "Kamma": "Karma in Buddhism",
    "Paticcasamuppada": "Pratītyasamutpāda",
}

FIXTURE_WIKITEXT = """
'''Karma''' ({{langx|sa|कर्म}}) is a concept in [[Buddhism]]. The Pali term is
[[Kamma|kamma]], a redirect whose target is [[Kamma]]. Romanized as
{{transl|sa|ISO|karman}}.

== Origin ==
The idea is related to [[Paticcasamuppada|dependent origination]].<ref>a
citation that must vanish</ref>{{sfn|Smith|2001|p=3}} See [[Sanskrit grammar]]
for morphology.

{| class="wikitable"
! Col A
|-
| cell
|}

[[File:an image.jpg|thumb|a caption]]
[[Category:Buddhist concepts]]

See [https://example.com this external link] for more.

{{citation needed}}
"""


def test_normalize_title_resolves_redirect() -> None:
    assert normalize_title("Kamma", REDIRECTS) == "Karma in Buddhism"


def test_normalize_title_strips_section_anchor() -> None:
    assert normalize_title("Buddhism#Ethics", REDIRECTS) == "Buddhism"


def test_remove_blocks_strips_refs_and_metadata_templates() -> None:
    cleaned = remove_blocks(FIXTURE_WIKITEXT)
    assert "<ref" not in cleaned
    assert "citation that must vanish" not in cleaned
    assert "{{" not in cleaned
    assert "Smith" not in cleaned
    assert "citation needed" not in cleaned
    assert 'class="wikitable"' not in cleaned
    assert "Col A" not in cleaned


def test_remove_blocks_strips_parser_functions_and_reference_tags() -> None:
    # snippets copied from the Anattā, Arwal district, Battle of Canhe Slope
    # and Boshin War articles
    text = (
        "Text.\n{{DEFAULTSORT:Anatta}}\n"
        "{{#section:18th Bihar Assembly|MLA Header}}\n"
        "<references/>\n"
        "<imagemap id=Victuallers>\nImage:French Military Advisors Jules Brunet"
        " and Japanese Allies Boshin War 1868-1869.png|thumb|225px|The Japanese"
        "\n</imagemap>\nEnd."
    )
    cleaned = remove_blocks(text)
    assert "DEFAULTSORT" not in cleaned
    assert "#section" not in cleaned
    assert "references" not in cleaned
    assert "thumb|" not in cleaned
    assert cleaned.split() == ["Text.", "End."]


def test_about_entry_has_no_raw_wiki_bold() -> None:
    html = about_entry_html()
    assert "'''" not in html
    assert "<b>Buddhist Wiki</b>" in html
    assert "https://creativecommons.org/licenses/by-sa/4.0/" in html
    # trademark policy: no "Wikipedia" in the product name
    assert "Wikipedia" not in BOOKNAME


def test_remove_blocks_keeps_content_template_text() -> None:
    cleaned = remove_blocks(FIXTURE_WIKITEXT)
    # langx and transl keep the foreign text / romanization
    assert "कर्म" in cleaned
    assert "karman" in cleaned
    assert "langx" not in cleaned
    assert "transl" not in cleaned


def test_convert_links_piped_link() -> None:
    html = convert_links("[[Kamma|kamma]]", REDIRECTS)
    assert html == '<a class="wl" href="wiki://Karma in Buddhism">kamma</a>'


def test_convert_links_unpiped_link() -> None:
    html = convert_links("[[Buddhism]]", REDIRECTS)
    assert html == '<a class="wl" href="wiki://Buddhism">Buddhism</a>'


def test_convert_links_redirect_target_normalized() -> None:
    html = convert_links("[[Kamma]]", REDIRECTS)
    assert 'href="wiki://Karma in Buddhism"' in html


def test_convert_links_drops_file_and_category() -> None:
    html = convert_links("[[File:x.jpg|thumb]] [[Category:Test]]", REDIRECTS)
    assert html.strip() == ""


def test_convert_links_in_dictionary_vs_not() -> None:
    text = "[[Buddhism]] and [[Sanskrit grammar]]"
    html = convert_links(text, REDIRECTS, store_titles={"Buddhism"})
    assert 'href="wiki://Buddhism"' in html
    # out-of-dictionary target: plain text, no anchor
    assert "wiki://Sanskrit grammar" not in html
    assert "Sanskrit grammar" in html


def test_convert_links_in_dictionary_via_redirect() -> None:
    html = convert_links("[[Kamma]]", REDIRECTS, store_titles={"Karma in Buddhism"})
    assert 'href="wiki://Karma in Buddhism"' in html


def test_normalize_title_capitalises_first_letter_and_underscores() -> None:
    assert normalize_title("parinibbana", {}) == "Parinibbana"
    assert normalize_title("Four_Noble__Truths", {}) == "Four Noble Truths"
    assert normalize_title("kamma", REDIRECTS) == "Karma in Buddhism"


def test_convert_links_lowercase_link_is_live_and_keeps_its_text() -> None:
    html = convert_links(
        "the [[parinibbana]] of the [[kamma]]",
        REDIRECTS,
        store_titles={"Parinibbana", "Karma in Buddhism"},
    )
    assert html == (
        'the <a class="wl" href="wiki://Parinibbana">parinibbana</a> of the '
        '<a class="wl" href="wiki://Karma in Buddhism">kamma</a>'
    )


def test_clean_punctuation_removes_empty_parens_and_doubled_commas() -> None:
    assert clean_punctuation("Karma (, from , ; ) is ancient") == "Karma is ancient"
    assert clean_punctuation("Karma ( ) is") == "Karma is"
    assert clean_punctuation("a , , b") == "a, b"


def test_clean_punctuation_keeps_real_parens() -> None:
    assert "(कर्म, karman)" in clean_punctuation("Karma (कर्म, karman) is")


def test_convert_links_drops_external_link_keeps_label() -> None:
    html = convert_links("[https://example.com this label]", REDIRECTS)
    assert "https://example.com" not in html
    assert "this label" in html


def test_wikitext_to_html_full_fixture() -> None:
    html = wikitext_to_html(FIXTURE_WIKITEXT, REDIRECTS)
    # link converted
    assert '<a class="wl" href="wiki://Buddhism">' in html
    # debris gone
    assert "<ref" not in html
    assert "wikitable" not in html
    assert "[[" not in html
    assert "}}" not in html
    assert "http" not in html
    assert "File:" not in html
    assert "Category:" not in html
    # heading converted
    assert "<h2>Origin</h2>" in html
    # bold lead
    assert "<b>Karma</b>" in html
    # paragraphs wrapped
    assert "<p>" in html


def test_paragraphs_drop_cut_sections() -> None:
    html = paragraphs_to_html(
        "Lead text.\n\n== See also ==\n[[Something]]\n\n== Origin ==\nBody."
    )
    assert "Something" not in html
    assert "<h2>Origin</h2>" in html
    assert "Body." in html


def test_attribution_footer_carries_license_and_link() -> None:
    footer = attribution_footer("Karma in Buddhism")
    assert "CC BY-SA 4.0" in footer
    assert 'href="https://creativecommons.org/licenses/by-sa/4.0/"' in footer
    assert "https://en.wikipedia.org/wiki/Karma_in_Buddhism" in footer


def test_attribution_footer_escapes_quotes_and_encodes_url() -> None:
    # real titles from the build
    footer = attribution_footer('Marvin "Bugalu" Smith')
    assert 'href="https://en.wikipedia.org/wiki/Marvin_%22Bugalu%22_Smith"' in footer
    assert ">Marvin &quot;Bugalu&quot; Smith</a>" in footer
    assert "Who_Were_the_Shudras%3F" in attribution_footer("Who Were the Shudras?")


def test_convert_links_escapes_quotes_in_href() -> None:
    html = convert_links('[[Marvin "Bugalu" Smith]]', {})
    assert 'href="wiki://Marvin &quot;Bugalu&quot; Smith"' in html


@pytest.mark.parametrize(
    ("wikitext", "expected"),
    [
        # snippets copied from articles in the store
        ("It lies {{convert|150|km}} north.", "It lies 150 km north."),
        ("{{convert|12|and|15|m|abbr=on|-1}}", "12 and 15 m"),
        ("{{nihongo|[[Enni|Enni-bennen]]|圓爾辨圓}}", "Enni-bennen"),
        ("{{birth date|602|4|6|df=y}}", "6 April 602"),
        ("{{Start date and age|2005}}", "2005"),
        ("Text.{{sfnp|Anālayo|2003|p=125}} More.", "Text. More."),
        ("Fact.{{rp|87–88}}", "Fact."),
        ("He{{in lang|en|mn}}", "He"),
        (
            "{{plainlist|\n* Jingtu Monastery\n* [[Nalanda]]\n}}",
            "Jingtu Monastery, Nalanda",
        ),
        ("{{blockquote|text=The quote.|author=X}}", "The quote."),
        ("{{lang|pi-Latn|Ānāpānasati}}", "Ānāpānasati"),
        ("{{IMDb title|0078428}}", ""),
    ],
)
def test_templates_collapse_to_their_display_text(wikitext: str, expected: str) -> None:
    html = wikitext_to_html(wikitext, {})
    text = re.sub(r"<[^>]+>", "", html)
    assert text == expected


def test_empty_list_items_and_empty_sections_are_dropped() -> None:
    html = paragraphs_to_html(
        remove_blocks(
            "Lead.\n\n== Published books ==\n* {{cite book|title=x}}\n\n"
            "== Life ==\n=== Youth ===\nBody."
        )
    )
    assert "<li></li>" not in html
    assert "Published books" not in html
    # a heading followed by a deeper sub-heading with content stays
    assert "<h2>Life</h2>" in html
    assert "<h3>Youth</h3>" in html


def test_self_closing_nowiki_is_removed() -> None:
    assert "nowiki" not in wikitext_to_html("Ka<nowiki/>rma and <nowiki />x", {})


@pytest.fixture()
def store_files(tmp_path: Path) -> tuple[Path, Path]:
    jsonl = tmp_path / "wikitext.jsonl"
    jsonl.write_text(
        '{"title": "Karma in Buddhism", "wikitext": "Lead about karma."}\n'
        '{"title": "Buddhism", "wikitext": "Lead about Buddhism."}\n',
        encoding="utf-8",
    )
    redirects = tmp_path / "redirects.json"
    redirects.write_text(
        '{"Kamma": "Karma in Buddhism", "Paticcasamuppada": "Pratītyasamutpāda"}',
        encoding="utf-8",
    )
    return jsonl, redirects


def test_build_entries_redirects_become_synonyms(
    store_files: tuple[Path, Path],
) -> None:
    jsonl, redirects = store_files
    entries = build_entries(jsonl, redirects)

    words = [e["word"] for e in entries]
    # About entry first, then alphabetical articles
    assert words[0] == "About Buddhist Wiki"
    assert words[1] == "Buddhism"
    assert words[2] == "Karma in Buddhism"

    karma = entries[2]
    assert karma["synonyms"] == ["Kamma"]
    # redirect whose target is not in the store is not a synonym anywhere
    assert all("Paticcasamuppada" not in e["synonyms"] for e in entries)

    # every article entry carries the attribution footer
    assert all("CC BY-SA 4.0" in e["definition_html"] for e in entries[1:])

    # About entry explains license and links
    about = entries[0]["definition_html"]
    assert "CC BY-SA 4.0" in about

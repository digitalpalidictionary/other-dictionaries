# -*- coding: utf-8 -*-
"""Build dictionary entries from fetched Wikipedia wikitext.

Converts wikitext to clean prose HTML with internal links as neutral
``wiki://`` anchors (the export step substitutes ``bword://`` or
``Entry://``), strips images, files, refs, templates, tables, external
links and categories, and assembles a list of entries with redirects as
synonyms plus an "About" attribution entry.
"""

import html
import json
import re
import urllib.parse
from pathlib import Path
from typing import Any

import wikitextparser as wtp

from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr

# the Wikimedia trademark policy bars "Wikipedia" in a product name without
# permission; saying the text comes from Wikipedia is allowed
BOOKNAME = "Buddhist Wiki"
ABOUT_WORD = f"About {BOOKNAME}"
LICENSE = "CC BY-SA 4.0"
LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"
WIKI_URL = "https://en.wikipedia.org/wiki/"

# sections whose entire content is dropped
CUT_SECTIONS = {
    "see also",
    "references",
    "external links",
    "notes",
    "citations",
    "footnotes",
    "bibliography",
    "further reading",
    "sources",
    "works cited",
}

# wiki namespaces whose links are dropped entirely
SKIP_NAMESPACES = {
    "file",
    "image",
    "category",
    "wikipedia",
    "help",
    "template",
    "portal",
    "special",
    "mediawiki",
    "mos",
    "draft",
    "user",
    "talk",
    "wikipedia talk",
    "category talk",
    "file talk",
    "template talk",
}

# templates that carry no reading content: citations, metadata, hatnotes,
# maintenance tags, page furniture. Removed entirely.
TEMPLATE_JUNK_NAMES = {
    "sfn",
    "sfnmp",
    "harv",
    "harvnb",
    "harvp",
    "cite",
    "citation",
    "refn",
    "efn",
    "notetag",
    "short description",
    "infobox",
    "navbox",
    "sidebar",
    "about",
    "other uses",
    "see also",
    "main",
    "further",
    "redirect",
    "distinguish",
    "for",
    "hatnote",
    "wikt",
    "wiktionary",
    "commonscat",
    "commonscategory",
    "sister project links",
    "coord",
    "use mdy dates",
    "use dmy dates",
    "good article",
    "featured article",
    "multiple issues",
    "toc limit",
    "defaultsort",
    "anchor",
    "citation needed",
    "verify source",
    "dead link",
    "reflist",
    "notelist",
    "clear",
    "wide image",
    "stack",
    "audio",
    "audio-ipa",
    "ipa",
    "pronunciation",
    "respell",
    "r",
}

HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
MAGIC_WORD_RE = re.compile(r"__[A-Z]+__")
HEADING_RE = re.compile(r"^(={2,6})\s*(.+?)\s*\1\s*$")
BOLD_RE = re.compile(r"'''(.+?)'''")
ITALIC_RE = re.compile(r"''(.+?)''")
LIST_ITEM_RE = re.compile(r"^\*+\s*(.*)$")
# punctuation orphaned by stripped templates: doubled commas/semicolons,
# space before punctuation, parentheticals left holding only punctuation
# and connector words
PAREN_RE = re.compile(r"\(([^()]*)\)")
PAREN_LEADING_PUNCT_RE = re.compile(r"\(\s*[,;:]+\s*")
PAREN_TRAILING_PUNCT_RE = re.compile(r"\s*[,;:]+\s*\)")
DOUBLE_PUNCT_RE = re.compile(r"[,;]\s*[,;]")
SPACE_BEFORE_PUNCT_RE = re.compile(r"\s+([,;.])")
PAREN_FILLER_WORDS = {"from", "and", "or", "of", "in", "also", "see"}


def _spans_of(parsed: Any) -> list[tuple[int, int]]:
    return [s.span for s in parsed]


def _is_skipped_link(target: str) -> bool:
    """True for File:, Category:, interwiki-style links we drop entirely."""
    target = target.lstrip(":").lower()
    for ns in SKIP_NAMESPACES:
        if target.startswith(f"{ns}:"):
            return True
    return False


def normalize_title(title: str, redirects: dict[str, str]) -> str:
    """Strip section anchors and resolve a known redirect to its target."""
    # MediaWiki treats `_` as a space and enwiki capitalises the first
    # letter, so [[parinibbana]] and [[Pari_nibbana]] name real titles
    title = " ".join(title.split("#", 1)[0].replace("_", " ").split())
    title = title[:1].upper() + title[1:]
    return redirects.get(title, title)


MEDIA_FILE_RE = re.compile(
    r"\.(ogg|oga|wav|mp3|flac|jpg|jpeg|png|gif|webm|pdf|svg|ogv|tif|tiff)$",
    re.IGNORECASE,
)


# templates whose display text is their FIRST positional parameter
# (e.g. {{nihongo|Enni-bennen|圓爾辨圓}} shows "Enni-bennen")
TEMPLATE_FIRST_PARAM = {
    "nihongo",
    "nihongo2",
    "nihongo3",
    "small",
    "smaller",
    "big",
    "nobold",
    "nowrap",
    "nobr",
    "center",
    "flag",
    "flagcountry",
    "circa",
    "c.",
    "dts",
    "tooltip",
    "abbr",
    "ill",
    "interlanguage link",
    "interlanguage link multi",
    "ruby",
    "sic",
    "lit",
    "gloss",
    "quote",
    "blockquote",
    "quotation",
    "poem quote",
    "marriage",
    "korean",
}
# list templates: show every item
TEMPLATE_JOIN_PARAMS = {"ubl", "unbulleted list", "hlist", "flatlist", "plainlist"}
# date templates: positional year|month|day → "6 April 602"
TEMPLATE_DATES = {
    "birth date",
    "death date",
    "birth date and age",
    "death date and age",
    "start date",
    "end date",
    "start date and age",
    "birth year and age",
    "death year and age",
    "film date",
}
TEMPLATE_CONVERT = {"convert", "cvt"}
# prefixes of citation/footnote/furniture templates that carry no prose
TEMPLATE_JUNK_PREFIXES = (
    "#",
    "=",
    "ipa",
    "cite ",
    "sfn",
    "harv",
    "rp",
    "in lang",
    "party ",
    "flagicon",
    "family name",
    "commons",
    "portal",
    "tree chart",
    "composition bar",
    "percentage bar",
    "isbn",
    "issn",
    "oclc",
    "doi",
    "url",
    "official website",
    "box",
    "colombo stock exchange",
    "imdb",
    "color box",
    "location map",
    "coord",
    "contains special characters",
    "s-",
    "medal",
    "refbegin",
    "refend",
    "flagdeco",
)
MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
CONVERT_RANGE_WORDS = {"to", "and", "or", "-", "–", "and(-)", "to(-)", "x", "by"}


def _format_date(positional: list[str]) -> str:
    year, month, day = (positional + ["", "", ""])[:3]
    if not year.lstrip("-").isdigit():
        return year
    if month.isdigit() and 1 <= int(month) <= 12:
        month_name = MONTHS[int(month) - 1]
        return (
            f"{int(day)} {month_name} {year}"
            if day.isdigit()
            else f"{month_name} {year}"
        )
    return year


def _format_convert(positional: list[str]) -> str:
    # {{convert|150|km}} → "150 km"; {{convert|12|and|15|m}} → "12 and 15 m"
    if len(positional) >= 4 and positional[1] in CONVERT_RANGE_WORDS:
        return " ".join(positional[:4])
    return " ".join(positional[:2])


def _template_replacement(template: Any) -> str:
    """Decide what a template collapses to: nothing for metadata/citation
    templates, a rebuilt value for dates/units/lists, the first parameter
    for display wrappers, and otherwise the last positional parameter
    (e.g. {{langx|sa|कर्म}} -> कर्म)."""
    name = template.name.strip().lower()
    if name in TEMPLATE_JUNK_NAMES or name.startswith(TEMPLATE_JUNK_PREFIXES):
        return ""
    positional = [
        a.value.strip() for a in template.arguments if a.positional and a.value.strip()
    ]
    if name in TEMPLATE_DATES:
        return _format_date(positional)
    if name in TEMPLATE_CONVERT:
        return _format_convert(positional)
    if name in TEMPLATE_JOIN_PARAMS:
        items = [ln.lstrip("*# ").strip() for p in positional for ln in p.splitlines()]
        return ", ".join(i for i in items if i)
    if name in TEMPLATE_FIRST_PARAM:
        named_text = template.get_arg("text")
        if named_text is not None and named_text.value.strip():
            return named_text.value.strip()
        return positional[0] if positional else ""
    # last positional param: the content word in lang/transl-style
    # templates; empty for named-param-only templates like citations
    if not positional:
        return ""
    value = positional[-1]
    # audio/pronunciation templates leave media filenames behind
    if MEDIA_FILE_RE.search(value):
        return ""
    return value


def _remove_blocks_pass(text: str) -> str:
    """One pass: remove comments/tables/refs/galleries and collapse
    templates. Templates inside template parameter values survive until
    the next pass (remove_blocks iterates until stable)."""
    parsed = wtp.parse(text)

    replacements: list[tuple[int, int, str]] = []
    for span in (
        _spans_of(parsed.comments)
        + _spans_of(parsed.tables)
        + _spans_of(parsed.get_tags("ref"))
        + _spans_of(parsed.get_tags("references"))
        + _spans_of(parsed.get_tags("gallery"))
        + _spans_of(parsed.get_tags("imagemap"))
        # {{DEFAULTSORT:…}}, {{#section:…}} etc. are parser functions to
        # wikitextparser, not templates, so `templates` never sees them
        + _spans_of(parsed.parser_functions)
    ):
        replacements.append((*span, ""))
    for template in parsed.templates:
        replacements.append((*template.span, _template_replacement(template)))
    return _apply_replacements(text, replacements)


def remove_blocks(text: str) -> str:
    """Remove comments, refs, tables and galleries; collapse templates.
    Iterates until stable so nested templates resolve too."""
    text = HTML_COMMENT_RE.sub("", text)
    for _ in range(6):
        cleaned = _remove_blocks_pass(text)
        if cleaned == text:
            break
        text = cleaned
    return text


def _paren_is_debris(content: str) -> bool:
    """True when a parenthetical holds only punctuation and connector
    words — debris left behind by stripped templates."""
    words = re.findall(r"[^\s,;:.]+", content)
    return all(w.lower() in PAREN_FILLER_WORDS for w in words)


def clean_punctuation(text: str) -> str:
    """Remove punctuation orphaned by stripped templates.

    E.g. "Karma (, from , ; ) is" -> "Karma is": templates such as
    {{langx|sa|...}} vanish, leaving debris parentheticals and doubled
    commas/semicolons behind.
    """
    for _ in range(5):
        before = text
        text = PAREN_RE.sub(
            lambda m: "" if _paren_is_debris(m.group(1)) else m.group(0), text
        )
        text = PAREN_LEADING_PUNCT_RE.sub("(", text)
        text = PAREN_TRAILING_PUNCT_RE.sub(")", text)
        text = DOUBLE_PUNCT_RE.sub(",", text)
        text = SPACE_BEFORE_PUNCT_RE.sub(r"\1", text)
        if text == before:
            break
    return re.sub(r"  +", " ", text)


def convert_links(
    text: str,
    redirects: dict[str, str],
    store_titles: set[str] | None = None,
) -> str:
    """Replace wikilinks with wiki:// anchors; drop namespace links.

    If ``store_titles`` is given, only links whose redirect-resolved
    target is in the store become anchors — everything else is rendered
    as plain label text.
    """
    parsed = wtp.parse(text)

    replacements: list[tuple[int, int, str]] = []
    for link in parsed.wikilinks:
        target = link.target.strip()
        if not target or _is_skipped_link(target):
            replacements.append((*link.span, ""))
            continue
        # an unpiped link displays its target exactly as written, as on Wikipedia
        label = (link.text or "").strip() or target
        canonical = normalize_title(target, redirects)
        if store_titles is not None and canonical not in store_titles:
            replacements.append((*link.span, label))
            continue
        replacements.append(
            (
                *link.span,
                f'<a class="wl" href="wiki://{html.escape(canonical)}">{label}</a>',
            )
        )

    # standalone external links: keep the label text, drop the URL
    for ext in parsed.external_links:
        label = (ext.text or "").strip()
        replacements.append((*ext.span, label))

    return _apply_replacements(text, replacements)


def _apply_replacements(text: str, replacements: list[tuple[int, int, str]]) -> str:
    kept: list[tuple[int, int, str]] = []
    for span in replacements:
        nested = any(
            other[:2] != span[:2] and other[0] <= span[0] and span[1] <= other[1]
            for other in replacements
        )
        if not nested:
            kept.append(span)
    for start, end, repl in sorted(kept, key=lambda r: r[0], reverse=True):
        text = text[:start] + repl + text[end:]
    return text


def _convert_heading(match: re.Match[str]) -> str:
    level = len(match.group(1))
    title = match.group(2)
    # == x == is the article's h2 (the title itself is h1)
    tag = f"h{min(level, 6)}"
    return f"<{tag}>{title}</{tag}>"


def _drop_cut_sections(lines: list[str]) -> list[str]:
    """Drop everything from a cut-section heading to its next heading."""
    out: list[str] = []
    skipping = False
    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            title = match.group(2).strip().lower()
            skipping = title in CUT_SECTIONS
            if skipping:
                continue
        if not skipping:
            out.append(line)
    return out


def paragraphs_to_html(text: str) -> str:
    """Turn cleaned wikitext into simple HTML: p, h2/h3, ul blocks."""
    lines = _drop_cut_sections(text.splitlines())

    html_parts: list[str] = []
    block: list[str] = []

    def flush() -> None:
        if not block:
            return
        content = "\n".join(block).strip()
        block.clear()
        if not content:
            return
        list_items = [LIST_ITEM_RE.match(ln) for ln in content.splitlines()]
        if all(list_items) and any(list_items):
            # an item that held only a stripped template is left empty
            items = "".join(
                f"<li>{m.group(1).strip()}</li>"
                for m in list_items
                if m and m.group(1).strip()
            )
            if items:
                html_parts.append(f"<ul>{items}</ul>")
            return
        if "<br>" not in content:
            content = content.replace("\n", " ")
        html_parts.append(f"<p>{content}</p>")

    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            flush()
            html_parts.append(_convert_heading(match))
        elif line.strip():
            block.append(line)
        else:
            flush()
    flush()

    return "\n".join(_drop_empty_headings(html_parts))


def _heading_level(part: str) -> int | None:
    match = re.match(r"<h(\d)>", part)
    return int(match.group(1)) if match else None


def _drop_empty_headings(parts: list[str]) -> list[str]:
    """Drop a heading whose section kept no content: it is followed by a
    heading of the same or a higher level, or by the end of the entry."""
    kept: list[str] = []
    for part in reversed(parts):
        level = _heading_level(part)
        if level is not None:
            next_level = _heading_level(kept[-1]) if kept else 0
            if next_level is not None and next_level <= level:
                continue
        kept.append(part)
    return kept[::-1]


def wikitext_to_html(
    wikitext: str,
    redirects: dict[str, str],
    store_titles: set[str] | None = None,
) -> str:
    """Full pipeline: raw wikitext -> clean prose HTML with wiki:// links."""
    text = remove_blocks(wikitext)
    text = clean_punctuation(text)
    text = convert_links(text, redirects, store_titles)
    text = MAGIC_WORD_RE.sub("", text)
    text = re.sub(r"</?nowiki\s*/?>", "", text)
    text = BOLD_RE.sub(r"<b>\1</b>", text)
    text = ITALIC_RE.sub(r"<i>\1</i>", text)
    return paragraphs_to_html(text)


def attribution_footer(title: str) -> str:
    """Per-entry CC BY-SA attribution + link back to the online article."""
    url = WIKI_URL + urllib.parse.quote(title.replace(" ", "_"), safe="/:(),'")
    return (
        f'<div class="wp-attribution">Source: '
        f'<a class="external" href="{html.escape(url)}">{html.escape(title)}</a>'
        f" — English Wikipedia, adapted (text only), "
        f'<a class="external" href="{LICENSE_URL}">{LICENSE}</a></div>'
    )


def load_store(
    jsonl_path: Path, redirects_path: Path
) -> tuple[dict[str, str], dict[str, str]]:
    """Load the wikitext store and the redirect map."""
    store: dict[str, str] = {}
    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            store[row["title"]] = row["wikitext"]
    redirects: dict[str, str] = {}
    if redirects_path.exists():
        with open(redirects_path, encoding="utf-8") as f:
            redirects = dict(json.load(f))
    return store, redirects


def about_entry_html() -> str:
    """The About entry: license terms and how links work."""
    return paragraphs_to_html(
        f"""<b>{BOOKNAME}</b> is an offline reading selection of English
Wikipedia articles on Buddhism, built for GoldenDict and MDict.

Colored links inside an article jump to other entries in this
dictionary. Links to articles that are not part of this build are
shown as plain text.

The text of every article is from English Wikipedia, written by its
contributors, and is licensed under the <a class="external"
href="{LICENSE_URL}">{LICENSE}</a> license. Each entry ends with a source
line linking back to the online article and its full list of authors.
Any reuse of this content must credit English Wikipedia and carry the
same {LICENSE} share-alike license. This dictionary is not affiliated
with or endorsed by Wikipedia or the Wikimedia Foundation.

The articles have been changed: images, infoboxes, references and tables
are stripped, templates are reduced to plain text, and only a subset of
the Wikipedia Buddhism category tree is included. It is a reading aid,
not a Wikipedia mirror."""
    )


def build_entries(jsonl_path: Path, redirects_path: Path) -> list[dict[str, Any]]:
    """Build all entries: About first, then one per article, redirects as synonyms."""
    store, redirects = load_store(jsonl_path, redirects_path)
    pr.white(f"{len(store)} articles in store, {len(redirects)} redirects")

    # invert redirects, keeping only redirects whose target was fetched
    synonyms: dict[str, list[str]] = {title: [] for title in store}
    for source, target in sorted(redirects.items()):
        if target in store:
            synonyms[target].append(source)

    entries: list[dict[str, Any]] = [
        {
            "word": ABOUT_WORD,
            "definition_html": about_entry_html(),
            "synonyms": [BOOKNAME],
        }
    ]

    for title in sorted(store, key=str.lower):
        html = wikitext_to_html(store[title], redirects, set(store))
        if not html.strip():
            continue
        html += attribution_footer(title)
        entries.append(
            {
                "word": title,
                "definition_html": html,
                "synonyms": synonyms[title],
            }
        )
    return entries


def build_store_entries(pth: RepoPaths | None = None) -> list[dict[str, Any]]:
    """Convenience wrapper used by buddhist_wiki.py."""
    pth = pth or RepoPaths()
    return build_entries(
        pth.buddhist_wiki_wikitext_path, pth.buddhist_wiki_redirects_path
    )

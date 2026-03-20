"""MW2 renderer — converts Cologne XML markup to HTML.

Phase A: Pre-processing transformations (matching basicadjust.php).
Phase B: Tag-to-HTML conversions (matching basicdisplay.php).
"""

import re
from html import escape

from vendor.dpd_tools.sanskrit_translit import slp1_translit


def strip_slp1_accents(xml: str) -> str:
    """Remove SLP1 accent marks (/ ^ \\) from <s> and <key2> tag content.

    Protects XML slashes by temporarily replacing </ and /> before stripping.
    """

    def _strip_in_tag(match: re.Match) -> str:
        tag = match.group(1)
        content = match.group(2)
        content = content.replace("</", "<_").replace("/>", "_>")
        content = re.sub(r"[/^\\]", "", content)
        content = content.replace("<_", "</").replace("_>", "/>")
        return f"<{tag}>{content}</{tag}>"

    xml = re.sub(r"<(s)>(.*?)</s>", _strip_in_tag, xml)
    xml = re.sub(r"<(key2)>(.*?)</key2>", _strip_in_tag, xml)
    return xml


def normalize_tags(xml: str) -> str:
    """Convert <lang n="X">...</lang> → <ab n="X">...</ab>
    and <s1 n="X">...</s1> → <ab n="X">...</ab>."""
    xml = re.sub(r"<lang\b([^>]*)>(.*?)</lang>", r"<ab\1>\2</ab>", xml)
    xml = re.sub(r"<s1\b([^>]*)>(.*?)</s1>", r"<ab\1>\2</ab>", xml)
    return xml


def inject_abbreviation_tooltips(xml: str, abbreviations: dict[str, str]) -> str:
    """Inject tooltip text into <ab> tags that lack an n attribute."""

    def _ab_callback(match: re.Match) -> str:
        attrs = match.group(1)
        data = match.group(2)
        if 'n="' in attrs or "n='" in attrs:
            return match.group(0)
        tooltip = escape(abbreviations.get(data, ""), quote=True)
        return f"<ab n='{tooltip}'>{data}</ab>"

    return re.sub(r"<ab(.*?)>(.*?)</ab>", _ab_callback, xml)


def inject_literature_tooltips(xml: str, author_tooltips: dict[str, str]) -> str:
    """Inject tooltip text into <ls> tags for MW literature references."""

    xml = re.sub(r"<ls>ib[.]", "<ls><ab>ib.</ab>", xml)

    def _ls_callback(match: re.Match) -> str:
        abbrev = match.group(1)
        rest = match.group(2)
        title = author_tooltips.get(abbrev, "Unknown literary source")
        tooltip = escape(title, quote=True)
        return f"<ls n='{tooltip}'>{abbrev}{rest}</ls>"

    xml = re.sub(
        r"<ls>([A-ZĀĪŚṚṢṬ][A-Za-zÂáâêîñôĀāĪīŚśūûḍḥṃṅṇṉṚṛṢṣṬṭ.]*[.])(.*?)</ls>",
        _ls_callback,
        xml,
    )
    return xml


def inject_lex_tooltips(xml: str, abbreviations: dict[str, str]) -> str:
    """Convert <lex> inner text to <ab> tags, keeping the <lex> wrapper for bold."""

    def _lex_callback(match: re.Match) -> str:
        content = match.group(1)
        parts = re.split(r"(<[^>]+>.*?</[^>]+>|<[^>]+/>)", content)
        result = []
        for part in parts:
            if part.startswith("<"):
                result.append(part)
            else:
                result.append(_abbreviate_text(part, abbreviations))
        return f"<lex>{''.join(result)}</lex>"

    return re.sub(r"<lex[^>]*>(.*?)</lex>", _lex_callback, xml)


def _abbreviate_text(text: str, abbreviations: dict[str, str]) -> str:
    """Convert plain text segments to <ab> tags where abbreviations match."""
    if not text.strip():
        return text

    segments = re.split(r"(\s+)", text)
    result = []
    for seg in segments:
        if not seg.strip():
            result.append(seg)
            continue
        tooltip = abbreviations.get(seg, "")
        if not tooltip:
            cleaned = seg.strip().rstrip(".") + "."
            tooltip = abbreviations.get(cleaned, "")
        if tooltip:
            tooltip = escape(tooltip, quote=True)
            result.append(f"<ab n='{tooltip}'>{seg}</ab>")
        else:
            result.append(seg)
    return "".join(result)


def preprocess_entry(
    xml: str,
    abbreviations: dict[str, str],
    author_tooltips: dict[str, str],
) -> str:
    """Apply all pre-processing transformations to a single MW entry."""
    xml = xml.replace("¦", " ")
    xml = strip_slp1_accents(xml)
    xml = normalize_tags(xml)
    xml = inject_literature_tooltips(xml, author_tooltips)
    xml = inject_abbreviation_tooltips(xml, abbreviations)
    xml = inject_lex_tooltips(xml, abbreviations)
    return xml


# --- Phase B: Tag-to-HTML conversion ---

_STRIP_TAGS = re.compile(
    r"</?(?:info|pb|pcol|to|ns|shortlong|srs|key1|key2|body|tail|head"
    r"|lbinfo|hwtype|vlex|edit|note|symbol|type)\b[^>]*>"
)

_SELF_CLOSING_STRIP = re.compile(r"<(?:info|pb|pcol|lbinfo)\b[^>]*/>")

_H_TYPE_RE = re.compile(r"<(H[1-4][A-Z]?)\b")
_PRIMARY_H_RE = re.compile(r"^H[1-4]$")


def render_xml_to_html(xml: str) -> str:
    """Convert pre-processed XML tags to HTML with CSS classes.

    Zero inline styles — all styling via CSS class names from mw.css.
    """
    h_match = _H_TYPE_RE.search(xml)
    h_type = h_match.group(1) if h_match else ""
    is_primary = bool(_PRIMARY_H_RE.match(h_type))

    pc_match = re.search(r"<pc>(.*?)</pc>", xml)
    pc_value = pc_match.group(1) if pc_match else ""

    l_match = re.search(r"<L>(.*?)</L>", xml)
    l_value = l_match.group(1) if l_match else ""

    xml = re.sub(r"<h>.*?</h>", "", xml, flags=re.DOTALL)

    xml = re.sub(r"</?H[1-4][A-Z]?>", "", xml)
    xml = re.sub(r"<pc>.*?</pc>", "", xml)
    xml = re.sub(r"<L\d?>.*?</L\d?>", "", xml)

    xml = _SELF_CLOSING_STRIP.sub("", xml)
    xml = _STRIP_TAGS.sub("", xml)

    xml = _render_s_tags(xml)
    xml = _render_ab_tags(xml)
    xml = _render_ls_tags(xml)
    xml = _render_hom_tags(xml)
    xml = _render_bot_bio_tags(xml)
    xml = _render_foreign_lang_tags(xml)
    xml = _render_div_tags(xml)
    xml = _render_footnote_tags(xml)
    xml = _render_c_tags(xml)
    xml = _render_misc_tags(xml)

    body = xml.strip()

    _COLOGNE_SCAN_URL = (
        "https://www.sanskrit-lexicon.uni-koeln.de"
        "/scans/csl-apidev/servepdf.php?dict=MW&page="
    )

    parts: list[str] = []
    if is_primary:
        label = f"<strong>({h_type})</strong>"
        if pc_value:
            page_col = pc_value.replace(",", ".")
            page_parts = page_col.split(".", 1)
            page_num = page_parts[0]
            col_num = page_parts[1] if len(page_parts) > 1 else ""
            scan_url = f"{_COLOGNE_SCAN_URL}{page_num}"
            label += (
                f' <span class="pcol-ref">'
                f'[Printed book page <a href="{scan_url}">{page_num}</a>.{col_num}]'
                f"</span>"
            )
        parts.append(label)

    if body:
        id_suffix = ""
        if l_value:
            id_suffix = f' <span class="record-id">[ID={l_value}]</span>'
        parts.append(f"{body}{id_suffix}")

    return "<br/>\n".join(parts)


def _render_s_tags(xml: str) -> str:
    """<s>SLP1</s> → <span class="sdata">IAST</span>."""

    def _s_to_span(match: re.Match) -> str:
        iast = slp1_translit(match.group(1))
        return f'<span class="sdata">{iast}</span>'

    return re.sub(r"<s>(.*?)</s>", _s_to_span, xml)


def _render_ab_tags(xml: str) -> str:
    """<ab n='tooltip'>text</ab> → <span class="dotunder" title="tooltip">text</span>."""

    def _ab_to_span(match: re.Match) -> str:
        attrs = match.group(1)
        text = match.group(2)
        n_match = re.search(r"""n=['"](.*?)['"]""", attrs)
        if n_match:
            tooltip = n_match.group(1)
            return f'<span class="dotunder" title="{tooltip}">{text}</span>'
        return f"<span>{text}</span>"

    return re.sub(r"<ab(.*?)>(.*?)</ab>", _ab_to_span, xml)


def _render_ls_tags(xml: str) -> str:
    """<ls n='tooltip'>text</ls> → <span class="ls" title="tooltip">text</span>."""

    def _ls_to_span(match: re.Match) -> str:
        attrs = match.group(1)
        text = match.group(2)
        n_match = re.search(r"""n=['"](.*?)['"]""", attrs)
        if n_match:
            tooltip = n_match.group(1)
            return f'<span class="ls" title="{tooltip}">{text}</span> '
        return f'<span class="ls">{text}</span> '

    return re.sub(r"<ls(.*?)>(.*?)</ls>", _ls_to_span, xml)


def _render_hom_tags(xml: str) -> str:
    """<hom>N</hom> → <span class="hom" title="Homonym">N</span>."""
    return re.sub(
        r"<hom>(.*?)</hom>",
        r'<span class="hom" title="Homonym">\1</span>',
        xml,
    )


def _render_bot_bio_tags(xml: str) -> str:
    """Render <bot>, <zoo>, <bio> tags. With n attr → brown + dotted underline."""

    def _bot_zoo_callback(match: re.Match) -> str:
        attrs = match.group(1)
        text = match.group(2)
        n_match = re.search(r"""n=['"](.*?)['"]""", attrs)
        if n_match:
            tooltip = n_match.group(1)
            return f'<span class="foreign dotunder" title="{tooltip}">{text}</span>'
        return f'<span class="foreign">{text}</span>'

    xml = re.sub(r"<bot(.*?)>(.*?)</bot>", _bot_zoo_callback, xml)
    xml = re.sub(r"<zoo(.*?)>(.*?)</zoo>", _bot_zoo_callback, xml)
    xml = re.sub(r"<bio>(.*?)</bio>", r'<span class="foreign">\1</span>', xml)
    return xml


def _render_foreign_lang_tags(xml: str) -> str:
    """Render foreign script tags (<gk>, <fr>, etc.) with brown color and tooltips."""
    lang_map = {
        "gk": "Greek script",
        "fr": "French language",
        "ger": "German language",
        "lat": "Latin language",
        "tib": "Tibetan language",
        "toch": "Tocharian language",
        "arab": "Arabic script",
        "rus": "Russian language",
        "mong": "Mongolian language",
    }
    for tag, title in lang_map.items():
        xml = re.sub(
            rf"<{tag}>(.*?)</{tag}>",
            rf'<span class="foreign" title="{title}">\1</span>',
            xml,
        )
    return xml


def _render_div_tags(xml: str) -> str:
    """<div n="X"/> → <div class="div-sep"></div>."""
    xml = re.sub(r"<div\b[^>]*/>", '<div class="div-sep"></div>', xml)
    xml = re.sub(r"<div\b[^>]*>", '<div class="div-sep">', xml)
    xml = re.sub(r"</div>", "</div>", xml)
    return xml


def _render_footnote_tags(xml: str) -> str:
    """<F>text</F> → <br/>[<span class="fn-label">Footnote: </span>text]."""
    xml = re.sub(
        r"<F>(.*?)</F>",
        r'<br/>[<span class="fn-label">Footnote: </span><span>\1</span>]',
        xml,
    )
    return xml


def _render_c_tags(xml: str) -> str:
    """<C n="X">text</C> → <strong>(CX)</strong>text."""

    def _c_to_html(match: re.Match) -> str:
        n = match.group(1)
        text = match.group(2)
        return f"<strong>(C{n})</strong>{text}"

    return re.sub(r'<C n="(\w+)">(.*?)</C>', _c_to_html, xml)


def _render_misc_tags(xml: str) -> str:
    """Handle remaining simple tag conversions."""
    xml = re.sub(r"<b>(.*?)</b>", r"<strong>\1</strong>", xml)
    xml = re.sub(r"<i>(.*?)</i>", r"<em>\1</em>", xml)
    xml = re.sub(r"<etym>(.*?)</etym>", r"<em>\1</em>", xml)
    xml = re.sub(r"<lex[^>]*>(.*?)</lex>", r"<strong>\1</strong>", xml)
    xml = re.sub(r"<br/>", "<br/>", xml)
    xml = re.sub(r"<lb/>", "<br/>", xml)
    xml = re.sub(r"<Poem[^>]*>", "<br/>", xml)
    xml = re.sub(r"</Poem>", "", xml)
    xml = re.sub(r"<lang\b[^>]*>(.*?)</lang>", r"<em>\1</em>", xml)
    xml = re.sub(r"<alt>(.*?)</alt>", r'<span class="alt-hw">(\1)</span>', xml)
    return xml

# -*- coding: utf-8 -*-
"""Convert the BuddhaDust PTS Pāli-English Dictionary page into pts.json.

Reads source/ped.htm (one page holding the whole dictionary) and writes
source/pts.json, a list of {"word", "definition_html"}. All cleaning happens
here so GoldenDict, MDict and the mobile app get the same text.
"""

import json
import re

from vendor.dpd_tools.paths import RepoPaths
from vendor.dpd_tools.printer import printer as pr

REGION_START = 'class="palientry"'
REGION_END = '<h4 class="ctr">Afterword</h4>'

ANCHOR_RE = re.compile(
    r'<p><a (?:id="[^"]*" href="[^"]*" )?class="palientry">(.*?)</a>', re.S
)
# A variant headword inside an entry ("Amha and<br /> Amhan (neuter) ...").
VARIANT_RE = re.compile(r'<a [^>]*class="palientry">(.*?)</a>', re.S)

# BuddhaDust page furniture. None of it is PTS text, and the links and
# images do not work offline.
SIDE_BOX_RE = re.compile(r'<div class="float[lr][^"]*">.*?</div>', re.S)
DIVIDER_RE = re.compile(r'<p>-----<a href="#e_.*?</p>', re.S)
SPACER_RE = re.compile(r"<p>&nbsp;</p>")
PAGE_MARKER_RE = re.compile(
    r'<a id="(?:pg|pre)\d+" href="#(?:pg|pre)\d+"><span class="f2[^"]*"><b>\{\d+\}</b></span></a>'
)
# Two "[Page N]" markers of the pre-2015 editions. In "Taca" the marker is a
# paragraph of its own that splits one sentence, so the paragraphs are joined.
PAGE_LINK = r'<a id="(?:pg|pre)\d+" href="#(?:pg|pre)\d+"><b>\[Page \d+\]</b></a>'
OLD_PAGE_PARA_RE = re.compile(
    r'</p>\s*<p class="f2 g">---\[ ' + PAGE_LINK + r" \]---</p>\s*<p>"
)
OLD_PAGE_INLINE_RE = re.compile(r"\s*---\[ " + PAGE_LINK + r" \] — pre 2015 eds ---")
IMG_RE = re.compile(r"<img [^>]*>")
H4_RE = re.compile(r'<h4 class="ctr">(.*?)</h4>', re.S)
SITE_LINKS_RE = re.compile(
    r'\s*(?:\[<a href="[^"]*">|<a href="[^"]*">\[)(?:SUTTA SEARCH|GLOSSOLOGY)</a>\]'
)

# Notes BuddhaDust added from its own editor (BD) and merged from Childers
# (DPL), CPD and DOP. The user chose PTS text only.
TAG = r"\[(?:BD|bd|DPL|CPD|DOP)\]:?"
BRACKETED_NOTE_RE = re.compile(
    r"\s*\(" + TAG + r"[^()]*(?:\([^()]*\)[^()]*)*\)|\s*\[" + TAG + r"[^\[\]]*\]"
)
PARA_NOTE_RE = re.compile(r'<p(?: class="[^"]*")?>\s*\*?' + TAG + r".*?</p>", re.S)
# Most notes end at the line break. In "Taṇhā" PTS text resumes after " — "
# on the same line.
LINE_NOTE_RE = re.compile(
    r"(?:<br ?/>\s*)?\*?" + TAG + r".*?(?=<br ?/>|</p>|\s—\s)", re.S
)
# These two notes run over several lines to the end of their paragraph
# ("Nahuta" and "Niddasa"). Found by reading every removed note.
LONG_NOTE_RE = re.compile(
    r"(?:<br ?/>\s*)?\[BD\]: (?:One followed by 28 zeros|tenless\.).*?(?=</p>)", re.S
)
# Headwords BuddhaDust added, with no entry in the print edition (checked
# against the Digital Pali Reader copy). Their own text was a merged note, and
# only a fragment such as "and Esa (pronoun)," is left once it is removed.
NOT_IN_PTS = {
    "Amhākaṁ",
    "Avyatta",
    "Bhātā",
    "Eso",
    "Hīyo",
    "Paṭilekhanaṁ",
    "So",
    "Sūpatiṭṭha",
}

FULLNESS_RE = re.compile(r"(\w)fullness")
# BuddhaDust lost "DhsA" (Atthasālinī) and left "as 121". Every "as N" in
# the output was checked against the same entry in the Digital Pali Reader
# copy. These are the English "as", matched on the text that ends with them.
DHSA_RE = re.compile(r"\b[Aa]s (\d+)(?![\w-])")
# Four of them are bold ("at <b>as</b> 124", "<b> As </b>411").
BOLD_DHSA_RE = re.compile(r"<b>\s*[Aa]s\s*</b>\s*(\d+)")
ENGLISH_AS = (
    "viz. As 3",
    "increase, as 1",
    "§479 as 2",
    "Bhagavā), as 18",
    "much as 2",
    "viz. (as 5",
    "III 44; (as 4",
    "(sama°); (as 3",
    "II 112; (as 7",
    "kṣam) as 1",
    "taken as 2",
    "kaṅkhati, as 3",
    "enumerations: as 3",
    "given as 38",
    "240f., as 40",
    "(same as 1",
    "(same as 3",
    "be same as 1",
    "phenomena. As 44",
    "56f., as 77",
    "(explained as 3",
    "(or as 4",
    "(as 68",
    "(α) as 4",
    "vāyāma as 146",
    "much as 3",
)


def _strip_furniture(html: str) -> str:
    html = SIDE_BOX_RE.sub("", html)
    html = html.replace('<div class="inner">', "").replace("</div>", "")
    html = H4_RE.sub(r"<p><b>\1</b></p>", html)
    html = DIVIDER_RE.sub("", html)
    html = SPACER_RE.sub("", html)
    html = PAGE_MARKER_RE.sub("", html)
    html = OLD_PAGE_PARA_RE.sub(" ", html)
    html = OLD_PAGE_INLINE_RE.sub("", html)
    html = IMG_RE.sub("", html)
    html = SITE_LINKS_RE.sub("", html)
    html = re.sub(r"<hr [^>]*>", "", html)
    # "Yena" is the one headword typed as bold italic instead of an anchor.
    html = re.sub(r"<p><b><i>(:: .*?)</i></b>", r'<p><a class="palientry">\1</a>', html)
    return html


def _strip_editor_notes(body: str) -> str:
    body = BRACKETED_NOTE_RE.sub("", body)
    body = PARA_NOTE_RE.sub("", body)
    body = LONG_NOTE_RE.sub("", body)
    body = LINE_NOTE_RE.sub("", body)
    return body


def _restore_dhsa(m: re.Match) -> str:
    before = re.sub(r"<[^>]+>", "", m.string[max(0, m.start() - 120) : m.end()])
    if re.sub(r"\s+", " ", before).endswith(ENGLISH_AS):
        return m.group(0)
    return f"<b>DhsA</b> {m.group(1)}"


def _clean_body(body: str) -> str:
    body = _strip_editor_notes(body)
    body = re.sub(r"</?a\b[^>]*>", "", body)
    body = re.sub(r"</?span\b[^>]*>", "", body)
    body = re.sub(r'<p class="(?!in1")[^"]*">', "<p>", body)
    body = re.sub(r"<p>\s*</p>", "", body)
    body = body.replace("&nbsp;", " ")
    body = FULLNESS_RE.sub(r"\1fulness", body)
    body = BOLD_DHSA_RE.sub(r"<b>DhsA</b> \1", body)
    body = DHSA_RE.sub(_restore_dhsa, body)
    # One "<i>PG</I>" in "Takka".
    body = body.replace("</I>", "</i>")
    body = body.replace("ṁ", "ṃ")
    body = re.sub(r"\s+", " ", body).strip()
    # The headword is shown as the card title, so a body that began
    # "Bhadda ,<br /> Bhadara ..." would otherwise open with a stray comma
    # and line break.
    body = re.sub(r"^<p>(?:\s|,|<br />)*", "<p>", body)
    return body


def _has_words(html: str) -> bool:
    # Bodies such as "." and "(q.v.)." are left where a merged note was.
    return len(re.findall(r"[^\W\d_]", re.sub(r"<[^>]+>", "", html))) >= 3


def _headword(anchor_text: str) -> str:
    word = re.sub(r"<sup>.*?</sup>", "", anchor_text)
    word = re.sub(r"<[^>]+>", "", word).replace("::", "")
    return word.split("[")[0].strip()


def _search_forms(headword: str) -> list[str]:
    """The forms a user would type to find this headword.

    "pa°", "an-" and "-da" mark prefixes, stems and suffixes; the marks are
    dropped. A space inside a word ("upa kappati") is a BuddhaDust typing
    error. Bracketed letters are optional, so "jap(p)aka" gives "jappaka" and
    "japaka". A hyphenated compound ("paṭicca-samuppāda") is also indexed
    without the hyphen, as a user types it.
    """
    word = headword.replace("(adjective)", "").replace(" ", "").strip("°-")
    forms = [word]
    if "(" in word:
        forms = [re.sub(r"[()]", "", word), re.sub(r"\(.*?\)", "", word)]
    if "-" in word:
        forms += [f.replace("-", "") for f in forms]
    return forms


def _variant_to_bold(m: re.Match, variants: list[str]) -> str:
    word = _headword(m.group(1))
    if not re.search(r"\w", word):
        return ""
    variants.append(word)
    return f"<b>{word}</b>"


def convert(raw_html: str) -> list[dict[str, str]]:
    start = raw_html.rindex("<p>", 0, raw_html.index(REGION_START))
    end = raw_html.index(REGION_END)
    region = _strip_furniture(raw_html[start:end])

    anchors = list(ANCHOR_RE.finditer(region))
    entries: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for i, m in enumerate(anchors):
        rest_end = anchors[i + 1].start() if i + 1 < len(anchors) else len(region)
        head = m.group(1)
        if _headword(head) in NOT_IN_PTS:
            continue
        sup = re.search(r"<sup>(.*?)</sup>", head)

        # Text BuddhaDust left inside the anchor (only "Ahu 3,4") follows the
        # headword, so it stays with the body.
        head_tail = re.sub(r"^.*?(?:</sup>|$)", "", head, count=1, flags=re.S)
        variants: list[str] = []
        rest = VARIANT_RE.sub(
            lambda v: _variant_to_bold(v, variants), region[m.end() : rest_end]
        )
        body = _clean_body("<p>" + head_tail + rest)
        if not _has_words(body):
            continue
        if sup:
            body = body.replace("<p>", f"<p><sup>{sup.group(1)}</sup> ", 1)
        for headword in [_headword(head), *variants]:
            for word in _search_forms(headword):
                word = word.replace("ṁ", "ṃ").lower()
                # "Ut(t)aṇḍa" also gives "uttaṇḍa", which has its own anchor.
                if (word, body) in seen:
                    continue
                seen.add((word, body))
                entries.append({"word": word, "definition_html": body})
    return entries


def main():
    pr.tic()
    pr.title("converting BuddhaDust PTS to json")
    pth = RepoPaths()

    pr.green("reading ped.htm")
    raw_html = pth.pts_raw_path.read_text(encoding="utf-8")
    pr.yes("")

    pr.green("converting")
    entries = convert(raw_html)
    pr.yes(len(entries))

    pr.green("writing pts.json")
    with open(pth.pts_source_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=1)
    pr.yes("")

    pr.toc()


if __name__ == "__main__":
    main()

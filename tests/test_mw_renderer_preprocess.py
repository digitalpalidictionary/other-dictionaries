"""Test mw renderer pre-processing transformations (Phase A).

Tests verify XML pre-processing that matches Cologne's basicadjust.php:
- SLP1 accent stripping with XML slash escaping
- Tag conversions (<lang> → <ab>, <s1 n> → <ab n>)
- Abbreviation tooltip injection from mwab data
- Literature tooltip injection from mwauthtooltips data
- Lex tooltip injection (convert <lex> content to <ab> with tooltips)
"""

import pytest

from dictionaries.mw.mw_renderer import (
    inject_abbreviation_tooltips,
    inject_lex_tooltips,
    inject_literature_tooltips,
    normalize_tags,
    strip_slp1_accents,
)


class TestSlp1AccentStripping:
    """Task 3.1: SLP1 accent stripping with XML slash escaping."""

    def test_removes_udatta_from_s_tag(self):
        xml = "<s>a/gni</s>"
        assert strip_slp1_accents(xml) == "<s>agni</s>"

    def test_removes_svarita_from_s_tag(self):
        xml = "<s>a^gni</s>"
        assert strip_slp1_accents(xml) == "<s>agni</s>"

    def test_removes_anudatta_from_s_tag(self):
        xml = r"<s>a\gni</s>"
        assert strip_slp1_accents(xml) == "<s>agni</s>"

    def test_preserves_xml_closing_slash(self):
        xml = "<s>a/gni</s>"
        result = strip_slp1_accents(xml)
        assert "</s>" in result

    def test_preserves_self_closing_tags_inside_s(self):
        xml = "<s>a/gni<srs/>test</s>"
        result = strip_slp1_accents(xml)
        assert "<srs/>" in result
        assert "agni" in result

    def test_strips_from_key2_tag(self):
        xml = "<key2>a/gni</key2>"
        assert strip_slp1_accents(xml) == "<key2>agni</key2>"

    def test_no_change_without_accents(self):
        xml = "<s>agni</s>"
        assert strip_slp1_accents(xml) == "<s>agni</s>"

    def test_multiple_s_tags(self):
        xml = "text <s>a/gni</s> and <s>va/yu</s>"
        result = strip_slp1_accents(xml)
        assert result == "text <s>agni</s> and <s>vayu</s>"


class TestTagNormalization:
    """Task 3.2: <lang> → <ab> and <s1 n> → <ab n> conversions."""

    def test_lang_to_ab(self):
        xml = '<lang n="greek">τεχνη</lang>'
        assert normalize_tags(xml) == '<ab n="greek">τεχνη</ab>'

    def test_s1_to_ab(self):
        xml = '<s1 n="test">word</s1>'
        assert normalize_tags(xml) == '<ab n="test">word</ab>'

    def test_no_change_for_other_tags(self):
        xml = "<s>agni</s>"
        assert normalize_tags(xml) == "<s>agni</s>"


class TestAbbreviationTooltipInjection:
    """Task 3.3: Abbreviation tooltip injection from abbreviation dict."""

    @pytest.fixture
    def abbrevs(self) -> dict[str, str]:
        return {"f.": "feminine", "m.": "masculine gender", "ind.": "indeclinable"}

    def test_injects_tooltip_when_no_n_attr(self, abbrevs: dict[str, str]):
        xml = "<ab>f.</ab>"
        result = inject_abbreviation_tooltips(xml, abbrevs)
        assert result == "<ab n='feminine'>f.</ab>"

    def test_preserves_existing_n_attr(self, abbrevs: dict[str, str]):
        xml = '<ab n="already set">f.</ab>'
        result = inject_abbreviation_tooltips(xml, abbrevs)
        assert result == '<ab n="already set">f.</ab>'

    def test_unknown_abbreviation_gets_empty_tooltip(self, abbrevs: dict[str, str]):
        xml = "<ab>xyz.</ab>"
        result = inject_abbreviation_tooltips(xml, abbrevs)
        assert result == "<ab n=''>xyz.</ab>"

    def test_multiple_abbreviations(self, abbrevs: dict[str, str]):
        xml = "<ab>m.</ab> or <ab>f.</ab>"
        result = inject_abbreviation_tooltips(xml, abbrevs)
        assert "n='masculine gender'" in result
        assert "n='feminine'" in result


class TestLiteratureTooltipInjection:
    """Task 3.4: Literature tooltip injection from author tooltips dict."""

    @pytest.fixture
    def tooltips(self) -> dict[str, str]:
        return {"Mn.": "Manu-smṛti", "MBh.": "Mahā-bhārata"}

    def test_injects_tooltip_for_known_source(self, tooltips: dict[str, str]):
        xml = "<ls>Mn. iii, 4</ls>"
        result = inject_literature_tooltips(xml, tooltips)
        assert "n='" in result
        assert "Mn." in result

    def test_unknown_source_gets_unknown_tooltip(self, tooltips: dict[str, str]):
        xml = "<ls>Xyz. 42</ls>"
        result = inject_literature_tooltips(xml, tooltips)
        assert "n='" in result

    def test_ib_abbreviation_marked(self, tooltips: dict[str, str]):
        xml = "<ls>ib. 42</ls>"
        result = inject_literature_tooltips(xml, tooltips)
        assert "<ab>ib.</ab>" in result

    def test_no_change_for_ls_with_existing_n(self, tooltips: dict[str, str]):
        xml = "<ls n='already'>text</ls>"
        result = inject_literature_tooltips(xml, tooltips)
        assert result == "<ls n='already'>text</ls>"


class TestLexTooltipInjection:
    """Task 3.5: Lex tooltip injection."""

    @pytest.fixture
    def abbrevs(self) -> dict[str, str]:
        return {
            "f.": "feminine",
            "m.": "masculine gender",
            "mfn.": "masculine, feminine and neuter; or = adjective",
        }

    def test_simple_lex_to_ab(self, abbrevs: dict[str, str]):
        xml = "<lex>f.</lex>"
        result = inject_lex_tooltips(xml, abbrevs)
        assert "<ab n='feminine'>f.</ab>" in result
        assert "<lex>" in result

    def test_lex_with_unknown_content(self, abbrevs: dict[str, str]):
        xml = "<lex>unknown</lex>"
        result = inject_lex_tooltips(xml, abbrevs)
        assert "unknown" in result

    def test_lex_with_nested_s_tag(self, abbrevs: dict[str, str]):
        xml = "<lex>m. (<s>scil.</s>)</lex>"
        result = inject_lex_tooltips(xml, abbrevs)
        assert "<ab n='masculine gender'>m.</ab>" in result
        assert "<s>scil.</s>" in result

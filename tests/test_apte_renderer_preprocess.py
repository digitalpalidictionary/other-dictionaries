"""Test apte renderer pre-processing transformations (Phase A).

Tests verify XML pre-processing:
- Broken bar replacement
- SLP1 accent stripping with XML slash protection
- Tag normalization (<lang> → <ab>, <s1> → <ab>)
- Literature tooltip injection
- Abbreviation tooltip injection
- Lex tooltip injection (KEEP <lex> wrapper)
"""

import pytest

from dictionaries.apte.apte_renderer import (
    inject_abbreviation_tooltips,
    inject_lex_tooltips,
    inject_literature_tooltips,
    normalize_tags,
    strip_slp1_accents,
)


class TestBrokenBarReplacement:
    def test_broken_bar_replaced_with_space(self):
        from dictionaries.apte.apte_renderer import preprocess_xml

        result = preprocess_xml("a¦b", {}, {})
        assert "¦" not in result
        assert "a b" in result


class TestSlp1AccentStripping:
    """SLP1 accent stripping with XML slash protection."""

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

    def test_closing_tag_not_corrupted(self):
        """CRITICAL: </s> must not become <_s> or similar."""
        xml = "<s>a/b^c</s>"
        result = strip_slp1_accents(xml)
        assert "</s>" in result
        assert "<_s>" not in result


class TestTagNormalization:
    def test_lang_to_ab(self):
        xml = '<lang n="greek">τεχνη</lang>'
        assert normalize_tags(xml) == '<ab n="greek">τεχνη</ab>'

    def test_s1_to_ab(self):
        xml = '<s1 n="test">word</s1>'
        assert normalize_tags(xml) == '<ab n="test">word</ab>'

    def test_no_change_for_other_tags(self):
        xml = "<s>agni</s>"
        assert normalize_tags(xml) == "<s>agni</s>"


class TestLiteratureTooltipInjection:
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


class TestAbbreviationTooltipInjection:
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


class TestLexTooltipInjection:
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

    def test_lex_wrapper_preserved(self, abbrevs: dict[str, str]):
        """CRITICAL: <lex> wrapper must be kept for Phase B bold conversion."""
        xml = "<lex>f.</lex>"
        result = inject_lex_tooltips(xml, abbrevs)
        assert "<lex>" in result

    def test_lex_with_unknown_content(self, abbrevs: dict[str, str]):
        xml = "<lex>unknown</lex>"
        result = inject_lex_tooltips(xml, abbrevs)
        assert "unknown" in result

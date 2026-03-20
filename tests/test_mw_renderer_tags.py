"""Test mw renderer tag-to-HTML conversions (Phase B).

Tests verify XML→HTML rendering matching Cologne's basicdisplay.php:
- <s> → <span class="sdata"> with SLP1→IAST transliteration
- <ab> → <span class="dotunder"> with tooltip
- <ls>, <hom>, <lex> rendering
- Foreign language tags → .foreign/.greek classes
- Structural tags stripped (<info>, <pb>, <pcol>, etc.)
- <div>, <F>, <C>, <Poem>, <sup> rendering
"""

from dictionaries.mw.mw_renderer import render_xml_to_html


class TestSanskritTagRendering:
    """Task 4.1: <s> → <span class="sdata"> with SLP1→IAST."""

    def test_s_tag_to_sdata_span(self):
        xml = "<s>agni</s>"
        result = render_xml_to_html(xml)
        assert '<span class="sdata">' in result
        assert "agni" in result
        assert "</span>" in result

    def test_slp1_to_iast_conversion(self):
        xml = "<s>DArA</s>"
        result = render_xml_to_html(xml)
        assert "dhārā" in result

    def test_capital_slp1_chars(self):
        xml = "<s>dfzwvA</s>"
        result = render_xml_to_html(xml)
        assert "dṛṣṭvā" in result


class TestAbbreviationRendering:
    """Task 4.2: <ab> → <span class="dotunder"> with tooltip."""

    def test_ab_with_tooltip(self):
        xml = "<ab n='feminine'>f.</ab>"
        result = render_xml_to_html(xml)
        assert 'class="dotunder"' in result
        assert "title='feminine'" in result or 'title="feminine"' in result
        assert "f." in result

    def test_ab_without_tooltip(self):
        xml = "<ab>f.</ab>"
        result = render_xml_to_html(xml)
        assert "f." in result


class TestLiteratureHomonymLexRendering:
    """Task 4.3: <ls>, <hom>, <lex> rendering."""

    def test_ls_with_tooltip(self):
        xml = "<ls n='Manu'>Mn. iii</ls>"
        result = render_xml_to_html(xml)
        assert 'class="ls"' in result
        assert "title=" in result

    def test_hom_rendering(self):
        xml = "<hom>1</hom>"
        result = render_xml_to_html(xml)
        assert 'class="hom"' in result
        assert "1" in result

    def test_bold_tag(self):
        xml = "<b>text</b>"
        result = render_xml_to_html(xml)
        assert "<strong>" in result
        assert "text" in result


class TestForeignLanguageTags:
    """Task 4.4: Foreign tags → .foreign/.greek classes."""

    def test_bot_tag(self):
        xml = "<bot>Ficus</bot>"
        result = render_xml_to_html(xml)
        assert 'class="foreign"' in result
        assert "Ficus" in result

    def test_bot_with_n_attr_gets_dotunder(self):
        xml = "<bot n='Ficus religiosa'>Fig tree</bot>"
        result = render_xml_to_html(xml)
        assert 'class="foreign dotunder"' in result
        assert 'title="Ficus religiosa"' in result

    def test_zoo_tag(self):
        xml = "<zoo>Cervus</zoo>"
        result = render_xml_to_html(xml)
        assert 'class="foreign"' in result
        assert "Cervus" in result

    def test_zoo_with_n_attr_gets_dotunder(self):
        xml = "<zoo n='Cervus axis'>spotted deer</zoo>"
        result = render_xml_to_html(xml)
        assert 'class="foreign dotunder"' in result

    def test_gk_tag(self):
        xml = "<gk>τεχνη</gk>"
        result = render_xml_to_html(xml)
        assert 'class="foreign"' in result
        assert 'title="Greek script"' in result
        assert "τεχνη" in result

    def test_fr_tag(self):
        xml = "<fr>mot</fr>"
        result = render_xml_to_html(xml)
        assert 'class="foreign"' in result
        assert 'title="French language"' in result

    def test_ger_tag(self):
        xml = "<ger>Wort</ger>"
        result = render_xml_to_html(xml)
        assert 'class="foreign"' in result
        assert 'title="German language"' in result

    def test_lat_tag(self):
        xml = "<lat>verbum</lat>"
        result = render_xml_to_html(xml)
        assert 'class="foreign"' in result
        assert 'title="Latin language"' in result

    def test_lex_renders_bold(self):
        xml = "<lex>f.</lex>"
        result = render_xml_to_html(xml)
        assert "<strong>" in result
        assert "f." in result

    def test_lang_fallback_renders_italic(self):
        xml = "<lang>word</lang>"
        result = render_xml_to_html(xml)
        assert "<em>" in result
        assert "word" in result


class TestStructuralTagStripping:
    """Task 4.5: Strip <info>, <pb>, <pcol>, <to>, <ns>, etc."""

    def test_info_stripped(self):
        xml = '<info lex="m."/>rest'
        result = render_xml_to_html(xml)
        assert "info" not in result
        assert "rest" in result

    def test_pb_stripped_for_mw(self):
        xml = "<pb>text</pb>"
        result = render_xml_to_html(xml)
        assert "<pb>" not in result

    def test_pcol_stripped(self):
        xml = "<pcol>1,2</pcol>"
        result = render_xml_to_html(xml)
        assert "<pcol>" not in result

    def test_key1_stripped(self):
        xml = "<key1>agni</key1>"
        result = render_xml_to_html(xml)
        assert "<key1>" not in result

    def test_head_body_tail_stripped(self):
        xml = "<h>head</h><body>content</body><tail>end</tail>"
        result = render_xml_to_html(xml)
        assert "content" in result
        assert "<body>" not in result


class TestDivFootnoteSup:
    """Task 4.6: <div>, <F>, <C>, <sup> rendering."""

    def test_div_renders_separator(self):
        xml = '<div n="p"/>'
        result = render_xml_to_html(xml)
        assert 'class="div-sep"' in result or "<br" in result

    def test_footnote_rendering(self):
        xml = "<F>note text</F>"
        result = render_xml_to_html(xml)
        assert "Footnote" in result
        assert "note text" in result

    def test_c_rendering(self):
        xml = '<C n="2">text</C>'
        result = render_xml_to_html(xml)
        assert "(C2)" in result

    def test_sup_rendering(self):
        xml = "<sup>2</sup>"
        result = render_xml_to_html(xml)
        assert "<sup>" in result
        assert "2" in result

    def test_no_inline_styles(self):
        xml = '<s>agni</s> <ab n="test">f.</ab> <hom>1</hom> <bot>Rosa</bot>'
        result = render_xml_to_html(xml)
        assert "style=" not in result

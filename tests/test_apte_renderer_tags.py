"""Test apte renderer tag-to-HTML conversions (Phase B).

Tests verify XML→HTML rendering:
- <h> block stripped entirely (content included)
- H-type extraction and primary vs secondary headings
- <pc> and <L> extraction/stripping
- <s> → <span class="sdata"> with SLP1→IAST
- <ab>, <ls>, <hom> rendering
- <bot>, <zoo>, <bio> with/without n attr
- All 9 foreign language tags
- <div>, <F>, <C>, <lex>, misc tags
- Assembly: primary heading label + page link + record ID
- Scan URL uses dict=AP90
- NO <h3> headword title
"""

from dictionaries.apte.apte_renderer import render_xml_to_html


class TestHBlockStripping:
    def test_h_block_stripped_entirely_including_content(self):
        """<h>...</h> blocks must be stripped with content — no SLP1 leakage."""
        xml = "<H1><h>ADAra</h><body>fire</body></H1>"
        result = render_xml_to_html(xml)
        assert "ADAra" not in result
        assert "fire" in result

    def test_h_type_extraction(self):
        xml = "<H1><body>text</body></H1>"
        result = render_xml_to_html(xml)
        assert "(H1)" in result

    def test_h1a_is_secondary_no_label(self):
        xml = "<H1A><body>sub</body></H1A>"
        result = render_xml_to_html(xml)
        assert "(H1A)" not in result

    def test_h2_is_primary(self):
        xml = "<H2><body>text</body></H2>"
        result = render_xml_to_html(xml)
        assert "(H2)" in result


class TestPcAndLExtraction:
    def test_pc_value_used_in_page_link(self):
        xml = "<H1><body>text</body><tail><pc>5,1</pc></tail></H1>"
        result = render_xml_to_html(xml)
        assert "Printed book page" in result
        assert "5" in result

    def test_l_value_appended_as_record_id(self):
        xml = "<H1><L>42</L><body>text</body></H1>"
        result = render_xml_to_html(xml)
        assert "[ID=42]" in result
        assert "record-id" in result


class TestSanskritTagRendering:
    def test_s_tag_to_sdata_span(self):
        xml = "<s>agni</s>"
        result = render_xml_to_html(xml)
        assert '<span class="sdata">' in result
        assert "agni" in result

    def test_slp1_to_iast_conversion(self):
        xml = "<s>DArA</s>"
        result = render_xml_to_html(xml)
        assert "dhārā" in result


class TestAbbreviationRendering:
    def test_ab_with_tooltip(self):
        xml = "<ab n='feminine'>f.</ab>"
        result = render_xml_to_html(xml)
        assert 'class="dotunder"' in result
        assert "f." in result

    def test_ab_without_tooltip(self):
        xml = "<ab>f.</ab>"
        result = render_xml_to_html(xml)
        assert "f." in result


class TestLsHomRendering:
    def test_ls_with_tooltip(self):
        xml = "<ls n='Manu'>Mn. iii</ls>"
        result = render_xml_to_html(xml)
        assert 'class="ls"' in result
        assert "title=" in result

    def test_hom_rendering(self):
        xml = "<hom>1</hom>"
        result = render_xml_to_html(xml)
        assert 'class="hom"' in result
        assert 'title="Homonym"' in result
        assert "1" in result


class TestBotBioZooRendering:
    def test_bot_without_n_gets_foreign_only(self):
        xml = "<bot>Ficus</bot>"
        result = render_xml_to_html(xml)
        assert 'class="foreign"' in result
        assert "dotunder" not in result

    def test_bot_with_n_gets_dotunder(self):
        xml = "<bot n='Ficus religiosa'>Fig tree</bot>"
        result = render_xml_to_html(xml)
        assert 'class="foreign dotunder"' in result
        assert 'title="Ficus religiosa"' in result

    def test_zoo_without_n(self):
        xml = "<zoo>Cervus</zoo>"
        result = render_xml_to_html(xml)
        assert 'class="foreign"' in result

    def test_zoo_with_n_gets_dotunder(self):
        xml = "<zoo n='Cervus axis'>spotted deer</zoo>"
        result = render_xml_to_html(xml)
        assert 'class="foreign dotunder"' in result

    def test_bio_renders_foreign(self):
        xml = "<bio>Darwin</bio>"
        result = render_xml_to_html(xml)
        assert 'class="foreign"' in result


class TestForeignLanguageTags:
    def test_gk_tag(self):
        xml = "<gk>τεχνη</gk>"
        result = render_xml_to_html(xml)
        assert 'title="Greek script"' in result

    def test_fr_tag(self):
        xml = "<fr>mot</fr>"
        result = render_xml_to_html(xml)
        assert 'title="French language"' in result

    def test_ger_tag(self):
        xml = "<ger>Wort</ger>"
        result = render_xml_to_html(xml)
        assert 'title="German language"' in result

    def test_lat_tag(self):
        xml = "<lat>verbum</lat>"
        result = render_xml_to_html(xml)
        assert 'title="Latin language"' in result

    def test_tib_tag(self):
        xml = "<tib>text</tib>"
        result = render_xml_to_html(xml)
        assert 'title="Tibetan language"' in result

    def test_toch_tag(self):
        xml = "<toch>text</toch>"
        result = render_xml_to_html(xml)
        assert 'title="Tocharian language"' in result

    def test_arab_tag(self):
        xml = "<arab>text</arab>"
        result = render_xml_to_html(xml)
        assert 'title="Arabic script"' in result

    def test_rus_tag(self):
        xml = "<rus>text</rus>"
        result = render_xml_to_html(xml)
        assert 'title="Russian language"' in result

    def test_mong_tag(self):
        xml = "<mong>text</mong>"
        result = render_xml_to_html(xml)
        assert 'title="Mongolian language"' in result


class TestDivFootnoteC:
    def test_div_renders_separator(self):
        xml = '<div n="p"/>'
        result = render_xml_to_html(xml)
        assert 'class="div-sep"' in result

    def test_footnote_rendering(self):
        xml = "<F>note text</F>"
        result = render_xml_to_html(xml)
        assert "Footnote" in result
        assert "note text" in result

    def test_c_rendering(self):
        xml = '<C n="2">text</C>'
        result = render_xml_to_html(xml)
        assert "(C2)" in result


class TestMiscTags:
    def test_lex_renders_bold(self):
        """<lex> → <strong> (bold grammar labels)."""
        xml = "<lex>f.</lex>"
        result = render_xml_to_html(xml)
        assert "<strong>" in result
        assert "f." in result

    def test_bold_tag(self):
        xml = "<b>text</b>"
        result = render_xml_to_html(xml)
        assert "<strong>" in result

    def test_italic_tag(self):
        xml = "<i>text</i>"
        result = render_xml_to_html(xml)
        assert "<em>" in result

    def test_etym_tag(self):
        xml = "<etym>text</etym>"
        result = render_xml_to_html(xml)
        assert "<em>" in result

    def test_lang_fallback_renders_italic(self):
        xml = "<lang>word</lang>"
        result = render_xml_to_html(xml)
        assert "<em>" in result

    def test_lb_renders_br(self):
        xml = "text<lb/>more"
        result = render_xml_to_html(xml)
        assert "<br/>" in result


class TestAssembly:
    def test_scan_url_uses_ap90(self):
        xml = "<H1><body>text</body><tail><pc>5,1</pc></tail></H1>"
        result = render_xml_to_html(xml)
        assert "dict=AP90" in result

    def test_no_h3_headword_title(self):
        """GoldenDict shows headword automatically — no duplicate."""
        xml = "<H1><body>text</body></H1>"
        result = render_xml_to_html(xml)
        assert "<h3>" not in result

    def test_no_inline_styles(self):
        xml = '<s>agni</s> <ab n="test">f.</ab> <hom>1</hom>'
        result = render_xml_to_html(xml)
        assert "style=" not in result

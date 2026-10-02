"""Test the BuddhaDust PTS converter.

Every fixture is copied from dictionaries/pts/source/ped.htm.
"""

from dictionaries.pts.pts_from_buddhadust import (
    REGION_END,
    _clean_body,
    _strip_editor_notes,
    _strip_furniture,
    convert,
)

SATHERA = """<p><a id="xsathera" href="#xsathera" class="palientry">:: Sathera</a> (adjective) [<i>sa</i><sup>3</sup> + <i>thera</i>] including the <i>theras</i> <b>AN</b> II 169</p>
"""

AGHA_1 = """<p><a id="xagha-1" href="#xagha-1" class="palientry">:: Agha<sup>1</sup></a> (neuter) [<i>cf.</i> Skt. <i>agha,</i> of uncertain etymology] evil, grief, pain, suffering, misfortune <b>SN</b> I 22; <b>MN</b> I 500 <i>(roga gaṇḍa salla agha);</i> <b>AN</b> II 128 (the same); <b>Jāt</b> V 100; <b>Theri</b> 491; <b>Saddhammopāyana</b> 51. — adjective painful, bringing pain <b>Jāt</b> VI 507 (<i>agha-m-miga = aghakara</i> masculine commentary).</p>
<p class="in1"><i>-bhūta</i> a source of pain <b>SN</b> III 189 (+ <i>agha</i> and <i>salla</i>).</p>
"""

ABHIDHAMMA = """<p><a id="xabhidhamma" href="#xabhidhamma" class="palientry">:: Abhidhamma</a> <a href="../../../../resources/audios/glossology_audios/palwvm48k/abhidhamma-48k.mp3"><img src="../../../../resources/images/audio-verysmall.jpg" width="18" height="19" alt="Abhidhamma" title="Abhidhamma" /></a> <i>[abhi + dhamma]</i> the "special <i>Dhamma,</i>" i.e.,<br /> 
1. theory of the Doctrine, the Doctrine classified, the Doctrine pure and simple (without any admixture of literary grace or of personalities, or of anecdotes, or of arguments <i>ad personam</i>), <b>Vinaya</b> I 64, 68; IV 144; IV 344. Coupled with <i>abhivinaya,</i> <b>DN</b> III 267; <b>MN</b> I 272.<br /> 
2. (only in the Chronicles and commentaries) name of the Third <i>Piṭaka,</i> the third group of the canonical books. <b>Dīpavaṁsa</b> V 37; <b>Peta Vatthu Commentary</b> 140. See the detailed discussion at <b>Sumaṅgalavilāsinī</b> I 15, 18<i>f.</i> [As the word <b>Abhidhamma</b> standing alone is not found in <b>Snp</b> or <b>SN</b> or <b>A,</b> and only once or twice in the <b>DB</b>, it probably came into use only towards the end of the period in which the four great <i>Nikāyas</i> grew up.]<a id="pg58" href="#pg58"><span class="f2 g"><b>{58}</b></span></a></p>
<p class="in1"><i>-kathā</i> discourse on philosophical or psychological matters, <b>MN</b> I 214, 218; <b>AN</b> III 106, 392. See <i>dhammakathā.</i></p>
"""

ABHIYOBBANA = """<p><a id="xabhiyobbana" href="#xabhiyobbana" class="palientry">:: Abhiyobbana</a> (neuter) <i>[abhi + yobbana]</i> much youthfullness, early or tender youth <b>Theri</b> 258 (= <i>abhinavayobbanakāla</i> <b>Therīgāthā Commentary</b> 211).</p>
"""

ABHISANGA = """<p><a id="xabhisa-nga" href="#xabhisa-nga" class="palientry">:: Abhisaṅga</a> [from <i>abhi + sañj, cf. abhisajjati</i> and Skt. <i>abhisaṅga</i>] sticking to, cleaving to, adherence to <b>Jāt</b> V 6; <b>Nettipakaraṇa</b> 110, 112; as 129 <i>(°hetukaṁ dukkhaṁ)</i> 249 <i>(°rasa).</i></p>
"""

ABBHUDIRETI = """<p><a id="xabbhudiireti" href="#xabbhudiireti" class="palientry">:: Abbhudīreti</a> <i>[abhi + ud + īreti]</i> to raise the voice, to utter <b>Theri</b> 402; <b>Sumaṅgalavilāsinī</b> I 61; <b>Saddhammopāyana</b> 514.<br />
[BD]: high dudgeon, ire</p>
"""

ABHIGACCHATI = """<p><a id="xabhigacchati" href="#xabhigacchati" class="palientry">:: Abhigacchati</a> <a href="../../../../resources/audios/glossology_audios/palwvm48k/abhigacchati-48k.mp3"><img src="../../../../resources/images/audio-verysmall.jpg" width="18" height="19" alt="Abhigacchati" title="Abhigacchati" /></a><br />
[DPL]: To go to, to approach. <b>Mah.</b> 107.</p>
"""

NISAMSA = """<p><a id="xnisamsa" href="#xnisamsa" class="palientry">:: Nisamsa</a> <br /> 
<a id="xnisa_msa" href="#xnisa_msa" class="palientry">:: Nisaṁsa</a> see <i>Ānisaṁsa, Mahānisaṁsa,</i> of great advantage.</p>
"""

CHAB = """<p><a id="xchab" href="#xchab" class="palientry">:: Chab°</a> see under <i>cha.</i></p>
"""

JAPPAKA = """<p><a id="xjapaka" href="#xjapaka" class="palientry">:: Jap(p)aka</a> (adjective) whispering, see <i>kaṇṇa°.</i></p>
"""

UPAKAPPATI = """<p><a id="xupa-kappati" href="#xupa-kappati" class="palientry">:: Upa kappati</a> <i>[upa + kappati]</i> (intransitive) to be beneficial to (with dative), to serve, to accrue <b>SN</b> I 85; <b>Peta Vatthu</b> I 4<sup>4</sup> (= <i>nippajjati</i> <b>Peta Vatthu Commentary</b> 19); I 5<sup>7</sup> <i>(petānaṁ);</i> I 10<sup>4</sup> (= <i>viniyujjati</i> <b>Peta Vatthu Commentary</b> 49); <b>Jāt</b> V 350; <b>Peta Vatthu Commentary</b> 8, 29 <i>(petānaṁ),</i> 27 (the same), 241; <b>Saddhammopāyana</b> 501, 504.</p>
"""

ANUMATTA = """<p><a id="xanumatta" href="#xanumatta" class="palientry">:: Anumatta</a> [DPL]: small, least, <b>Dhp</b> 50, 375, 386<br />
see <i><a href="#xa_nu">aṇu°</a>.</i></p>
"""

ESO = """<p><a id="xeso" href="#xeso" class="palientry">:: Eso</a> , and <i>Esa</i> (pronoun),<br /> 
[DPL]: This, this one; that <i>Ko nām'eso,</i> who is this? (F. <b>Jāt.</b> 47). <i>Nirupakāro esa amhākaṁ,</i> this fellow is no use to us (F. <b>Jāt.</b> 3). <i>Eso mahārāja Bhagavā,</i> that, great king, is Buddha. Sometimes pleonastically joined to a personal pronoun, as <i>esāhaṁ,</i> I accusative <i>etaṁ.</i> Instrumental <i>etena.</i> Plural ete (<b>Dhp</b> 81). Genative and dative plural <i>etesaṁ, etesānaṁ</i> (<b>Dhp</b> 90). Fem. <i>esā</i> (<b>Dhp</b> 60). Accusative feminine <i>etaṁ.</i> Genative and dative feminine <i>etissā, etassā</i> (<b>Dhp</b> 233). Intr. and ablative feminine plural <i>etāhi</i> (<b>Dhp</b> 234). Gen and dative feminine plural <i>etāsaṁ</i> (<b>Dhp</b> 117). Neut. <i>etaṁ,</i> and before a vowel frequently etad. <i>Etad avoca, etad abruvi,</i> said this (<b>Dhp</b> 124). For <b>etad ahosi,</b> see <i>Bhavati. Kim etaṁ,</i> what's this? (<b>Mah.</b> 59). <i>N'etaṁ tathā,</i> it is not so (<b>Mah.</b> 198). <i>No h'etaṁ,</i> certainly not (<b>Sen. K.</b> 205). The base in composition is <i>etad. etadatthāya,</i> on this account (<b>Kh.</b> 19).</p>
"""

PALIGHA_1 = """<p><a id="xpaligha" href="#xpaligha" class="palientry">:: Paligha</a>.<br /> 
[DPL] An iron beam or bar for fastening up a door; an obstacle, hindrance. <b>Ab.</b> 217; <b>Dhp</b> 71, 296. Of ignorance as a bar to religious progress (<b>Dhp</b> 428).</p>
"""

YENA = """<p><b><i>:: Yena</i></b> see Ya.</p>
"""

ATI_UDAKA = """<p><a id="xati-udaka" href="#xati-udaka" class="palientry">:: Ati-udaka</a> too much water, excess of water <b>Dhp</b> I 52.</p>
"""

UTTANDA = """<p><a id="xutta_n_da" href="#xutta_n_da" class="palientry">:: Uttaṇḍa</a> ,<br /> 
<a id="xuta_n_da" href="#xuta_n_da" class="palientry">:: Ut(t)aṇḍa</a> see <i>uddaṇḍa.</i></p>
"""

SIDE_BOX = """<div class="floatrpp wpx200 marl6"> <p class="f2"><b>Moil:</b> hard work; drudgery</p> <p><img src="../../../../resources/images/king_of_ny_vrysm.gif" width="38" height="32" alt="p.p. explains it all" /> <span class="f2">— p.p.</span></p> </div>"""

ASAVA_HEAD = """<p><a id="xaasava" href="#xaasava" class="palientry">:: Āsava</a> [<a href="../../../../backmatter/indexes/sutta_search.htm#xaasava">SUTTA SEARCH</a>] [<a href="../../../../backmatter/glossology/glossology/asavas.htm">GLOSSOLOGY</a>] [from <i>ā + sru,</i>"""

TANHA_LINE = """<b>Dhp</b> III 286.[?]<br />
[BD] <a href="../../../../dhamma-vinaya/pali/kd/dhp/kd.dhp.pali.bd.htm#pg44">pg 44,</a> <a href="../../../../dhamma-vinaya/pali/kd/dhp/kd.dhp.pali.bd.htm#v180">v 180,</a> <a href="../../../../dhamma-vinaya/pali/kd/dhp/kd.dhp.pali.bd.htm#v186">186,</a> <a href="../../../../dhamma-vinaya/pali/kd/dhp/kd.dhp.pali.bd.htm#v216">216,</a> <a href="../../../../backmatter/indexes/sutta/kd/dhp/idx_dhp.htm#ch24">ch 24.</a>
— 18 varieties of <i>taṇhā</i>"""

BRAHMA_NOTE = """On etymology see Mayrhofer 1994. ([BD]: was: Osthoff, <b>"Bezzenberger's Beitrage"</b> XXIV 142<i>f.</i> (= Middle Irish <i>bricht</i> charm, spell: Old-Icelandic <i>bragr</i> poetry))]<br />"""

NAHUTA_END = """<b>Peta Vatthu Commentary</b> 22, 265.<br /> 
[BD]: One followed by 28 zeros —<br /> 
10,000,000,000,000,000,000,000,000,000.</p>"""

TACA_PAGE = """see <i>kāya</i> I.(a)</p> <p class="f2 g">---[ <a id="pg267" href="#pg267"><b>[Page 267]</b></a> ]---</p> <p>of which the first deals"""

KAMMA_AS_38 = """These subjects of meditation are given as 38 at as 168 (<i>cf.</i> <b>Compendium</b> 202)"""

BALA_BOLD_AS = """At <b>as</b> 124 <i>bala</i> is understood"""


def _convert(*snippets: str) -> list[dict[str, str]]:
    return convert("".join(snippets) + REGION_END)


def _only(*snippets: str) -> dict[str, str]:
    entries = _convert(*snippets)
    assert len(entries) == 1
    return entries[0]


class TestPlainEntry:
    def test_word(self):
        assert _only(SATHERA)["word"] == "sathera"

    def test_body_drops_anchor(self):
        body = _only(SATHERA)["definition_html"]
        assert body.startswith("<p>(adjective) [<i>sa</i><sup>3</sup>")
        assert "palientry" not in body
        assert "::" not in body


class TestHomonymWithCompounds:
    def test_word_has_no_number(self):
        assert _only(AGHA_1)["word"] == "agha"

    def test_body_starts_with_homonym_number(self):
        assert _only(AGHA_1)["definition_html"].startswith("<p><sup>1</sup> (neuter)")

    def test_compound_paragraph_stays_with_headword(self):
        assert (
            '<p class="in1"><i>-bhūta</i> a source of pain'
            in _only(AGHA_1)["definition_html"]
        )


class TestFurniture:
    def test_audio_link_and_image_removed(self):
        body = _only(ABHIDHAMMA)["definition_html"]
        assert "<img" not in body
        assert "audios" not in body
        assert "<a " not in body

    def test_page_marker_removed(self):
        body = _only(ABHIDHAMMA)["definition_html"]
        assert "{58}" not in body
        assert "grew up.]</p>" in body

    def test_niggahita_folded(self):
        body = _only(ABHIDHAMMA)["definition_html"]
        assert "ṁ" not in body
        assert "Dīpavaṃsa" in body


class TestErrorFixes:
    def test_fullness_misspelling_fixed(self):
        body = _only(ABHIYOBBANA)["definition_html"]
        assert "much youthfulness, early" in body

    def test_broken_dhsa_restored(self):
        body = _only(ABHISANGA)["definition_html"]
        assert "112; <b>DhsA</b> 129 <i>(°hetukaṃ" in body
        assert " as 129" not in body


class TestEditorNotes:
    def test_bd_note_removed(self):
        body = _only(ABBHUDIRETI)["definition_html"]
        assert "[BD]" not in body
        assert "dudgeon" not in body
        assert body.endswith("<b>Saddhammopāyana</b> 514.</p>")

    def test_merged_only_entry_dropped(self):
        words = [e["word"] for e in _convert(SATHERA, ABHIGACCHATI)]
        assert words == ["sathera"]


class TestHeadwordForms:
    def test_variant_headword_gets_its_own_row(self):
        entries = _convert(NISAMSA)
        assert [e["word"] for e in entries] == ["nisamsa", "nisaṃsa"]
        assert entries[0]["definition_html"] == entries[1]["definition_html"]
        assert entries[0]["definition_html"].startswith("<p><b>Nisaṃsa</b> see")

    def test_stem_mark_dropped(self):
        assert _only(CHAB)["word"] == "chab"

    def test_optional_letters_indexed_both_ways(self):
        assert [e["word"] for e in _convert(JAPPAKA)] == ["jappaka", "japaka"]

    def test_space_inside_word_removed(self):
        assert _only(UPAKAPPATI)["word"] == "upakappati"


class TestMoreFurniture:
    def test_side_box_removed(self):
        body = _only(SATHERA, SIDE_BOX)["definition_html"]
        assert "Moil" not in body
        assert "p.p." not in body

    def test_site_links_removed(self):
        html = _strip_furniture(ASAVA_HEAD)
        assert "SUTTA SEARCH" not in html
        assert "GLOSSOLOGY" not in html
        assert ":: Āsava</a> [from <i>ā + sru,</i>" in html

    def test_old_page_marker_joins_the_sentence(self):
        html = _strip_furniture(TACA_PAGE)
        assert "Page 267" not in html
        assert "I.(a) of which the first deals" in html


class TestMoreEditorNotes:
    def test_pts_text_after_a_dash_survives(self):
        html = _strip_editor_notes(TANHA_LINE)
        assert "pg 44" not in html
        assert "[BD]" not in html
        assert "— 18 varieties of <i>taṇhā</i>" in html

    def test_bracketed_note_removed(self):
        html = _strip_editor_notes(BRAHMA_NOTE)
        assert "Osthoff" not in html
        assert html.startswith("On etymology see Mayrhofer 1994.]<br />")

    def test_long_note_removed_to_paragraph_end(self):
        html = _strip_editor_notes(NAHUTA_END)
        assert "zeros" not in html
        assert "10,000" not in html
        assert html.endswith("22, 265.</p>")

    def test_merged_only_paragraph_dropped(self):
        assert _convert(SATHERA, ANUMATTA) == _convert(SATHERA)

    def test_headword_not_in_pts_dropped(self):
        assert _convert(SATHERA, ESO) == _convert(SATHERA)

    def test_body_without_words_dropped(self):
        assert _convert(SATHERA, PALIGHA_1) == _convert(SATHERA)


class TestMoreDhsA:
    def test_english_as_left_alone_next_to_a_reference(self):
        body = _clean_body(KAMMA_AS_38)
        assert "given as 38 at <b>DhsA</b> 168" in body

    def test_bold_as_restored(self):
        assert _clean_body(BALA_BOLD_AS).startswith("At <b>DhsA</b> 124")


class TestMoreHeadwords:
    def test_bold_italic_headword_becomes_an_entry(self):
        words = [e["word"] for e in _convert(SATHERA, YENA)]
        assert words == ["sathera", "yena"]

    def test_hyphenated_word_also_indexed_without_hyphen(self):
        assert [e["word"] for e in _convert(ATI_UDAKA)] == ["ati-udaka", "atiudaka"]

    def test_duplicate_row_skipped(self):
        assert [e["word"] for e in _convert(UTTANDA)] == ["uttaṇḍa", "utaṇḍa"]

import json


abbrev_html = """
<div>
  <div class="title"><span class="title">A Dictionary of Pāli</span></div>
  <div class="byline">Texts, Works Cited, Abbreviations, and Symbols<br>
    Parts I–III combined, revised by Martin Straube</div>
  <h3>Abbreviations</h3>
  
  
  <table>
    <tbody><tr>
      <td>AAWG</td>
      <td>Abhandlungen der Akademie der Wissenschaften zu Göttingen</td>
    </tr>
    <tr>
      <td>abl.</td>
      <td>ablative</td>
    </tr>
    <tr>
      <td>absol.</td>
      <td>absolutive</td>
    </tr>
    <tr>
      <td>abstr.</td>
      <td>abstract noun</td>
    </tr>
    <tr>
      <td>acc.</td>
      <td>accusative</td>
    </tr>
    <tr>
      <td>act.</td>
      <td>active</td>
    </tr>
    <tr>
      <td>adj.</td>
      <td>adjective</td>
    </tr>
    <tr>
      <td>adv.</td>
      <td>adverb</td>
    </tr>
    <tr>
      <td>AiG</td>
      <td><i>Altindische Grammatik</i>, A. Debrunner, J. Wackernagel, Göttingen 1930–57</td>
    </tr>
    <tr>
      <td>AMg</td>
      <td>Ardhamāgadhī</td>
    </tr>
    <tr>
      <td>aor.</td>
      <td>aorist</td>
    </tr>
    <tr>
      <td>App.</td>
      <td>Appendix</td>
    </tr>
    <tr>
      <td>Aś</td>
      <td>
	Aśokan Inscriptions<br>
	G:&nbsp;Gīrnar;
	K:&nbsp;Kālsī;
	Dh:&nbsp;Dhauli;
	J:&nbsp;Jaugaḍa;
	M:&nbsp;Mānsehra;
	Sh:&nbsp;Shāhbāzgaṛhī;
	S:&nbsp;Sōpārā;
	Y:&nbsp;Yeṛṛaguḍi<br>
	RE:&nbsp;Rock Edict;
	PE:&nbsp;Pillar Edict
      </td>
    </tr>
    <tr>
      <td>Ātm.</td>
      <td>ātmanepada</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Be</td>
      <td>Burmese edition: Chaṭṭhasaṅgīti series, Rangoon 1956 foll.</td>
    </tr>
    <tr>
      <td>BHS</td>
      <td>Buddhist Hybrid Sanskrit (as in BHSD)</td>
    </tr>
    <tr>
      <td>BHSD</td>
      <td><i>Buddhist Hybrid Sanskrit Dictionary</i>, F. Edgerton, New Haven 1953</td>
    </tr>
    <tr>
      <td>BHSG</td>
      <td><i>Buddhist Hybrid Sanskrit Grammar</i>, F. Edgerton, New Haven
	1953</td>
    </tr>
    <tr>
      <td>bhvr.</td>
      <td>bahuvrīhi compound</td>
    </tr>
    <tr>
      <td>BSU</td>
      <td>= H. Lüders, 1954</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>caus.</td>
      <td>causative</td>
    </tr>
    <tr>
      <td>CDIAL</td>
      <td><i>A Comparative Dictionary of the Indo-Aryan Languages</i>, R.L. Turner, London 1966</td>
    </tr>
    <tr>
      <td>Ce</td>
      <td>Sinhalese edition: Buddha Jayanti Tripitaka Series, Colombo 1959 foll.; Simon Hewavitarne
	Bequest, Colombo 1911 foll.</td>
    </tr>
    <tr>
      <td>Cf</td>
      <td>compare</td>
    </tr>
    <tr>
      <td>compar.</td>
      <td>comparative</td>
    </tr>
    <tr>
      <td>cond.</td>
      <td>conditional</td>
    </tr>
    <tr>
      <td>conj.</td>
      <td>conjecture</td>
    </tr>
    <tr>
      <td>cpd., cpds.</td>
      <td>compound(s)</td>
    </tr>
    <tr>
      <td>CPD</td>
      <td><i>A Critical Pāli Dictionary</i>, begun by V. Trenckner, revised, continued, and edited by Dines Andersen [et al.], Copenhagen, Bristol 1924–2011</td>
    </tr>
    <tr>
      <td>ct, cts</td>
      <td>commentary, commentaries</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>dat.</td>
      <td>dative</td>
    </tr>
    <tr>
      <td>DED</td>
      <td><i>A Dravidian Etymological Dictionary</i>, T. Burrow, M.B. Emeneau, 2nd ed., Oxford 1984</td>
    </tr>
    <tr>
      <td>demonstr.</td>
      <td>demonstrative</td>
    </tr>
    <tr>
      <td>denom.</td>
      <td>denominative</td>
    </tr>
    <tr>
      <td>desid.</td>
      <td>desiderative</td>
    </tr>
    <tr>
      <td>dv.</td>
      <td>dvandva compound</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>ed.</td>
      <td>edited by, editor, edition</td>
    </tr>
    <tr>
      <td>eds</td>
      <td>editions (ie Be, Ce, Ee, Se)</td>
    </tr>
    <tr>
      <td>Ee</td>
      <td>European edition: PTS</td>
    </tr>
    <tr>
      <td>eg</td>
      <td>for example</td>
    </tr>
    <tr>
      <td>esp.</td>
      <td>especially</td>
    </tr>
    <tr>
      <td>et al.</td>
      <td>and others</td>
    </tr>
    <tr>
      <td>etc</td>
      <td>et cetera</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>f.</td>
      <td>feminine</td>
    </tr>
    <tr>
      <td>fig.</td>
      <td>figurative(ly)</td>
    </tr>
    <tr>
      <td>fn</td>
      <td>footnote</td>
    </tr>
    <tr>
      <td>foll.</td>
      <td>following</td>
    </tr>
    <tr>
      <td>fpp</td>
      <td>future passive participle</td>
    </tr>
    <tr>
      <td>fut.</td>
      <td>future</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>gen.</td>
      <td>genitive</td>
    </tr>
    <tr>
      <td>gr.t.t</td>
      <td>grammatical technical term</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>id.</td>
      <td>the same</td>
    </tr>
    <tr>
      <td>ie</td>
      <td>that is</td>
    </tr>
    <tr>
      <td>IeT</td>
      <td>Indica et Tibetica, Bonn, et al.</td>
    </tr>
    <tr>
      <td>ifc</td>
      <td>in fine compositi (at the end of a compound)</td>
    </tr>
    <tr>
      <td>iic</td>
      <td>in initio compositi (at the beginning of a compound)</td>
    </tr>
    <tr>
      <td>IIJ</td>
      <td><i>Indo-Iranian Journal</i>, The Hague</td>
    </tr>
    <tr>
      <td>imperat.</td>
      <td>imperative</td>
    </tr>
    <tr>
      <td>imperf.</td>
      <td>imperfect</td>
    </tr>
    <tr>
      <td>impers.</td>
      <td>impersonal</td>
    </tr>
    <tr>
      <td>ind.</td>
      <td>indeclinable</td>
    </tr>
    <tr>
      <td>indic.</td>
      <td>indicative</td>
    </tr>
    <tr>
      <td>inf.</td>
      <td>infinitive</td>
    </tr>
    <tr>
      <td>instr.</td>
      <td>instrumental</td>
    </tr>
    <tr>
      <td>intens.</td>
      <td>intensive</td>
    </tr>
    <tr>
      <td>interrog.</td>
      <td>interrogative</td>
    </tr>
    <tr>
      <td>intrans.</td>
      <td>intransitive</td>
    </tr>
    <tr>
      <td>IT</td>
      <td><i>Indologica Taurinensia</i>, Torino</td>
    </tr>
    <tr>
      <td>JAOS</td>
      <td><i>Journal of the American Oriental Society</i>, New Haven</td>
    </tr>
    <tr>
      <td>JAs</td>
      <td><i>Journal Asiatique</i>, Paris</td>
    </tr>
    <tr>
      <td>JOI(B)</td>
      <td><i>Journal of the Oriental Institute</i>, Baroda</td>
    </tr>
    <tr>
      <td>JPTS</td>
      <td><i>Journal of the Pali Text Society</i>, London, et al.</td>
    </tr>
    <tr>
      <td>JRAS</td>
      <td><i>Journal of the Royal Asiatic Society</i>, London</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>karmadh.</td>
      <td>karmadhāraya compound</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>lex.</td>
      <td>lexica</td>
    </tr>
    <tr>
      <td>lit.</td>
      <td>literally</td>
    </tr>
    <tr>
      <td>loc.</td>
      <td>locative</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>m.</td>
      <td>masculine</td>
    </tr>
    <tr>
      <td>mc</td>
      <td>metri causa</td>
    </tr>
    <tr>
      <td>metaph.</td>
      <td>metaphorical(ly)</td>
    </tr>
    <tr>
      <td>mfn.</td>
      <td>masculine, feminine and neuter, i.e., adjective</td>
    </tr>
    <tr>
      <td>ms(s)</td>
      <td>manuscript(s)</td>
    </tr>
    <tr>
      <td>MSS</td>
      <td><i>Münchener Studien zur Sprachwissenschaft</i>, München</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>n.</td>
      <td>neuter</td>
    </tr>
    <tr>
      <td>neg.</td>
      <td>negative</td>
    </tr>
    <tr>
      <td>nom.</td>
      <td>nominative</td>
    </tr>
    <tr>
      <td>Npr.</td>
      <td>proper name</td>
    </tr>
    <tr>
      <td>num.</td>
      <td>numeral</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>onomat.</td>
      <td>onomatopoeic</td>
    </tr>
    <tr>
      <td>opp.</td>
      <td>opposite (in meaning to)</td>
    </tr>
    <tr>
      <td>opt.</td>
      <td>optative</td>
    </tr>
    <tr>
      <td>orig.</td>
      <td>original(ly)</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>p., pp.</td>
      <td>page(s)</td>
    </tr>
    <tr>
      <td>part.</td>
      <td>participle</td>
    </tr>
    <tr>
      <td>part.pr.</td>
      <td>present participle</td>
    </tr>
    <tr>
      <td>pass.</td>
      <td>passive</td>
    </tr>
    <tr>
      <td>perf.</td>
      <td>perfect</td>
    </tr>
    <tr>
      <td>pers.</td>
      <td>personae (of the person)</td>
    </tr>
    <tr>
      <td>Pkt</td>
      <td>Prakrit</td>
    </tr>
    <tr>
      <td>pl.</td>
      <td>plural</td>
    </tr>
    <tr>
      <td>poss.</td>
      <td>possibly</td>
    </tr>
    <tr>
      <td>postp.</td>
      <td>postposition</td>
    </tr>
    <tr>
      <td>pp</td>
      <td>past participle</td>
    </tr>
    <tr>
      <td>pr.</td>
      <td>present</td>
    </tr>
    <tr>
      <td>prep.</td>
      <td>preposition</td>
    </tr>
    <tr>
      <td>prob.</td>
      <td>probably</td>
    </tr>
    <tr>
      <td>pron.</td>
      <td>pronoun</td>
    </tr>
    <tr>
      <td>PTS</td>
      <td>Pali Text Society</td>
    </tr>
    <tr>
      <td>qv, qvv</td>
      <td>which see</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>redupl.</td>
      <td>reduplicated</td>
    </tr>
    <tr>
      <td>rel.</td>
      <td>relative</td>
    </tr>
    <tr>
      <td>repr.</td>
      <td>reprint(ed)</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>S.</td>
      <td>Sanskrit</td>
    </tr>
    <tr>
      <td>SAF</td>
      <td>= J. Liyanaratne, 1994</td>
    </tr>
    <tr>
      <td>scil.</td>
      <td>scilicet (understand, supply)</td>
    </tr>
    <tr>
      <td>Se</td>
      <td>Thai edition, BUDSIR IV, Bangkok 1997 (CD-ROM)</td>
    </tr>
    <tr>
      <td>sg.</td>
      <td>singular</td>
    </tr>
    <tr>
      <td>Sinh.</td>
      <td>Sinhalese</td>
    </tr>
    <tr>
      <td>subj.</td>
      <td>subjunctive</td>
    </tr>
    <tr>
      <td>subst.</td>
      <td>substantive</td>
    </tr>
    <tr>
      <td>superl.</td>
      <td>superlative</td>
    </tr>
    <tr>
      <td>sv, svv</td>
      <td>sub verbo (under that word), sub verbis (under these words)</td>
    </tr>
    <tr>
      <td>SWTF</td>
      <td><i>Sanskrit-Wörterbuch der buddhistischen Texte aus den Turfanfunden und der kanonischen Literatur der Sarvāstivāda-Schule.</i> Begonnen von Ernst Waldschmidt [...] herausgegeben von Heinz Bechert [et al.], Göttingen 1973–2018
      </td>
    </tr>
    <tr>
      <td>Ta</td>
      <td>Tamil</td>
    </tr>
    <tr>
      <td>tatp.</td>
      <td>tatpuruṣa compound</td>
    </tr>
    <tr>
      <td>trans.</td>
      <td>transitive</td>
    </tr>
    <tr>
      <td>ts</td>
      <td>tatsama (same as Sanskrit)</td>
    </tr>
    <tr>
      <td>t.t.</td>
      <td>technical term</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Ved.</td>
      <td>Vedic Sanskrit</td>
    </tr>
    <tr>
      <td>VHGS</td>
      <td>Veröffentlichungen der Helmuth von Glasenapp-Stiftung, Wiesbaden</td>
    </tr>
    <tr>
      <td>Vinmu</td>
      <td>= Vajirañāṇavarorasa, 1969–83</td>
    </tr>
    <tr>
      <td>vl, vll</td>
      <td>varia lectio,variae lectiones (variant reading[s])</td>
    </tr>
    <tr>
      <td>voc.</td>
      <td>vocative</td>
    </tr>
    <tr>
      <td>vol., vols</td>
      <td>volume(s)</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>wr, wrr</td>
      <td>wrong reading(s)</td>
    </tr>
    <tr>
      <td>Wg</td>
      <td>= N.L. Westergaard, 1841</td>
    </tr>
    <tr>
      <td>WZKS(O)</td>
      <td><i>Wiener Zeitschrift für die Kunde Süd- (und Ost)asiens</i>, Wien</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>ZVS</td>
      <td><i>Zeitschrift für Vergleichende Sprachforschung</i>, Berlin, et al.</td>
    </tr>
  </tbody></table>

  <h4>Note that:</h4>
  <table>
    <tbody><tr>
      <td>°</td>
      <td>represents the head-word of the article</td>
    </tr>
    <tr>
      <td>~</td>
      <td>represents the stem of the nearest preceding word in bold character</td>
    </tr>
    <tr>
      <td>*</td>
      <td>denotes the quotation is from a verse portion of the text</td>
    </tr>
    <tr>
      <td>**</td>
      <td>denotes the quotation is from a portion of the text in the veḍha metre</td>
    </tr>
    <tr>
      <td>´</td>
      <td>after a Ja reference: denotes the quotation is from the word commentary</td>
    </tr>
    <tr>
      <td>=</td>
      <td>stands between identical passages</td>
    </tr>
    <tr>
      <td>≠</td>
      <td>stands between parallel, not quite identical, passages</td>
    </tr>
  </tbody></table>

  <h3>Order of the Pāli letters</h3>
  <p>
    a ā i ī u ū e o<br>
    ṃ<br>
    k kh g gh ṅ<br>
    c ch j jh ñ<br>
    ṭ ṭh ḍ ḍh ṇ<br>
    t th d dh n<br>
    p ph b bh m<br>
    y r l ḷ ḷh v<br>
    s h
  </p>
  <p>
    The <i>anusvāra</i> (the pure nasal <i>ṃ</i>) does not change before <i>y, r, l, v, s,</i> and <i>h</i>; and in that position it comes before all other consonants in the alphabetical order. For example, <i>saṃvara</i> and <i>saṃsaya</i> come before <i>saka</i>.
  </p>
  <p>
    Before other consonants, <i>ṃ</i> may change to the class nasal, i.e. that in the same line in the table above. For example, <i>-ṃk-</i> may be written <i>-ṅk-</i>, <i>-ṃc-</i> may be written <i>-ñc-</i>, etc. Thus <i>saṃgha</i> is the same as <i>saṅgha</i>, <i>saṃcaya</i> as <i>sañcaya</i>, etc. Even when the <i>anusvāra</i> is written in that position, its place in the alphabetical order is that of the equivalent class nasal.
  </p>
</div>
"""

foreword_html = """
<div>
	<div class="title"><span class="title">A Dictionary of Pāli</span></div>
	<div class="byline">
		Texts, Works Cited, Abbreviations, and Symbols<br>
		Parts I–III combined, revised by Martin Straube
	</div>

	<h3>Foreword to the digital edition</h3>
	<p>
		The first modern Pali-English dictionary was Robert Childers’ A Dictionary of the Pali Language, published in two volumes (1872–1875). T.W. Rhys Davids and William Stede’s The Pali Text Society’s Pali-English Dictionary (1921–1925) took as its starting point Childers’ dictionary and was fifty years in the making. In his foreword Rhys Davids commented: ‘This work is essentially preliminary.’
	</p>
	<p>
		A project to provide a comprehensive Pali dictionary in the form of the Copenhagen A Critical Pāli Dictionary dates from the early decades of the twentieth century, but through lack of secure funding this came to an end in 2011 with the publication of a third volume in 2011, ending with the word karetu-kama. Hence A Critical Pāli Dictionary covers no more than a third of the Pali lexicon.
	</p>
	<p>
		Alongside the Copenhagen project, the Pali Text Society has been working on revising Rhys Davids and Stede’s dictionary for fifty years. Since 1984, using funds bequeathed to the Society by I.B. Horner (1896–1981), the Society has funded a full-time research fellow to work on this project. From 1984 to 2018 this position was occupied by Dr Margaret Cone. While the original plan was to revise the PTS’s 1925 dictionary and produce a second edition, it became apparent that so little of the original dictionary would remain unaltered that what was actually being undertaken was the production of a completely new dictionary. This has become A Dictionary of Pāli. Part one of this dictionary, covering the letters a–kh was published by the Pali Text Society in 2001, part two, covering the letters g–n, in 2010, and part three, covering the letters p–bh, in 2020. Since 2018 the Society has funded Dr Martin Straube to continue Dr Cone’s work on the Dictionary by working on volume 4, the final volume.
	</p>
	<p>
	  Writing in 1995 about the prospects for the publication of Pali dictionaries, K.R. Norman suggested that when the new dictionary was eventually published the PTS would likely keep the old single-volume 1925 dictionary in print at a subsidised price for the benefit of students who could not afford the new dictionary. The advent of online publishing in the intervening years means that the problem of access to expensive scholarly resources for students and others can be readily solved by online publication: the 1925 Pali-English Dictionary is now available online via several websites, as is also <a href="https://cpd.uni-koeln.de/">A Critical Pāli Dictionary</a>. The PTS has now facilitated the translation of the first three volumes of A Dictionary of Pāli into a digital format for publication online. In keeping with its aim to promote the study of Pali literature, the Pali Text Society is happy to make this new dictionary freely available online on the gandhari.org site for the benefit of students and scholars. Despite all efforts to ensure a correct reproduction of the printed volumes, errors may have crept into the online edition. Users are therefore requested to consult the printed volumes in cases of doubt.
	</p>
	<p>
		T.W. Rhys Davids’ words at the end of his foreword to the 1925 dictionary apply equally to the current dictionary:
	</p>
	<p>
		‘Anybody familiar with this sort of work will know what care and patience, what scholarly knowledge and judgment are involved in the collection of such material, in the sorting, the sifting and final arrangement of it, in the adding of cross references, in the consideration of etymological puzzles, in the comparison and correction of various or faulty readings, and in the verification of references given by others, or found in the indexes.’
	</p>
	<p>
		Anyone wishing to learn more about the Pali Text Society, purchase its publications (including A Dictionary of Pāli) or support its projects by becoming a member is invited to visit its website <a href="palitextsociety.org">palitextsociety.org</a>.
	</p>

	<h3>Foreword to the print edition</h3>
	<p>
		The first Pāli-English dictionary, published in two volumes in 1872 and 1875, was the work of Robert Caesar Childers. His main soure was <i>Abhidhānappadīpikā,</i> a dictionary in Pāli, probably of the late 12th century, which was itself based on the Sanskrit <i>Amarakośa</i>. He was able to consult Singhalese bhikkhus, but had access to very few Pāli texts. Even so, his dictionary is an admirable work and a considerable achievement for its time.
	</p>
	<p>
		As European knowledge of Pāli texts grew, Childers’ dictionary became unsatisfactory, and one of the aims of Thomas William Rhys Davids, the founder of the Pāli Text Society, was to produce a Pāli-English dictionary better able to serve the needs of those wishing to read or indeed edit Pāli texts. In the early years of the last century he tried to find scholars throughout Europe to co-operate in producing such a dictionary, but he met various setbacks and disappointments, and after the First World War had ended most hopes of international co-operation, he at last decided that he himself would launch what he thought of as a provisional dictionary, with Dr. William Stede as co-editor, and using some material provided by other scholars. This invaluable dictionary was published from 1921–1925.
	</p>
	<p>
		Meanwhile, in Copenhagen, Dines Andersen and Helmer Smith had begun to produce the Critical Pāli Dictionary, the first fascicle of which appeared in 1924. They had the benefit of the work of Carl Wilhelm Trenckner (1824–1891), who, while making transcripts of most of the Pāli manuscripts in the rich Copenhagen Collection, and of others from London, had made preparations for a dictionary, writing small paper-slips containing words and references, observations on grammar and syntax, and quotations illustrating secular and daily life. Andersen and Smith possessed a wide knowledge of Pāli combined with expertise in philology, in grammar, in Sanskrit and in other Indo-Aryan languages, and they laid strong and solid foundations for the Critical Pāli Dictionary. It is a giant work, an exhaustive dictionary, and for any serious Pali scholar, indispensable. Fascicles continue to be produced, but it will be many years before it is completed.
	</p>
	<p>
		In the Foreword to the first fascicle of the Pāli Text Society’s dictionary, Rhys Davids wrote:
	</p>
	<div class="introquote">
		<p>
			‘It has been decided … to reserve the proceeds of the sale [of the first edition] for the eventual issue of a second edition which shall come nearer to our ideals of what a Pāli Dictionary should be.’
		</p>
	</div>
	<p>
		This was the task I began several years ago. Within a very short time I realised that so little could be left unaltered that I had to produce a completely new dictionary, not a revision of the existing one. Rhys Davids’ dictionary is only one of my sources, although an important one. The dictionary does however remain essentially a dictionary of the texts published by the Pāli Text Society.
	</p>
	<p>
		This dictionary has two main aims: first, to help its user read and understand the Pāli Canon and its commentaries; and second, to provide a picture of the language, syntax, and even grammar of these texts.
	</p>
	<p>
		To achieve the first aim, I have tried to define all the words which appear in the texts in so far as that is possible given the fallibility of even the most recent technological aids and the limits of human capability. For the second, I have extensively used quotation to illustrate meaning, rather than providing mere references, and have given detailed information on declension and especially on parts of verbs. As a secondary aim was to produce a relatively concise dictionary, there are some things this dictionary is not. It is not an etymological dictionary, its primary reference being to Sanskrit. It is not a concordance, but quotes selectively. I have tried to show the range of texts in which a word appears, but the emphasis is on canonical texts, with less reference to commentaries. Not every compound is listed, only those where the members do not appear independently, or where the meaning might not be immediately apparent. Negative forms and many forms with <i>su-, du(r)-</i> or <i>ni(r)-</i> are given under the primary word.
	</p>
	<p>
		The writing of this dictionary presented two main difficulties. The first is that it proved impossible to be sure of the meaning of some words, where etymology and context were not sufficient to produce certainty. There are, therefore, more queries remaining than one would like. The second difficulty concerns the texts themselves. It is likely that most users of this dictionary will also be using mainly the editions of the Pāli Text Society. The majority of these editions were made many years ago, sometimes from only one or a very few manuscripts, by editors who had little help to aid their decisions. The consequence is a considerable number of doubtful readings. I have therefore very often quoted from the Burmese, Singhalese and Thai editions. Sometimes it is possible to express a preference for one or the other reading, sometimes each reading could be justified, sometimes no reading is really convincing. I give these alternative readings so that the reader may consider and choose, and to point out the fallibility of all editions.
	</p>
	<p>
		I have tried to give the quotations as they appear in the texts, but I have regularised some spellings: whatever the edition has, I always write final <i>anusvāra</i> (eg <i>~aṃ ca,</i> not <i>~añ ca; ~aṃ yeva,</i> not <i>~aññeva</i>), and <i>vy-</i> (not <i>by-</i>).
	</p>
	<p>
		It hardly needs to be said that I, as any writer of a dictionary, depend on the work of previous and present scholars, in particular of the writers of the Pāli Text Society’s first Pāli-English Dictionary and of the continuing Critical Pāli Dictionary. Generally I make no acknowledgement to these scholars in the articles of the dictionary, but I do so now, for my debt to them is great.
	</p>
	<p class="right">
		Margaret Cone<br>
	</p>
	<p class="left">
		Darwin College<br>
		Cambridge<br>
		2001<br>
	</p>
</div>"""

references_html = """
<div>
  <div class="title"><span class="title">A Dictionary of Pāli</span></div>
  <div class="byline">Texts, Works Cited, Abbreviations, and Symbols<br>
    Parts I–III combined, revised by Martin Straube</div>
  <h3>Texts</h3>
  <p>(references are to vol., page, and line unless otherwise specified)</p>
  <table>
    <tbody><tr>
      <td>A</td>
      <td>Aṅguttaranikāya, ed. R. Morris, E. Hardy, PTS, London 1885–1900 (Ee<sup>1</sup>). — A I Ee<sup>2</sup> revised A.K. Warder, PTS, Oxford 1961
      </td>
    </tr>
    <tr>
      <td>Abh</td>
      <td>Abhidhānappadīpikā, ed. W. Subhūti, 3rd ed., Colombo 1900</td>
    </tr>
    <tr>
      <td>Abhidh‑av</td>
      <td>Abhidhammāvatāra, ed. A.P. Buddhadatta, PTS, London 1915</td>
    </tr>
    <tr>
      <td>Abh-sūci</td>
      <td>Abhidhānasūcī, index and notes to Abh, W. Subhūti, Colombo 1893</td>
    </tr>
    <tr>
      <td>Anāg</td>
      <td>Anāgatavaṃsa (including parts of Anāg-a), ed. J. Minayeff, <i>JPTS</i>, 1886, pp. 1–37</td>
    </tr>
    <tr>
      <td>Anāg-a</td>
      <td>Samantabhaddikā (Anāgatavaṃsa-aṭṭhakathā); see Anāg</td>
    </tr>
    <tr>
      <td>Ap</td>
      <td>Apadāna, ed. M.E. Lilley, PTS, London 1925–27</td>
    </tr>
    <tr>
      <td>Ap-a</td>
      <td>Visuddhajanavilāsinī (Apadāna-aṭṭhakathā), ed. C.E. Godakumbura, PTS, London 1954</td>
    </tr>
    <tr>
      <td>Āp.Śr.</td>
      <td>Āpastamba’s Śrautasūtra</td>
    </tr>
    <tr>
      <td>As</td>
      <td>Atthasālinī, ed. E. Müller, PTS, London 1897</td>
    </tr>
    <tr>
      <td>As-mṭ</td>
      <td>Dhammasaṅgaṇī-mūlaṭīkā, Rangoon 1960</td>
    </tr>
    <tr>
      <td>Aup</td>
      <td>Aupapātika Sūtra, ed. E. Leumann, Leipzig 1883</td>
    </tr>
    <tr>
      <td>AV</td>
      <td>Atharva-Veda</td>
    </tr>
    <tr>
      <td>Bhī Vin</td>
      <td>Bhikṣuṇī-Vinaya, ed. G. Roth, Patna 1970</td>
    </tr>
    <tr>
      <td>Buddha-c</td>
      <td>Buddhacarita, ed. E.H. Johnston, Calcutta 1935–36</td>
    </tr>
    <tr>
      <td>Bv</td>
      <td>Buddhavaṃsa, ed. N.A. Jayawickrama, PTS, London 1974 (by poem and verse)</td>
    </tr>
    <tr>
      <td>Bv-a</td>
      <td>Madhuratthavilāsinī (Buddhavaṃsa-aṭṭhakathā), ed. I.B. Horner, PTS, London 1946</td>
    </tr>
    <tr>
      <td>Cp</td>
      <td>Cariyāpiṭaka, ed. N.A. Jayawickrama, PTS, London 1974 (by vagga, poem and verse)</td>
    </tr>
    <tr>
      <td>Cp-a</td>
      <td>Paramatthadīpanī VII (Cariyāpiṭaka-aṭṭhakathā), ed. D.L. Barua, 2nd ed., PTS, London 1979</td>
    </tr>
    <tr>
      <td>D</td>
      <td>Dīghanikāya, ed. T.W. Rhys Davids, J.E. Carpenter, PTS, London 1890–1911</td>
    </tr>
    <tr>
      <td>Dāṭh</td>
      <td>Dāṭhāvaṃsa, ed. T.W. Rhys Davids, R. Morris, <i>JPTS</i>, 1884, pp. 109–151 (by chapter and verse)</td>
    </tr>
    <tr>
      <td>Dhātuk</td>
      <td>The Dhātukathāpakaraṇa and its commentary (Ppk-a I), ed. E.R. Gooneratne, PTS, London 1892</td>
    </tr>
    <tr>
      <td>Dhātuk-a</td>
      <td>included in Dhātuk</td>
    </tr>
    <tr>
      <td>Dhātum</td>
      <td>Dhātumañjūsā, see Dhātup</td>
    </tr>
    <tr>
      <td>Dhātup</td>
      <td>The Pāli Dhātupāṭha and the Dhātumañjūsā, ed. D. Andersen, H. Smith, København 1921 (by root-number)</td>
    </tr>
    <tr>
      <td>Dhp</td>
      <td>Dhammapada, ed. O. von Hinüber, K.R. Norman, PTS, Oxford 1994 (by verse)</td>
    </tr>
    <tr>
      <td>Dhp-a</td>
      <td>Dhammapada-aṭṭhakathā, ed. H.C. Norman, PTS, London 1906–14</td>
    </tr>
    <tr>
      <td>Dhs</td>
      <td>Dhammasaṅgaṇī, ed. E. Müller, PTS, London 1885</td>
    </tr>
    <tr>
      <td>Dīp</td>
      <td>Dīpavaṃsa, ed. and translated H. Oldenberg, London 1879 (by chapter and verse)</td>
    </tr>
    <tr>
      <td>Dukap</td>
      <td>Dukapaṭṭhāna, ed C.A.F. Rhys Davids, PTS, London 1906</td>
    </tr>
    <tr>
      <td>GDhp</td>
      <td>Gāndhārī Dharmapada, ed. J. Brough, London 1962</td>
    </tr>
    <tr>
      <td>Gv</td>
      <td>Gaṇḍavyūha, ed. D. T. Suzuki, H. Idzumi, Kyoto 1934–36</td>
    </tr>
    <tr>
      <td>It</td>
      <td>Itivuttaka, ed. E. Windisch, PTS, London 1889</td>
    </tr>
    <tr>
      <td>It-a</td>
      <td>Paramatthadīpanī II (Itivuttaka-aṭṭhakathā), ed. M.M. Bose, PTS, London 1934–36</td>
    </tr>
    <tr>
      <td>Ja</td>
      <td>The Jātaka together with its commentary, ed. V. Fausbøll, London 1877–96</td>
    </tr>
    <tr>
      <td>Jina-c</td>
      <td>Jinacarita, ed. W.H.D. Rouse, <i>JPTS</i>, 1904–05, pp. 1–31 (by verse)</td>
    </tr>
    <tr>
      <td>Jinak</td>
      <td>Jinakālamālī, ed. A.P. Buddhadatta, PTS, London 1962</td>
    </tr>
    <tr>
      <td>Jināl</td>
      <td>Jinālaṅkāra, ed. J. Gray, London 1894</td>
    </tr>
    <tr>
      <td>Jm</td>
      <td>Jātakamālā of Āryaśūra, ed. H. Kern, Cambridge, Mass. 1943</td>
    </tr>
    <tr>
      <td>Kacc</td>
      <td>Kaccāyanapakaraṇa, ed. É. Senart, <i>JAs</i>, 1871, pp. 1–339</td>
    </tr>
    <tr>
      <td>Kāś</td>
      <td>Kāśikā, ed. A. Sharma, K. Deshpande, D.G. Padye, Hyderabad 1969–70</td>
    </tr>
    <tr>
      <td>Khp</td>
      <td>Khuddakapāṭha, ed. H. Smith, PTS, London 1915 (by poem and verse)</td>
    </tr>
    <tr>
      <td>Kkh, Kkh<sup>1</sup></td>
      <td>Kaṅkhāvitaraṇī, ed. D. Maskell, PTS, London 1981</td>
    </tr>
    <tr>
      <td>Kkh<sup>2</sup></td>
      <td>Kaṅkhāvitaraṇī, ed. K.R. Norman, W. Pruitt, PTS, Oxford 2003</td>
    </tr>
    <tr>
      <td>Khuddas</td>
      <td>Khuddasikkhā, ed. E. Müller, <i>JPTS</i>, 1883, pp. 86–121 (by chapter and verse)</td>
    </tr>
    <tr>
      <td>Kv</td>
      <td>Kathāvatthu, ed. A.C. Taylor, PTS, London 1894</td>
    </tr>
    <tr>
      <td>Kv-a</td>
      <td>Kathāvatthu-aṭṭhakathā (Ppk-a III), ed. N.A. Jayawickrama, PTS, London 1979</td>
    </tr>
    <tr>
      <td>M</td>
      <td>Majjhimanikāya, ed. V. Trenckner, R. Chalmers, PTS, London 1887–1902. — M II Ee<sup>2</sup>: re-typeset repr. W. Pruitt, PTS, Bristol 2016</td>
    </tr>
    <tr>
      <td>Mhbh</td>
      <td>Mahābhārata, ed. V.S. Sukthankar, et al., Poona 1933–72</td>
    </tr>
    <tr>
      <td>Mhbv</td>
      <td>Mahābodhivaṃsa, ed. S.A. Strong, PTS, London 1891</td>
    </tr>
    <tr>
      <td>Mhv</td>
      <td>Mahāvaṃsa and ‘Cūlavaṃsa’. Mhv 1:1–37:50 ed. W. Geiger, PTS, London 1908; Mhv 37:51 foll. (‘Cūlavaṃsa’) ed. W. Geiger, PTS, London 1925–27 (by chapter and verse)</td>
    </tr>
    <tr>
      <td>Mhv-ṭ</td>
      <td>Vaṃsatthapakāsinī (Mahāvaṃsa commentary), ed. G.P. Malalasekera, PTS, London 1977</td>
    </tr>
    <tr>
      <td>Mil</td>
      <td>Milindapañha, ed. V. Trenckner, PTS, London 1880</td>
    </tr>
    <tr>
      <td>Mil-ṭ</td>
      <td>Milindaṭīkā, ed. P.S. Jaini, PTS, London 1961</td>
    </tr>
    <tr>
      <td>Moh</td>
      <td>Mohavicchedanī, ed. A.P. Buddhadatta, A.K. Warder, PTS, London 1961</td>
    </tr>
    <tr>
      <td>Mp</td>
      <td>Manorathapūraṇī (Aṅguttaranikāya-aṭṭhakathā), ed. M. Walleser, H. Kopp, PTS, London 1936–57</td>
    </tr>
    <tr>
      <td>Mp-ṭ</td>
      <td>Sāratthamañjūsā IV (ṭīkā on Mp), Ekanipāta- and Dukanipāta-ṭīkā ed. P. Pecenko, PTS, Oxford 1996–99 (Ee). — Be Rangoon 1961</td>
    </tr>
    <tr>
      <td>MPS</td>
      <td>Mahāpariṇirvāṇasūtra, ed. E. Waldschmidt, Berlin 1950–51</td>
    </tr>
    <tr>
      <td>Mvu</td>
      <td>Mahāvastu, ed. É. Senart, Paris 1882–97</td>
    </tr>
    <tr>
      <td>Nāmar-p</td>
      <td>Nāmarūpapariccheda, ed. A.P. Buddhadatta, <i>JPTS</i>, 1914, pp. 1–114</td>
    </tr>
    <tr>
      <td>Nett</td>
      <td>Nettipakaraṇa, ed. E. Hardy, PTS, London 1902</td>
    </tr>
    <tr>
      <td>Nett-a</td>
      <td>Nettippakaraṇa-atthakathā, ed. Widuropola Piyatissa Thera, Colombo 1921</td>
    </tr>
    <tr>
      <td>Nidd I</td>
      <td>Mahāniddesa, ed. L. de La Vallée Poussin, E. J. Thomas, PTS, London 1978</td>
    </tr>
    <tr>
      <td>Nidd II</td>
      <td>Cullaniddesa, ed. W. Stede, PTS, London 1916</td>
    </tr>
    <tr>
      <td>Nidd-a I</td>
      <td>Saddhammapajjotikā, vol. I, II (Mahāniddesa-aṭṭhakathā), ed. A.P. Buddhadatta, PTS, London 1931, 1939</td>
    </tr>
    <tr>
      <td>Nidd-a II</td>
      <td>Saddhammapajjotikā, vol. III (Cullaniddesa-aṭṭhakathā), ed. A.P. Buddhadatta, PTS, London 1940</td>
    </tr>
    <tr>
      <td>Pāṇ</td>
      <td>Aṣṭādhyāyī of Pāṇini, ed. O. Böhtlingk, Leipzig 1887</td>
    </tr>
    <tr>
      <td>Pañca-g</td>
      <td>Pañcagatidīpanī, ed. M.L. Feer, <i>JPTS</i>, 1884, pp. 152–161 (by verse)</td>
    </tr>
    <tr>
      <td>Paṭis</td>
      <td>Paṭisambhidāmagga, ed. A.C. Taylor, PTS, London 1905–1907</td>
    </tr>
    <tr>
      <td>Paṭis-a</td>
      <td>Saddhammappakāsinī (Paṭisambhidāmagga-aṭṭhakathā), ed. C.V. Joshi, PTS, London 1979</td>
    </tr>
    <tr>
      <td>PDhp</td>
      <td>Patna Dharmapada, ed. M. Cone, <i>JPTS</i>, 13, 1989, pp. 101–217</td>
    </tr>
    <tr>
      <td>Peṭ</td>
      <td>Peṭakopadesa, ed. A. Barua, PTS, London 1949</td>
    </tr>
    <tr>
      <td>Pj I</td>
      <td>Paramatthajotikā I (Khuddakapāṭha-aṭṭhakathā), ed. H. Smith, PTS, London 1915</td>
    </tr>
    <tr>
      <td>Pj II</td>
      <td>Paramatthajotikā II (Suttanipāta-aṭṭhakathā), ed. H. Smith, PTS, London 1916–18</td>
    </tr>
    <tr>
      <td>Pp</td>
      <td>Puggalapaññatti, ed. R. Morris, PTS, London 1883, repr. together with Pp-a, London 1972</td>
    </tr>
    <tr>
      <td>Pp-a</td>
      <td>Puggalapaññatti-aṭṭhakathā (Ppk-a II), ed. G. Landsberg, C.A.F. Rhys Davids (<i>JPTS</i>, 1913, pp. 170–254), included in Pp</td>
    </tr>
    <tr>
      <td>Ppk-a</td>
      <td>Pañcappakaraṇa-aṭṭhakathā</td>
    </tr>
    <tr>
      <td>Ps</td>
      <td>Papañcasūdanī (Majjhimanikāya-aṭṭhakathā), ed. J.H. Woods, D. Kosambi, I.B. Horner, PTS, London 1933–38</td>
    </tr>
    <tr>
      <td>Ps-ṭ</td>
      <td>Līnatthappakāsanī II (ṭīkā on Ps), Rangoon 1961</td>
    </tr>
    <tr>
      <td>Pv</td>
      <td>Petavatthu, ed. N.A. Jayawickrama, PTS, London 1977 (by poem and verse)</td>
    </tr>
    <tr>
      <td>Pv-a</td>
      <td>Paramatthadīpanī IV (Petavatthu-aṭṭhakathā). Ee1 ed. E. Hardy, PTS, London 1894. — Ee<sup>2</sup> The Burmese edition, with other editions collated by P. Jackson, PTS, Bristol 2019</td>
    </tr>
    <tr>
      <td>ṚV</td>
      <td>Ṛgveda-saṃhitā</td>
    </tr>
    <tr>
      <td>S</td>
      <td>Saṃyuttanikāya, ed. M.L. Feer, PTS, London 1884–98. — S I Ee<sup>2</sup> ed. G. A. Somaratne, PTS, Oxford 1998</td>
    </tr>
    <tr>
      <td>Sadd</td>
      <td>Saddanīti, ed. H. Smith, Lund 1928–54</td>
    </tr>
    <tr>
      <td>Saddh</td>
      <td>Saddhammopāyana, ed. R. Morris, <i>JPTS</i>, 1887, pp. 35–98 (by verse)</td>
    </tr>
    <tr>
      <td>Samantak</td>
      <td>Samantakūṭavaṇṇanā, ed. C.E. Godakumbura, PTS, London 1958 (by verse)</td>
    </tr>
    <tr>
      <td>Sās</td>
      <td>Sāsanavaṃsa, ed. M. Bode, PTS, London 1897</td>
    </tr>
    <tr>
      <td>S. Dhātup</td>
      <td>Sanskrit Dhātupāṭha, in N.L. Westergaard, 1841</td>
    </tr>
    <tr>
      <td>Śikṣ</td>
      <td>Śikṣāsamuccaya, ed. C. Bendall, St. Pétersbourg 1897–1902</td>
    </tr>
    <tr>
      <td>Sn</td>
      <td>Suttanipāta, ed. D. Andersen, H. Smith, PTS, London 1913 (by verse)</td>
    </tr>
    <tr>
      <td>Sp</td>
      <td>Samantapāsādikā (Vinaya-aṭṭhakathā), ed. J. Takakusu, M. Nagai, PTS, London 1924–47</td>
    </tr>
    <tr>
      <td>Spk</td>
      <td>Sāratthappakāsinī (Saṃyuttanikāya-aṭṭhakathā), ed. F.L. Woodward, PTS, London 1929–37</td>
    </tr>
    <tr>
      <td>Spk-ṭ</td>
      <td>Līnatthappakāsanī III (ṭīkā on Spk), Rangoon 1961</td>
    </tr>
    <tr>
      <td>Sp-ṭ</td>
      <td>Sāratthadīpanī (ṭīkā on Sp), Rangoon 1960</td>
    </tr>
    <tr>
      <td>Subodh</td>
      <td>Subodhālaṅkāra, ed. P.S. Jaini, PTS, Oxford 2000 </td>
    </tr>
    <tr>
      <td>Subodh-ṭ</td>
      <td>Porāṇaṭīkā on Subodhālaṅkāra ed. P.S. Jaini, PTS, Oxford 2000</td>
    </tr>
    <tr>
      <td>Sv</td>
      <td>Sumaṅgalavilāsinī (Dīghanikāya-aṭṭhakathā), ed. T.W. Rhys Davids, J.E. Carpenter, PTS, London 1886–1932</td>
    </tr>
    <tr>
      <td>TB</td>
      <td>Taittirīya Brāhmaṇa</td>
    </tr>
    <tr>
      <td>Tel</td>
      <td>Telakaṭāhagātha, ed. E.R. Goonaratne, <i>JPTS</i>, 1884, pp. 49–68 (by verse)</td>
    </tr>
    <tr>
      <td>Th</td>
      <td>Theragāthā and Therīgāthā, ed. H. Oldenberg, R. Pischel, 2nd ed. with appendices by K.R. Norman, L. Alsdorf, PTS, London 1966 (by verse)</td>
    </tr>
    <tr>
      <td>Th-a</td>
      <td>Paramatthadīpanī V (Theragāthā-aṭṭhakathā), ed. F.L. Woodward, PTS, London 1940–59</td>
    </tr>
    <tr>
      <td>Thī</td>
      <td>Therīgāthā, see Th</td>
    </tr>
    <tr>
      <td>Thī-a</td>
      <td>Paramatthadīpanī VI (Therīgāthā-aṭṭhakathā), ed. W. Pruitt, PTS, Oxford 1998</td>
    </tr>
    <tr>
      <td>Thūp</td>
      <td>Thūpavaṃsa, ed. N.A. Jayawickrama, PTS, London 1971</td>
    </tr>
    <tr>
      <td>Tikap</td>
      <td>Tikapaṭṭhāna, ed. C.A.F. Rhys Davids, PTS, London 1921</td>
    </tr>
    <tr>
      <td>Tikap-a</td>
      <td>Tikapaṭṭhāna-aṭṭhakathā (Ppk-a V), ed. C.A.F. Rhys Davids, PTS, London 1921</td>
    </tr>
    <tr>
      <td>Ud</td>
      <td>Udāna, ed. P. Steinthal, PTS, London 1885</td>
    </tr>
    <tr>
      <td>Ud-a</td>
      <td>Paramatthadīpanī I (Udāna-aṭṭhakathā), ed. F.L. Woodward, PTS, London 1926</td>
    </tr>
    <tr>
      <td>Udāna-v</td>
      <td>Udānavarga, ed. F. Bernhard, Göttingen 1965</td>
    </tr>
    <tr>
      <td>Utt</td>
      <td>Uttarādhyayanasūtra, ed. J. Charpentier, Uppsala 1922</td>
    </tr>
    <tr>
      <td>Utt-vn</td>
      <td>Uttaravinicchaya, ed. A.P. Buddhadatta, PTS, London 1927 (by verse)</td>
    </tr>
    <tr>
      <td>Vibh</td>
      <td>Vibhaṅga, ed. C.A.F. Rhys Davids, PTS, London 1904</td>
    </tr>
    <tr>
      <td>Vibh-a</td>
      <td>Sammohavinodanī (Vibhaṅga-aṭṭhakathā), ed. A.P. Buddhadatta, PTS, London 1923</td>
    </tr>
    <tr>
      <td>Vin</td>
      <td>Vinayapiṭaka, ed. H. Oldenberg, London 1879–83</td>
    </tr>
    <tr>
      <td>Vin-vn</td>
      <td>Vinayavinicchaya, ed. A.P. Buddhadatta, PTS, London 1927 (by verse)</td>
    </tr>
    <tr>
      <td>Vism</td>
      <td>Visuddhimagga, ed. C.A.F. Rhys Davids, PTS, London 1920–21 (Ee). — HOS ed. H.C. Warren, revised by D. Kosambi, Cambridge, Mass., 1950</td>
    </tr>
    <tr>
      <td>Vism-mhṭ</td>
      <td>Paramatthamañjusā (Visuddhimagga-mahāṭīkā), Rangoon 1960</td>
    </tr>
    <tr>
      <td>Vjb</td>
      <td>Vajirabuddhi-ṭīkā (ṭīkā on Sp), Rangoon 1960</td>
    </tr>
    <tr>
      <td>Vmv</td>
      <td>Vimativinodanī (ṭīkā on Sp), Rangoon 1960</td>
    </tr>
    <tr>
      <td>VS</td>
      <td>Vājasaneyi-saṃhitā</td>
    </tr>
    <tr>
      <td>Vv</td>
      <td>Vimānavatthu, ed. N.A. Jayawickrama, PTS, London 1977 (by poem and verse)</td>
    </tr>
    <tr>
      <td>Vv-a</td>
      <td>Paramatthadīpanī III (Vimānavatthu-aṭṭhakathā), ed. E. Hardy, PTS, London 1901</td>
    </tr>
    <tr>
      <td>Yam</td>
      <td>Yamakapakaraṇa, ed. C.A.F. Rhys Davids, PTS, London 1911–13</td>
    </tr>
    <tr>
      <td>Yam-a</td>
      <td>Yamakappakaraṇa-atthakathā, ed. C.A.F. Rhys Davids, <i>JPTS</i>, 1912, pp. 52–107</td>
    </tr>
  </tbody></table>
  <h3>Works Cited</h3>
  <table>
    <tbody><tr>
      <td>V.S. Agrawala</td>
      <td>1968</td>
      <td>‘Ancient Indian Palace Architecture’, <i>Shri Mahavir Jaina Vidyalaya Golden Jubilee Volume, Part I.</i> Bombay: Shri Mahavir Jaina Vidyalaya, pp. 242–259</td>
    </tr>
    <tr>
      <td>L. Alsdorf</td>
      <td>1957</td>
      <td>‘Bemerkungen zum Vessantara-Jātaka’, <i>WZKSO</i>, 1, pp. 1–70; repr. 2001, pp. 270–339</td>
    </tr>
    <tr>
      <td></td>
      <td>1968</td>
      <td><i>Die Āryā-Strophen des Pali-Kanons metrisch hergestellt und textgeschichtlich untersucht.</i> Wiesbaden: Steiner (Akademie der Wissenschaften und der Literatur, Mainz. Abhandlungen der Geistes- und Sozialwissenschaftlichen Klasse, 1967, 4)</td>
    </tr>
    <tr>
      <td></td>
      <td>1971</td>
      <td>‘Das Jātaka vom weisen Vidhura’, <i>WZKSO</i>, 15, pp. 23–56; repr. 2001, pp. 380–413</td>
    </tr>
    <tr>
      <td></td>
      <td>1974</td>
      <td>‘The Impious Brahman and the Pious Caṇḍāla’, L. Cousins et al., 1974, pp. 9–13; repr. 1998, pp. 763–7</td>
    </tr>
    <tr>
      <td></td>
      <td>1977</td>
      <td>‘Das Bhūridatta-Jātaka. Ein anti-brahmanischer Nāga-Roman’, <i>WZKSO</i>, 21, pp. 25–55; repr. 1998, pp. 785–815</td>
    </tr>
    <tr>
      <td></td>
      <td>1998</td>
      <td><i>Kleine Schriften. Nachtragsband.</i> Herausgegeben von Albrecht Wezler. Suttgart: Steiner (VHGS, 35)</td>
    </tr>
    <tr>
      <td></td>
      <td>2001</td>
      <td><i>Kleine Schriften.</i> Herausgegeben von Albrecht Wezler. 2. Auflage. Suttgart: Steiner (VHGS, 10)</td>
    </tr>
    <tr>
      <td>N. Balbir</td>
      <td>2000</td>
      <td>‘Jain-Buddhist Dialogue: Material from the Pāli Scriptures’, <i>JPTS</i>, 26, pp. 1–42</td>
    </tr>
    <tr>
      <td>A.L. Basham</td>
      <td>1951</td>
      <td><i>History and Doctrines of the Ājīvikas. A vanished Indian religion.</i> London: Luzac</td>
    </tr>
    <tr>
      <td>H.W. Bailey</td>
      <td>1954</td>
      <td>‘Analecta Indoscythica II’, <i>JRAS</i>, 86, pp. 26–34</td>
</tr>
<tr>
  <td>H. Bechert</td>
  <td>1980</td>
  <td><i>Die Sprache der ältesten buddhistischen Überlieferung / The Language of the Earliest Buddhist Tradition.</i> (Symposien zur Buddhismusforschung, II). Herausgegeben von Heinz Bechert. Göttingen: Vandenhoeck &amp; Ruprecht (AAWG, Philologisch-Historische Klasse, 3,117)</td>
</tr>
<tr>
  <td>H. Berger</td>
  <td>1955</td>
  <td><i>Zwei Probleme der mittelindischen Lautlehre.</i> München: Kitzinger (Münchener Indologische Studien, 1)</td>
</tr>
<tr>
  <td>Bodhi (Bhikkhu)</td>
  <td>2001</td>
  <td><i>The Middle Length Discourses of the Buddha. A Translation of the Majjhima Nikāya.</i> Translated from the Pāli by Bhikkhu Ñāṇamoli and Bhikkhu Bodhi. [2nd] revised [ed.] Oxford: PTS (PTS Translation Series, 49)</td>
</tr>
<tr>
  <td>W.B. Bollée</td>
  <td>1970</td>
  <td><i>Kuṇālajātaka, being an edition and translation.</i> London: Luzac; repr. with additional notes: Oxford 2009</td>
</tr>
<tr>
  <td>J. Brough</td>
  <td>1962</td>
  <td><i>The Gāndhārī Dharmapada.</i> London: Oxford University Press (London Oriental Series, 7)</td>
</tr>
<tr>
  <td></td>
  <td>1980</td>
  <td>‘Sakāya Niruttiyā: Cauld kale het’, H. Bechert, 1980, pp. 35–42</td>
</tr>
<tr>
  <td>T. Burrow</td>
  <td>1955</td>
  <td><i>The Sanskrit Language.</i> London: Faber and Faber</td>
</tr>
<tr>
  <td></td>
  <td>1956</td>
  <td>‘Skt. <i>lubh</i> “to disturb”’, <i>JRAS</i>, pp. 191–200</td>
</tr>
<tr>
  <td></td>
  <td>1973</td>
  <td>‘Sanskrit <i>pā-</i> “go, move, pass, traverse”’, <i>IIJ</i>, 15, pp. 81–108</td>
</tr>
<tr>
  <td></td>
  <td>1984</td>
  <td>‘Vedic urvárī; “Lady of Choice, Wife”’, <i>JRAS</i>, pp. 209–216</td>
</tr>
<tr>
  <td>C. Caillat</td>
  <td>1960</td>
  <td>‘Deux études de moyen-indien’, <i>JAs</i>, 248, pp. 41–64; repr. 2011, pp. 25–48</td>
</tr>
<tr>
  <td></td>
  <td>1965</td>
  <td>‘Les dérivés moyen-indiens du type <i>kārima</i>’, <i>JAs</i>, 253, pp. 289–308; repr. 2011, pp. 55–74</td>
</tr>
<tr>
  <td></td>
  <td>1968</td>
  <td>‘La finale <i>-ima</i> dans les adjectifs moyen- et néo-indiens de sens spatial’, <i>Mélanges d’Indianisme, à la mémoire de Louis Renou</i>. Paris: de Boccard (Publications de l’Institut de civilisation indienne, Série in 8, 28), pp. 187–204; repr. 2011, pp. 79–96</td>
</tr>
<tr>
  <td></td>
  <td>1974</td>
  <td>‘Pāli <i>ibbha</i>, Vedic <i>íbhya-</i>’, L. Cousins et al., 1974, pp. 41–49; repr. 2011, pp. 105–113</td>
</tr>
<tr>
  <td></td>
  <td>2011</td>
  <td><i>Selected Papers</i>. Bristol: PTS</td>
</tr>
<tr>
  <td>J. Charpentier</td>
  <td>1932</td>
  <td>‘Some Sanskrit and Pāli Notes’, <i>Indian Linguistics</i>, 2, pp. 45–71</td>
</tr>
<tr>
  <td>S. Collins</td>
  <td>1982</td>
  <td><i>Selfless persons. Imagery and thought in Theravāda Buddhism.</i> Cambridge [et al.]: Cambridge University Press</td>
</tr>
<tr>
  <td>A.K. Coomaraswamy</td>
  <td>1930a</td>
  <td>‘Pali <i>kaṇṇikā</i><i> </i>= Circular Roof-Plate’, <i>JAOS</i>, 50, pp. 238–243</td>
</tr>
<tr>
  <td></td>
  <td>1930b</td>
  <td>‘The Parts of a <i>vīṇā</i>’, <i>JAOS</i>, 50, pp. 244–253</td>
</tr>
<tr>
  <td></td>
  <td>1931</td>
  <td>‘Early Indian Architecture. III: Palaces’, <i>Eastern Art</i>, 3, pp. 180–217</td>
</tr>
<tr>
  <td></td>
  <td>1956</td>
  <td><i>La sculpture de Bharhut.</i> Paris: Vanoest (Annales du Musée Guimet. Bibliothèque d’Art, Nouvelle Série, 6)</td>
</tr>
<tr>
  <td>L. Cousins, et al.</td>
  <td>1974</td>
  <td><i>Buddhist Studies in Honour of I.B. Horner.</i> Edited by L. Cousins, A. Kunst, and K.R. Norman. Dordrecht, Boston: D. Reidel</td>
</tr>
<tr>
  <td>R.O. Franke</td>
  <td>1908</td>
  <td>‘The Buddhist councils at Rājagaha and Vesālī, as alleged in Cullavagga XI., XII.’, <i>JPTS</i>, pp. 1–80; repr. 1978, pp. 1381–1460</td>
</tr>
<tr>
  <td></td>
  <td>1978</td>
  <td><i>Kleine Schriften.</i> Herausgegeben von Oskar v. Hinüber. Wiesbaden: Steiner (VHGS, 17)</td>
</tr>
<tr>
  <td>W. Geiger</td>
  <td>1994</td>
  <td><i>A Pāli Grammar</i>, translated by Batakrishna Ghosh, revised and edited by K.R. Norman. Oxford: PTS</td>
</tr>
<tr>
  <td>R.M.L. Gethin</td>
  <td>2001</td>
  <td><i>The Buddhist Path to Awakening.</i> 2nd ed., Oxford: Oneworld</td>
</tr>
<tr>
  <td></td>
  <td>2015</td>
  <td>‘A Note on the <i>Mahākammavibhaṅga-sutta</i> and Its Commentary’, <i>JPTS</i>, 32, pp. 241–260</td>
</tr>
<tr>
  <td>C. Hallisey</td>
  <td>1990</td>
  <td>‘Apropos the Pāli Vinaya as a historical document: a reply to Gregory Schopen’, <i>JPTS</i>, 15, pp. 197–208</td>
</tr>
<tr>
  <td>S. Hamilton</td>
  <td>1996</td>
  <td><i>Identity and experience. The constitution of the human being according to early Buddhism.</i> London: Luzac Oriental</td>
</tr>
<tr>
  <td>M. Hara</td>
  <td>1992</td>
  <td>‘A note on Dhammapada 97’, <i>IIJ</i>, 35, pp. 179–191</td>
</tr>
<tr>
  <td>P. Harrison</td>
  <td>1992</td>
  <td>‘Is the Dharma-kāya the Real “Phantom Body” of the Buddha?’, <i>Journal of the International Association of Buddhist Studies</i>, 15, pp. 44–94</td>
</tr>
<tr>
  <td>A.A. Hazlewood</td>
  <td>1986</td>
  <td><i>In Praise of Mount Samanta (Samantakūṭavaṇṇanā) by Vedeha Thera.</i> Translated. London: PTS (Sacred Books of the Buddhists, 37)</td>
</tr>
<tr>
  <td>O. von Hinüber</td>
  <td>1967</td>
  <td>‘Pāli <i>ulloka-</i>’, <i>ZVS</i>, 81, pp. 247–253; English translation: 1994, pp. 1–8</td>
</tr>
<tr>
  <td></td>
  <td>1968a</td>
  <td>‘Vedisch <i>nivāté</i> und Pāli <i>nivātake</i>’, <i>MSS</i>, 23, pp. 21–28; English translation: 1994, pp. 9–16</td>
</tr>
<tr>
  <td></td>
  <td>1968b</td>
  <td><i>Studien zur Kasussyntax des Pāli, besonders des Vinaya-Piṭaka.</i> München: Kitzinger; 2nd ed. Halle: Universitätsverlag Halle-Wittenberg, 2022 (Studia Indologica Universitatis Halensis, 19)</td>
</tr>
<tr>
  <td></td>
  <td>1970</td>
  <td><i>‘Gāthā anacchariyā pubbe assutapubbā’</i>, <i>ZVS</i>, 84, pp. 5–10; English translation: 1994, pp. 17–24</td>
</tr>
<tr>
  <td></td>
  <td>1972a</td>
  <td>‘Die “dreifache” Wirkung des Karma’, <i>IIJ</i>, 13, pp. 241–249; English translation: 1994, pp. 39–51</td>
</tr>
<tr>
  <td></td>
  <td>1972b</td>
  <td>‘Pāli philology and the Tibetan translation of Buddhist texts. Two examples <i>(pacuṭa, sotā)</i>’, <i>IIJ,</i> 14, pp. 198–203; repr. 2009–19, pp. 32–37</td>
</tr>
<tr>
  <td></td>
  <td>1974a</td>
  <td>‘Reste des reduplizierten Aorists in Pāli’, <i>MSS</i>, 32, pp. 65–72; English translation: 1994, pp. 52–61</td>
</tr>
<tr>
  <td></td>
  <td>1978a</td>
  <td>‘On the tradition of Pāli texts in India, Ceylon and Burma’, <i>Buddhism in Ceylon and studies on religious syncretism in Buddhist countries.</i> (Symposien zur Buddhismusforschung, 1). Edited by Heinz Bechert. Göttingen: Vandenhoeck &amp; Ruprecht (AAWG, Philologisch-Historische Klasse, 3,108), pp. 48–57; repr. 2009–19, pp. 293–302</td>
</tr>
<tr>
  <td></td>
  <td>1978b</td>
  <td>‘<i>Gotrabhū:</i> Die sprachliche Vorgeschichte eines philosophischen Terminus’, <i>Zeitschrift der Deutschen Morgenländischen Gesellschaft</i>, 128, pp. 326–332; English translation: 1994, pp. 91–100</td>
</tr>
<tr>
  <td></td>
  <td>1979a</td>
  <td>‘Pāli kaṭhati: Ein Beitrag zur Überlieferungsgeschichte des Theravāda-Kanons’, <i>IIJ</i>, 21, pp. 21–26; English translation: 1994, pp. 107–115</td>
</tr>
<tr>
  <td></td>
  <td>1979b</td>
  <td>‘A Vedic Verb in Pāli: udājita’, <i>Ludwik Sternbach Felicitation Volume</i>, [ed. by] J.P. Sinha. Lucknow: Akhila Bharatiya Sanskrit Parishad, pp. 819–822; repr. 2009–19, pp. 616–619</td>
</tr>
<tr>
  <td></td>
  <td>1979c</td>
  <td>‘Über drei Begriffe der buddhistischen Rechtssprache: <i>issaratā, gīvā</i> und <i>bhaṇḍadeyya</i>’, <i>IT</i>, 7, pp. 275–279; English translation: 1994, pp. 116–122</td>
</tr>
<tr>
  <td></td>
  <td>1980</td>
  <td>‘Bemerkungen zum Critical Pāli Dictionary II’, <i>ZVS</i>, 94, pp. 10–31; English translation: 1994, pp. 123–161</td>
</tr>
<tr>
  <td></td>
  <td>1981</td>
  <td>‘The ghost word <i>dvīhitikā</i> and the description of famines in early Buddhist literature’, <i>JPTS</i>, 9, pp. 74–86; repr. 2009–19, pp. 603–615</td>
</tr>
<tr>
  <td></td>
  <td>1982a</td>
  <td>‘Zum Perfekt im Pāli’, <i>ZVS</i>, 96 (1982/83), pp. 30–32; English translation: 1994, pp. 173–176</td>
</tr>
<tr>
  <td></td>
  <td>1982b</td>
  <td>‘Pāli as an artificial language’, <i>IT</i>, 10, pp. 133–140; repr. 2009–19, pp. 451–458</td>
</tr>
<tr>
  <td></td>
  <td>1983</td>
  <td><i>Notes on the Pāli Tradition in Burma.</i> (Beiträge zur Überlieferungsgeschichte des Buddhismus in Birma, I). Göttingen: Vandenhoeck &amp; Ruprecht. (Nachrichten der Akademie der Wissenschaften zu Göttingen, Philologisch-Historische Klasse, 1983, 3)</td>
</tr>
<tr>
  <td></td>
  <td>1986<b></b></td>
  <td><i>Das ältere Mittelindisch im Überblick.</i> Wien: Österreichische Akademie der Wissenschaften (Philosophisch-Historische Klasse, Sitzungsberichte, 467. Veröffentlichungen der Kommission für Sprachen und Kulturen Südasiens, 20); 2nd, enlarged ed. Wien 2001<b></b></td>
</tr>
<tr>
  <td></td>
  <td>1990</td>
  <td>‘Khandhakavatta: Loss of text in the Pāli Vinayapiṭaka?’, <i>JPTS</i>, 15, pp. 127–138; repr. 2009–19, pp. 132–143</td>
</tr>
<tr>
  <td></td>
  <td>1994</td>
  <td><i>Selected Papers on Pāli Studies.</i> Oxford: PTS; repr. 2005</td>
</tr>
<tr>
  <td></td>
  <td>2008</td>
  <td>‘The Foundation of the Bhikkhunīsaṃgha. A Contribution to the Earliest History of Buddhism’, <i>Annual Report of the International Research Institute for Advanced Buddhology at Soka University</i>, 11, pp. 3–29; repr. 2009–19, pp. 1197–1223</td>
</tr>
<tr>
  <td></td>
  <td>2009–19</td>
  <td><i>Kleine Schriften.</i> Teil I–II: Herausgegeben von Harry Falk und Walter Slaje. Teil III: Herausgegeben von Harry Falk, Haiyan Hu-von Hinüber und Walter Slaje. Wiesbaden: Harrassowitz, 2009, 2019 (VHGS, 47, 49)</td>
</tr>
<tr>
  <td>K. Hoffmann</td>
  <td>1960</td>
  <td>‘Ved. <i>ucchvaṅká-, ucchlaṅkhá-</i>, Pāli <i>ussaṅkha-</i>’, <i>IIJ</i>, 4, pp. 111–118</td>
</tr>
<tr>
  <td>N.A. Jayawickrama</td>
  <td>1971</td>
  <td><i>The Chronicle of the Thūpa and the Thūpavaṃsa.</i> Being a Translation and Edition of Vācissaratthera’s Thūpavaṃsa. Oxford: PTS</td>
</tr>
<tr>
  <td>E.H. Johnston</td>
  <td>1931</td>
  <td>‘Notes on Some Pali Words’, <i>JRAS</i>, pp. 565–592</td>
</tr>
<tr>
  <td>S.M. Katre</td>
  <td>1944</td>
  <td><i>Some Problems of Historical Linguistics in Indo-Aryan.</i> Bombay: University of Bombay</td>
</tr>
<tr>
  <td>H. Kern</td>
  <td>1916</td>
  <td><i>Toevoegselen op ’t Woordenboek van Childers.</i> Amsterdam: Johannes Müller (Verhandelingen der Koninklijke Akademie van Wetenschappen te Amsterdam, Afdeeling Letterkunde, nieuwe reeks, 16,4–5)</td>
</tr>
<tr>
  <td>P.A. Khoroche</td>
  <td>1987</td>
  <td><i>Towards a New Edition of Ārya-Śūra’s Jātakamālā.</i> Bonn: Indica et Tibetica Verlag (IeT, 12)</td>
</tr>
<tr>
  <td></td>
  <td>1989</td>
  <td><i>Once the Buddha Was a Monkey. Ārya Śūra’s Jātakamālā</i>. Translated from the Sanskrit. Chicago: University of Chicago Press</td>
</tr>
<tr>
  <td>F.B.J. Kuiper</td>
  <td>1948</td>
  <td><i>Proto-Munda words in Sanskrit.</i> Amsterdam: Noord-Hollandsche Uitgevers Maatschappij (Verhandelingen der Koninklijke Akademie van Wetenschappen te Amsterdam, Afdeeling Letterkunde, nieuwe reeks, 51,3)</td>
</tr>
<tr>
  <td>S. Lienhard</td>
  <td>1978</td>
  <td>‘On the meaning and use of the word <i>indragopa</i>’, <i>IT</i>, 6, 177–188; repr. 2008, pp. 373–384</td>
</tr>
<tr>
  <td></td>
  <td>2008</td>
  <td><i>Kleine Schriften.</i> Herausgegeben von Oskar von Hinüber. Wiesbaden: Harrassowitz (VHGS, 44)</td>
</tr>
<tr>
  <td>J. Liyanaratne</td>
  <td>1994</td>
  <td>‘South Asian flora as reflected in the twelfth-century Pāli lexicon Abhidhānappadīpikā’, <i>JPTS</i>, 20, pp. 43–161 = SAF</td>
</tr>
<tr>
  <td>H. Lüders</td>
  <td>1907</td>
  <td><i>Das Würfelspiel im alten Indien.</i> Berlin: Weidmannsche Buchhandlung (Abhandlungen der Königlichen Gesellschaft der Wissenschaften zu Göttingen, Philologisch-Historische Klasse, Neue Folge, 9,2); repr. 1940, pp. 106–75</td>
</tr>
<tr>
  <td></td>
  <td>1940</td>
  <td><i>Philologica Indica. Ausgewählte kleine Schriften von Heinrich Lüders.</i> Festgabe zum siebzigsten Geburtstage am 25. Juni 1939 dargebracht von Kollegen, Freunden und Schülern. Göttingen: Vandenhoeck &amp; Ruprecht</td>
</tr>
<tr>
  <td></td>
  <td>1941</td>
  <td><i>Bhārhut und die buddhistische Literatur.</i> Leipzig: Brockhaus (Abhandlungen für die Kunde des Morgenlandes, 26,3); repr. Nendeln, Liechtenstein 1966</td>
</tr>
<tr>
  <td></td>
  <td>1954</td>
  <td><i>Beobachtungen über die Sprache des buddhistischen Urkanons.</i> Aus dem Nachlass herausgegeben von Ernst Waldschmidt. Berlin (Abhandlungen der Deutschen Akademie der Wissenschaften zu Berlin, Klasse für Sprachen, Literatur und Kunst, 1952, 10) = BSU</td>
</tr>
<tr>
  <td>P. Masefield</td>
  <td>1989</td>
  <td><i>Elucidation of the Intrinsic Meaning so named The Commentary on the Vimāna Stories (Paramattha-dīpanī nāma Vimānavatthu-aṭṭhakathā).</i> Translated by Peter Masefield assisted by N.A. Jayawickrama. Oxford: PTS</td>
</tr>
<tr>
  <td>M.A. Mehendale</td>
  <td>1955</td>
  <td>Review of H. Lüders, 1954, <i>Bulletin of the Deccan College Research Institute</i>, 17.1, pp. 53–75</td>
</tr>
<tr>
  <td>G.J. Meulenbeld</td>
  <td>1974</td>
  <td><i>The Mādhavanidāna and its chief commentary, chapters 1--10.</i> Introduction, translation and notes. Leiden: Brill (Orientalia Rheno-Traiectina, 19)</td>
</tr>
<tr>
  <td>R. Morris</td>
  <td>1884</td>
  <td>‘Notes and Queries’, <i>JPTS</i>, pp. 69–108</td>
</tr>
<tr>
  <td></td>
  <td>1885</td>
  <td>‘Notes and Queries’, <i>JPTS</i>, pp. 29–76</td>
</tr>
<tr>
  <td></td>
  <td>1893</td>
  <td>‘Notes and Queries’, <i>JPTS</i>, pp. 1–75</td>
</tr>
<tr>
  <td>P. Mus</td>
  <td>1939</td>
  <td><i>La Lumière sur les Six Voies.</i> Tableau de la transmigration bouddhique, d’après des sources sanskrites, Pāli, tibétaines et chinoises en majeure partie inédites. Paris: Institut d’Ethnologie (Travaux et mémoires de l’Institut d’Ethnologie, 35)</td>
</tr>
<tr>
  <td>Ñāṇamoli (Bhikkhu)</td>
  <td>1956</td>
  <td><i>The path of Purification. Bhadantācariya Buddhaghosa.</i> Translated from the Pali. Colombo: Semage; 3rd ed. Kandy: Buddhist Publication Society, 1975</td>
</tr>
<tr>
  <td></td>
  <td>1962</td>
  <td><i>The Guide (Netti-Ppakaraṇaṃ) according to Kaccāna Thera.</i> Translated from the Pali. Londen: PTS</td>
</tr>
<tr>
  <td></td>
  <td>1964</td>
  <td><i>The Piṭaka-Disclosure (Peṭakopadesa) According to Kaccāna Thera.</i> Translated from the Pali. London: Luzac (PTS Translation Series, 35)</td>
</tr>
<tr>
  <td></td>
  <td>1982</td>
  <td><i>The Path of Discrimination (Paṭisambhidāmagga).</i> Translated from the Pāli. With an introduction by A.K. Warder. London: PTS (PTS Translation Series, 43); 2nd ed. Oxford 1997</td>
</tr>
<tr>
  <td>K.R. Norman</td>
  <td>1960</td>
  <td>‘Middle Indo-Aryan Studies’, <i>JOI(B)</i>, 9, pp. 268–273; re-edited 1990b, pp. 15–20</td>
</tr>
<tr>
  <td></td>
  <td>1961</td>
  <td>‘Middle Indo-Aryan Studies II’, <i>JOI(B)</i>, 10, pp. 348–352; re-edited 1990b, pp. 25–29</td>
</tr>
<tr>
  <td></td>
  <td>1965</td>
  <td>‘Middle Indo-Aryan Studies V’, <i>JOI(B)</i>, 15, pp. 113–117; re-edited 1990b, pp. 42–46</td>
</tr>
<tr>
  <td></td>
  <td>1966</td>
  <td>‘Middle Indo-Aryan Studies VI’, <i>JOI(B)</i>, 16, pp. 113–116; re-edited 1990b, pp. 77–84</td>
</tr>
<tr>
  <td></td>
  <td>1967</td>
  <td>‘Notes on Aśoka’s Fifth Pillar Edict’, <i>JRAS</i>, pp. 26–32; re-edited 1990b, pp. 68–76</td>
</tr>
<tr>
  <td></td>
  <td>1969</td>
  <td><i>The Elders’ Verses. I. Theragāthā.</i> Translated with an introduction and notes. London: Luzac (PTS Translation Series, 38); 2nd ed. Lancaster 2007</td>
</tr>
<tr>
  <td></td>
  <td>1971a</td>
  <td><i>The Elders’ Verses. II. Therīgāthā.</i> Translated with an introduction and notes. London: Luzac (PTS Translation Series, 40); 2nd ed. Lancaster 2007</td>
</tr>
<tr>
  <td></td>
  <td>1971b</td>
  <td>‘Middle Indo-Aryan Studies VIII’, <i>JOI(B)</i>, 20, pp. 329–336; re-edited 1990b, pp. 122–129</td>
</tr>
<tr>
  <td></td>
  <td>1977</td>
  <td>‘The Buddha’s View of Devas’, <i>Beiträge zur Indienforschung. Ernst Waldschmidt zum 80. Geburtstag gewidmet.</i> Berlin: Museum für indische Kunst (Veröffentlichungen des Museums für indische Kunst, 4), pp. 329–336; re-edited 1991, pp. 1–8</td>
</tr>
<tr>
  <td></td>
  <td>1979</td>
  <td>‘Two Pali Etymologies’, <i>Bulletin of the School of Oriental and African Studies</i>, 42, pp. 321–328; re-edited 1991, pp. 71–83</td>
</tr>
<tr>
  <td></td>
  <td>1980</td>
  <td>‘The dialects in which the Buddha preached’, <i>Die Sprache der ältesten buddhistischen Überlieferung / The Language of the Earliest Buddhist Tradition.</i> (Symposien zur Buddhismusforschung, II). Herausgegeben von Heinz Bechert. Göttingen: Vandenhoeck &amp; Ruprecht (AAWG, Philologisch-Historische Klasse,3,117), pp. 61–77; re-edited 1991, pp. 128–147</td>
</tr>
<tr>
  <td></td>
  <td>1981a</td>
  <td>‘Devas and adhidevas in Buddhism’, <i>JPTS</i>, 9, pp. 145–155; re-edited 1991, pp. 162–171</td>
</tr>
<tr>
  <td></td>
  <td>1981b</td>
  <td>‘Notes on the Vessantara-jātaka’, <i>Studien zum Jainismus und Buddhismus. Gedenkschrift für Ludwig Alsdorf.</i> Herausgegeben von Klaus Bruhn und Albrecht Wezler. Wiesbaden: Franz Steiner (Alt- und Neu-Indische Studien, 23), pp. 163–174; re-edited 1991, pp. 172–186</td>
</tr>
<tr>
  <td></td>
  <td>1983</td>
  <td>‘The Pratyeka-Buddha in Buddhism and Jainism’, <i>Buddhist Studies, Ancient and Modern.</i> Edited by Philip Denwood and Alexander Piatigorsky. London [et al.]: Curzon (Collected Papers on South Asia, 4), pp. 92–106; re-edited 1991, pp. 233–249</td>
</tr>
<tr>
  <td></td>
  <td>1987</td>
  <td>‘Pāli Lexicographical Studies IV. Eleven Pāli Etymologies’, <i>JPTS</i>, 11, pp. 33–49; re-edited 1992a, pp. 157–172</td>
</tr>
<tr>
  <td></td>
  <td>1987–88</td>
  <td>‘The metres of the Lakkhaṇa-suttanta (II)’, <i>IT</i>, 14, pp. 285–294; re-edited 1993b, pp. 36–45</td>
</tr>
<tr>
  <td></td>
  <td>1988</td>
  <td>‘Pali Lexicographical Studies V. Twelve Pāli Etymologies’, <i>JPTS</i>, 12, pp. 49–61; re-edited 1992a, pp. 257–268</td>
</tr>
<tr>
  <td></td>
  <td>1989 </td>
  <td>‘Pali Lexicographical Studies VI. Six Pāli Etymologies’, <i>JPTS</i>, 13, pp. 219–227; re-edited 1993b, pp. 71–79</td>
</tr>
<tr>
  <td></td>
  <td>1990a</td>
  <td>‘Pāli Lexicographical Studies VIII. Seven Pāli Etymologies’, <i>JPTS</i>, 15, pp. 145–154; re-edited 1993b, pp. 155–163</td>
</tr>
<tr>
  <td></td>
  <td>1990b</td>
  <td><i>Collected Papers. Volume I.</i> Oxford: PTS; repr. with corrections 1999</td>
</tr>
<tr>
  <td></td>
  <td>1991</td>
  <td><i>Collected Papers. Volume II.</i> Oxford: PTS; repr. with corrections 2003</td>
</tr>
<tr>
  <td></td>
  <td>1992a</td>
  <td><i>Collected Papers. Volume III.</i> Oxford: PTS; repr. with corrections 2008</td>
</tr>
<tr>
  <td></td>
  <td>1992b</td>
  <td><i>The Group of Discourses (Sutta-Nipāta). Volume II.</i> Revised translation with introduction and notes. Oxford: PTS (PTS Translation Series, 45); 2nd ed. 2001</td>
</tr>
<tr>
  <td></td>
  <td>1993a</td>
  <td>‘The metres of the Lakkhaṇa-suttanta (III)’, <i>Chi no kaikō Bukkyō to kagaku. Tsukamoto Keishō Kyōju kanreki kinen ronbunshū.</i> [Encounter of wisdom between Buddhism and science. Essays in Honour of Professor Keishō Tsukamoto on his Sixtieth Anniversary.] Tōkyō: Kōsei Shuppansha, pp. 79–91; re-edited 1994a, pp. 119–131</td>
</tr>
<tr>
  <td></td>
  <td>1993b</td>
  <td><i>Collected Papers. Volume IV.</i> Oxford: PTS; repr. with corrections 2008</td>
</tr>
<tr>
  <td></td>
  <td>1994a</td>
  <td><i>Collected Papers. Volume V.</i> Oxford: PTS; repr. with corrections 2013</td>
</tr>
<tr>
  <td></td>
  <td>1994b</td>
  <td>‘Pāli Lexicographical Studies XII. Ten Pāli Etymologies’, <i>JPTS</i>, 20, pp. 211–230; re-edited 1996, pp. 47–67</td>
</tr>
<tr>
  <td></td>
  <td>1997</td>
  <td><i>The Word of the Doctrine (Dhammapada)</i>, translated with an introduction and notes. Oxford: PTS (PTS Translation Series, 46); repr. with corrections 2000, 2004, 2021</td>
</tr>
<tr>
  <td></td>
  <td>2001a</td>
  <td>see 1992b</td>
</tr>
<tr>
  <td></td>
  <td>2001b</td>
  <td>‘The metres of the Lakkhaṇa-suttanta (V)’, <i>IT</i>, 17–18, pp. 273–282; re-edited 2007c, pp. 70–79</td>
</tr>
<tr>
  <td></td>
  <td>2007a</td>
  <td>see 1969</td>
</tr>
<tr>
  <td></td>
  <td>2007b</td>
  <td><i>Collected Papers. Volume VIII.</i> Lancaster: PTS</td>
</tr>
<tr>
  <td>T. Oberlies</td>
  <td>1991</td>
  <td>‘Die Verwendung des Part. Präs. als Konditional im Pali’, <i>IIJ</i>, 34, pp. 121–122</td>
</tr>
<tr>
  <td></td>
  <td>1995a</td>
  <td>‘Beiträge zur Pali-Lexikographie (Miscellanea Palica II)’, <i>IIJ</i>, 38, pp. 105–147</td>
</tr>
<tr>
  <td></td>
  <td>1995b</td>
  <td>‘Beiträge zum Pali-Lexikon (Miscellanea Palica III)’, <i>Historische Sprachforschung</i>, 108, pp. 127–164</td>
</tr>
<tr>
  <td></td>
  <td>1997</td>
  <td>‘Pali, Pāṇini and ‘popular’ Sanskrit (Miscellanea Palica VI)’, <i>JPTS</i>, 23, pp. 1–26</td>
</tr>
<tr>
  <td></td>
  <td>2001</td>
  <td><i>Pāli. A Grammar of the Language of the Theravāda Tipiṭaka.</i> de Gruyter: Berlin, New York (Indian Philology and South Asian Studies, 3)</td>
</tr>
<tr>
  <td></td>
  <td>2002</td>
  <td>‘Language economy: ‘Short(ened)’ case-endings in Indo-Aryan’, <i>Bulletin d’études Indiennes</i>, 20, pp. 193–197</td>
</tr>
<tr>
  <td>Pe Maung Tin</td>
  <td>1971</td>
  <td><i>The Path of Purity.</i> Being a translation of Buddhaghosa’s Visuddhimagga. London: Luzac (PTS Translation Series, 11, 17, 21)</td>
</tr>
<tr>
  <td>O.H. Pind</td>
  <td>1997</td>
  <td>‘Pāli Miscellany’, <i>Bauddhavidyāsudhākaraḥ. Studies in Honour of Heinz Bechert on the Occasion of His 65th Birthday.</i> Edited by Petra Kieffer-Pülz and Jens-Uwe Hartmann. Swisttal-Odendorf: Indica et Tibetica Verlag (IeT, 30), pp. 515–536</td>
</tr>
<tr>
  <td></td>
  <td>1989</td>
  <td>‘Studies in the Pāli Grammarians I’, <i>JPTS</i>, 13, pp. 33–82</td>
</tr>
<tr>
  <td></td>
  <td>1990</td>
  <td>‘Studies in the Pāli Grammarians II.1’ <i>JPTS</i>, 14, pp. 175–218</td>
</tr>
<tr>
  <td>R. Pischel</td>
  <td>1900</td>
  <td><i>Grammatik der Prakrit-Sprachen.</i> Strassburg: Trübner; English translation: 1957</td>
</tr>
<tr>
  <td></td>
  <td>1957</td>
  <td><i>Comparative Grammar of the Prākrit Languages.</i> Translated from the German by Subhadra Jhā. Varanasī [et al.]: Motilal Banarsidass; English translation of 1900</td>
</tr>
<tr>
  <td>W. Pruitt</td>
  <td>1998</td>
  <td><i>The Commentary on the Verses of the Therīs (Therīgāthā-Aṭṭhakathā, Paramatthadīpanī VI) by Ācariya Dhammapāla.</i> Translated. Oxford: PTS; repr. with corrections 1999</td>
</tr>
<tr>
  <td>W. Rahula</td>
  <td>1956</td>
  <td><i>History of Buddhism in Ceylon. The Anuradhapura Period. 3rd Century BC – 10th Century AC.</i> Colombo: M.D. Gunasena</td>
</tr>
<tr>
  <td>L. Renou</td>
  <td>1939</td>
  <td>‘Les éléments védiques dans le vocabulaire du sanskrit classique’, <i>JAs</i>, 231, pp. 321–403</td>
</tr>
<tr>
  <td></td>
  <td>1975</td>
  <td><i>Grammaire Sanscrite.</i> Seconde édition revue, corrigée et augmentée. Paris: Maisonneuve</td>
</tr>
<tr>
  <td>N. Ross Reat</td>
  <td>1987</td>
  <td>‘Some fundamental concepts of Buddhist psychology’, <i>Religion</i>, 17, pp. 15–28</td>
</tr>
<tr>
  <td>G. Schopen</td>
  <td>1989</td>
  <td>‘The Stūpa Cult and the Extant Pāli Vinaya’, <i>JPTS</i>, 13, pp. 83–100; re-edited 1997, pp. 86–98</td>
</tr>
<tr>
  <td></td>
  <td>1996</td>
  <td>‘The suppression of nuns and the ritual murder of their special dead in two Buddhist monastic texts’, <i>Journal of Indian Philosophy</i>, 24, pp. 563–592; re-edited 2004, pp. 329–359</td>
</tr>
<tr>
  <td></td>
  <td>1997</td>
  <td><i>Bones, Stones, and Buddhist Monks. Collected Papers on the Archaeology, Epigraphy, and Texts of Monastic Buddhism in India.</i> Honolulu: University of Hawai’i Press (Studies in the Buddhist Traditions)</td>
</tr>
<tr>
  <td></td>
  <td>2004</td>
  <td><i>Buddhist Monks and Business Matters. Still More Papers on Monastic Buddhism in India.</i> Honolulu: University of Hawai’i Press (Studies in the Buddhist Traditions)</td>
</tr>
<tr>
  <td>D. Seyfort Ruegg</td>
  <td>1974</td>
  <td>‘Pāli <i>Gotta/Gotra</i> and the Term <i>Gotrabhū</i> in Pāli and Buddhist Sanskrit’, L. Cousins et al., 1974, 199–210</td>
</tr>
<tr>
  <td></td>
  <td>1981</td>
  <td>‘A further note on Pali <i>gotrabhū</i>’, <i>JPTS</i>, 9, pp. 175–177</td>
</tr>
<tr>
  <td>L. de Silva</td>
  <td>1978</td>
  <td>‘Cetovimutti, Paññāvimutti and Ubhatobhāgavimutti’, <i>Pāli Buddhist Review</i>, 3, pp. 118–145</td>
</tr>
<tr>
  <td>J.S. Strong</td>
  <td>1977</td>
  <td>‘<i>Gandhakuṭī:</i> The Perfumed Chamber of the Buddha’, <i>History of Religions</i>, 16, pp. 390–406</td>
</tr>
<tr>
  <td>V. Trenckner</td>
  <td>1908</td>
  <td>‘Critical and philological notes to the first chapter (Bāhirakathā) of the Milinda-pañha. Revised and edited, together with an index of words and subjects by Dines Andersen’, <i>JPTS</i>, pp. 102–151</td>
</tr>
<tr>
  <td>R.L. Turner</td>
  <td>1975</td>
  <td><i>Collected Papers 1912–1973.</i> London [et al.]: Oxford University Press</td>
</tr>
<tr>
  <td>Vajirañāṇavarorasa</td>
  <td>1969–83</td>
  <td><i>The Entrance to the Vinaya. Vinayamukha.</i> Vols I–III. Bangkok: Mahāmakuṭarājavidyālaya, 1969, 1973, 1983 = Vinmu</td>
</tr>
<tr>
  <td>C. Vogel</td>
  <td>1971</td>
  <td>‘Pali lexical studies’, <i>IIJ</i>, 13, pp. 20–30</td>
</tr>
<tr>
  <td>A.K. Warder</td>
  <td>1967</td>
  <td><i>Pali Metre.</i> A Contribution to the History of Indian Literature. London: Luzac</td>
</tr>
<tr>
  <td></td>
  <td>1982</td>
  <td><i>Introduction</i> to Ñāṇamoli, 1982, pp. v–lxiv</td>
</tr>
<tr>
  <td>N.L. Westergaard</td>
  <td>1841</td>
  <td><i>Radices Linguae Sanscritae.</i> Bonnae ad Rhenum: H.B. König, 1841</td>
</tr>
<tr>
  <td>W.D. Whitney</td>
  <td>1879</td>
  <td><i>A Sanskrit Grammar. Including both the classical Language, and the older Dialects, of Veda and Brahmana.</i> Leipzig: Breitkopp &amp; Haertel (Bibliothek indogermanischer Grammatiken, 2)</td>
</tr>
<tr>
  <td>O.H de A. Wijesekera</td>
  <td>1979</td>
  <td>‘The Etymology of Pali <i>Gotrabhū</i>’, <i>Studies in Pali and Buddhism. A Memorial Volume in Honor of Bhikkhu Jagdish Kashyap.</i> Editor: A.K. Narain. Delhi: B.R. Publishing, pp. 381–382</td>
</tr>
</tbody></table>
</div>"""

dict = {
    "abbreviations": abbrev_html,
    "foreword": foreword_html,
    "references": references_html}

with open("./front_matter.json", "w") as f:
    json.dump(dict, f, ensure_ascii=False, indent=1)
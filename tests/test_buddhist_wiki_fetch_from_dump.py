"""Tests for the pages-articles dump extractor.

The fixture is copied from the head of enwiki-20261001-pages-articles.xml
(the Anarchism text is cut short; everything else is verbatim).
"""

import bz2
import json
from pathlib import Path

from dictionaries.buddhist_wiki.fetch_from_dump import extract_from_dump

DUMP_XML = """\
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.11/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.11/ http://www.mediawiki.org/xml/export-0.11.xsd" version="0.11" xml:lang="en">
  <siteinfo>
    <sitename>Wikipedia</sitename>
    <dbname>enwiki</dbname>
  </siteinfo>
  <page>
    <title>AccessibleComputing</title>
    <ns>0</ns>
    <id>10</id>
    <redirect title="Computer accessibility" />
    <revision>
      <id>1367012995</id>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text bytes="111" sha1="kmysdltgexdwkv2xsml3j44jb56dxvn" xml:space="preserve">#REDIRECT [[Computer accessibility]]</text>
    </revision>
  </page>
  <page>
    <title>Anarchism</title>
    <ns>0</ns>
    <id>12</id>
    <revision>
      <id>1375097780</id>
      <parentid>1375092023</parentid>
      <timestamp>2026-09-15T21:29:32Z</timestamp>
      <contributor>
        <username>Asterix12</username>
        <id>37877400</id>
      </contributor>
      <minor />
      <origin>1375097780</origin>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text bytes="114294" sha1="l18vk5wqrb9lzhcnp3evgpe49pf1yyp" xml:space="preserve">{{Short description|Political philosophy and movement}}
{{Other uses|Anarchism (disambiguation)|Anarchist (disambiguation)}}
[[Category:Political concepts]]</text>
      <sha1>l18vk5wqrb9lzhcnp3evgpe49pf1yyp</sha1>
    </revision>
  </page>
  <page>
    <title>AfghanistanHistory</title>
    <ns>0</ns>
    <id>13</id>
    <redirect title="History of Afghanistan" />
    <revision>
      <id>783865149</id>
      <parentid>74466652</parentid>
      <timestamp>2017-06-05T04:18:18Z</timestamp>
      <contributor>
        <username>Tom.Reding</username>
        <id>9784415</id>
      </contributor>
      <minor />
      <comment>+{{Redirect category shell}} using [[Project:AWB|AWB]]</comment>
      <origin>783865149</origin>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text bytes="90" sha1="iv7s0lr40b17x33tfb0caa2g5bplgrk" xml:space="preserve">#REDIRECT [[History of Afghanistan]]

{{Redirect category shell|1=
{{R from CamelCase}}
}}</text>
      <sha1>iv7s0lr40b17x33tfb0caa2g5bplgrk</sha1>
    </revision>
  </page>
</mediawiki>
"""


def _setup(tmp_path: Path, titles: list[str]) -> dict[str, Path]:
    dump = tmp_path / "dump.xml.bz2"
    dump.write_bytes(bz2.compress(DUMP_XML.encode("utf-8")))
    article_list = tmp_path / "article_list.txt"
    article_list.write_text("\n".join(titles) + "\n", encoding="utf-8")
    return {
        "dump_path": dump,
        "list_path": article_list,
        "jsonl_path": tmp_path / "wikitext.jsonl",
        "checkpoint_path": tmp_path / "checkpoint.txt",
        "redirects_path": tmp_path / "redirects.json",
    }


def _rows(jsonl: Path) -> list[dict[str, str]]:
    with open(jsonl, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def test_extracts_listed_article(tmp_path: Path) -> None:
    paths = _setup(tmp_path, ["Anarchism"])
    result = extract_from_dump(**paths)
    rows = _rows(paths["jsonl_path"])
    assert result["found"] == 1
    assert [r["title"] for r in rows] == ["Anarchism"]
    assert rows[0]["wikitext"].startswith("{{Short description|Political philosophy")
    assert paths["checkpoint_path"].read_text(encoding="utf-8") == "Anarchism\n"


def test_collects_only_redirects_into_the_list(tmp_path: Path) -> None:
    paths = _setup(tmp_path, ["Anarchism", "History of Afghanistan"])
    result = extract_from_dump(**paths)
    redirects = json.loads(paths["redirects_path"].read_text(encoding="utf-8"))
    assert redirects == {"AfghanistanHistory": "History of Afghanistan"}
    assert result["redirects"] == 1
    # a redirect page is never stored as an article
    assert [r["title"] for r in _rows(paths["jsonl_path"])] == ["Anarchism"]


def test_merges_existing_redirects(tmp_path: Path) -> None:
    paths = _setup(tmp_path, ["History of Afghanistan"])
    paths["redirects_path"].write_text(json.dumps({"Kamma": "Karma"}), encoding="utf-8")
    extract_from_dump(**paths)
    redirects = json.loads(paths["redirects_path"].read_text(encoding="utf-8"))
    assert redirects == {
        "AfghanistanHistory": "History of Afghanistan",
        "Kamma": "Karma",
    }


def test_reports_titles_missing_from_dump(tmp_path: Path) -> None:
    paths = _setup(tmp_path, ["Anarchism", "History of Afghanistan"])
    result = extract_from_dump(**paths)
    assert result["missing"] == 1
    missing = (tmp_path / "missing_dump.txt").read_text(encoding="utf-8")
    assert missing == "History of Afghanistan\n"


def test_rerun_after_full_pass_does_nothing(tmp_path: Path) -> None:
    paths = _setup(tmp_path, ["Anarchism"])
    extract_from_dump(**paths)
    result = extract_from_dump(**paths)
    assert result["scanned_pages"] == 0
    assert len(_rows(paths["jsonl_path"])) == 1


def test_rerun_without_marker_rescans_for_redirects(tmp_path: Path) -> None:
    paths = _setup(tmp_path, ["Anarchism", "History of Afghanistan"])
    extract_from_dump(**paths)
    (tmp_path / "dump_redirects.done").unlink()
    paths["redirects_path"].unlink()
    result = extract_from_dump(**paths)
    assert result["scanned_pages"] == 3
    assert len(_rows(paths["jsonl_path"])) == 1
    assert json.loads(paths["redirects_path"].read_text(encoding="utf-8")) == {
        "AfghanistanHistory": "History of Afghanistan"
    }

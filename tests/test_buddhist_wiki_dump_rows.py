# -*- coding: utf-8 -*-
"""Tests for the MySQL dump row parser."""

import io

from dictionaries.buddhist_wiki.dump_rows import iter_dump_rows, _unescape


def test_simple_rows() -> None:
    fh = io.StringIO("INSERT INTO `t` VALUES (1,'A','page'),(2,'B','subcat');\n")
    rows = list(iter_dump_rows(fh, "t"))
    assert rows == [[1, "A", "page"], [2, "B", "subcat"]]


def test_escaped_quotes_and_backslashes() -> None:
    fh = io.StringIO(
        "INSERT INTO `t` VALUES (1,'John\\'s \\'wiki\\\\path'),(2,'say \\'\\'hi\\'\\'');\n"
    )
    rows = list(iter_dump_rows(fh, "t"))
    assert rows[0][1] == "John's 'wiki\\path"
    assert rows[1][1] == "say ''hi''"


def test_row_separator_inside_string_not_split() -> None:
    fh = io.StringIO("INSERT INTO `t` VALUES (1,'weird ),( title','x'),(2,'next');\n")
    rows = list(iter_dump_rows(fh, "t"))
    assert rows == [
        [1, "weird ),( title", "x"],
        [2, "next"],
    ]


def test_null_and_parentheses_in_titles() -> None:
    fh = io.StringIO("INSERT INTO `t` VALUES (1,'Foo (bar)',NULL),(2,'Baz (a,b)',3);\n")
    rows = list(iter_dump_rows(fh, "t"))
    assert rows == [[1, "Foo (bar)", None], [2, "Baz (a,b)", 3]]


def test_ignores_other_statements() -> None:
    fh = io.StringIO(
        "CREATE TABLE `t` (a int);\n"
        "INSERT INTO `t` VALUES (1,'one');\n"
        "/* comment */;\n"
        "INSERT INTO `other` VALUES (9,'nine');\n"
    )
    rows = list(iter_dump_rows(fh, "t"))
    assert rows == [[1, "one"]]


def test_unescape_sequences() -> None:
    assert _unescape("a\\nb\\tc\\\\d\\'e") == "a\nb\tc\\d'e"


def test_wikimedia_multiline_values() -> None:
    # real dumps.wikimedia.org layout: VALUES ends the line, rows follow
    fh = io.StringIO(
        "/*!40101 SET NAMES utf8mb4 */;\n"
        "INSERT INTO `page_props` VALUES\n"
        "(103,'hiddencat',''),\n"
        "(104,'disambiguation','');\n"
    )
    rows = list(iter_dump_rows(fh, "page_props"))
    assert rows == [[103, "hiddencat", ""], [104, "disambiguation", ""]]


def test_wikimedia_column_list_layout() -> None:
    fh = io.StringIO(
        "INSERT INTO `page` (page_id,page_namespace,page_title) VALUES\n"
        "(1,0,'A'),\n"
        "(2,14,'Cat');\n"
    )
    rows = list(iter_dump_rows(fh, "page"))
    assert rows == [[1, 0, "A"], [2, 14, "Cat"]]


def test_same_line_layout_still_works() -> None:
    fh = io.StringIO("INSERT INTO `t` VALUES (1,'A'),(2,'B');\n")
    rows = list(iter_dump_rows(fh, "t"))
    assert rows == [[1, "A"], [2, "B"]]


def test_second_insert_statement_after_multiline() -> None:
    fh = io.StringIO(
        "INSERT INTO `t` VALUES\n(1,'one');\nINSERT INTO `t` VALUES\n(2,'two');\n"
    )
    rows = list(iter_dump_rows(fh, "t"))
    assert rows == [[1, "one"], [2, "two"]]

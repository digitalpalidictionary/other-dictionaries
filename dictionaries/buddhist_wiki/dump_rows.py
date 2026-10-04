# -*- coding: utf-8 -*-
"""Minimal MySQL dump INSERT-statement row parser.

Parses the `INSERT INTO `table` VALUES (...),(...);` lines emitted by
dumps.wikimedia.org, using quote-aware scans with str.find jumps so we
never walk the multi-GB text char by char. Only built for the simple
column layouts of the enwiki SQL dumps (no raw newlines inside values).
"""

import re
from typing import Any, Iterator, TextIO

_ESCAPES = {
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "b": "\b",
    "0": "\0",
    "Z": "\x1a",
    "'": "'",
    '"': '"',
    "\\": "\\",
}
_ESCAPE_RE = re.compile(r"\\(.)")


def _unescape(raw: str) -> str:
    return _ESCAPE_RE.sub(lambda m: _ESCAPES.get(m.group(1), m.group(1)), raw)


def _iter_rows(values: str) -> Iterator[str]:
    """Yield the raw text of each top-level (...) row in a values string."""
    i, n = 0, len(values)
    row_start = -1
    while i < n:
        c = values[i]
        if c == "'":
            # jump over the whole string literal (handles \\ and '' escapes)
            j = i + 1
            while True:
                j = values.find("'", j)
                if j == -1:
                    i = n
                    break
                back = j - 1
                slashes = 0
                while back >= 0 and values[back] == "\\":
                    slashes += 1
                    back -= 1
                if slashes % 2 == 1 or values[j + 1 : j + 2] == "'":
                    j = j + 2 if slashes % 2 == 0 else j + 1
                    continue
                i = j + 1
                break
        elif c == "(":
            row_start = i + 1
            i += 1
        elif c == ")":
            if row_start != -1:
                yield values[row_start:i]
                row_start = -1
            i += 1
        else:
            i += 1


def _split_fields(row: str) -> list[str]:
    """Split one row's raw text on top-level commas."""
    fields: list[str] = []
    start = 0
    i, n = 0, len(row)
    while i < n:
        c = row[i]
        if c == "'":
            j = i + 1
            while True:
                j = row.find("'", j)
                if j == -1:
                    i = n
                    break
                back = j - 1
                slashes = 0
                while back >= 0 and row[back] == "\\":
                    slashes += 1
                    back -= 1
                if slashes % 2 == 1 or row[j + 1 : j + 2] == "'":
                    j = j + 2 if slashes % 2 == 0 else j + 1
                    continue
                i = j + 1
                break
        elif c == ",":
            fields.append(row[start:i])
            start = i + 1
            i += 1
        else:
            i += 1
    fields.append(row[start:])
    return fields


def _coerce(field: str) -> Any:
    if field == "NULL":
        return None
    if field.startswith("'"):
        return _unescape(field[1:-1])
    return int(field) if field.lstrip("-").isdigit() else field


def iter_dump_rows(fh: TextIO, table: str) -> Iterator[list[Any]]:
    """Yield each row of `table` as a list of Python values.

    Handles both dump layouts: values on the INSERT line itself, and the
    wikimedia layout where ``INSERT INTO `t` VALUES`` ends the line and
    the rows follow on subsequent lines, optionally after a column list
    (``INSERT INTO `t` (a,b) VALUES``).
    """
    prefix = f"INSERT INTO `{table}`"
    in_insert = False
    buffer: list[str] = []
    for line in fh:
        if not in_insert:
            if not line.startswith(prefix):
                continue
            rest = line[len(prefix) :]
            idx = rest.find("VALUES")
            if idx == -1:
                # values start on the following line(s)
                in_insert = True
                buffer = []
                continue
            after = rest[idx + len("VALUES") :].rstrip("\r\n")
            if after.endswith(";"):
                after = after[:-1]
            if after.strip():
                for row_text in _iter_rows(after):
                    yield [_coerce(f) for f in _split_fields(row_text)]
                continue
            in_insert = True
            buffer = []
            continue
        buffer.append(line)
        if line.rstrip("\r\n").endswith(";"):
            text = "".join(buffer).rstrip()
            if text.endswith(";"):
                text = text[:-1]
            for row_text in _iter_rows(text):
                yield [_coerce(f) for f in _split_fields(row_text)]
            in_insert = False
            buffer = []

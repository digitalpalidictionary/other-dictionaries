"""Sanskrit alphabetical sort key — adapted from tools/pali_sort_key.py."""

import re

_LETTER_TO_NUMBER = {
    "√": "00",
    "a": "01",
    "ā": "02",
    "i": "03",
    "ī": "04",
    "u": "05",
    "ū": "06",
    "ṛ": "07",
    "ṝ": "08",
    "ḷ": "09",
    "ḹ": "10",
    "e": "11",
    "ai": "12",
    "o": "13",
    "au": "14",
    "ḥ": "15",
    "ṃ": "16",
    "k": "17",
    "kh": "18",
    "g": "19",
    "gh": "20",
    "ṅ": "21",
    "c": "22",
    "ch": "23",
    "j": "24",
    "jh": "25",
    "ñ": "26",
    "ṭ": "27",
    "ṭh": "28",
    "ḍ": "29",
    "ḍh": "30",
    "ṇ": "31",
    "t": "32",
    "th": "33",
    "d": "34",
    "dh": "35",
    "n": "36",
    "p": "37",
    "ph": "38",
    "b": "39",
    "bh": "40",
    "m": "41",
    "y": "42",
    "r": "43",
    "l": "44",
    "v": "45",
    "ś": "46",
    "ṣ": "47",
    "s": "48",
    "h": "49",
}

_PATTERN = "|".join(re.escape(k) for k in _LETTER_TO_NUMBER)


def sanskrit_sort_key(word: str) -> str:
    """Return a sort key for Sanskrit alphabetical ordering.

    Input should be IAST-transliterated text.
    Usage:
        sorted_list = sorted(words, key=sanskrit_sort_key)
    """
    if isinstance(word, int):
        return str(word)
    return re.sub(_PATTERN, lambda m: _LETTER_TO_NUMBER[m.group(0)], word)

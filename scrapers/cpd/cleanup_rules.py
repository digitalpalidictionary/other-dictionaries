"""
CPD Cleanup Rules
=================
All transformation rules applied to headword and webkeyword fields.
Source of truth: cleanup.md

Applied in this order by clean.py:
    1. Word-level fixes    — exact replacements for known OCR errors
    2. Char substitutions  — systematic single-character mappings
    3. Slash split         — [[x/y]suffix] → two rows  (must precede delete,
                             which removes the [ ] characters)
    4. Delete chars        — remove unwanted characters entirely
    5. Lowercase           — lowercase the entire string

Note: CPD uses ṁ (U+1E41, dot above) not ṃ (U+1E43, dot below).
"""

# ---------------------------------------------------------------------------
# 1. Word-level fixes
#
# Known OCR errors identified during manual review of diagnose output.
# Applied as exact string replacements before any char-level changes,
# so the original OCR patterns are still intact and matchable.
#
# Characters used as OCR artifacts:
#   I  → l or ll (capital-I mistaken for lowercase-l)
#   P  → trailing artifact, deleted
#   fl → ū  (OCR ligature misread)
#   ft → ññ (OCR ligature misread)
#   f  → ñ  (OCR ligature misread)
#   ê  → different targets each time — no general rule possible
#   à  → different targets each time — no general rule possible
#   ṛ  → r  (Sanskrit character misread — only this one word)
# ---------------------------------------------------------------------------

HEADWORD_WORD_FIXES: dict[str, str] = {
    "aIubbhita":             "alubbhita",
    "IIIīsa":                "illīsa",
    "anujjavatiP":           "anujjavati",
    "apàtheyya":             "apātheyya",
    "àbhideyya":             "abhideyya",
    "asāmaêgiya":            "asāmaggiya",
    "anilêrita":             "anilerita",
    "aṭṭhiṛāsi":             "aṭṭhirāsi",
    "aparibrflhayi":         "aparibrūhayi",
    "anflpaghātika":         "anūpaghātika",
    "ākāsaviñftāṇa":         "ākāsaviññāṇa",
    "ākiñcafiñâyatanasaññā": "ākiñcaññāyatanasaññā",
    "ābhikkhañfta":          "ābhikkhañña",
    "āraftjana":             "ārañjana",
    "icchificchitaṭṭhāna":   "icchiticchitaṭṭhāna",
    "uttamapañfla":          "uttamapañña",
    "kammanipphatfatthaṁ":   "kammanipphattatthaṁ",
    "kafañjali":             "katañjali",
    "kafañjalī":             "katañjalī",
}

WEBKEYWORD_WORD_FIXES: dict[str, str] = {
    "a-Iubbhita":                 "a-lubbhita",
    "IIIīsa":                     "illīsa",
    "anu-jjavatiP":               "anu-jjavati",
    "a-pàtheyya":                 "a-pātheyya",
    "àbhi-deyya":                 "abhi-deyya",
    "a-sāmaêgiya":                "a-sāmaggiya",
    "anilêrita":                  "anilerita",
    "aṭṭhi-ṛāsi":                 "aṭṭhi-rāsi",
    "a-paribrflhayi":             "a-paribrūhayi",
    "an-flpaghātika":             "an-ūpaghātika",
    "ākāsa-viñftāṇa":             "ākāsa-viññāṇa",
    "ākiñcafiñâyatana-saññā":     "ākiñcaññâyatana-saññā",
    "ābhikkhañfta":               "ābhikkhañña",
    "āraftjana":                  "ārañjana",
    "icchif-icchita-ṭṭhāna":      "icchit-icchita-ṭṭhāna",
    "uttama-pañfla":              "uttama-pañña",
    "kamma-nipphatf-atthaṁ":      "kamma-nipphatt-atthaṁ",
    "kaf-añjali":                 "kat-añjali",
    "kaf-añjalī":                 "kat-añjalī",
}


# ---------------------------------------------------------------------------
# 2. Character substitutions
#
# Applied to both headword and webkeyword after word-level fixes.
# These are systematic encoding/OCR errors where one character
# consistently stands in for a specific Pali character.
#
# Not included here (no general rule — context-dependent):
#   à  \u00e0  maps to both a and ā depending on word — word fixes only
#   ê  \u00ea  maps to gg, e, etc. depending on word — word fixes only
#   f  \u0066  maps to ū, ñ, etc. depending on context — word fixes only
#   ṛ  \u1e5b  maps to r in one word only — word fix only
# ---------------------------------------------------------------------------

CHAR_SUBSTITUTIONS: dict[str, str] = {
    "â": "ā",   # a with circumflex  → a with macron
    "á": "a",   # a with acute       → plain a
    "ã": "ā",   # a with tilde       → a with macron
    "í": "ī",   # i with acute       → i with macron
    "î": "ī",   # i with circumflex  → i with macron
    "ï": "ī",   # i with diaeresis   → i with macron
    "ô": "o",   # o with circumflex  → plain o
    "û": "ū",   # u with circumflex  → u with macron
    "ă": "ā",   # a with breve       → a with macron
    "ĩ": "ī",   # i with tilde       → i with macron
    "ĭ": "ī",   # i with breve       → i with macron
    "ň": "ṅ",   # n with caron       → n with dot above (velar nasal)
    "Ā": "ā",   # A with macron      → a with macron  (also caught by lowercase)
    "Ī": "ī",   # I with macron      → i with macron  (also caught by lowercase)
    "Ū": "ū",   # U with macron      → u with macron
    "ḥ": "h",   # h with dot below   → plain h (Sanskrit visarga → Pali h)
}


# ---------------------------------------------------------------------------
# 3. Characters to delete
#
# Removed entirely. Applied after slash split so [ ] and / are still
# available for pattern matching during the split step.
#
# &gt; is the HTML entity for > appearing as a literal 4-char string.
# It is listed first so it is removed as a unit before & is processed.
# ---------------------------------------------------------------------------

HEADWORD_DELETE: list[str] = [
    "&gt;",                              # HTML entity — removed as full string
    "\u0306",                            # combining breve — no visible effect, removed
    "(", ")",
    '"',
    "'", "\u2019",                       # ASCII apostrophe + right single quote
    "*",
    ",",
    "/",                                 # bare / remaining after slash split
    "0", "1", "2", "3", "4",
    "5", "6", "7", "8", "9",
    ":",
    ";",
    "?",
    "[", "]",
    "~",
    "°",
    "´",
    "†",
]

WEBKEYWORD_DELETE: list[str] = [
    "&gt;",                              # HTML entity — removed as full string
    "\u0306",                            # combining breve — no visible effect, removed
    "(", ")",
    '"',
    "'", "\u2019",                       # ASCII apostrophe + right single quote
    "*",
    ",",
    ":",
    "?",
    "[", "]",
    "~",
    "°",
    "´",
    "†",
    "\xa0",                              # non-breaking space
]


# ---------------------------------------------------------------------------
# Characters explicitly allowed in each field (used by diagnose.py)
#
# Space: legitimate in multi-word headwords (e.g. "a karaṇīya")
# ṁ:     CPD uses ṁ (U+1E41, dot above) rather than standard ṃ (U+1E43)
# ṛ:     Sanskrit ṛ legitimately appears in some CPD entries
# ---------------------------------------------------------------------------

HEADWORD_ALLOW_EXTRA: list[str] = [" ", "ṁ", "ṛ"]
WEBKEYWORD_ALLOW_EXTRA: list[str] = [" ", "ṁ", "ṛ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

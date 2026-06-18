"""Custom fontbakery checks shared between the Roboto profiles.

Each profile (general/android/web) loads this module via the
``check_definitions`` field of its ``PROFILE`` dict and then references the
relevant check ids in its ``sections``. Profile-specific checks (vertical
metrics, charset coverage, features) are registered with distinct ids so the
three profiles can keep their own thresholds.
"""
from fontbakery.prelude import check, condition, FAIL, PASS
from fontbakery.testable import Font


# ---------------------------------------------------------------------------
# Conditions
# ---------------------------------------------------------------------------

@condition(Font)
def font_features(font):
    """Union of GSUB and GPOS feature tags present in the font."""
    ttFont = font.ttFont
    tags = set()
    if "GSUB" in ttFont:
        tags |= {f.FeatureTag for f in ttFont["GSUB"].table.FeatureList.FeatureRecord}
    if "GPOS" in ttFont:
        tags |= {f.FeatureTag for f in ttFont["GPOS"].table.FeatureList.FeatureRecord}
    return frozenset(tags)


# ---------------------------------------------------------------------------
# Helpers (used inside check functions)
# ---------------------------------------------------------------------------

def _font_style(ttFont):
    subfamily_name = ttFont["name"].getName(2, 3, 1, 1033)
    typo_subfamily_name = ttFont["name"].getName(17, 3, 1, 1033)
    if typo_subfamily_name:
        return typo_subfamily_name.toUnicode()
    return subfamily_name.toUnicode()


def _font_family(ttFont):
    family_name = ttFont["name"].getName(1, 3, 1, 1033)
    typo_family_name = ttFont["name"].getName(16, 3, 1, 1033)
    if typo_family_name:
        return typo_family_name.toUnicode()
    return family_name.toUnicode()


def _check_metrics(ttFont, expected):
    failed = []
    for (table, k), v in expected.items():
        font_val = getattr(ttFont[table], k)
        if font_val != v:
            failed.append((table, k, v, font_val))
    if not failed:
        yield PASS, "Fonts have correct vertical metrics"
    else:
        msg = "\n".join(
            f"- {tbl}.{k} is {font_val} it should be {v}"
            for tbl, k, v, font_val in failed
        )
        yield FAIL, f"Fonts have incorrect vertical metrics:\n{msg}"


def _check_charset(ttFont, include_glyphs, exclude_glyphs):
    font_unicodes = set(ttFont.getBestCmap().keys())

    missing = include_glyphs - font_unicodes
    if missing:
        yield FAIL, (
            "Font must include the following codepoints "
            f"{sorted(map(hex, missing))}"
        )
    else:
        yield PASS, "Font includes correct encoded glyphs"

    overlap = exclude_glyphs & font_unicodes
    if overlap:
        yield FAIL, (
            "Font must exclude the following codepoints "
            f"{sorted(map(hex, overlap))}"
        )
    else:
        yield PASS, "Font excludes correct encoded glyphs"


def _check_features(font_features, expected):
    missing = expected - font_features
    if missing:
        yield FAIL, f"Font is missing features {sorted(missing)}"
    else:
        yield PASS, "Font has correct features"


# ---------------------------------------------------------------------------
# Per-profile data
# ---------------------------------------------------------------------------

GENERAL_INCLUDE_GLYPHS = frozenset([
    0x2117,  # SOUND RECORDING COPYRIGHT
    0xEE01, 0xEE02, 0xF6C3,  # legacy PUA
    # superior and inferior figures
    0x2070, 0x2074, 0x2075, 0x2076, 0x2077, 0x2078, 0x2079,
    0x2080, 0x2081, 0x2082, 0x2083, 0x2084, 0x2085, 0x2086,
    0x2087, 0x2088, 0x2089,
])
GENERAL_EXCLUDE_GLYPHS = frozenset(
    [0x2072, 0x2073, 0x208F]
    + list(range(0xE000, 0xF8FF + 1))
    + list(range(0xF0000, 0x10FFFF + 1))
) - GENERAL_INCLUDE_GLYPHS

ANDROID_INCLUDE_GLYPHS = frozenset(
    [0x2117, 0xEE01, 0xEE02, 0xF6C3]
    + list(range(0x0000, 0x0020))  # First 32 control characters
)
ANDROID_EXCLUDE_GLYPHS = frozenset(
    [
        0x20E3,  # COMBINING ENCLOSING KEYCAP
        0x2191,  # UPWARDS ARROW
        0x2193,  # DOWNWARDS ARROW
        0x2072, 0x2073, 0x208F,
    ]
    + list(range(0xE000, 0xF8FF + 1))
    + list(range(0xF0000, 0x10FFFF + 1))
) - ANDROID_INCLUDE_GLYPHS

WEB_INCLUDE_GLYPHS = frozenset([
    0x2070, 0x2074, 0x2075, 0x2076, 0x2077, 0x2078, 0x2079,
    0x2080, 0x2081, 0x2082, 0x2083, 0x2084, 0x2085, 0x2086,
    0x2087, 0x2088, 0x2089,
])
# test_web.py reused the general exclude_glyphs
WEB_EXCLUDE_GLYPHS = GENERAL_EXCLUDE_GLYPHS

GENERAL_INCLUDE_FEATURES = frozenset([
    "frac", "subs", "salt", "numr", "sups", "unic", "ccmp", "c2sc", "smcp",
    "dnom", "dlig", "onum", "lnum", "tnum", "ss06", "ss07", "ss02", "ss01",
    "ss04", "liga", "locl", "ss05", "pnum", "ss03",
])
ANDROID_INCLUDE_FEATURES = GENERAL_INCLUDE_FEATURES
WEB_INCLUDE_FEATURES = frozenset([
    "c2sc", "ccmp", "cpsp", "dlig", "dnom", "frac", "kern", "liga", "lnum",
    "locl", "numr", "onum", "pnum", "smcp", "ss01", "ss02", "ss03", "ss04",
    "ss05", "ss06", "ss07", "tnum", "sups", "subs",
])

GENERAL_VERTICAL_METRICS = {
    ("head", "yMin"): -555,
    ("head", "yMax"): 2163,
    ("hhea", "descent"): -500,
    ("hhea", "ascent"): 1900,
    ("hhea", "lineGap"): 0,
    ("OS/2", "sTypoDescender"): -555,
    ("OS/2", "sTypoAscender"): 2146,
    ("OS/2", "sTypoLineGap"): 0,
    ("OS/2", "usWinDescent"): 555,
    ("OS/2", "usWinAscent"): 2146,
}
# Android values come from v2.136 android fonts
# https://github.com/googlefonts/roboto/releases/tag/v2.136
ANDROID_VERTICAL_METRICS = dict(GENERAL_VERTICAL_METRICS)
WEB_VERTICAL_METRICS = {
    ("head", "yMin"): -555,
    ("head", "yMax"): 2163,
    ("hhea", "descent"): -500,
    ("hhea", "ascent"): 1900,
    ("hhea", "lineGap"): 0,
    ("OS/2", "sTypoDescender"): -512,
    ("OS/2", "sTypoAscender"): 1536,
    ("OS/2", "sTypoLineGap"): 102,
    ("OS/2", "usWinDescent"): 512,
    ("OS/2", "usWinAscent"): 1946,
}


# ---------------------------------------------------------------------------
# Shared checks
# ---------------------------------------------------------------------------

ROBOTO_PROPOSAL = "https://github.com/googlefonts/roboto-classic"


@check(
    id="com.roboto.fonts/check/italic_angle",
    conditions=["is_italic"],
    rationale="Italic Roboto fonts must have post.italicAngle set to -12.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_italic_angle(ttFont):
    """Check italic fonts have correct italic angle"""
    if ttFont["post"].italicAngle != -12:
        yield FAIL, "post.italicAngle must be set to -12"
    else:
        yield PASS, "post.italicAngle is set correctly"


@check(
    id="com.roboto.fonts/check/fs_type",
    rationale="OS/2.fsType should be 0 (Installable Embedding).",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_fs_type(ttFont):
    """Check OS/2 fsType is 0"""
    if ttFont["OS/2"].fsType != 0:
        yield FAIL, "OS/2.fsType must be 0"
    else:
        yield PASS, "OS/2.fsType is set correctly"


@check(
    id="com.roboto.fonts/check/vendorid",
    rationale="OS/2.achVendID must be 'GOOG'.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_vendorid(ttFont):
    """Check vendorID is correct"""
    if ttFont["OS/2"].achVendID != "GOOG":
        yield FAIL, "OS/2.achVendID must be set to 'GOOG'"
    else:
        yield PASS, "OS/2.achVendID is set correctly"


@check(
    id="com.roboto.fonts/check/name_copyright",
    rationale="Roboto's copyright string is fixed.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_copyright(ttFont):
    """Check font copyright is correct"""
    expected = (
        "Copyright 2011 The Roboto Project Authors "
        "(https://github.com/googlefonts/roboto-classic)"
    )
    record = ttFont["name"].getName(0, 3, 1, 1033).toUnicode()
    if record == expected:
        yield PASS, "Copyright is correct"
    else:
        yield FAIL, f"Copyright is incorrect. It should be {expected}"


@check(
    id="com.roboto.fonts/check/name_unique_id",
    rationale="Unique ID should be 'Google:<family> <style>:2016'.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_name_unique_id(ttFont):
    """Check font unique id is correct"""
    family_name = _font_family(ttFont)
    style = _font_style(ttFont)
    expected = f"Google:{family_name} {style}:2016"
    font_unique_id = ttFont["name"].getName(3, 3, 1, 1033).toUnicode()
    if font_unique_id == expected:
        yield PASS, "Unique ID is correct"
    else:
        yield FAIL, (
            f"Unique ID, '{font_unique_id}' is incorrect. "
            f"It should be '{expected}'"
        )


@check(
    id="com.roboto.fonts/check/digit_widths",
    rationale="All decimal digit glyphs must have the same advance width.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_digit_widths(ttFont):
    """Check that all digits have the same width"""
    widths = {
        ttFont["hmtx"][name][0]
        for name in (
            "zero", "one", "two", "three", "four",
            "five", "six", "seven", "eight", "nine",
        )
    }
    if len(widths) != 1:
        yield FAIL, "Numerals 0-9 do not have the same width"
    else:
        yield PASS, "Numerals 0-9 have the same width"


@check(
    id="com.roboto.fonts/check/cmap4",
    rationale="Font should contain a MS Unicode BMP cmap subtable.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_cmap4(ttFont):
    """Check fonts have cmap format 4"""
    cmap_table = ttFont["cmap"].getcmap(3, 1)
    if cmap_table and cmap_table.format == 4:
        yield PASS, "Font contains a MS Unicode BMP encoded cmap"
    else:
        yield FAIL, "Font does not contain a MS Unicode BMP encoded cmap"


# ---------------------------------------------------------------------------
# General profile checks
# ---------------------------------------------------------------------------

@check(
    id="com.roboto.fonts/check/general/vertical_metrics",
    rationale="Roboto general vertical metrics must match the v2.136 release.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_general_vertical_metrics(ttFont):
    """Check vertical metrics are correct (general profile)"""
    yield from _check_metrics(ttFont, GENERAL_VERTICAL_METRICS)


@check(
    id="com.roboto.fonts/check/general/charset_coverage",
    rationale="Required encoded glyphs must be present and PUA codepoints absent.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_general_charset_coverage(ttFont):
    """Check certain unicode encoded glyphs are included and excluded (general)"""
    yield from _check_charset(ttFont, GENERAL_INCLUDE_GLYPHS, GENERAL_EXCLUDE_GLYPHS)


@check(
    id="com.roboto.fonts/check/general/features",
    rationale="General Roboto builds must contain a fixed set of OT features.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_general_features(font_features):
    """Check font has correct features (general).
    https://github.com/googlefonts/roboto-classic/issues/97"""
    yield from _check_features(font_features, GENERAL_INCLUDE_FEATURES)


# ---------------------------------------------------------------------------
# Android profile checks
# ---------------------------------------------------------------------------

@check(
    id="com.roboto.fonts/check/android/vertical_metrics",
    rationale="Roboto Android vertical metrics match the v2.136 release.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_android_vertical_metrics(ttFont):
    """Check vertical metrics are correct (android profile)"""
    yield from _check_metrics(ttFont, ANDROID_VERTICAL_METRICS)


@check(
    id="com.roboto.fonts/check/android/charset_coverage",
    rationale="Android subset includes control chars and excludes some symbols.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_android_charset_coverage(ttFont):
    """Check certain unicode encoded glyphs are included and excluded (android)"""
    yield from _check_charset(ttFont, ANDROID_INCLUDE_GLYPHS, ANDROID_EXCLUDE_GLYPHS)


@check(
    id="com.roboto.fonts/check/android/features",
    rationale="Android Roboto builds must contain a fixed set of OT features.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_android_features(font_features):
    """Check font has correct features (android)."""
    yield from _check_features(font_features, ANDROID_INCLUDE_FEATURES)


@check(
    id="com.roboto.fonts/check/glyph_dont_round_to_grid",
    rationale="Round-to-grid flag must be off for ellipsis components on Android.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_glyph_dont_round_to_grid(ttFont):
    """Test certain glyphs don't round to grid"""
    failed = False
    for name in ["ellipsis"]:
        glyph = ttFont["glyf"][name]
        for component in glyph.components:
            if component.flags & (1 << 2):
                failed = True
                yield FAIL, (
                    f"Round to grid flag must be disabled for '{name}' components"
                )
    if not failed:
        yield PASS, "Glyphs do not have round to grid enabled"


# ---------------------------------------------------------------------------
# Web profile checks
# ---------------------------------------------------------------------------

@check(
    id="com.roboto.fonts/check/web/vertical_metrics",
    rationale="Roboto Web's OS/2 win values match the v1 metrics.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_web_vertical_metrics(ttFont):
    """Check vertical metrics are correct (web profile)"""
    yield from _check_metrics(ttFont, WEB_VERTICAL_METRICS)


@check(
    id="com.roboto.fonts/check/web/charset_coverage",
    rationale="Web subset must include superior/inferior figures.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_web_charset_coverage(ttFont):
    """Check certain unicode encoded glyphs are included and excluded (web)"""
    yield from _check_charset(ttFont, WEB_INCLUDE_GLYPHS, WEB_EXCLUDE_GLYPHS)


@check(
    id="com.roboto.fonts/check/web/features",
    rationale="Web Roboto builds must contain a fixed set of OT features.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_web_features(font_features):
    """Check font has correct features (web)."""
    yield from _check_features(font_features, WEB_INCLUDE_FEATURES)


@check(
    id="com.roboto.fonts/check/oblique_bits_not_set",
    rationale="OS/2.fsSelection bit 9 (Oblique) must not be set.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_oblique_bits_not_set(ttFont):
    """Check oblique bits are not set in fonts"""
    if ttFont["OS/2"].fsSelection & (1 << 9) != 0:
        yield FAIL, "fsSelection bit 9 (Oblique) must not be enabled"
    else:
        yield PASS, "fsSelection bit 9 is disabled"


@check(
    id="com.roboto.fonts/check/web/unique_id",
    rationale="Web build's unique ID is the family/style name (no Google: prefix).",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_web_unique_id(ttFont):
    """Check font unique id is correct (web)"""
    family_name = _font_family(ttFont)
    style = _font_style(ttFont)
    expected = family_name if style == "Regular" else f"{family_name} {style}"
    font_unique_id = ttFont["name"].getName(3, 3, 1, 1033).toUnicode()
    if font_unique_id == expected:
        yield PASS, "Unique ID is correct"
    else:
        yield FAIL, (
            f"Unique ID, '{font_unique_id}' is incorrect. "
            f"It should be '{expected}'"
        )


@check(
    id="com.roboto.fonts/check/hinting",
    rationale="Web binaries are hinted; every contour glyph should carry a TT program.",
    proposal=ROBOTO_PROPOSAL,
)
def com_roboto_fonts_check_hinting(ttFont):
    """Check glyphs have hinting"""
    # we can ignore these according to Mike D
    # https://github.com/TypeNetwork/Roboto/issues/70#issuecomment-641221200
    ignore = {".notdef", "uni0488", "uni0489", "uniFFFC", "uniFFFD"}
    missing = []
    for glyph_name in ttFont.getGlyphOrder():
        glyph = ttFont["glyf"][glyph_name]
        if glyph.numberOfContours <= 0:
            continue
        if len(glyph.program.bytecode) <= 0 and glyph_name not in ignore:
            missing.append(glyph_name)
    if missing:
        yield FAIL, f"Following glyphs are missing hinting {missing}"
    else:
        yield PASS, "All glyphs are hinted"

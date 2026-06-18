"""Fontbakery profile for the general (unhinted) Roboto build.

Run with::

    fontbakery check-profile tests/test_general.py \\
        fonts/unhinted/Roboto[ital,wdth,wght].ttf
"""
import os

_HERE = os.path.dirname(os.path.abspath(__file__))

# Universal/opentype checks that fail on Roboto v2 by design and can't be
# fixed without causing regressions in a family delivered ~40B times per week.
EXCLUDED_INHERITED_CHECKS = [
    "required_tables",
    "family/win_ascent_and_descent",
    "os2_metrics_match_hhea",
    "fontbakery_version",
    "outline_semi_vertical",
    "outline_jaggy_segments",
    "outline_colinear_vectors",
    "outline_short_segments",
    "outline_alignment_miss",
    "opentype/varfont/valid_default_instance_nameids",
    "varfont/unsupported_axes",
    "smart_dropout",
    "no_mac_entries",
    "control_chars",
    "case_mapping",
    "base_has_width"
]

PROFILE = {
    "include_profiles": ["universal"],
    "check_definitions": [os.path.join(_HERE, "roboto_checks.py")],
    "sections": {
        "Roboto v3 general": [
            # selected googlefonts/opentype checks
            "googlefonts/weightclass",
            "opentype/fsselection",
            # custom Roboto checks
            "com.roboto.fonts/check/italic_angle",
            "com.roboto.fonts/check/fs_type",
            "com.roboto.fonts/check/vendorid",
            "com.roboto.fonts/check/digit_widths",
            "com.roboto.fonts/check/name_copyright",
            "com.roboto.fonts/check/name_unique_id",
            "com.roboto.fonts/check/cmap4",
            "com.roboto.fonts/check/general/vertical_metrics",
            "com.roboto.fonts/check/general/charset_coverage",
            "com.roboto.fonts/check/general/features",
        ],
    },
    "exclude_checks": EXCLUDED_INHERITED_CHECKS,
}

"""Fontbakery profile for the Web Roboto build.

Run with::

    fontbakery check-profile tests/test_web.py \\
        fonts/web/Roboto[ital,wdth,wght].ttf
"""
import os

_HERE = os.path.dirname(os.path.abspath(__file__))

PROFILE = {
    "check_definitions": [os.path.join(_HERE, "roboto_checks.py")],
    "sections": {
        "Roboto web v3": [
            "com.roboto.fonts/check/italic_angle",
            "com.roboto.fonts/check/fs_type",
            "com.roboto.fonts/check/vendorid",
            "com.roboto.fonts/check/digit_widths",
            "com.roboto.fonts/check/oblique_bits_not_set",
            "com.roboto.fonts/check/hinting",
            "com.roboto.fonts/check/web/unique_id",
            "com.roboto.fonts/check/web/vertical_metrics",
            "com.roboto.fonts/check/web/charset_coverage",
            "com.roboto.fonts/check/web/features",
        ],
    },
}

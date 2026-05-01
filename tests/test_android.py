"""Fontbakery profile for the Android Roboto build.

Run with::

    fontbakery check-profile tests/test_android.py \\
        fonts/android/Roboto[ital,wdth,wght].ttf
"""
import os

_HERE = os.path.dirname(os.path.abspath(__file__))

PROFILE = {
    "check_definitions": [os.path.join(_HERE, "roboto_checks.py")],
    "sections": {
        "Roboto android v3": [
            "com.roboto.fonts/check/italic_angle",
            "com.roboto.fonts/check/fs_type",
            "com.roboto.fonts/check/vendorid",
            "com.roboto.fonts/check/digit_widths",
            "com.roboto.fonts/check/glyph_dont_round_to_grid",
            "com.roboto.fonts/check/android/vertical_metrics",
            "com.roboto.fonts/check/android/charset_coverage",
            "com.roboto.fonts/check/android/features",
        ],
    },
}

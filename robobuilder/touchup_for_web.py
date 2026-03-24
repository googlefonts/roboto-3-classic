"""Web-specific font touchups."""
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from robobuilder.utils import (
    disable_oblique_bits,
    update_attribs,
    update_font_version,
    update_gasp,
    update_psname_and_fullname,
)


def main(font_path):
    font = TTFont(font_path)
    filename = Path(font_path).name
    # Set usWeightClass to 250 for Thin fonts
    if "Thin" in filename and "fvar" not in font:
        font['OS/2'].usWeightClass = 250
    # Update vertical metrics to match v2.138 webfonts
    update_attribs(
        font,
        **{"ascent": 1900,
           "descent": -500,
           "sTypoAscender": 1536,
           "sTypoDescender": -512,
           "sTypoLineGap": 102,
           "usWinAscent": 1946,
           "usWinDescent": 512,}
    )
    update_psname_and_fullname(font)
    update_gasp(font, {8: 8, 65535: 15})
    disable_oblique_bits(font)
    update_font_version(font)
    font.save(font_path)


if __name__ == "__main__":
    main(sys.argv[1])

"""ChromeOS-specific font touchups."""
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from robobuilder.utils import (
    ANDROID_AND_CROS_VERT_METRICS,
    disable_oblique_bits,
    update_attribs,
    update_font_version,
    update_psname_and_fullname,
)


def main(font_path):
    font = TTFont(font_path, recalcBBoxes=False)
    update_attribs(font, **ANDROID_AND_CROS_VERT_METRICS)
    update_psname_and_fullname(font)
    update_font_version(font)
    disable_oblique_bits(font)
    # Enable Bold bits for Black fonts
    if "Black" in Path(font_path).name:
        font['head'].macStyle |= (1 << 0)
        font['OS/2'].fsSelection |= (1 << 5)
        font['OS/2'].fsSelection &= ~(1 << 6)
    font.save(font_path)


if __name__ == "__main__":
    main(sys.argv[1])

"""Android-specific font touchups."""
import sys
from fontTools.ttLib import TTFont
from nototools import font_data
from robobuilder.utils import (
    ANDROID_AND_CROS_VERT_METRICS,
    update_attribs,
    update_font_version,
    update_psname_and_fullname,
)


def main(font_path):
    font = TTFont(font_path, recalcBBoxes=False)
    glyf = font["glyf"]
    # turn off round-to-grid flags in certain problem components
    # https://github.com/google/roboto/issues/153
    ellipsis = glyf['ellipsis']
    for component in ellipsis.components:
        component.flags &= ~(1 << 2)

    # Add first 32 control chars to font.
    for table in font["cmap"].tables:
        for uni in range(32):
            if uni in table.cmap:
                continue
            table.cmap[uni] = "uni0002"

    font_data.delete_from_cmap(font, [
        0x20E3,  # COMBINING ENCLOSING KEYCAP
        0x2191,  # UPWARDS ARROW
        0x2193,  # DOWNWARDS ARROW
    ])
    update_attribs(font, **ANDROID_AND_CROS_VERT_METRICS)
    update_psname_and_fullname(font, include_year=True)
    update_font_version(font)
    font.save(font_path)


if __name__ == "__main__":
    main(sys.argv[1])

"""Split a variable font with an ital axis into separate Roman and Italic VFs."""
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables as ot
from fontTools.varLib.instancer import (
    instantiateVariableFont,
    sanityCheckVariableTables,
)


def split_slnt(ttfont, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    sanityCheckVariableTables(ttfont)

    axes = {a.axisTag: a for a in ttfont['fvar'].axes}
    ital_angle = axes['ital'].maxValue
    roman = instantiateVariableFont(ttfont, {"ital": 0}, updateFontNames=True)
    italic = instantiateVariableFont(ttfont, {"ital": ital_angle}, updateFontNames=True)

    _update_roman_stat(roman)
    _update_italic_stat(italic)

    roman.save(str(out_dir / vf_filename(roman)))
    italic.save(str(out_dir / vf_filename(italic)))


def _update_roman_stat(ttfont):
    stat = ttfont['STAT'].table
    record = ot.AxisValue()
    record.AxisIndex = 2
    record.Flags = 2
    record.ValueNameID = 296  # Roman
    record.LinkedValue = 1
    record.Value = 0
    record.Format = 3
    stat.AxisValueArray.AxisValue[-1] = record


def _update_italic_stat(ttfont):
    stat = ttfont['STAT'].table
    record = ot.AxisValue()
    record.AxisIndex = 2
    record.Flags = 0
    record.ValueNameID = 258  # Italic
    record.Value = 1.0
    record.Format = 1
    stat.AxisValueArray.AxisValue[-1] = record


def vf_filename(ttfont):
    axes = sorted([a.axisTag for a in ttfont['fvar'].axes])
    axes = ",".join(axes)
    family_name = ttfont['name'].getName(1, 3, 1, 1033)
    name = family_name.toUnicode()
    if "Italic" in ttfont['name'].getName(2, 3, 1, 1033).toUnicode():
        return f"{name}-Italic[{axes}].ttf"
    return f"{name}[{axes}].ttf"


def main(font_path, out_dir):
    ttfont = TTFont(font_path)
    split_slnt(ttfont, out_dir)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

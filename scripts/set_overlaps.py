"""Taken from https://github.com/google/fonts/issues/4405#issuecomment-1079185880"""
from __future__ import annotations

import argparse
from typing import Any, Mapping

import pathops
from fontTools.ttLib import TTFont
from fontTools.ttLib.removeOverlaps import componentsOverlap, skPathFromGlyph
from fontTools.ttLib.tables import _g_l_y_f


def set_overlap_bits_if_overlapping(varfont: TTFont) -> tuple[int, int]:
    glyph_set = varfont.getGlyphSet()
    glyf_table: _g_l_y_f.table__g_l_y_f = varfont["glyf"]
    flag_overlap_compound = _g_l_y_f.OVERLAP_COMPOUND
    flag_overlap_simple = _g_l_y_f.flagOverlapSimple
    overlapping_contours = 0
    overlapping_components = 0
    for glyph_name in glyf_table.keys():
        glyph = glyf_table[glyph_name]
        # Set OVERLAP_COMPOUND bit for compound glyphs
        if glyph.isComposite() and componentsOverlap(glyph, glyph_set):
            overlapping_components += 1
            glyph.components[0].flags |= flag_overlap_compound
        # Set OVERLAP_SIMPLE bit for simple glyphs
        elif glyph.numberOfContours > 0 and glyph_overlaps(glyph_name, glyph_set):
            overlapping_contours += 1
            glyph.flags[0] |= flag_overlap_simple
    return (overlapping_contours, overlapping_components)


def glyph_overlaps(glyph_name: str, glyph_set: Mapping[str, Any]) -> bool:
    path = skPathFromGlyph(glyph_name, glyph_set)
    path2 = pathops.simplify(path, clockwise=path.clockwise)  # remove overlaps
    if path != path2:
        return True
    return False


parser = argparse.ArgumentParser()
parser.add_argument("font", type=TTFont)
parsed_args = parser.parse_args()

font = parsed_args.font
ocont, ocomp = set_overlap_bits_if_overlapping(font)
num_glyphs = font["maxp"].numGlyphs
ocont_p = ocont / num_glyphs
ocomp_p = ocomp / num_glyphs
print(
    font.reader.file.name,
    f"{num_glyphs} glyphs, {ocont} overlapping contours ({ocont_p:.2%}), {ocomp} overlapping components ({ocomp_p:.2%})",
)
font.save(font.reader.file.name)

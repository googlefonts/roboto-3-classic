import sys
import shutil
import os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from scripts import (
    update_names,
    update_attribs,
    mkdir
)


instances = [
    {
        "attribs": {"fsSelection": 64, "macStyle": 0, "usWeightClass": 250},
        "axes": {"ital": 0.0, "wdth": 100, "wght": 100},
        "filename": "Roboto-Thin.ttf",
        "names": {
            "1,3,1,1033": "Roboto Thin",
            "16,3,1,1033": "Roboto",
            "17,3,1,1033": "Thin",
            "2,3,1,1033": "Regular",
            "3,3,1,1033": "Google:Roboto Thin:2016",
            "4,3,1,1033": "Roboto Thin",
            "6,3,1,1033": "Roboto-Thin",
        },
    },
    {
        "attribs": {"fsSelection": 513, "macStyle": 2, "usWeightClass": 250, "italicAngle": -12, "caretSlopeRise": 2048, "caretSlopeRun": 435},
        "axes": {"ital": 1.0, "wdth": 100, "wght": 100},
        "filename": "Roboto-ThinItalic.ttf",
        "names": {
            "1,3,1,1033": "Roboto Thin",
            "16,3,1,1033": "Roboto",
            "17,3,1,1033": "Thin Italic",
            "2,3,1,1033": "Italic",
            "3,3,1,1033": "Google:Roboto Thin Italic:2016",
            "4,3,1,1033": "Roboto Thin Italic",
            "6,3,1,1033": "Roboto-ThinItalic",
        },
    },
    {
        "attribs": {"fsSelection": 64, "macStyle": 0, "usWeightClass": 300},
        "axes": {"ital": 0.0, "wdth": 100, "wght": 300},
        "filename": "Roboto-Light.ttf",
        "names": {
            "1,3,1,1033": "Roboto Light",
            "16,3,1,1033": "Roboto",
            "17,3,1,1033": "Light",
            "2,3,1,1033": "Regular",
            "3,3,1,1033": "Google:Roboto Light:2016",
            "4,3,1,1033": "Roboto Light",
            "6,3,1,1033": "Roboto-Light",
        },
    },
    {
        "attribs": {"fsSelection": 64, "macStyle": 0, "usWeightClass": 300, "usWidthClass": 3},
        "axes": {"ital": 0.0, "wdth": 75.0, "wght": 300},
        "filename": "RobotoCondensed-Light.ttf",
        "names": {
            "1,3,1,1033": "Roboto Condensed Light",
            "16,3,1,1033": "Roboto Condensed",
            "17,3,1,1033": "Light",
            "2,3,1,1033": "Regular",
            "3,3,1,1033": "Google:Roboto Condensed Light:2016",
            "4,3,1,1033": "Roboto Condensed Light",
            "6,3,1,1033": "RobotoCondensed-Light",
        },
    },
    {
        "attribs": {"fsSelection": 513, "macStyle": 2, "usWeightClass": 300, "italicAngle": -12, "usWidthClass": 3, "caretSlopeRise": 2048, "caretSlopeRun": 435},
        "axes": {"ital": 1.0, "wdth": 75.0, "wght": 300},
        "filename": "RobotoCondensed-LightItalic.ttf",
        "names": {
            "1,3,1,1033": "Roboto Condensed Light",
            "16,3,1,1033": "Roboto Condensed",
            "17,3,1,1033": "Light Italic",
            "2,3,1,1033": "Italic",
            "3,3,1,1033": "Google:Roboto Condensed Light Italic:2016",
            "4,3,1,1033": "Roboto Condensed Light Italic",
            "6,3,1,1033": "RobotoCondensed-LightItalic",
        },
    },
    {
        "attribs": {"fsSelection": 513, "macStyle": 2, "usWeightClass": 300, "italicAngle": -12, "caretSlopeRise": 2048, "caretSlopeRun": 435},
        "axes": {"ital": 1.0, "wdth": 100, "wght": 300},
        "filename": "Roboto-LightItalic.ttf",
        "names": {
            "1,3,1,1033": "Roboto Light",
            "16,3,1,1033": "Roboto",
            "17,3,1,1033": "Light Italic",
            "2,3,1,1033": "Italic",
            "3,3,1,1033": "Google:Roboto Light Italic:2016",
            "4,3,1,1033": "Roboto Light Italic",
            "6,3,1,1033": "Roboto-LightItalic",
        },
    },
    {
        "attribs": {"fsSelection": 64, "macStyle": 0, "usWeightClass": 400},
        "axes": {"ital": 0.0, "wdth": 100, "wght": 400},
        "filename": "Roboto-Regular.ttf",
        "names": {
            "1,3,1,1033": "Roboto",
            "2,3,1,1033": "Regular",
            "3,3,1,1033": "Google:Roboto Regular:2016",
            "4,3,1,1033": "Roboto",
            "6,3,1,1033": "Roboto-Regular",
        },
    },
    {
            "attribs": {"fsSelection": 64, "macStyle": 0, "usWeightClass": 400, "usWidthClass": 3},
        "axes": {"ital": 0.0, "wdth": 75.0, "wght": 400},
        "filename": "RobotoCondensed-Regular.ttf",
        "names": {
            "1,3,1,1033": "Roboto Condensed",
            "2,3,1,1033": "Regular",
            "3,3,1,1033": "Google:Roboto Condensed Regular:2016",
            "4,3,1,1033": "Roboto Condensed",
            "6,3,1,1033": "RobotoCondensed-Regular",
        },
    },
    {
        "attribs": {"fsSelection": 513, "macStyle": 2, "usWeightClass": 400, "italicAngle": -12, "usWidthClass": 3, "caretSlopeRise": 2048, "caretSlopeRun": 435},
        "axes": {"ital": 1.0, "wdth": 75.0, "wght": 400},
        "filename": "RobotoCondensed-Italic.ttf",
        "names": {
            "1,3,1,1033": "Roboto Condensed",
            "2,3,1,1033": "Italic",
            "3,3,1,1033": "Google:Roboto Condensed Italic:2016",
            "4,3,1,1033": "Roboto Condensed Italic",
            "6,3,1,1033": "RobotoCondensed-Italic",
        },
    },
    {
        "attribs": {"fsSelection": 513, "macStyle": 2, "usWeightClass": 400, "italicAngle": -12, "caretSlopeRise": 2048, "caretSlopeRun": 435},
        "axes": {"ital": 1.0, "wdth": 100, "wght": 400},
        "filename": "Roboto-Italic.ttf",
        "names": {
            "1,3,1,1033": "Roboto",
            "2,3,1,1033": "Italic",
            "3,3,1,1033": "Google:Roboto Italic:2016",
            "4,3,1,1033": "Roboto Italic",
            "6,3,1,1033": "Roboto-Italic",
        },
    },
    {
        "attribs": {"fsSelection": 64, "macStyle": 0, "usWeightClass": 500, "usWidthClass": 3},
        "axes": {"ital": 0.0, "wdth": 75.0, "wght": 500},
        "filename": "RobotoCondensed-Medium.ttf",
        "names": {
            "1,3,1,1033": "Roboto Condensed Medium",
            "2,3,1,1033": "Regular",
            "3,3,1,1033": "Google:Roboto Condensed Medium:2016",
            "4,3,1,1033": "Roboto Condensed Medium",
            "6,3,1,1033": "RobotoCondensed-Medium",
            "16,3,1,1033": "Roboto Condensed",
            "17,3,1,1033": "Medium",
        },
    },
    {
        "attribs": {"fsSelection": 64, "macStyle": 0, "usWeightClass": 500},
        "axes": {"ital": 0.0, "wdth": 100, "wght": 500},
        "filename": "Roboto-Medium.ttf",
        "names": {
            "1,3,1,1033": "Roboto Medium",
            "16,3,1,1033": "Roboto",
            "17,3,1,1033": "Medium",
            "2,3,1,1033": "Regular",
            "3,3,1,1033": "Google:Roboto Medium:2016",
            "4,3,1,1033": "Roboto Medium",
            "6,3,1,1033": "Roboto-Medium",
        },
    },
    {
        "attribs": {"fsSelection": 513, "macStyle": 2, "usWeightClass": 500, "italicAngle": -12, "usWidthClass": 3, "caretSlopeRise": 2048, "caretSlopeRun": 435},
        "axes": {"ital": 1.0, "wdth": 75.0, "wght": 500},
        "filename": "RobotoCondensed-MediumItalic.ttf",
        "names": {
            "1,3,1,1033": "Roboto Condensed Medium",
            "2,3,1,1033": "Italic",
            "3,3,1,1033": "Google:Roboto Condensed Medium Italic:2016",
            "4,3,1,1033": "Roboto Condensed Medium Italic",
            "6,3,1,1033": "RobotoCondensed-MediumItalic",
            "16,3,1,1033": "Roboto Condensed",
            "17,3,1,1033": "Medium Italic",
        },
    },
    {
        "attribs": {"fsSelection": 513, "macStyle": 2, "usWeightClass": 500, "italicAngle": -12, "caretSlopeRise": 2048, "caretSlopeRun": 435},
        "axes": {"ital": 1.0, "wdth": 100, "wght": 500},
        "filename": "Roboto-MediumItalic.ttf",
        "names": {
            "1,3,1,1033": "Roboto Medium",
            "16,3,1,1033": "Roboto",
            "17,3,1,1033": "Medium Italic",
            "2,3,1,1033": "Italic",
            "3,3,1,1033": "Google:Roboto Medium Italic:2016",
            "4,3,1,1033": "Roboto Medium Italic",
            "6,3,1,1033": "Roboto-MediumItalic",
        },
    },
    {
        "attribs": {"fsSelection": 32, "macStyle": 1, "usWeightClass": 700, "usWidthClass": 3},
        "axes": {"ital": 0.0, "wdth": 75.0, "wght": 700},
        "filename": "RobotoCondensed-Bold.ttf",
        "names": {
            "1,3,1,1033": "Roboto Condensed",
            "2,3,1,1033": "Bold",
            "3,3,1,1033": "Google:Roboto Condensed Bold:2016",
            "4,3,1,1033": "Roboto Condensed Bold",
            "6,3,1,1033": "RobotoCondensed-Bold",
        },
    },
    {
        "attribs": {"fsSelection": 32, "macStyle": 1, "usWeightClass": 700},
        "axes": {"ital": 0.0, "wdth": 100, "wght": 700},
        "filename": "Roboto-Bold.ttf",
        "names": {
            "1,3,1,1033": "Roboto",
            "2,3,1,1033": "Bold",
            "3,3,1,1033": "Google:Roboto Bold:2016",
            "4,3,1,1033": "Roboto Bold",
            "6,3,1,1033": "Roboto-Bold",
        },
    },
    {
        "attribs": {"fsSelection": 545, "macStyle": 3, "usWeightClass": 700, "italicAngle": -12, "usWidthClass": 3, "caretSlopeRise": 2048, "caretSlopeRun": 435},
        "axes": {"ital": 1.0, "wdth": 75.0, "wght": 700},
        "filename": "RobotoCondensed-BoldItalic.ttf",
        "names": {
            "1,3,1,1033": "Roboto Condensed",
            "2,3,1,1033": "Bold Italic",
            "3,3,1,1033": "Google:Roboto Condensed Bold Italic:2016",
            "4,3,1,1033": "Roboto Condensed Bold Italic",
            "6,3,1,1033": "RobotoCondensed-BoldItalic",
        },
    },
    {
        "attribs": {"fsSelection": 545, "macStyle": 3, "usWeightClass": 700, "italicAngle": -12, "caretSlopeRise": 2048, "caretSlopeRun": 435},
        "axes": {"ital": 1.0, "wdth": 100, "wght": 700},
        "filename": "Roboto-BoldItalic.ttf",
        "names": {
            "1,3,1,1033": "Roboto",
            "2,3,1,1033": "Bold Italic",
            "3,3,1,1033": "Google:Roboto Bold Italic:2016",
            "4,3,1,1033": "Roboto Bold Italic",
            "6,3,1,1033": "Roboto-BoldItalic",
        },
    },
    {
        "attribs": {"fsSelection": 64, "macStyle": 0, "usWeightClass": 900},
        "axes": {"ital": 0.0, "wdth": 100, "wght": 900},
        "filename": "Roboto-Black.ttf",
        "names": {
            "1,3,1,1033": "Roboto Black",
            "16,3,1,1033": "Roboto",
            "17,3,1,1033": "Black",
            "2,3,1,1033": "Regular",
            "3,3,1,1033": "Google:Roboto Black:2016",
            "4,3,1,1033": "Roboto Black",
            "6,3,1,1033": "Roboto-Black",
        },
    },
    {
        "attribs": {"fsSelection": 513, "macStyle": 2, "usWeightClass": 900, "italicAngle": -12, "caretSlopeRise": 2048, "caretSlopeRun": 435},
        "axes": {"ital": 1.0, "wdth": 100, "wght": 900},
        "filename": "Roboto-BlackItalic.ttf",
        "names": {
            "1,3,1,1033": "Roboto Black",
            "16,3,1,1033": "Roboto",
            "17,3,1,1033": "Black Italic",
            "2,3,1,1033": "Italic",
            "3,3,1,1033": "Google:Roboto Black Italic:2016",
            "4,3,1,1033": "Roboto Black Italic",
            "6,3,1,1033": "Roboto-BlackItalic",
        },
    },
]


vf = TTFont(sys.argv[1])
out_dir = mkdir(sys.argv[2])

for inst in instances:
    print(f"Making {inst['filename']}")
    instance = instantiateVariableFont(vf, inst["axes"])
    update_attribs(instance, **inst["attribs"])
    update_names(instance, **inst["names"])
    del instance['STAT']
    out_path = os.path.join(sys.argv[2], inst["filename"])
    instance.save(out_path)

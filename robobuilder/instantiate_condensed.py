"""Create condensed width variants from split variable fonts."""
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from robobuilder.utils import update_names, update_attribs, mkdir


ROMAN_INSTANCE = {
    "attribs": {"usWidthClass": 3},
    "axes": {"wdth": 75},
    "filename": "RobotoCondensed[wght].ttf",
    "names": {
        "1,3,1,1033": "Roboto Condensed",
        "2,3,1,1033": "Regular",
        "3,3,1,1033": "Google:Roboto Condensed Regular:2016",
        "4,3,1,1033": "Roboto Condensed Regular",
        "6,3,1,1033": "RobotoCondensed-Regular",
        "25,3,1,1033": "RobotoCondensed",
    },
}

ITALIC_INSTANCE = {
    "attribs": {"usWidthClass": 3, "italicAngle": -12, "caretSlopeRise": 2048, "caretSlopeRun": 435},
    "axes": {"wdth": 75},
    "filename": "RobotoCondensed-Italic[wght].ttf",
    "names": {
        "1,3,1,1033": "Roboto Condensed",
        "2,3,1,1033": "Italic",
        "3,3,1,1033": "Google:Roboto Condensed Italic:2016",
        "4,3,1,1033": "Roboto Condensed Italic",
        "6,3,1,1033": "RobotoCondensed-Italic",
        "25,3,1,1033": "RobotoCondensed",
    },
}


def update_fvar_instances(ttfont):
    name = ttfont["name"]
    instances = ttfont['fvar'].instances
    for instance in instances:
        subfamily_id = instance.subfamilyNameID
        post_id = instance.postscriptNameID
        for record in name.names:
            if record.nameID in [subfamily_id]:
                current_name = record.toUnicode()
                new_name = current_name.replace("Condensed", "").strip()
                name.setName(new_name, record.nameID, record.platformID, record.platEncID, record.langID)
            if record.nameID in [post_id]:
                current_name = record.toUnicode()
                new_name = current_name.replace("-Condensed", "Condensed-").strip()
                name.setName(new_name, record.nameID, record.platformID, record.platEncID, record.langID)

            string = record.toUnicode()
            name.setName(string.replace("Roboto-Condensed", "RobotoCondensed-"), record.nameID, record.platformID, record.platEncID, record.langID)


def update_stat(ttfont):
    stat = ttfont["STAT"].table
    name_table = ttfont["name"]
    axis_values = [a for a in stat.AxisValueArray.AxisValue]
    for av in axis_values:
        name_id = av.ValueNameID
        name_record = name_table.getName(name_id, 3, 1, 0x409)
        if name_record:
            name = name_record.toUnicode()
            if name == "Condensed":
                av.Flags = 2


def main(roman_path, italic_path, out_dir):
    vf_roman = TTFont(roman_path)
    vf_italic = TTFont(italic_path)
    out_dir = Path(mkdir(out_dir))

    for inst, vf in zip([ROMAN_INSTANCE, ITALIC_INSTANCE], [vf_roman, vf_italic]):
        print(f"Making {inst['filename']}")
        instance = instantiateVariableFont(vf, inst["axes"])
        update_attribs(instance, **inst["attribs"])
        update_names(instance, rm_private=False, **inst["names"])
        update_fvar_instances(instance)
        update_stat(instance)
        instance.save(str(out_dir / inst["filename"]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])

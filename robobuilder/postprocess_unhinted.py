"""Drop MVAR table and add STAT table to a variable font."""
import sys
from fontTools.ttLib import TTFont
from robobuilder.gen_stat import AXES, update_fvar
from fontTools.otlLib.builder import buildStatTable


def main(input_path, output_path):
    font = TTFont(input_path)
    if "MVAR" in font:
        del font["MVAR"]
    buildStatTable(font, AXES)
    update_fvar(font)
    font.save(output_path)
    print(f"Dropped MVAR and added STAT: {output_path}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

"""Subset a font for web delivery using a predefined character list."""
import sys
from pathlib import Path
from nototools import subset


def read_charlist(filename):
    with open(filename) as datafile:
        charlist = []
        for line in datafile:
            if '#' in line:
                line = line[:line.index('#')]
            line = line.strip()
            if not line:
                continue
            if line.startswith('U+'):
                line = line[2:]
            char = int(line, 16)
            charlist.append(char)
        return charlist


def main(source_filename, target_filename):
    charlist_path = Path(__file__).parent / 'web_subset.txt'
    charlist = read_charlist(str(charlist_path))
    # Add private use characters for legacy reasons
    charlist += [0xEE01, 0xEE02, 0xF6C3]

    features_to_keep = [
        'c2sc', 'ccmp', 'cpsp', 'dlig', 'dnom', 'frac', 'kern', 'liga', 'lnum',
        'locl', 'numr', 'onum', 'pnum', 'smcp', 'ss01', 'ss02', 'ss03', 'ss04',
        'ss05', 'ss06', 'ss07', 'tnum', 'sups', 'subs', 'mark', 'mkmk']

    subset.subset_font(
        source_filename, target_filename,
        include=charlist,
        options={'layout_features': features_to_keep})


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

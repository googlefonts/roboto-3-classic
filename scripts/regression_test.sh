#!/bin/sh
# Regression test generated fonts against last tagged release
set -e

mkdir -p prev_release

OLD_FONT=prev_release/Roboto\[ital\,wdth\,wght\].ttf
GENNED_FONT=fonts/hinted/Roboto\[ital\,wdth\,wght\].ttf

curl -s https://api.github.com/repos/googlefonts/roboto-classic/releases/latest \
| grep "https://github.com/googlefonts/roboto-classic/releases/download/*" \
| cut -d ":" -f 2,3 \
| tr -d \"\, \
| wget -i -
unzip -po Roboto_*.zip "hinted/Roboto\[ital\,wdth\,wght\].ttf" > $OLD_FONT


# Diff old hinted variable font against current
diff ()
{
    diffenator $OLD_FONT $GENNED_FONT -i "$2" \
        -html > $1/index.html \
        -rd -r ./img/ \
        --ft-hinting normal
    mv img/ $1
}


mkdir -p diffs \
	 diffs/Regular \
	 diffs/Condensed \
	 diffs/Italic \
	 diffs/CondensedItalic


diff diffs/Regular "wght=400, wdth=100"
diff diffs/Condensed "wght=400, wdth=75"
diff diffs/Italic "ital=1, wght=400, wdth=100"
diff diffs/CondensedItalic "ital=1, wght=400, wdth=75"


#!/bin/sh
# Regression test generated fonts against last tagged release
set -e

mkdir -p prev_release

OLD_FONT=prev_release/hinted/Roboto\[ital\,wdth\,wght\].ttf
GENNED_FONT=fonts/hinted/Roboto\[ital\,wdth\,wght\].ttf

DL_URL=$(curl https://api.github.com/repositories/86081751/releases/latest | jq -r .assets[0].browser_download_url)
wget $DL_URL
unzip Roboto_*.zip -d prev_release

diffenator3 $OLD_FONT $GENNED_FONT --html --output diffs

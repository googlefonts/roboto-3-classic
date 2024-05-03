set -e

mkdir -p fonts


#Make unhinted
mkdir -p fonts/unhinted
UNHINTED_VF_PATH=fonts/unhinted/Roboto[ital,wdth,wght].ttf
fontmake -m sources/Roboto.designspace -o variable --output-path $UNHINTED_VF_PATH
python scripts/set_overlaps.py $UNHINTED_VF_PATH
python scripts/drop_mvar.py $UNHINTED_VF_PATH
python scripts/gen_stat.py $UNHINTED_VF_PATH
python scripts/instantiate_statics.py $UNHINTED_VF_PATH fonts/unhinted/static


# Make Android
mkdir -p fonts/android
ANDROID_VF_PATH=fonts/android/Roboto[ital,wdth,wght].ttf
subset.py $UNHINTED_VF_PATH $ANDROID_VF_PATH
python scripts/touchup_for_android.py $ANDROID_VF_PATH
python scripts/instantiate_statics.py $ANDROID_VF_PATH fonts/android/static
for font in $(ls fonts/android/static/*.ttf)
do
	python scripts/touchup_for_android.py $font;
done


# Make hinted
mkdir -p fonts/hinted
HINTED_VF_PATH=fonts/hinted/Roboto[ital,wdth,wght].ttf
# Transfer Hints and compile them
cp $UNHINTED_VF_PATH $HINTED_VF_PATH
python -m vttLib mergefile sources/vtt-hinting.ttx $HINTED_VF_PATH
python -m vttLib compile $HINTED_VF_PATH $HINTED_VF_PATH.fix --ship
mv $HINTED_VF_PATH.fix $HINTED_VF_PATH
python scripts/touchup_for_web.py $HINTED_VF_PATH
python scripts/instantiate_statics.py $HINTED_VF_PATH fonts/hinted/static
for font in $(ls fonts/web/hinted/*.ttf)
do
	python scripts/touchup_for_web.py $font;
done


# Make web
mkdir -p fonts/web
WEB_VF_PATH=fonts/web/Roboto[ital,wdth,wght].ttf
python scripts/subset_for_web.py $HINTED_VF_PATH $WEB_VF_PATH
python scripts/touchup_for_web.py $WEB_VF_PATH
# Split fonts can be removed once all browsers support slnt and ital axes properly
mkdir -p fonts/web/split
python scripts/split_slnt_vf.py $WEB_VF_PATH fonts/web/split
python scripts/instantiate_statics.py $WEB_VF_PATH fonts/web/static
python scripts/instantiate_condensed.py \
	fonts/web/split/Roboto[wdth,wght].ttf \
	fonts/web/split/Roboto-Italic[wdth,wght].ttf \
	fonts/web/condensed
for font in $(ls fonts/web/static/*.ttf)
do
	python scripts/touchup_for_web.py $font;
done


# Make ChromeOS
mkdir -p fonts/chromeos
CHROMEOS_VF_PATH=fonts/chromeos/Roboto[ital,wdth,wght].ttf
subset.py $HINTED_VF_PATH $CHROMEOS_VF_PATH
python scripts/touchup_for_cros.py $CHROMEOS_VF_PATH
python scripts/instantiate_statics.py $CHROMEOS_VF_PATH fonts/chromeos/static
for font in $(ls fonts/chromeos/static/*.ttf)
do
	python scripts/touchup_for_cros.py $font;
done


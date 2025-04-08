# Roboto VF

This is a variable version of Roboto intended to be a 1:1 match with the official non-variable release from Google.

This is not an official Google project, but was enabled with generous funding by Google Fonts, who contracted Type Network.
The Roboto family of instances contained 6 weights and two widths of normal, along with italic of the regular width.
The project began by taking UFO instances generated during the build process of the Roboto v2.136 release, which have quadratic outlines. 
The Thin, Regular and Bold UFOs required some fixes for interpolation compatibility, and a build script was written that preserves outline overlaps.

* [/sources](sources/) contains 'new' source UFOs (compared to the 'old' UFOs used in the static-only era of the project).

* [github.com/TypeNetwork/Roboto/releases](https://github.com/TypeNetwork/Roboto/releases) contains variation font TTFs.

Both fonts have named instances for all the styles in the v2.136 release.

## Install

    # Create a new virtualenv
    virtualenv env
    # Activate env
    source env/bin/activate
    # Install dependencies
    pip install .
    pip install -r requirements.txt

## Generate

    sh sources/build.sh

## Font hinting

The fonts have been hinted using Microsoft VTT and compiled using [vttLib](https://github.com/daltonmaag/vttLib). The hinting data is stored as xml in `sources/vtt-hinting.ttx`.

If you would like to make modifications to the hints using VTT, you'll need to do the following:

- Rebuild the fonts. We MUST ensure that hint modifications are being done on the latest binaries.
- Make a VTT source font which contains the existing hinting data by running `sh sources/make_vtt_src_font.sh`. The font will be exported to `sources/Roboto[ital,wdth,wght]_VTT.ttf`.
- In VTT, edit the newly generated font.
- Export the source font's hinting data back to `sources/vtt-hinting.ttx` by running `sh sources/export_vtt_hints.sh`
- Commit your changes using git.

Warning: vttLib doesn't support transformed composites. Please ensure source files do not contain them.

## Family variants

Roboto provides the following sibling families:


**Unhinted**

This family will work well for platforms that don't require hinting such as Mac OS. This is the first family that gets built. The rest of the families are based on this one.


**Hinted**

This family is intended for operating systems that use hinting such as MS Windows. The hints have been created in VTT by Mike Duggan.


**Android**

This family is intended for the Android operating system. It includes the following changes:

- No glyph hints
- First 32 control characters in the ASCII encoding
- Modified vertical metrics


**ChromesOS**

This family is intended for the ChromeOS operating system. It includes the following changes:

- Glyph hints
- Modified vertical metrics
- No bits enabled for Oblique


**Web**

This family is intended for use on the web. It includes the following changes:

- Glyph hints
- Modified vertical metrics
- Smaller character set
- Thin OS/2.usWeightClass set to 250
- Updated GASP table with different ranges
- No bits enabled for Oblique

It is advisable to use the Roboto webfonts that are available at https://fonts.google.com/specimen/Roboto instead.


# License

Both fonts and software found in this repo are all available under the OFL License v1.1

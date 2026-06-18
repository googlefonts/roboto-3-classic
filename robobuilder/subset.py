"""Subset a font, dropping unused parts while preserving layout features."""
import sys
from fontTools import subset
from fontTools.ttLib import TTFont


def character_set(font_path):
    """Get the set of Unicode codepoints covered by a font."""
    font = TTFont(font_path)
    cmap = font.getBestCmap()
    return set(cmap.keys())


def subset_font(source_file, target_file,
                include=None, exclude=None, options=None):
    opt = subset.Options()

    opt.name_IDs = ['*']
    opt.name_legacy = True
    opt.name_languages = ['*']
    opt.layout_features = ['*']
    opt.notdef_outline = True
    opt.recalc_bounds = True
    opt.recalc_timestamp = True
    opt.canonical_order = True
    opt.drop_tables = ['+TTFA']
    opt.no_subset_tables += ["BASE"]

    if options is not None:
        for name, value in options.items():
            setattr(opt, name, value)

    if include is not None:
        if exclude is not None:
            raise NotImplementedError(
                'Subset cannot include and exclude a set at the same time.')
        target_charset = include
    else:
        if exclude is None:
            exclude = []
        source_charset = character_set(source_file)
        target_charset = source_charset - set(exclude)

    font = subset.load_font(source_file, opt)
    subsetter = subset.Subsetter(options=opt)
    subsetter.populate(unicodes=target_charset)
    subsetter.subset(font)
    subset.save_font(font, target_file, opt)


def main(source_file, target_file):
    subset_font(source_file, target_file)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

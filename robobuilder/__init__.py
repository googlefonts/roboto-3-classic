import sys
from pathlib import Path

from gftools.builder.recipeproviders import RecipeProviderBase

PYTHON = sys.executable
VF_NAME = "Roboto[ital,wdth,wght].ttf"
FONTS_DIR = Path("..") / "fonts"


class RoboBuilder(RecipeProviderBase):
    def write_recipe(self):
        self.recipe = {}
        source = self.config["sources"][0]

        unhinted = str(FONTS_DIR / "unhinted" / VF_NAME)
        hinted = str(FONTS_DIR / "hinted" / VF_NAME)
        android = str(FONTS_DIR / "android" / VF_NAME)
        web = str(FONTS_DIR / "web" / VF_NAME)
        chromeos = str(FONTS_DIR / "chromeos" / VF_NAME)

        self._build_unhinted(source, unhinted)
        self._build_android(unhinted, android)
        self._build_hinted(unhinted, hinted)
        self._build_web(hinted, web)
        self._build_chromeos(hinted, chromeos)

        return self.recipe

    def _post(self, args):
        return {"postprocess": "exec", "exe": PYTHON, "args": args}

    def fontmake_args(self, source, variable=False):
        return ""

    def build_all_variables(self):
        for source in self.sources:
            self.build_a_variable(source)

    def build_a_variable(self, source):
        target = self._vf_filename(source, roman=True)
        steps = [{"source": source.path}] + [
            {
                "operation": "buildVariable",
                "args": self.fontmake_args(source, variable=True),
            },
        ]
        self.recipe[target] = steps

    def _build_unhinted(self, source, target):
        static_dir = str(FONTS_DIR / "unhinted" / "static")
        self.recipe[target] = [
            {"source": source},
            {"operation": "buildVariable"},
            # Regular exec so the target file is only ready when fully processed.
            # Other recipes that use unhinted as a source will wait for this.
            {
                "operation": "exec",
                "exe": PYTHON,
                "args": "-m robobuilder.postprocess_unhinted $in $out",
            },
            self._post(f"-m robobuilder.instantiate_statics {target} {static_dir}"),
        ]

    def _build_android(self, source, target):
        static_dir = str(FONTS_DIR / "android" / "static")
        self.recipe[target] = [
            {"source": source},
            {
                "operation": "exec",
                "exe": PYTHON,
                "args": "-m robobuilder.subset $in $out",
            },
            self._post(f"-m robobuilder.touchup_for_android {target}"),
            self._post(f"-m robobuilder.instantiate_statics {target} {static_dir}"),
            self._post(
                f"-m robobuilder.touchup_statics"
                f" robobuilder.touchup_for_android {static_dir}"
            ),
        ]

    def _build_hinted(self, source, target):
        static_dir = str(FONTS_DIR / "hinted" / "static")
        self.recipe[target] = [
            {"source": source},
            {
                "operation": "exec",
                "exe": PYTHON,
                "args": "-m robobuilder.apply_vtt $in $out vtt-hinting.ttx",
            },
            {
                "operation": "exec",
                "exe": PYTHON,
                "args": "-m robobuilder.touchup_for_web $in $out",
            },
            self._post(
                f"-m robobuilder.instantiate_statics {target} {static_dir}"
            ),
        ]

    def _build_web(self, source, target):
        split_dir = FONTS_DIR / "web" / "split"
        static_dir = str(FONTS_DIR / "web" / "static")
        condensed_dir = str(FONTS_DIR / "web" / "condensed")
        roman_split = str(split_dir / "Roboto[wdth,wght].ttf")
        italic_split = str(split_dir / "Roboto-Italic[wdth,wght].ttf")
        self.recipe[target] = [
            {"source": source},
            {
                "operation": "exec",
                "exe": PYTHON,
                "args": "-m robobuilder.subset_for_web $in $out",
            },
            self._post(f"-m robobuilder.touchup_for_web {target}"),
            self._post(f"-m robobuilder.split_slnt_vf {target} {split_dir}"),
            self._post(f"-m robobuilder.instantiate_statics {target} {static_dir}"),
            self._post(
                f"-m robobuilder.instantiate_condensed"
                f" {roman_split} {italic_split} {condensed_dir}"
            ),
            self._post(
                f"-m robobuilder.touchup_statics"
                f" robobuilder.touchup_for_web {static_dir}"
            ),
        ]

    def _build_chromeos(self, source, target):
        static_dir = str(FONTS_DIR / "chromeos" / "static")
        self.recipe[target] = [
            {"source": source},
            {
                "operation": "exec",
                "exe": PYTHON,
                "args": "-m robobuilder.subset $in $out",
            },
            self._post(f"-m robobuilder.touchup_for_cros {target}"),
            self._post(
                f"-m robobuilder.instantiate_statics {target} {static_dir}"
            ),
            self._post(
                f"-m robobuilder.touchup_statics"
                f" robobuilder.touchup_for_cros {static_dir}"
            ),
        ]

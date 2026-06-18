"""Run a touchup module's main() on all static fonts in a directory."""
import importlib
import sys
from pathlib import Path


def main():
    module_name = sys.argv[1]
    static_dir = Path(sys.argv[2])

    mod = importlib.import_module(module_name)
    for font_path in sorted(static_dir.glob("*.ttf")):
        print(f"Running {module_name} on {font_path}")
        mod.main(str(font_path))


if __name__ == "__main__":
    main()

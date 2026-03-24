"""Copy a font and apply VTT hints (merge + compile --ship)."""
import shutil
import subprocess
import sys


def main():
    src = sys.argv[1]
    dst = sys.argv[2]
    vtt_source = sys.argv[3]

    shutil.copy2(src, dst)
    subprocess.run(
        [sys.executable, "-m", "vttLib", "mergefile", vtt_source, dst],
        check=True,
    )
    fix_path = dst + ".fix"
    subprocess.run(
        [sys.executable, "-m", "vttLib", "compile", dst, fix_path, "--ship"],
        check=True,
    )
    shutil.move(fix_path, dst)


if __name__ == "__main__":
    main()

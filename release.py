"""Zips the datapack for a release: python release.py -> build/Survirec-vX.Y.Z.zip"""
import json
import os
import sys
import traceback
import zipfile


def main():
    # always work from the folder containing this script (double-click safe)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with open("pack.mcmeta", encoding="utf-8") as fh:
        meta = json.load(fh)
    with open("VERSION", encoding="utf-8") as fh:
        version = fh.read().strip()

    os.makedirs("build", exist_ok=True)
    out = os.path.join("build", "Survirec-v%s.zip" % version)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for extra in ("pack.mcmeta", "pack.png", "LICENSE"):
            if os.path.exists(extra):
                z.write(extra)
        for root, _, files in os.walk("data"):
            for name in files:
                z.write(os.path.join(root, name))
    print("Built", os.path.abspath(out), "(id: %s)" % meta["id"])


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
    # keep the window open when launched by double-click (not in CI)
    if sys.stdin is not None and sys.stdin.isatty():
        input("Press Enter to close...")

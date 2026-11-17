"""Zips the datapack for a release: python release.py -> build/Survirec-vX.Y.Z.zip"""
import json
import os
import zipfile

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
print("Built", out, "(id: %s)" % meta["id"])

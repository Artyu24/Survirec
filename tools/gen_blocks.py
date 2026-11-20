"""Survirec - génère la reconnaissance des blocs (tags de blocs + fonctions).

Un datapack ne peut pas lire l'identité d'un bloc. Survirec la retrouve par recherche
dichotomique sur des tags de blocs, puis teste les propriétés utiles (orientation, moitié...).

Usage : python tools/gen_blocks.py
Lit tools/blocks.txt (un identifiant par ligne) et écrit dans src/data/survirec :
  tags/block/b/*.json                    arbre de recherche (feuilles l*, noeuds n*)
  function/v1/private/bk/t/*.mcfunction  recherche dichotomique
  function/v1/private/bk/props.mcfunction tests des propriétés
Les identifiants inconnus d'une version sont ignorés ("required": false).
Pour une nouvelle version de Minecraft : mettre à jour blocks.txt et relancer.
"""
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src", "data", "survirec")
TAGS = os.path.join(SRC, "tags", "block", "b")
FUNC = os.path.join(SRC, "function", "v1", "private", "bk")

# propriété -> valeurs testées. Un drapeau (score) peut être posé en plus de l'ajout à la liste.
PROPS = [
    ("facing", ["north", "south", "east", "west", "up", "down"]),
    ("half", ["top", "bottom", "upper", "lower"]),
    ("axis", ["x", "y", "z"]),
    ("type", ["top", "bottom", "double", "single", "left", "right"]),
    ("shape", ["straight", "inner_left", "inner_right", "outer_left", "outer_right", "north_south", "east_west",
               "ascending_east", "ascending_west", "ascending_north", "ascending_south",
               "south_east", "south_west", "north_west", "north_east"]),
    ("hinge", ["left", "right"]),
    ("face", ["floor", "wall", "ceiling"]),
    ("rotation", [str(i) for i in range(16)]),
    ("attachment", ["floor", "ceiling", "single_wall", "double_wall"]),
    ("hanging", ["true"]),
    ("waterlogged", ["true"]),
    ("in_wall", ["true"]),
    ("part", ["head", "foot"]),
    ("delay", ["1", "2", "3", "4"]),
    ("mode", ["compare", "subtract"]),
    ("candles", ["1", "2", "3", "4"]),
    ("pickles", ["1", "2", "3", "4"]),
    ("eggs", ["1", "2", "3", "4"]),
    ("layers", [str(i) for i in range(1, 9)]),
    ("flower_amount", ["1", "2", "3", "4"]),
    ("segment_amount", ["1", "2", "3", "4"]),
    ("vertical_direction", ["up", "down"]),
    ("thickness", ["tip_merge", "tip", "frustum", "middle", "base"]),
    ("orientation", ["down_east", "down_north", "down_south", "down_west", "up_east", "up_north", "up_south",
                     "up_west", "west_up", "east_up", "north_up", "south_up"]),
]
FLAGS = {  # (propriété, valeur) -> (score, valeur)
    ("facing", "north"): ("#bfc", 1), ("facing", "south"): ("#bfc", 2),
    ("facing", "east"): ("#bfc", 3), ("facing", "west"): ("#bfc", 4),
    ("facing", "up"): ("#bfc", 5), ("facing", "down"): ("#bfc", 6),
    ("half", "upper"): ("#bhl", 1), ("half", "lower"): ("#bhl", 2),
    ("part", "head"): ("#bpt", 1), ("part", "foot"): ("#bpt", 2),
    ("face", "floor"): ("#bfa", 1), ("face", "ceiling"): ("#bfa", 2), ("face", "wall"): ("#bfa", 3),
}
# lues comme drapeaux seulement (recomposées selon l'action)
ONLY_FLAGS = [("open", "#bop"), ("powered", "#bpw")]


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text if text.endswith("\n") else text + "\n")


def main():
    with open(os.path.join(ROOT, "tools", "blocks.txt"), encoding="utf-8") as fh:
        blocks = []
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#") and line not in blocks:
                blocks.append(line if ":" in line else "minecraft:" + line)
    shutil.rmtree(TAGS, ignore_errors=True)
    shutil.rmtree(os.path.join(FUNC, "t"), ignore_errors=True)

    for i, b in enumerate(blocks):
        write(os.path.join(TAGS, "l%d.json" % i), json.dumps({"values": [{"id": b, "required": False}]}))

    counter = [0]

    def build(lo, hi):
        """Renvoie ("l", i) pour une feuille ou ("n", k) pour un noeud couvrant blocks[lo:hi]."""
        if hi - lo == 1:
            return ("l", lo)
        counter[0] += 1
        k = counter[0]
        mid = (lo + hi) // 2
        left, right = build(lo, mid), build(mid, hi)
        lines = []
        for kind, idx in (left, right):
            ref = "#survirec:b/%s%d" % (kind, idx)
            if kind == "l":
                go = 'data modify storage survirec:bk r set value {id:"%s",leaf:"l%d"}' % (blocks[idx], idx)
            else:
                go = "function survirec:v1/private/bk/t/n%d" % idx
            lines.append("execute if block ~ ~ ~ %s run return run %s" % (ref, go))
        write(os.path.join(FUNC, "t", "n%d.mcfunction" % k), "\n".join(lines))
        if k != 1:
            write(os.path.join(TAGS, "n%d.json" % k),
                  json.dumps({"values": ["#survirec:b/%s%d" % left, "#survirec:b/%s%d" % right]}))
        return ("n", k)

    build(0, len(blocks))

    lines = ["# généré par tools/gen_blocks.py : propriétés du bloc reconnu (feuille $(leaf))"]
    for prop, values in PROPS:
        for v in values:
            test = "$execute if block ~ ~ ~ #survirec:b/$(leaf)[%s=%s] run " % (prop, v)
            lines.append(test + 'data modify storage survirec:bk pl append value "%s=%s"' % (prop, v))
            if (prop, v) in FLAGS:
                score, val = FLAGS[(prop, v)]
                lines.append(test + "scoreboard players set %s survirec.v %d" % (score, val))
    for prop, score in ONLY_FLAGS:
        lines.append("$execute if block ~ ~ ~ #survirec:b/$(leaf)[%s=true] run scoreboard players set %s survirec.v 1" % (prop, score))
    write(os.path.join(FUNC, "props.mcfunction"), "\n".join(lines))
    print("%d blocs, %d noeuds" % (len(blocks), counter[0]))


if __name__ == "__main__":
    main()

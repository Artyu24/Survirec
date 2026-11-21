""" Block reading for the recorded actions, on top of Bookshelf's block module (bs.block).

`#bs.block:get_block` knows every block and state of the Minecraft version it is built for,
so Survirec no longer ships its own block list. StewBeet sees the `#bs.block:` calls, adds the
dependency check to the load and welds the module into the `_with_libs` zip.
"""
# Imports
from stewbeet import Mem, write_versioned_function

# Constants
FLAGS: dict[str, tuple[str, dict[str, int]]] = {
	"facing": ("#bfc", {"north": 1, "south": 2, "east": 3, "west": 4, "up": 5, "down": 6}),
	"half": ("#bhl", {"upper": 1, "lower": 2}),
	"part": ("#bpt", {"head": 1, "foot": 2}),
	"face": ("#bfa", {"floor": 1, "ceiling": 2, "wall": 3}),
	"open": ("#bop", {"true": 1}),
	"powered": ("#bpw", {"true": 1}),
}
""" Block property -> (score holding it, value of the score for each property value). 0 when the property is missing. """


def main() -> None:
	ns: str = Mem.ctx.project_id

	resets: str = "\n".join(f"scoreboard players set {score} {ns}.data 0" for score, _ in FLAGS.values())
	flags: str = "\n".join(
		f'execute if data storage bs:out block.properties{{{prop}:"{value}"}} run scoreboard players set {score} {ns}.data {n}'
		for prop, (score, values) in FLAGS.items() for value, n in values.items()
	)
	write_versioned_function("block/read", f"""
# positionné sur un bloc : {ns}:bk r.id ("" pour de l'air), drapeaux {" ".join(score for score, _ in FLAGS.values())}
# le bloc lu reste dans bs:out block (état complet), modifiable avec #bs.block:replace_properties
data modify storage {ns}:bk r set value {{id:""}}
{resets}
execute if block ~ ~ ~ #minecraft:air run return fail
function #bs.block:get_block
data modify storage {ns}:bk r.id set from storage bs:out block.type
{flags}
""")

	write_versioned_function("block/full", f"""
# {ns}:bk full = "id[état]" du bloc de bs:out block (sans NBT), prêt pour setblock
data modify storage {ns}:bk full set from storage bs:out block.block
""")

	write_versioned_function("block/pair", f"""
# bloc double (porte, lit, grande plante) : décalage vers l'autre moitié dans #pdx #pdy #pdz, #pair 1
scoreboard players set #pair {ns}.data 0
scoreboard players set #pdx {ns}.data 0
scoreboard players set #pdy {ns}.data 0
scoreboard players set #pdz {ns}.data 0
execute if score #bhl {ns}.data matches 2 run scoreboard players set #pdy {ns}.data 1
execute if score #bhl {ns}.data matches 1 run scoreboard players set #pdy {ns}.data -1
execute if score #bhl {ns}.data matches 1..2 run scoreboard players set #pair {ns}.data 1
execute if score #bpt {ns}.data matches 1..2 run scoreboard players set #pair {ns}.data 1
execute if score #bpt {ns}.data matches 1..2 if score #bfc {ns}.data matches 1 run scoreboard players set #pdz {ns}.data -1
execute if score #bpt {ns}.data matches 1..2 if score #bfc {ns}.data matches 2 run scoreboard players set #pdz {ns}.data 1
execute if score #bpt {ns}.data matches 1..2 if score #bfc {ns}.data matches 3 run scoreboard players set #pdx {ns}.data 1
execute if score #bpt {ns}.data matches 1..2 if score #bfc {ns}.data matches 4 run scoreboard players set #pdx {ns}.data -1
execute if score #bpt {ns}.data matches 1 run scoreboard players operation #pdx {ns}.data *= #-1 {ns}.data
execute if score #bpt {ns}.data matches 1 run scoreboard players operation #pdz {ns}.data *= #-1 {ns}.data
""")

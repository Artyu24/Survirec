""" Block reading for the recorded actions, on top of Bookshelf's block module (bs.block).

`#bs.block:get_block` knows every block and state of the Minecraft version it is built for.
StewBeet sees the `#bs.block:` calls, checks the dependency at load and welds the module into the `_with_libs` zip.
"""
# Imports
from stewbeet import Mem, write_versioned_function

from .common import Storages

# Constants
FLAGS: dict[str, tuple[str, dict[str, int]]] = {
	"facing": ("#block_facing", {"north": 1, "south": 2, "east": 3, "west": 4, "up": 5, "down": 6}),
	"half": ("#block_half", {"upper": 1, "lower": 2}),
	"part": ("#block_part", {"head": 1, "foot": 2}),
	"face": ("#block_face", {"floor": 1, "ceiling": 2, "wall": 3}),
	"open": ("#block_open", {"true": 1}),
	"powered": ("#block_powered", {"true": 1}),
}
""" Block property -> (score holding it, score of each property value). 0 when the block has no such property. """


def main() -> None:
	ns: str = Mem.ctx.project_id
	block: str = Storages(ns).block

	resets: str = ""
	flags: str = ""
	for prop, (score, values) in FLAGS.items():
		resets += f"scoreboard players set {score} {ns}.data 0\n"
		for value, number in values.items():
			flags += f'execute if data storage bs:out block.properties{{{prop}:"{value}"}} run scoreboard players set {score} {ns}.data {number}\n'
	write_versioned_function("block/read", f"""
# {block} id is "" for air; bs:out block keeps the full block, editable with #bs.block:replace_properties
data modify storage {block} id set value ""
{resets}execute if block ~ ~ ~ #minecraft:air run return fail
function #bs.block:get_block
data modify storage {block} id set from storage bs:out block.type
{flags}""")

	write_versioned_function("block/store_state", f"""
# "id[state]" without NBT, ready for setblock
data modify storage {block} state set from storage bs:out block.block
""")

	write_versioned_function("block/find_other_half", f"""
# door, bed or tall plant: #is_pair 1 and the offset to the other half in #pair_x #pair_y #pair_z
scoreboard players set #is_pair {ns}.data 0
scoreboard players set #pair_x {ns}.data 0
scoreboard players set #pair_y {ns}.data 0
scoreboard players set #pair_z {ns}.data 0
execute if score #block_half {ns}.data matches 2 run scoreboard players set #pair_y {ns}.data 1
execute if score #block_half {ns}.data matches 1 run scoreboard players set #pair_y {ns}.data -1
execute if score #block_half {ns}.data matches 1..2 run scoreboard players set #is_pair {ns}.data 1
execute if score #block_part {ns}.data matches 1..2 run scoreboard players set #is_pair {ns}.data 1
execute if score #block_part {ns}.data matches 1..2 if score #block_facing {ns}.data matches 1 run scoreboard players set #pair_z {ns}.data -1
execute if score #block_part {ns}.data matches 1..2 if score #block_facing {ns}.data matches 2 run scoreboard players set #pair_z {ns}.data 1
execute if score #block_part {ns}.data matches 1..2 if score #block_facing {ns}.data matches 3 run scoreboard players set #pair_x {ns}.data 1
execute if score #block_part {ns}.data matches 1..2 if score #block_facing {ns}.data matches 4 run scoreboard players set #pair_x {ns}.data -1
execute if score #block_part {ns}.data matches 1 run scoreboard players operation #pair_x {ns}.data *= #-1 {ns}.data
execute if score #block_part {ns}.data matches 1 run scoreboard players operation #pair_z {ns}.data *= #-1 {ns}.data
""")

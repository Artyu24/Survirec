""" Copies of the blocks changed by entities, kept in the survirec:vault dimension (chunk 0), restored at every loop. """
# Imports
from dataclasses import dataclass

from stewbeet import Mem, write_versioned_function

from .common import Storages, store_position

# Constants
CAGE_LAYERS: tuple[tuple[int, int], ...] = ((-64, 31), (32, 127), (128, 223), (224, 319))
""" Height ranges filled one by one (a single fill is limited to 32768 blocks). """


@dataclass(frozen=True, slots=True)
class SlotAxis:
	""" How the block slot index #next_block_slot gives one coordinate of the slot: operations, then x2 and a shift. """

	axis: str
	operations: tuple[str, ...]
	shift: str
	amount: int


SLOT_AXES: tuple[SlotAxis, ...] = (
	SlotAxis("x", ("%= #7",), "add", 1), SlotAxis("z", ("/= #7", "%= #7"), "add", 1), SlotAxis("y", ("/= #49",), "remove", 63),
)
""" One slot out of two, 7 x 7 per layer: x and z from 1 to 13, y from -63. """


def cage(ns: str, chunk: int) -> str:
	""" Fill a vault chunk with barriers: every copy is isolated (no fall, no flow, no update between copies). """
	start: int = chunk * 16
	content: str = ""
	for bottom, top in CAGE_LAYERS:
		content += f"execute in {ns}:vault run fill {start} {bottom} 0 {start + 15} {top} 15 minecraft:barrier strict\n"
	return content


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	functions: str = f"{ns}:v{version}"
	playback: str = Storages(ns).playback

	slot: str = ""
	for slot_axis in SLOT_AXES:
		slot += f"scoreboard players operation #slot_index {ns}.data = #next_block_slot {ns}.data\n"
		for operation in slot_axis.operations:
			slot += f"scoreboard players operation #slot_index {ns}.data {operation} {ns}.data\n"
		slot += f"""scoreboard players operation #slot_index {ns}.data *= #2 {ns}.data
execute store result storage {playback} block_copy.vault_{slot_axis.axis} int 1 run scoreboard players {slot_axis.shift} #slot_index {ns}.data {slot_axis.amount}
"""
	write_versioned_function("vault/back_up", f"""
# as the entity, at the block; {playback} block_copy = {{x,y,z,mode}}, mode: "strict" or "replace" when it is put back
# only the first copy of a block is kept: it is the original state, restored at every loop
execute unless score @s {ns}.restore_mode matches 1.. run return 0
execute unless data storage {ns}:config are_blocks_ready run return 0
execute store result storage {playback} block_copy.instance_id int 1 run scoreboard players get @s {ns}.instance_id
scoreboard players set #has_copy {ns}.data 0
function {functions}/vault/has_copy with storage {playback} block_copy
execute if score #has_copy {ns}.data matches 1 run return 0
execute if data storage {ns}:config free_block_slots[0] run return run function {functions}/vault/reuse_slot
{slot}scoreboard players add #next_block_slot {ns}.data 1
execute if score #next_block_slot {ns}.data matches 9359.. run scoreboard players set #next_block_slot {ns}.data 0
function {functions}/vault/copy_block with storage {playback} block_copy
""")

	write_versioned_function("vault/copy_block", f"""
$clone $(x) $(y) $(z) $(x) $(y) $(z) to {ns}:vault $(vault_x) $(vault_y) $(vault_z) strict
$data modify storage {ns}:instances i$(instance_id).block_copies append from storage {playback} block_copy
""")

	write_versioned_function("vault/free", f"""
# the entity is removed: its slots become barriers again, free for the next copies
execute store result storage {playback} instance_id int 1 run scoreboard players get @s {ns}.instance_id
function {functions}/vault/pull_copies with storage {playback}
execute if data storage {playback} block_copies[0] run function {functions}/vault/free_next
""")

	write_versioned_function("vault/free_next", f"""
function {functions}/vault/free_slot with storage {playback} block_copies[-1]
data remove storage {playback} block_copies[-1]
execute if data storage {playback} block_copies[0] run function {functions}/vault/free_next
""")

	write_versioned_function("vault/free_slot", f"""
$execute in {ns}:vault run setblock $(vault_x) $(vault_y) $(vault_z) minecraft:barrier strict
$data modify storage {ns}:config free_block_slots append value {{vault_x:$(vault_x),vault_y:$(vault_y),vault_z:$(vault_z)}}
""")

	write_versioned_function("vault/has_copy", f"$execute if data storage {ns}:instances i$(instance_id).block_copies[{{x:$(x),y:$(y),z:$(z)}}] run scoreboard players set #has_copy {ns}.data 1")

	write_versioned_function("vault/back_up_here", f"""
# #restore_strict 1: put back without block updates (both halves of a door or bed)
data modify storage {playback} block_copy set value {{x:0,y:0,z:0,mode:"replace"}}
execute if score #restore_strict {ns}.data matches 1 run data modify storage {playback} block_copy.mode set value "strict"
execute summon minecraft:marker run function {functions}/vault/store_position
function {functions}/vault/back_up
""")

	write_versioned_function("vault/store_position", f"""
{store_position(f"{playback} block_copy.")}
kill @s
""")

	write_versioned_function("vault/prepare_blocks", f"""
{cage(ns, 0)}data modify storage {ns}:config are_blocks_ready set value 1b
""")

	write_versioned_function("vault/prepare_cubes", f"""
{cage(ns, 1)}{cage(ns, 2)}data modify storage {ns}:config are_cubes_ready set value 1b
""")

	write_versioned_function("vault/restore", f"""
# blocks changed by this entity, put back in reverse order
execute store result storage {playback} instance_id int 1 run scoreboard players get @s {ns}.instance_id
function {functions}/vault/pull_copies with storage {playback}
execute if data storage {playback} block_copies[0] at @s run function {functions}/vault/restore_next
""")

	reused: str = ""
	for axis in ("vault_x", "vault_y", "vault_z"):
		reused += f"data modify storage {playback} block_copy.{axis} set from storage {ns}:config free_block_slots[-1].{axis}\n"
	write_versioned_function("vault/reuse_slot", f"""
{reused}data remove storage {ns}:config free_block_slots[-1]
function {functions}/vault/copy_block with storage {playback} block_copy
""")

	write_versioned_function("vault/pull_copies", f"""
data modify storage {playback} block_copies set value []
$data modify storage {playback} block_copies set from storage {ns}:instances i$(instance_id).block_copies
""")

	write_versioned_function("vault/restore_next", f"""
function {functions}/vault/restore_copy with storage {playback} block_copies[-1]
data remove storage {playback} block_copies[-1]
execute if data storage {playback} block_copies[0] run function {functions}/vault/restore_next
""")

	write_versioned_function("vault/restore_copy", f"$clone from {ns}:vault $(vault_x) $(vault_y) $(vault_z) $(vault_x) $(vault_y) $(vault_z) $(x) $(y) $(z) $(mode)")

	write_versioned_function("vault/try_prepare", f"""
# the dimension is only loaded some ticks after the world starts
execute unless data storage {ns}:config are_blocks_ready in {ns}:vault if loaded 0 0 0 run function {functions}/vault/prepare_blocks
execute unless data storage {ns}:config are_cubes_ready in {ns}:vault if loaded 16 0 0 if loaded 32 0 0 run function {functions}/vault/prepare_cubes
""")

	write_versioned_function("vault/wipe", f"""
{cage(ns, 0)}data modify storage {ns}:config free_block_slots set value []
scoreboard players set #next_block_slot {ns}.data 0
""")

""" Spawning a playback entity from its settings, <ns>:call spawn (the playback options, or the double of a challenge). """
# Imports
from dataclasses import dataclass

from stewbeet import Mem, write_versioned_function

from .common import AXES, DIMENSIONS, EQUIPMENT_FIELDS, Storages, store_position

# Constants
MANNEQUIN_IDS: tuple[str, ...] = ("", "minecraft:mannequin", "mannequin")
""" Values of the entity setting spawning a mannequin (any other value is summoned as it is). """

SEQUENCE_SCORES: tuple[tuple[str, str], ...] = (
	("keyframe_ticks", "n 100"), ("start_yaw", "y"), ("start_pitch", "p"), ("keyframe_count", "d"), ("has_swings", "s"), ("has_actions", "a"),
)
""" Objective of the entity -> key of its sequence (and scale): keyframe step, start rotation, lengths of the lists. """


@dataclass(frozen=True, slots=True)
class TimedList:
	""" A timed list of the sequence, played by an event reader of playback.py. """

	has_entries: str
	""" Objective: 1 when the sequence has some. """

	index: str
	""" Objective: index of the next entry. """

	folder: str
	""" Folder of the reader functions (load_next, skip_past). """


TIMED_LISTS: tuple[TimedList, ...] = (TimedList("has_swings", "swing_index", "swing"), TimedList("has_actions", "action_index", "action"))


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	functions: str = f"{ns}:v{version}"
	call: str = Storages(ns).call
	tags: str = f'Tags:["{ns}.instance","{ns}.entity","{ns}.new","smithed.entity","smithed.strict"]'

	def setting(objective: str, key: str, default: int) -> str:
		""" Objective from the setting <key>, `default` when it is missing. """
		return f"""scoreboard players set @s {ns}.{objective} {default}
execute if data storage {call} spawn.{key} store result score @s {ns}.{objective} run data get storage {call} spawn.{key}
"""

	write_versioned_function("spawn/store_command_block_position", f"""
{store_position(f"{call} options.command_block_")}
kill @s
""")

	sequence_scores: str = ""
	for objective, key in SEQUENCE_SCORES:
		sequence_scores += f"$execute store result score @s {ns}.{objective} run data get storage {ns}:data seqs.$(name).{key}\n"
	write_versioned_function("spawn/read_sequence", sequence_scores)

	write_versioned_function("spawn/join_local_group", f"""
# joins the nearest group of the same name within group_radius blocks, else starts a new one
scoreboard players set #found_group {ns}.data 0
$execute as @e[tag={ns}.instance,tag={ns}.group.$(group),distance=..$(group_radius),sort=nearest,limit=1] run scoreboard players operation #found_group {ns}.data = @s {ns}.group_id
execute if score #found_group {ns}.data matches ..0 run scoreboard players add #next_group_id {ns}.data 1
execute if score #found_group {ns}.data matches ..0 run scoreboard players operation #found_group {ns}.data = #next_group_id {ns}.data
scoreboard players operation @s {ns}.group_id = #found_group {ns}.data
$tag @s add {ns}.group.$(group)
""")

	start_point: str = ""
	for index, axis in enumerate(AXES):
		start_point += f"execute store result score @s {ns}.start_{axis} run data get entity @s Pos[{index}] 1000\n"
	write_versioned_function("spawn/init", f"""
tag @s remove {ns}.new
scoreboard players operation @s {ns}.instance_id = #next_instance_id {ns}.data
scoreboard players add #instance_count {ns}.data 1
{start_point}execute store result storage {call} spawn.instance_id int 1 run scoreboard players get @s {ns}.instance_id
function {functions}/spawn/register with storage {call} spawn
function {functions}/spawn/tag_name with storage {call} spawn
execute unless data storage {call} spawn{{tag:""}} run function {functions}/spawn/tag_user with storage {call} spawn
{setting("group_id", "group_id", 0)}execute if score @s {ns}.group_id matches -1 run function {functions}/spawn/join_local_group with storage {call} spawn
{setting("group_loop", "group_loop", 1)}scoreboard players set @s {ns}.group_start_tick -1
function {functions}/spawn/init_sequence
function {functions}/spawn/init_appearance
function {functions}/spawn/init_start
""")

	has_lists: str = ""
	for timed_list in TIMED_LISTS:
		has_lists += f"scoreboard players set @s {ns}.{timed_list.has_entries} 0\n"
	clamp_lists: str = ""
	for timed_list in TIMED_LISTS:
		clamp_lists += f"execute if score @s {ns}.{timed_list.has_entries} matches 1.. run scoreboard players set @s {ns}.{timed_list.has_entries} 1\n"
	command_block: str = ""
	for axis in AXES:
		command_block += f"execute if score @s {ns}.redstone matches 1 store result score @s {ns}.command_block_{axis} run data get storage {call} spawn.command_block_{axis}\n"
	start_block: str = ""
	for index, axis in enumerate(AXES):
		start_block += f"execute store result score @s {ns}.start_block_{axis} run data get entity @s Pos[{index}]\n"
	keyframe_start: str = ""
	for name in DIMENSIONS:
		keyframe_start += f"scoreboard players operation @s {ns}.keyframe_{name} = @s {ns}.start_{name}\n"
	write_versioned_function("spawn/init_sequence", f"""
scoreboard players set @s {ns}.restart_pending 0
{has_lists}function {functions}/spawn/read_sequence with storage {call} spawn
{clamp_lists}{setting("restore_mode", "restore", 1)}{setting("hit_players", "hit_players", 0)}scoreboard players set @s {ns}.next_release_tick -1
{setting("redstone", "redstone", 0)}{command_block}{start_block}function {functions}/spawn/set_size with storage {call} spawn
execute unless score @s {ns}.keyframe_ticks matches 1.. run scoreboard players set @s {ns}.keyframe_count 0
scoreboard players operation @s {ns}.keyframe_divisor = @s {ns}.keyframe_ticks
execute store result score @s {ns}.loop_mode run data get storage {call} spawn.loop
execute store result score @s {ns}.speed run data get storage {call} spawn.speed
{keyframe_start}scoreboard players set @s {ns}.is_still 0
scoreboard players set @s {ns}.is_still_placed 0
scoreboard players set @s {ns}.is_near 1
{setting("own_range", "range", 0)}execute if score @s {ns}.own_range matches 1.. run tag @s add {ns}.has_own_range
scoreboard players set @s {ns}.keyframe_index 0
scoreboard players set @s {ns}.equipment_index 0
scoreboard players set @s {ns}.next_equipment_keyframe 0
scoreboard players set @s {ns}.is_equipment_forced 0
scoreboard players set @s {ns}.pose_flags -1
scoreboard players set @s {ns}.is_pose_fixed 0
execute unless entity @s[type=minecraft:mannequin] run scoreboard players set @s {ns}.is_pose_fixed 1
scoreboard players set @s {ns}.turns_body 0
scoreboard players set @s {ns}.play_state 0
execute if score @s {ns}.keyframe_count matches 1.. run scoreboard players set @s {ns}.play_state 1
execute if score @s {ns}.play_state matches 1 run function {functions}/playback/load_keyframe
execute if score @s {ns}.group_id matches 1.. run function {functions}/group/join
""")

	write_versioned_function("spawn/init_appearance", f"""
function {functions}/spawn/override_equipment
execute if entity @s[type=minecraft:mannequin] if data storage {call} profile run data modify entity @s profile set from storage {call} profile
data remove storage {call} profile
execute if entity @s[type=minecraft:mannequin] unless data storage {call} spawn{{skin:""}} run function {functions}/spawn/set_skin with storage {call} spawn
execute if entity @s[type=minecraft:mannequin] if data storage {call} spawn{{skin:""}} unless data storage {call} spawn{{texture:""}} run function {functions}/spawn/set_texture with storage {call} spawn
execute unless data storage {call} spawn{{pose:""}} run function {functions}/spawn/force_pose with storage {call} spawn
""")

	timed_lists: str = ""
	for timed_list in TIMED_LISTS:
		timed_lists += f"""execute if score @s {ns}.{timed_list.has_entries} matches 1 run scoreboard players set @s {ns}.{timed_list.index} 0
execute if score @s {ns}.{timed_list.has_entries} matches 1 run function {functions}/{timed_list.folder}/load_next
execute if score @s {ns}.{timed_list.has_entries} matches 1 run function {functions}/{timed_list.folder}/skip_past
"""
	write_versioned_function("spawn/init_start", f"""
# a delayed start moves into the sequence, past swings and actions included
execute store result score @s {ns}.keyframe_progress run data get storage {call} spawn.delay 100
scoreboard players operation #sequence_length {ns}.data = @s {ns}.keyframe_count
scoreboard players operation #sequence_length {ns}.data *= @s {ns}.keyframe_ticks
execute if score #sequence_length {ns}.data matches 1.. run scoreboard players operation @s {ns}.keyframe_progress %= #sequence_length {ns}.data
execute if score @s {ns}.play_state matches 1 if score @s {ns}.keyframe_progress >= @s {ns}.keyframe_ticks run function {functions}/playback/advance_keyframe
{timed_lists}function {functions}/playback/move
function #{ns}:v{version.split(".")[0]}/signals/on_spawn
""")

	write_versioned_function("spawn/tag_name", f"$tag @s add {ns}.sequence.$(name)")
	write_versioned_function("spawn/tag_user", f"$tag @s add {ns}.tag.$(tag)")
	write_versioned_function("spawn/register", f'$data modify storage {ns}:instances i$(instance_id) set value {{name:"$(name)"}}')

	overrides: str = ""
	for field, slot in EQUIPMENT_FIELDS.items():
		overrides += f"""execute unless data storage {call} spawn{{{field}:""}} run data modify storage {call} slot_override set value {{slot:"{slot}"}}
execute unless data storage {call} spawn{{{field}:""}} run data modify storage {call} slot_override.item set from storage {call} spawn.{field}
execute unless data storage {call} spawn{{{field}:""}} run function {functions}/spawn/set_slot with storage {call} slot_override
execute unless data storage {call} spawn{{{field}:""}} run scoreboard players set @s {ns}.is_equipment_forced 1
"""
	write_versioned_function("spawn/override_equipment", f"""
# a filled equipment field also stops the recorded equipment changes
{overrides}""")

	write_versioned_function("spawn/force_pose", f"""
$data modify entity @s pose set value "$(pose)"
execute if data storage {call} spawn{{pose:"fall_flying"}} run data modify entity @s OnGround set value 0b
execute if data storage {call} spawn{{pose:"fall_flying"}} run data modify entity @s FallFlying set value 1b
scoreboard players set @s {ns}.is_pose_fixed 1
""")

	write_versioned_function("spawn/set_size", "$attribute @s minecraft:scale base set $(size)")
	write_versioned_function("spawn/set_skin", '$data modify entity @s profile set value "$(skin)"')
	write_versioned_function("spawn/set_texture", '$data modify entity @s profile set value {properties:[{name:"textures",value:"$(texture)"}]}')
	write_versioned_function("spawn/set_slot", "$item replace entity @s $(slot) with $(item)")

	mannequins: str = ""
	for entity in MANNEQUIN_IDS:
		mannequins += f'execute if data storage {call} spawn{{entity:"{entity}"}} run function {functions}/spawn/summon_mannequin\n'
	not_mannequin: str = " ".join(f'unless data storage {call} spawn{{entity:"{entity}"}}' for entity in MANNEQUIN_IDS)
	write_versioned_function("spawn/summon", f"""
execute unless data storage {call} spawn{{tag:""}} run function {functions}/kill/by_tag with storage {call} spawn
{mannequins}execute {not_mannequin} run function {functions}/spawn/summon_other with storage {call} spawn
scoreboard players add #next_instance_id {ns}.data 1
execute as @e[tag={ns}.new,sort=nearest,limit=1] run function {functions}/spawn/init
""")

	write_versioned_function("spawn/summon_mannequin", f"summon minecraft:mannequin ~ ~ ~ {{{tags},immovable:true,hide_description:true,Invulnerable:1b,Silent:1b,NoGravity:1b}}")
	write_versioned_function("spawn/summon_other", f"$summon $(entity) ~ ~ ~ {{{tags},NoAI:1b,Silent:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b}}")

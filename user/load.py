""" Load, tick and unload: objectives, world state kept between versions, and the main loop. """
# Imports
from stewbeet import Mem, write_load_file, write_tick_file, write_unload_file

from .common import AXES, DIMENSIONS
from .menu import MENU_MATCH

# Constants
DUMMY_OBJECTIVES: tuple[str, ...] = (
	# Playback entities
	"instance_id", "play_state", "loop_mode", "speed", "keyframe_index", "keyframe_count", "keyframe_ticks", "keyframe_progress", "keyframe_divisor",
	*(f"start_{dimension}" for dimension in DIMENSIONS), *(f"keyframe_{dimension}" for dimension in DIMENSIONS), *(f"delta_{dimension}" for dimension in DIMENSIONS),
	"pose_flags", "next_pose_flags", "is_pose_fixed", "turns_body", "is_still", "is_still_placed", "is_near", "own_range",
	"equipment_index", "next_equipment_keyframe", "is_equipment_forced", "has_swings", "swing_index", "next_swing_tick",
	"group_id", "group_loop", "group_start_tick", "restart_pending",
	# Played back actions
	"has_actions", "action_index", "next_action_tick", "restore_mode", "hit_players", "next_release_tick", "redstone", "pulse_end_tick",
	*(f"start_block_{axis}" for axis in AXES), *(f"command_block_{axis}" for axis in AXES),
	# Players: recording state
	"player_id", "record_tick", "keyframe_step", "ticks_since_keyframe", "recorded_keyframes", "chunk_keyframes", "last_swing_tick",
	"is_challenge", "challenge_ticks", "waited_group", "armed_kind",
	*(f"recorded_{dimension}" for dimension in DIMENSIONS), *(f"record_start_{dimension}" for dimension in DIMENSIONS),
	"previous_sneak_time", "previous_swim_distance", "previous_glide_distance",
	# Players: recorded actions
	*(f"record_block_{axis}" for axis in AXES), "is_looking_at_block", *(f"look_cube_{axis}" for axis in AXES),
	"has_pending_use", "has_placed", *(f"used_block_{axis}" for axis in AXES), "used_tick", "last_hit_tick",
)
""" Dummy objectives, prefixed with the namespace. """

CRITERIA_OBJECTIVES: dict[str, str] = {
	"sneak_time": "minecraft.custom:minecraft.sneak_time",
	"swim_distance": "minecraft.custom:minecraft.swim_one_cm",
	"glide_distance": "minecraft.custom:minecraft.aviate_one_cm",
	"item_uses": "minecraft.used:minecraft.carrot_on_a_stick",
	"left_game": "minecraft.custom:minecraft.leave_game",
}
""" Statistic objectives, prefixed with the namespace. """

PERSISTENT_SCORES: dict[str, int] = {
	"#next_instance_id": 0,
	"#next_player_id": 0,
	"#next_group_id": 0,
	"#tick": 0,
	"#has_pending_group": 0,
	"#next_block_slot": 0,
	"#next_cube_slot": 0,
	"#pulse_count": 0,
	"#move_every": 2,
}
""" Scores of `<ns>.data` holding world state, kept on /reload. """

VAULT_CHUNKS: str = "0 0 47 15"
""" Blocks forceloaded in the survirec:vault dimension (chunks 0 to 2). """


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	functions: str = f"{ns}:v{version}"

	objectives: str = ""
	for name in DUMMY_OBJECTIVES:
		objectives += f"scoreboard objectives add {ns}.{name} dummy\n"
	for name, criterion in CRITERIA_OBJECTIVES.items():
		objectives += f"scoreboard objectives add {ns}.{name} {criterion}\n"
	defaults: str = ""
	for holder, value in PERSISTENT_SCORES.items():
		defaults += f"execute unless score {holder} {ns}.data = {holder} {ns}.data run scoreboard players set {holder} {ns}.data {value}\n"

	write_load_file(f"""
# Objectives
{objectives}
# World state defaults
{defaults}execute unless data storage {ns}:config range run data modify storage {ns}:config range set value 128
function {functions}/menu/set_head_texture
execute store result score #instance_count {ns}.data if entity @e[tag={ns}.instance]

# Hidden dimension holding the block copies
execute in {ns}:vault run forceload add {VAULT_CHUNKS}
""")

	write_tick_file(f"""
execute store result score #game_time {ns}.data run time query gametime
execute unless data storage {ns}:config are_cubes_ready run function {functions}/vault/try_prepare
scoreboard players add #tick {ns}.data 1
execute if score #tick {ns}.data matches 1000000.. run scoreboard players set #tick {ns}.data 0

# Players: rejoin, menu item, recordings
execute as @a[scores={{{ns}.left_game=1..}}] run function {functions}/record/on_rejoin
execute as @a[scores={{{ns}.item_uses=1..}}] if items entity @s weapon.* {MENU_MATCH.format(ns=ns)} run function {functions}/menu/open
execute as @a[tag={ns}.recording] at @s run function {functions}/record/tick

# Every 10 ticks: players near the entities, armed recordings, entity count (corrects kills and chunk loads)
scoreboard players operation #tick_mod_10 {ns}.data = #tick {ns}.data
scoreboard players operation #tick_mod_10 {ns}.data %= #10 {ns}.data
execute if score #tick_mod_10 {ns}.data matches 0 store result score #instance_count {ns}.data if entity @e[tag={ns}.instance]
execute if score #tick_mod_10 {ns}.data matches 0 if score #instance_count {ns}.data matches 1.. run function {functions}/range/check_global with storage {ns}:config
execute if score #tick_mod_10 {ns}.data matches 0 as @a[tag={ns}.armed] run function {functions}/challenge/check_armed

# Every 4 ticks: entities with their own range
scoreboard players operation #tick_mod_4 {ns}.data = #tick {ns}.data
scoreboard players operation #tick_mod_4 {ns}.data %= #4 {ns}.data
execute if score #tick_mod_4 {ns}.data matches 0 if score #instance_count {ns}.data matches 1.. as @e[tag={ns}.instance,tag={ns}.has_own_range] at @s run function {functions}/range/check_own

# Every 5 ticks: start markers, only while someone records
scoreboard players operation #tick_mod_5 {ns}.data = #tick {ns}.data
scoreboard players operation #tick_mod_5 {ns}.data %= #5 {ns}.data
execute if score #tick_mod_5 {ns}.data matches 0 if entity @a[tag={ns}.recording,limit=1] as @e[type=minecraft:text_display,tag={ns}.start_marker] at @s run function {functions}/record/show_start_marker

# Playback
execute if score #pulse_count {ns}.data matches 1.. as @e[type=minecraft:marker,tag={ns}.pulse_marker] if score #game_time {ns}.data >= @s {ns}.pulse_end_tick at @s run function {functions}/pulse/stop
execute if score #instance_count {ns}.data matches 1.. as @e[tag={ns}.instance] run function {functions}/playback/tick
execute if score #has_pending_group {ns}.data matches 1 run function {functions}/group/restart_pending
""")

	write_unload_file(f"""
execute in {ns}:vault run forceload remove {VAULT_CHUNKS}
""")

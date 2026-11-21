""" Playback entities: keyframe interpolation, equipment, swings, actions, groups, button releases and redstone pulses. """
# Imports
from stewbeet import Mem, write_versioned_function

from .common import AXES, DIMENSIONS, TELEPORT_SCALES, Storages, store_position, wrap_yaw

# Constants
KEYFRAME_SCORES: tuple[str, ...] = ("delta_x", "delta_y", "delta_z", "delta_yaw", "delta_pitch", "next_pose_flags")
""" Objectives read from a keyframe row [dx,dy,dz,dyaw,dpitch,flags], in this order. """

BLOCK_ACTIONS: dict[int, str] = {2: "use_block", 3: "place_block", 4: "break_block"}
""" Action kind played at a block -> action/<function>. Kind 1, a hit, is played where the entity stands. """

USABLE_BLOCKS: tuple[tuple[str, str], ...] = (
	("#minecraft:buttons", "press_button"), ("minecraft:lever", "toggle_lever"), ("#{ns}:doors_open", "toggle_door"),
	("#{ns}:trapdoors_open", "toggle_open"), ("#minecraft:fence_gates", "toggle_open"),
)
""" Block used by an entity -> use/<function> toggling it. """

SUPPORT_OFFSETS: tuple[tuple[str, str, int], ...] = (
	("1", "y", -1), ("2", "y", 1),
	("3 if score #block_facing {ns}.data matches 1", "z", 1), ("3 if score #block_facing {ns}.data matches 2", "z", -1),
	("3 if score #block_facing {ns}.data matches 3", "x", -1), ("3 if score #block_facing {ns}.data matches 4", "x", 1),
)
""" Button or lever (#block_face, then #block_facing) -> axis and offset of the block it is attached to. """

POSES: tuple[tuple[str, str], ...] = (("0", "standing"), ("1", "crouching"), ("2..3", "swimming"), ("4..7", "fall_flying"))
""" Keyframe flags -> entity pose. """

CLEARED_SLOTS: tuple[str, ...] = ("armor.head", "armor.chest", "armor.legs", "armor.feet", "weapon.mainhand", "weapon.offhand")
""" Slots emptied before an entity is removed, so that nothing drops. """

SOUND_LISTENERS: str = "@a[distance=..24]"
""" Players sent the sounds of the entities. """


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	functions: str = f"{ns}:v{version}"
	playback: str = Storages(ns).playback
	store_instance_id: str = f"execute store result storage {playback} instance_id int 1 run scoreboard players get @s {ns}.instance_id"
	sequence_time: str = f"""scoreboard players operation #sequence_time {ns}.data = @s {ns}.keyframe_index
scoreboard players operation #sequence_time {ns}.data *= @s {ns}.keyframe_ticks
scoreboard players operation #sequence_time {ns}.data += @s {ns}.keyframe_progress"""

	def read_sequence_name(path: str, then: str) -> None:
		""" `path`: puts the sequence name of instance $(id) in <ns>:playback name, then runs `then` with it. """
		write_versioned_function(path, f"""
$data modify storage {playback} name set from storage {ns}:instances i$(instance_id).name
function {functions}/{then} with storage {playback}
""")

	def event_reader(folder: str, index: str, next_tick: str, cursor: str, entries: str, time: str, on_event: str) -> None:
		""" Reader of a timed list of the sequence (s: swings, a: actions; the tick of an entry is `<entry><time>`):
		load_next puts the tick of entry @s <index> in @s <next_tick> (999999999 after the last one),
		run_due runs `on_event` for every entry due, skip_past passes the entries already behind (delayed start).
		"""
		write_versioned_function(f"{folder}/load_next", f"""
{store_instance_id}
execute store result storage {playback} {cursor} int 1 run scoreboard players get @s {ns}.{index}
scoreboard players set @s {ns}.{next_tick} 999999999
function {functions}/{folder}/read_name with storage {playback}
""")
		read_sequence_name(f"{folder}/read_name", f"{folder}/read_tick")
		entry: str = f"seqs.$(name).{entries}[$({cursor})]"
		write_versioned_function(f"{folder}/read_tick", f"$execute if data storage {ns}:data {entry} store result score @s {ns}.{next_tick} run data get storage {ns}:data {entry}{time} 100")
		write_versioned_function(f"{folder}/run_due", f"""
{sequence_time}
execute if score #sequence_time {ns}.data >= @s {ns}.{next_tick} run function {functions}/{on_event}
""")
		write_versioned_function(f"{folder}/skip_past", f"""
{sequence_time}
execute if score #sequence_time {ns}.data > @s {ns}.{next_tick} run function {functions}/{folder}/skip_next
""")
		write_versioned_function(f"{folder}/skip_next", f"""
scoreboard players add @s {ns}.{index} 1
function {functions}/{folder}/load_next
execute if score #sequence_time {ns}.data > @s {ns}.{next_tick} run function {functions}/{folder}/skip_next
""")

	def set_property(name: str, value: str) -> str:
		return f'function #bs.block:replace_properties {{properties:[{{name:"{name}",value:"{value}"}}]}}'

	## Swings
	event_reader("swing", "swing_index", "next_swing_tick", "swing_index", "s", "", "swing/run_next")
	write_versioned_function("swing/run_next", f"""
swing @s mainhand
scoreboard players add @s {ns}.swing_index 1
function {functions}/swing/load_next
execute if score #sequence_time {ns}.data >= @s {ns}.next_swing_tick run function {functions}/swing/run_next
""")

	## Actions (kind 1 hit, 2 use, 3 place, 4 break), at their recorded tick
	event_reader("action", "action_index", "next_action_tick", "action_index", "a", ".t", "action/run_next")
	write_versioned_function("action/run_next", f"""
{store_instance_id}
execute store result storage {playback} action_index int 1 run scoreboard players get @s {ns}.action_index
function {functions}/action/read_event_name with storage {playback}
function {functions}/action/run_event
scoreboard players add @s {ns}.action_index 1
function {functions}/action/load_next
execute if score #sequence_time {ns}.data >= @s {ns}.next_action_tick run function {functions}/action/run_next
""")
	read_sequence_name("action/read_event_name", "action/read_event")
	write_versioned_function("action/read_event", f"$data modify storage {playback} event set from storage {ns}:data seqs.$(name).a[$(action_index)]")

	block_position: str = ""
	for axis in AXES:
		block_position += f"""execute store result score #block_{axis} {ns}.data run data get storage {playback} event.{axis}
scoreboard players operation #block_{axis} {ns}.data += @s {ns}.start_block_{axis}
execute store result storage {playback} action_position.{axis} int 1 run scoreboard players get #block_{axis} {ns}.data
"""
	write_versioned_function("action/run_event", f"""
execute store result score #event_kind {ns}.data run data get storage {playback} event.k
execute if score #event_kind {ns}.data matches 1 run return run function {functions}/action/hit
# block of the action = start block of the entity + recorded offset
data modify storage {playback} action_position set value {{x:0,y:0,z:0}}
{block_position}execute if score #event_kind {ns}.data matches 2..4 run return run function {functions}/action/run_at with storage {playback} action_position
""")

	write_versioned_function("action/run_at", f"$execute at @s positioned $(x) $(y) $(z) run function {functions}/action/run_block_action")

	block_actions: str = ""
	for kind, target in BLOCK_ACTIONS.items():
		block_actions += f"execute if score #event_kind {ns}.data matches {kind} run return run function {functions}/action/{target}\n"
	write_versioned_function("action/run_block_action", block_actions)

	pair_offset: str = ""
	for axis in AXES:
		pair_offset += f"execute store result storage {playback} pair_offset.{axis} int 1 run scoreboard players get #pair_{axis} {ns}.data\n"
	write_versioned_function("action/back_up_other_half", f"""
data modify storage {playback} pair_offset set value {{x:0,y:0,z:0}}
{pair_offset}function {functions}/action/back_up_other_half_at with storage {playback} pair_offset
""")
	write_versioned_function("action/back_up_other_half_at", f"$execute positioned ~$(x) ~$(y) ~$(z) run function {functions}/vault/back_up_here")

	write_versioned_function("action/break_block", f"""
function {functions}/block/read
function {functions}/block/find_other_half
scoreboard players operation #restore_strict {ns}.data = #is_pair {ns}.data
function {functions}/vault/back_up_here
execute if score #is_pair {ns}.data matches 1 run function {functions}/action/back_up_other_half
setblock ~ ~ ~ minecraft:air destroy
execute align xyz positioned ~0.5 ~0.5 ~0.5 run kill @e[type=minecraft:item,distance=..1.6,nbt={{Age:0s}}]
execute align xyz positioned ~0.5 ~0.5 ~0.5 run kill @e[type=minecraft:experience_orb,distance=..1.6]
swing @s mainhand
""")

	write_versioned_function("action/hit_in_front", f"""
$execute as @e[distance=..1.6,tag=!{ns}.instance,tag=!smithed.strict,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker] run damage @s $(damage) minecraft:mob_attack by @e[tag={ns}.hitter,limit=1]
$execute if score @e[tag={ns}.hitter,limit=1] {ns}.hit_players matches 1 as @a[distance=..1.6,gamemode=!spectator] run damage @s $(damage) minecraft:mob_attack by @e[tag={ns}.hitter,limit=1]
""")

	write_versioned_function("action/place_block", f"""
# a door or a bed is placed without block updates, so that its halves do not copy each other
scoreboard players set #restore_strict {ns}.data 0
execute if data storage {playback} event.p run scoreboard players set #restore_strict {ns}.data 1
function {functions}/vault/back_up_here
execute if score #restore_strict {ns}.data matches 1 run function {functions}/action/place_other_half
execute if score #restore_strict {ns}.data matches 0 run function {functions}/block/set_recorded with storage {playback} event
execute if score #restore_strict {ns}.data matches 1 run function {functions}/block/set_recorded_strict with storage {playback} event
playsound minecraft:block.stone.place block {SOUND_LISTENERS} ~ ~ ~
""")

	half_position: str = ""
	for axis in AXES:
		half_position += f"""execute store result score #half_{axis} {ns}.data run data get storage {playback} event.p.{axis}
scoreboard players operation #half_{axis} {ns}.data += @s {ns}.start_block_{axis}
execute store result storage {playback} other_half.{axis} int 1 run scoreboard players get #half_{axis} {ns}.data
"""
	write_versioned_function("action/place_other_half", f"""
data modify storage {playback} other_half set value {{x:0,y:0,z:0,b:""}}
data modify storage {playback} other_half.b set from storage {playback} event.p.b
{half_position}function {functions}/action/place_other_half_at with storage {playback} other_half
""")
	write_versioned_function("action/place_other_half_at", f"""
$execute positioned $(x) $(y) $(z) run function {functions}/vault/back_up_here
$setblock $(x) $(y) $(z) $(b) strict
""")

	usable: str = ""
	for block, target in USABLE_BLOCKS:
		usable += f"execute if block ~ ~ ~ {block.format(ns=ns)} run return run function {functions}/use/{target}\n"
	write_versioned_function("action/use_block", f"""
function {functions}/block/read
execute if data storage {Storages(ns).block} {{id:""}} run return 0
{usable}""")

	## Keyframes
	advance: str = ""
	for name in DIMENSIONS:
		advance += f"scoreboard players operation @s {ns}.keyframe_{name} += @s {ns}.delta_{name}\n"
	write_versioned_function("playback/advance_keyframe", f"""
scoreboard players operation @s {ns}.keyframe_progress -= @s {ns}.keyframe_ticks
{advance}scoreboard players add @s {ns}.keyframe_index 1
execute if score @s {ns}.keyframe_index >= @s {ns}.keyframe_count run function {functions}/playback/on_sequence_end
execute if score @s {ns}.play_state matches 1 run function {functions}/playback/load_keyframe
execute if score @s {ns}.play_state matches 1 if score @s {ns}.keyframe_progress >= @s {ns}.keyframe_ticks run function {functions}/playback/advance_keyframe
""")

	write_versioned_function("playback/turn_body", f"""
$data modify entity @s Rotation set value [$(yaw)f,$(pitch)f]
execute if score @s {ns}.delta_yaw matches 0 run scoreboard players set @s {ns}.turns_body 0
""")

	cleared: str = ""
	for slot in CLEARED_SLOTS:
		cleared += f"item replace entity @s {slot} with minecraft:air\n"
	write_versioned_function("playback/delete", f"""
scoreboard players set @s {ns}.play_state 0
function {functions}/release/run_all
execute if score @s {ns}.restore_mode matches 2 run function {functions}/vault/restore
execute if score @s {ns}.restore_mode matches 1 if score #restore_on_kill {ns}.data matches 1 run function {functions}/vault/restore
function {functions}/vault/free
{store_instance_id}
function {functions}/playback/unregister with storage {playback}
tag @s remove {ns}.instance
scoreboard players remove #instance_count {ns}.data 1
# nothing may show nor drop: equipment emptied, entity sent below the world before it is removed
{cleared}effect give @s minecraft:invisibility infinite 0 true
tp @s ~ -1000 ~
kill @s
""")

	write_versioned_function("playback/on_sequence_end", f"""
execute if score @s {ns}.redstone matches 1 if score @s {ns}.group_id matches 0 run function {functions}/pulse/start
execute if score @s {ns}.loop_mode matches 1 run function {functions}/playback/restart
execute unless score @s {ns}.loop_mode matches 0..2 run function {functions}/playback/restart
execute if score @s {ns}.loop_mode matches 0 run function {functions}/playback/freeze
execute if score @s {ns}.loop_mode matches 2 run function {functions}/playback/delete
""")

	## Equipment events
	write_versioned_function("equipment/load_next", f"""
{store_instance_id}
execute store result storage {playback} equipment_index int 1 run scoreboard players get @s {ns}.equipment_index
scoreboard players add @s {ns}.equipment_index 1
execute store result storage {playback} next_equipment_index int 1 run scoreboard players get @s {ns}.equipment_index
scoreboard players set @s {ns}.next_equipment_keyframe 999999999
function {functions}/equipment/read_name with storage {playback}
execute if score @s {ns}.keyframe_index >= @s {ns}.next_equipment_keyframe run function {functions}/equipment/load_next
""")
	read_sequence_name("equipment/read_name", "equipment/apply")
	write_versioned_function("equipment/apply", f"""
$data modify entity @s equipment set from storage {ns}:data seqs.$(name).e[$(equipment_index)].v
$execute if data storage {ns}:data seqs.$(name).e[$(next_equipment_index)] store result score @s {ns}.next_equipment_keyframe run data get storage {ns}:data seqs.$(name).e[$(next_equipment_index)].k
""")

	still: str = ""
	for name in DIMENSIONS:
		still += f"scoreboard players set @s {ns}.delta_{name} 0\n"
	write_versioned_function("playback/freeze", f"""
{still}scoreboard players set @s {ns}.keyframe_progress 0
scoreboard players set @s {ns}.play_state 0
execute if score @s {ns}.group_id matches 0 if score @s {ns}.restore_mode matches 2 run function {functions}/vault/restore
function {functions}/playback/move
execute if score @s {ns}.group_id matches 1.. run function {functions}/group/on_member_frozen
""")

	## Groups
	write_versioned_function("group/check", f"""
function {functions}/group/mark_if_finished
execute if score #has_pending_group {ns}.data matches 1 run function {functions}/group/restart_pending
""")

	write_versioned_function("group/restart_pending", f"""
scoreboard players set #has_pending_group {ns}.data 0
execute as @e[tag={ns}.instance,scores={{{ns}.restart_pending=1}}] run function {functions}/group/walk_back
""")

	write_versioned_function("group/on_member_frozen", f"""
scoreboard players operation #group {ns}.data = @s {ns}.group_id
function {functions}/group/mark_if_finished
""")

	write_versioned_function("group/join", f"""
# an entity joining a group that plays waits for its next cycle, unless the group started this tick
tag @s add {ns}.self
scoreboard players operation #group {ns}.data = @s {ns}.group_id
scoreboard players set #group_alive {ns}.data 0
scoreboard players set #started_this_tick {ns}.data 0
execute as @e[tag={ns}.instance,tag=!{ns}.self] if score @s {ns}.group_id = #group {ns}.data if score @s {ns}.play_state matches 1..2 run scoreboard players set #group_alive {ns}.data 1
execute as @e[tag={ns}.instance,tag=!{ns}.self] if score @s {ns}.group_id = #group {ns}.data if score @s {ns}.play_state matches 1 if score @s {ns}.group_start_tick = #tick {ns}.data run scoreboard players set #started_this_tick {ns}.data 1
tag @s remove {ns}.self
execute if score #group_alive {ns}.data matches 1 unless score #started_this_tick {ns}.data matches 1 run scoreboard players set @s {ns}.play_state 0
execute unless score @s {ns}.play_state matches 0 run scoreboard players operation @s {ns}.group_start_tick = #tick {ns}.data
""")

	finished_members: str = f"execute if score #group_alive {ns}.data matches 0 as @e[tag={ns}.instance] if score @s {ns}.group_id = #group {ns}.data"
	write_versioned_function("group/mark_if_finished", f"""
scoreboard players set #group_alive {ns}.data 0
execute as @e[tag={ns}.instance] if score @s {ns}.group_id = #group {ns}.data if score @s {ns}.play_state matches 1..2 run scoreboard players set #group_alive {ns}.data 1
{finished_members} unless score @s {ns}.group_loop matches 0 unless score @s {ns}.group_loop matches 2 run scoreboard players set @s {ns}.restart_pending 1
{finished_members} if score @s {ns}.redstone matches 1 run function {functions}/pulse/start
{finished_members} if score @s {ns}.group_loop matches 2 run function {functions}/playback/delete
{finished_members} if score @s {ns}.group_loop matches 0 if score @s {ns}.restore_mode matches 2 run function {functions}/vault/restore
execute if score #group_alive {ns}.data matches 0 run scoreboard players set #has_pending_group {ns}.data 1
""")

	walk_back: str = ""
	for name in DIMENSIONS:
		walk_back += f"""scoreboard players operation @s {ns}.delta_{name} = @s {ns}.start_{name}
scoreboard players operation @s {ns}.delta_{name} -= @s {ns}.keyframe_{name}
"""
		if name == "yaw":
			walk_back += wrap_yaw(f"@s {ns}.delta_yaw") + "\n"
	write_versioned_function("group/walk_back", f"""
# 2 seconds back to the start point, then the group starts again together
scoreboard players set @s {ns}.restart_pending 0
execute if score @s {ns}.restore_mode matches 1.. run function {functions}/vault/restore
execute unless score @s {ns}.keyframe_count matches 1.. run return 0
{walk_back}scoreboard players set @s {ns}.keyframe_divisor 40
scoreboard players set @s {ns}.keyframe_progress 0
scoreboard players set @s {ns}.is_still 0
scoreboard players set @s {ns}.is_still_placed 0
scoreboard players set @s {ns}.next_pose_flags 0
execute if score @s {ns}.is_pose_fixed matches 0 unless score @s {ns}.next_pose_flags = @s {ns}.pose_flags run function {functions}/playback/apply_pose
scoreboard players set @s {ns}.play_state 2
""")

	## The block behind a button or lever is updated, so that a command block or redstone behind it reacts like with a player
	write_versioned_function("block/update_support", f"""
execute unless data storage {ns}:config are_blocks_ready run return 0
clone ~ ~ ~ ~ ~ ~ to {ns}:vault 15 319 15 strict
setblock ~ ~ ~ minecraft:barrier strict
clone from {ns}:vault 15 319 15 15 319 15 ~ ~ ~
""")
	write_versioned_function("block/update_support_at", f"$execute positioned ~$(x) ~$(y) ~$(z) run function {functions}/block/update_support")
	write_versioned_function("block/mark_support", f"$execute positioned ~$(x) ~$(y) ~$(z) summon minecraft:marker run function {functions}/block/store_support_position")

	support: str = ""
	for face, axis, offset in SUPPORT_OFFSETS:
		support += f"execute if score #block_face {ns}.data matches {face.format(ns=ns)} run data modify storage {playback} support_offset.{axis} set value {offset}\n"
	write_versioned_function("block/find_support", f"""
# at a button or lever read by block/read: offset to the block it is attached to
data modify storage {playback} support_offset set value {{x:0,y:0,z:0}}
{support}""")

	write_versioned_function("block/store_support_position", f"""
{store_position(f"{playback} release.support_")}
kill @s
""")

	## Keyframes
	write_versioned_function("playback/load_keyframe", f"""
{store_instance_id}
execute store result storage {playback} keyframe_index int 1 run scoreboard players get @s {ns}.keyframe_index
function {functions}/playback/read_keyframe_name with storage {playback}
execute if score @s {ns}.is_equipment_forced matches 0 if score @s {ns}.keyframe_index >= @s {ns}.next_equipment_keyframe run function {functions}/equipment/load_next
""")
	read_sequence_name("playback/read_keyframe_name", "playback/read_keyframe")

	row: str = ""
	for index, objective in enumerate(KEYFRAME_SCORES):
		row += f"execute store result score @s {ns}.{objective} run data get storage {playback} keyframe[{index}]\n"
	is_still: str = " ".join(f"if score @s {ns}.delta_{name} matches 0" for name in DIMENSIONS)
	write_versioned_function("playback/read_keyframe", f"""
$data modify storage {playback} keyframe set from storage {ns}:data seqs.$(name).d[$(keyframe_index)]
{row}scoreboard players operation #was_still {ns}.data = @s {ns}.is_still
scoreboard players set @s {ns}.is_still 0
execute {is_still} run scoreboard players set @s {ns}.is_still 1
execute unless score @s {ns}.is_still matches 1 run scoreboard players set @s {ns}.is_still_placed 0
execute unless score #was_still {ns}.data matches 1 run scoreboard players set @s {ns}.is_still_placed 0
# a swimming or gliding pose turns the body with the head
scoreboard players set @s {ns}.turns_body 0
execute if score @s {ns}.is_pose_fixed matches 0 if score @s {ns}.next_pose_flags matches 2..7 unless score @s {ns}.delta_yaw matches 0 run scoreboard players set @s {ns}.turns_body 1
execute if score @s {ns}.is_pose_fixed matches 0 if score @s {ns}.next_pose_flags matches 2..7 unless score @s {ns}.next_pose_flags = @s {ns}.pose_flags run scoreboard players set @s {ns}.turns_body 1
execute if score @s {ns}.turns_body matches 1 run scoreboard players set @s {ns}.is_still_placed 0
execute if score @s {ns}.is_pose_fixed matches 0 unless score @s {ns}.next_pose_flags = @s {ns}.pose_flags run function {functions}/playback/apply_pose
""")

	interpolation: str = ""
	for name in DIMENSIONS:
		interpolation += f"""scoreboard players operation #interpolated {ns}.data = @s {ns}.delta_{name}
scoreboard players operation #interpolated {ns}.data *= @s {ns}.keyframe_progress
scoreboard players operation #interpolated {ns}.data /= @s {ns}.keyframe_divisor
scoreboard players operation #interpolated {ns}.data += @s {ns}.keyframe_{name}
"""
		if name == "pitch":
			interpolation += f"""execute if score #interpolated {ns}.data matches 9001.. run scoreboard players set #interpolated {ns}.data 9000
execute if score #interpolated {ns}.data matches ..-9001 run scoreboard players set #interpolated {ns}.data -9000
"""
		interpolation += f"execute store result storage {playback} teleport.{name} double {TELEPORT_SCALES[name]} run scoreboard players get #interpolated {ns}.data\n"
	write_versioned_function("playback/move", f"""
{interpolation}function {functions}/playback/teleport with storage {playback} teleport
execute if score @s {ns}.turns_body matches 1 run function {functions}/playback/turn_body with storage {playback} teleport
execute if score @s {ns}.is_still matches 1 run scoreboard players set @s {ns}.is_still_placed 1
""")

	poses: str = ""
	for flags, pose in POSES:
		poses += f'execute if score @s {ns}.pose_flags matches {flags} run data modify entity @s pose set value "{pose}"\n'
	write_versioned_function("playback/apply_pose", f"""
scoreboard players operation @s {ns}.pose_flags = @s {ns}.next_pose_flags
{poses}execute if score @s {ns}.pose_flags matches 4..7 run data modify entity @s OnGround set value 0b
execute if score @s {ns}.pose_flags matches 4..7 run data modify entity @s FallFlying set value 1b
execute unless score @s {ns}.pose_flags matches 4..7 run data modify entity @s FallFlying set value 0b
""")

	## Redstone pulse at the end of a loop, 2 blocks above the command block (1 block gap, else it fires itself again)
	pulse_position: str = ""
	for axis in AXES:
		pulse_position += f"execute store result storage {playback} pulse_position.{axis} int 1 run scoreboard players get @s {ns}.command_block_{axis}\n"
	write_versioned_function("pulse/start", f"""
{pulse_position}function {functions}/pulse/start_at with storage {playback} pulse_position
""")
	write_versioned_function("pulse/start_at", f"$execute at @s positioned $(x) $(y) $(z) positioned ~ ~2 ~ run function {functions}/pulse/place")
	write_versioned_function("pulse/place", f"""
execute unless block ~ ~ ~ #minecraft:air run return 0
setblock ~ ~ ~ minecraft:redstone_block
execute align xyz positioned ~0.5 ~0.5 ~0.5 summon minecraft:marker run function {functions}/pulse/register
""")
	write_versioned_function("pulse/register", f"""
tag @s add {ns}.pulse_marker
tag @s add smithed.entity
tag @s add smithed.strict
scoreboard players operation @s {ns}.pulse_end_tick = #game_time {ns}.data
scoreboard players add @s {ns}.pulse_end_tick 4
scoreboard players add #pulse_count {ns}.data 1
""")
	write_versioned_function("pulse/stop", f"""
execute if block ~ ~ ~ minecraft:redstone_block run setblock ~ ~ ~ minecraft:air
scoreboard players remove #pulse_count {ns}.data 1
kill @s
""")

	## Buttons released after their delay
	write_versioned_function("release/run_due", f"""
execute store result storage {playback} instance_id int 1 run scoreboard players get @s {ns}.instance_id
function {functions}/release/pull_list with storage {playback}
scoreboard players set @s {ns}.next_release_tick -1
execute if data storage {playback} due_releases[0] at @s run function {functions}/release/check_next
""")
	write_versioned_function("release/pull_list", f"""
data modify storage {playback} due_releases set value []
$data modify storage {playback} due_releases set from storage {ns}:instances i$(instance_id).releases
$data modify storage {ns}:instances i$(instance_id).releases set value []
""")
	write_versioned_function("release/check_next", f"""
execute store result score #release_tick {ns}.data run data get storage {playback} due_releases[0].tick
execute if score #release_all {ns}.data matches 1 run scoreboard players set #release_tick {ns}.data -1
execute if score #release_tick {ns}.data <= #game_time {ns}.data run function {functions}/release/release_button with storage {playback} due_releases[0]
execute if score #release_tick {ns}.data > #game_time {ns}.data run function {functions}/release/keep
data remove storage {playback} due_releases[0]
execute if data storage {playback} due_releases[0] run function {functions}/release/check_next
""")
	write_versioned_function("release/release_button", f"""
$setblock $(x) $(y) $(z) $(block)
$execute positioned $(support_x) $(support_y) $(support_z) run function {functions}/block/update_support
$playsound minecraft:block.stone_button.click_off block {SOUND_LISTENERS} $(x) $(y) $(z)
""")
	write_versioned_function("release/run_all", f"""
scoreboard players set #release_all {ns}.data 1
function {functions}/release/run_due
scoreboard players set #release_all {ns}.data 0
""")
	write_versioned_function("release/keep", f"""
data modify storage {playback} release set from storage {playback} due_releases[0]
function {functions}/release/add
""")
	write_versioned_function("release/store_position", f"""
{store_position(f"{playback} release.")}
kill @s
""")
	write_versioned_function("release/add", f"""
execute store result storage {playback} release.instance_id int 1 run scoreboard players get @s {ns}.instance_id
function {functions}/release/add_to_instance with storage {playback} release
execute if score @s {ns}.next_release_tick matches -1 run scoreboard players operation @s {ns}.next_release_tick = #release_tick {ns}.data
execute if score #release_tick {ns}.data < @s {ns}.next_release_tick run scoreboard players operation @s {ns}.next_release_tick = #release_tick {ns}.data
""")
	write_versioned_function("release/add_to_instance", f'$data modify storage {ns}:instances i$(instance_id).releases append value {{tick:$(tick),x:$(x),y:$(y),z:$(z),block:"$(block)",support_x:$(support_x),support_y:$(support_y),support_z:$(support_z)}}')

	## Loops
	write_versioned_function("playback/finish_walk_back", f"""
scoreboard players operation @s {ns}.group_start_tick = #tick {ns}.data
scoreboard players operation @s {ns}.keyframe_divisor = @s {ns}.keyframe_ticks
scoreboard players set @s {ns}.keyframe_progress 0
scoreboard players set @s {ns}.pose_flags -1
scoreboard players set @s {ns}.is_still_placed 0
function {functions}/playback/restart
scoreboard players set @s {ns}.play_state 1
function {functions}/playback/load_keyframe
function {functions}/playback/move
scoreboard players operation #restarted_group {ns}.data = @s {ns}.group_id
execute as @a[tag={ns}.armed] if score @s {ns}.waited_group = #restarted_group {ns}.data run function {functions}/challenge/launch
""")

	start: str = ""
	for name in DIMENSIONS:
		start += f"scoreboard players operation @s {ns}.keyframe_{name} = @s {ns}.start_{name}\n"
	write_versioned_function("playback/restart", f"""
execute if score @s {ns}.restore_mode matches 1.. run function {functions}/vault/restore
scoreboard players set @s {ns}.keyframe_index 0
{start}scoreboard players set @s {ns}.is_still 0
scoreboard players set @s {ns}.equipment_index 0
scoreboard players set @s {ns}.next_equipment_keyframe 0
execute if score @s {ns}.has_swings matches 1 run scoreboard players set @s {ns}.swing_index 0
execute if score @s {ns}.has_swings matches 1 run function {functions}/swing/load_next
execute if score @s {ns}.has_actions matches 1 run scoreboard players set @s {ns}.action_index 0
execute if score @s {ns}.has_actions matches 1 run function {functions}/action/load_next
""")

	write_versioned_function("playback/walk_back_tick", f"""
execute unless score @s {ns}.is_near matches 1 run return 0
scoreboard players add @s {ns}.keyframe_progress 1
execute if score @s {ns}.keyframe_progress >= @s {ns}.keyframe_divisor run return run function {functions}/playback/finish_walk_back
execute if function {functions}/playback/is_turn_to_move run function {functions}/playback/move
""")

	# Block placed from a macro argument: b (recorded block) or state (from block/store_state); strict = no block update
	for name, argument in (("set_recorded", "b"), ("set_state", "state")):
		write_versioned_function(f"block/{name}", f"$setblock ~ ~ ~ $({argument})")
		write_versioned_function(f"block/{name}_strict", f"$setblock ~ ~ ~ $({argument}) strict")

	write_versioned_function("playback/tick", f"""
execute if score @s {ns}.next_release_tick matches 0.. if score #game_time {ns}.data >= @s {ns}.next_release_tick run function {functions}/release/run_due
execute if score @s {ns}.play_state matches 2 run return run function {functions}/playback/walk_back_tick
execute unless score @s {ns}.play_state matches 1 run return 0
execute unless score @s {ns}.is_near matches 1 run return 0
scoreboard players operation @s {ns}.keyframe_progress += @s {ns}.speed
execute if score @s {ns}.keyframe_progress >= @s {ns}.keyframe_ticks run function {functions}/playback/advance_keyframe
execute unless score @s {ns}.play_state matches 1 run return 0
execute if score @s {ns}.has_swings matches 1 run function {functions}/swing/run_due
execute if score @s {ns}.has_actions matches 1 run function {functions}/action/run_due
execute if score @s {ns}.is_still matches 1 if score @s {ns}.is_still_placed matches 1 run return 0
execute if function {functions}/playback/is_turn_to_move run function {functions}/playback/move
""")

	write_versioned_function("playback/teleport", "$tp @s $(x) $(y) $(z) $(yaw) $(pitch)")

	write_versioned_function("playback/is_turn_to_move", f"""
# one entity in #move_every moves on each tick, in turns
scoreboard players operation #turn_phase {ns}.data = @s {ns}.instance_id
scoreboard players operation #turn_phase {ns}.data += #tick {ns}.data
scoreboard players operation #turn_phase {ns}.data %= #move_every {ns}.data
execute if score #turn_phase {ns}.data matches 0 run return 1
return fail
""")

	## Blocks used by an entity
	write_versioned_function("use/press_button", f"""
execute if score #block_powered {ns}.data matches 1 run return 0
scoreboard players set #restore_strict {ns}.data 0
function {functions}/vault/back_up_here
{set_property("powered", "true")}
function {functions}/block/store_state
function {functions}/block/set_state with storage {Storages(ns).block}
function {functions}/block/find_support
function {functions}/block/update_support_at with storage {playback} support_offset
playsound minecraft:block.stone_button.click_on block {SOUND_LISTENERS} ~ ~ ~
# released after the vanilla delay: 1 s for stone, 1.5 s for wood
{set_property("powered", "false")}
function {functions}/block/store_state
data modify storage {playback} release set value {{tick:0,x:0,y:0,z:0,block:"",support_x:0,support_y:0,support_z:0}}
function {functions}/block/mark_support with storage {playback} support_offset
data modify storage {playback} release.block set from storage {Storages(ns).block} state
scoreboard players operation #release_tick {ns}.data = #game_time {ns}.data
scoreboard players add #release_tick {ns}.data 20
execute if block ~ ~ ~ #minecraft:wooden_buttons run scoreboard players add #release_tick {ns}.data 10
execute store result storage {playback} release.tick int 1 run scoreboard players get #release_tick {ns}.data
execute summon minecraft:marker run function {functions}/release/store_position
function {functions}/release/add
""")

	target_open: str = f"""scoreboard players set #target_open {ns}.data 1
execute if score #block_open {ns}.data matches 1 run scoreboard players set #target_open {ns}.data 0"""
	write_versioned_function("use/toggle_door", f"""
# both halves are set without block updates, so that they do not copy each other
{target_open}
function {functions}/block/find_other_half
scoreboard players set #restore_strict {ns}.data 1
function {functions}/vault/back_up_here
function {functions}/use/set_open_state
function {functions}/block/store_state
function {functions}/block/set_state_strict with storage {Storages(ns).block}
execute if score #is_pair {ns}.data matches 1 run function {functions}/use/toggle_other_half
execute if score #target_open {ns}.data matches 1 run playsound minecraft:block.wooden_door.open block {SOUND_LISTENERS} ~ ~ ~
execute if score #target_open {ns}.data matches 0 run playsound minecraft:block.wooden_door.close block {SOUND_LISTENERS} ~ ~ ~
""")
	write_versioned_function("use/toggle_other_half", f"""
data modify storage {playback} pair_offset set value {{x:0,y:0,z:0}}
execute store result storage {playback} pair_offset.y int 1 run scoreboard players get #pair_y {ns}.data
function {functions}/use/toggle_other_half_at with storage {playback} pair_offset
""")
	write_versioned_function("use/toggle_other_half_at", f"$execute positioned ~ ~$(y) ~ run function {functions}/use/toggle_door_half")
	write_versioned_function("use/toggle_door_half", f"""
# block/read resets the flags: the open state of the first half is kept aside
scoreboard players operation #kept_target_open {ns}.data = #target_open {ns}.data
function {functions}/block/read
execute if data storage {Storages(ns).block} {{id:""}} run return 0
scoreboard players operation #target_open {ns}.data = #kept_target_open {ns}.data
scoreboard players set #restore_strict {ns}.data 1
function {functions}/vault/back_up_here
function {functions}/use/set_open_state
function {functions}/block/store_state
function {functions}/block/set_state_strict with storage {Storages(ns).block}
""")

	write_versioned_function("use/toggle_lever", f"""
scoreboard players set #restore_strict {ns}.data 0
function {functions}/vault/back_up_here
execute if score #block_powered {ns}.data matches 0 run {set_property("powered", "true")}
execute if score #block_powered {ns}.data matches 1 run {set_property("powered", "false")}
function {functions}/block/store_state
function {functions}/block/set_state with storage {Storages(ns).block}
function {functions}/block/find_support
function {functions}/block/update_support_at with storage {playback} support_offset
playsound minecraft:block.lever.click block {SOUND_LISTENERS} ~ ~ ~
""")

	sounds: str = ""
	for test, sound in (("if", "fence_gate"), ("unless", "wooden_trapdoor")):
		for opened, action in (("0", "open"), ("1", "close")):
			sounds += f"execute {test} block ~ ~ ~ #minecraft:fence_gates if score #block_open {ns}.data matches {opened} run playsound minecraft:block.{sound}.{action} block {SOUND_LISTENERS} ~ ~ ~\n"
	write_versioned_function("use/toggle_open", f"""
scoreboard players set #restore_strict {ns}.data 0
function {functions}/vault/back_up_here
{target_open}
function {functions}/use/set_open_state
function {functions}/block/store_state
function {functions}/block/set_state with storage {Storages(ns).block}
{sounds}""")

	write_versioned_function("use/set_open_state", f"""
execute if score #target_open {ns}.data matches 1 run {set_property("open", "true")}
execute if score #target_open {ns}.data matches 0 run {set_property("open", "false")}
""")

	write_versioned_function("playback/unregister", f"$data remove storage {ns}:instances i$(instance_id)")

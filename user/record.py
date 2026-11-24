""" Recording: per player state, keyframes, equipment, swings and actions (hits, use, place, break).

The state of a recording lives in <ns>:rec p.p<pid> (meta, d, chunks, e, s, eq, a, wb, c) and in per player objectives (r*).
"""
# Imports
from stewbeet import Mem, write_versioned_function

from .common import (
	ARMED,
	AXES,
	DIMENSIONS,
	PLAYBACK_PROFILES,
	SEPARATOR,
	Storages,
	build_sequence,
	check_group_alive,
	compound,
	copy,
	info,
	run,
	say,
	text,
	timer,
	wrap_yaw,
)

# Constants
STOP_ITEM: str = (
	'minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},'
	'minecraft:item_name={{text:"Arrêter l\'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]'
)
""" Item stopping a recording (right-click, detected by the <ns>.use statistic). Format it with ns. """

STOP_MATCH: str = "minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}]"
""" Item predicate matching the stop item. Format it with ns. """

STOP_ITEM_SLOTS: tuple[str, ...] = ("weapon.mainhand", *(f"hotbar.{index}" for index in range(9)), *(f"inventory.{index}" for index in range(27)))
""" Where the stop item goes, the first empty slot in this order. """

KEYFRAME_ROW: tuple[str, ...] = ("#delta_x", "#delta_y", "#delta_z", "#delta_yaw", "#delta_pitch", "#flags")
""" Scores written in a keyframe row [dx,dy,dz,dyaw,dpitch,flags], in this order. """

RECORDED_SLOTS: tuple[str, ...] = ("head", "chest", "legs", "feet", "mainhand", "offhand", "body", "saddle")
""" Equipment recorded on the player. """

STRIPPED_COMPONENTS: tuple[str, ...] = (
	"custom_name", "item_name", "lore", "written_book_content", "writable_book_content", "container", "bundle_contents", "custom_data",
)
""" Item components dropped from the recorded equipment: invisible on the entity, and they would break the exported command (quotes, size). """

CHALLENGE_FIELDS: tuple[str, ...] = ("id", "time", "group", "sync", "tp_back", "player_id", "group_id")
""" Challenge settings kept with a recording, in <ns>:rec p.p<pid>.c. """

STATISTICS: tuple[str, ...] = ("sneak_time", "swim_distance", "glide_distance")
""" Statistics compared with their value of the previous tick (objective previous_<statistic>). """

STATISTIC_FLAGS: tuple[tuple[str, int], ...] = (("swim_distance", 2), ("glide_distance", 4))
""" Statistic -> keyframe flag. Sneaking (flag 1) is apart: it also tells a stop click from a stop and walk back. """

COPY_HOVER: str = "Clique pour copier, puis colle dans un command block"


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	functions: str = f"{ns}:v{version}"
	api: str = f"#{ns}:v{version.split('.')[0]}"
	storage: Storages = Storages(ns)
	recording: str = storage.recording
	stop_match: str = STOP_MATCH.format(ns=ns)
	cursor: str = f"@e[type=minecraft:marker,tag={ns}.ray_cursor,limit=1]"
	remove_start_marker: str = f"""scoreboard players operation #player_id {ns}.data = @s {ns}.player_id
execute as @e[type=minecraft:text_display,tag={ns}.start_marker] if score @s {ns}.player_id = #player_id {ns}.data run kill @s"""

	block_kind: tuple[str, str] = (text("command block $(block_number) · ", "gray"), text("$(block_kind)", "$(block_color)"))

	def copy_block(value: str, suffix: str = "") -> str:
		""" Copy button of command block $(block_number) of an export (macro line). """
		parts: list[str] = [copy("[Copier $(block_number)]", value, COPY_HOVER, extra="bold:true"), text("  -> ", "gray"), *block_kind]
		if suffix:
			parts.append(text(suffix, "gray"))
		return "$" + say(*parts)

	write_versioned_function("record/abort", f"""
execute if entity @s[tag={ns}.recording] run function {api}/signals/on_record_stop
execute if entity @s[tag={ns}.recording] run tag @s add {ns}.was_recording
tag @s remove {ns}.recording
tag @s remove {ns}.armed
scoreboard players set @s {ns}.is_challenge 0
function {functions}/record/cleanup
execute if entity @s[tag={ns}.was_recording] run function {functions}/record/restore_world
tag @s remove {ns}.was_recording
function {functions}/record/store_player_id
function {functions}/record/drop_state with storage {storage.recorder}
""")

	row: str = ""
	for index, score in enumerate(KEYFRAME_ROW):
		row += f"execute unless score {score} {ns}.data matches 0 store result storage {recording} keyframe[{index}] int 1 run scoreboard players get {score} {ns}.data\n"
	write_versioned_function("record/append_keyframe", f"""
data modify storage {recording} keyframe set value [0,0,0,0,0,0]
{row}function {functions}/record/push_keyframe with storage {storage.recorder}
scoreboard players add @s {ns}.recorded_keyframes 1
scoreboard players add @s {ns}.chunk_keyframes 1
execute if score @s {ns}.chunk_keyframes matches 300.. run function {functions}/record/store_keyframe_chunk with storage {storage.recorder}
""")

	write_versioned_function("record/arm", f"""
execute store result score @s {ns}.waited_group run data get storage {storage.call} options.group_id
scoreboard players operation #waited_group {ns}.data = @s {ns}.waited_group
{check_group_alive(ns)}
execute if score #group_alive {ns}.data matches 0 run return run function {functions}/record/begin
execute unless score @s {ns}.player_id matches 1.. run function {functions}/player/new_id
function {functions}/record/store_player_id
function {functions}/record/save_armed_info with storage {storage.recorder}
scoreboard players set @s {ns}.armed_kind 1
tag @s add {ns}.armed
{info(ARMED)}
""")

	write_versioned_function("record/arm_with_nearest_group", f"""
# no group of that name near the player: the recording starts at once
scoreboard players set #found_group {ns}.data 0
$execute at @s as @e[tag={ns}.instance,tag={ns}.group.$(group),distance=..$(group_radius),sort=nearest,limit=1] run scoreboard players operation #found_group {ns}.data = @s {ns}.group_id
execute if score #found_group {ns}.data matches ..0 run return run function {functions}/record/begin
execute store result storage {storage.call} options.group_id int 1 run scoreboard players get #found_group {ns}.data
function {functions}/record/arm
""")

	write_versioned_function("record/load_armed_info", f"$data modify storage {recording} meta set from storage {ns}:in_progress players.p$(player_id).meta")
	write_versioned_function("record/save_armed_info", f"$data modify storage {ns}:in_progress players.p$(player_id).meta set from storage {recording} meta")

	write_versioned_function("record/note_hit", f"""
execute if score @s {ns}.last_hit_tick = @s {ns}.record_tick run return 0
scoreboard players operation @s {ns}.last_hit_tick = @s {ns}.record_tick
function {functions}/record/store_player_id
data modify storage {recording} event set value {{t:0,k:1}}
execute store result storage {recording} event.t int 1 run scoreboard players get @s {ns}.record_tick
function {functions}/record/push_event with storage {storage.recorder}
""")

	write_versioned_function("record/begin", f"""
function {functions}/record/init
{remove_start_marker}
execute at @s run summon minecraft:text_display ~ ~1.3 ~ {{Tags:["{ns}.start_marker","{ns}.new_start_marker","smithed.entity","smithed.strict"],text:{{text:"Départ",color:"green"}},billboard:"center"}}
scoreboard players operation @e[type=minecraft:text_display,tag={ns}.new_start_marker] {ns}.player_id = #player_id {ns}.data
tag @e[type=minecraft:text_display,tag={ns}.new_start_marker] remove {ns}.new_start_marker
{SEPARATOR}
{say(text("Enregistrement ", "green"), f'{{storage:"{recording}",nbt:"meta.name",color:"gold"}}', text(" démarré.", "green"))}
function {functions}/record/give_stop_item
{say(
	run("[■ STOP]", f"/function {api}/stop", "red", "Arrêter l'enregistrement", extra="bold:true"),
	text("   "),
	run("[STOP + retour au départ]", f"/function {api}/stop_loop", "red", "Arrêter et ramener au point de départ (boucle propre)"),
)}
{SEPARATOR}
function {api}/signals/on_record_start
""")

	write_versioned_function("record/note_break", f"""
function {functions}/record/snapshot_looked_cube
data modify storage {recording} event set value {{t:0,k:4,x:0,y:0,z:0}}
execute store result storage {recording} event.t int 1 run scoreboard players get @s {ns}.record_tick
function {functions}/record/store_hit_position
function {functions}/record/push_event with storage {storage.recorder}
""")

	write_versioned_function("record/cast_from_eyes", f"""
# the ray uses the event marker of the player (@s, at their position)
scoreboard players operation #player_id {ns}.data = @s {ns}.player_id
execute as @e[type=minecraft:marker,tag={ns}.ray_marker] if score @s {ns}.player_id = #player_id {ns}.data run tag @s add {ns}.ray_cursor
scoreboard players set #ray_steps {ns}.data 0
scoreboard players set #ray_hit {ns}.data 0
execute anchored eyes positioned ^ ^ ^ run function {functions}/record/ray_step
""")

	write_versioned_function("record/store_keyframe_chunk", f"""
$data modify storage {ns}:in_progress players.p$(player_id).chunks append from storage {ns}:in_progress players.p$(player_id).d
$data modify storage {ns}:in_progress players.p$(player_id).d set value []
scoreboard players set @s {ns}.chunk_keyframes 0
""")

	write_versioned_function("record/cleanup", f"""
{remove_start_marker}
clear @s {stop_match}
title @s actionbar {{text:""}}
function {functions}/record/kill_markers
""")

	write_versioned_function("record/on_stop_item_click", f"""
scoreboard players set @s {ns}.item_uses 0
execute if score #is_sneaking {ns}.data matches 1 run return run function {functions}/record/stop_with_walk_back
function {functions}/record/finish
""")

	write_versioned_function("record/stop_with_walk_back", f"""
function {functions}/record/prepare_walk_back
function {functions}/record/finish
""")

	# Walk back to the start point: the remaining delta spread over #walk_back_steps keyframes
	steps: str = ""
	remainders: str = ""
	for name in DIMENSIONS:
		steps += f"scoreboard players operation #delta_{name} {ns}.data = #remaining_{name} {ns}.data\n"
		steps += f"scoreboard players operation #delta_{name} {ns}.data /= #walk_back_steps {ns}.data\n"
		remainders += f"scoreboard players operation #remaining_{name} {ns}.data -= #delta_{name} {ns}.data\n"
	write_versioned_function("record/walk_back_step", f"""
{steps}{remainders}function {functions}/record/append_keyframe
scoreboard players remove #walk_back_steps {ns}.data 1
execute if score #walk_back_steps {ns}.data matches 1.. run function {functions}/record/walk_back_step
""")

	remaining: str = ""
	for name in DIMENSIONS:
		remaining += f"""scoreboard players operation #remaining_{name} {ns}.data = @s {ns}.record_start_{name}
scoreboard players operation #remaining_{name} {ns}.data -= @s {ns}.recorded_{name}
"""
		if name == "yaw":
			remaining += wrap_yaw(f"#remaining_yaw {ns}.data") + "\n"
	write_versioned_function("record/prepare_walk_back", f"""
function {functions}/record/store_player_id
scoreboard players set #flags {ns}.data 0
{remaining}scoreboard players set #walk_back_steps {ns}.data 10
function {functions}/record/walk_back_step
""")

	write_versioned_function("record/store_player_id", f"execute store result storage {storage.recorder} player_id int 1 run scoreboard players get @s {ns}.player_id")

	write_versioned_function("record/find_cube_corner", f"""
# #cube_index -> corner of a 3x3x3 cube walled by barriers, in vault chunk 1 (x 17..31): #cube_x #cube_y #cube_z
scoreboard players operation #cube_x {ns}.data = #cube_index {ns}.data
scoreboard players operation #cube_x {ns}.data %= #4 {ns}.data
scoreboard players operation #cube_x {ns}.data *= #4 {ns}.data
scoreboard players add #cube_x {ns}.data 17
scoreboard players operation #cube_z {ns}.data = #cube_index {ns}.data
scoreboard players operation #cube_z {ns}.data /= #4 {ns}.data
scoreboard players operation #cube_z {ns}.data %= #4 {ns}.data
scoreboard players operation #cube_z {ns}.data *= #4 {ns}.data
scoreboard players add #cube_z {ns}.data 1
scoreboard players operation #cube_y {ns}.data = #cube_index {ns}.data
scoreboard players operation #cube_y {ns}.data /= #16 {ns}.data
scoreboard players operation #cube_y {ns}.data *= #4 {ns}.data
scoreboard players remove #cube_y {ns}.data 63
""")

	hit_position: str = ""
	for index, axis in enumerate(AXES):
		hit_position += f"""execute store result score #hit_{axis} {ns}.data run data get entity {cursor} Pos[{index}]
scoreboard players operation #hit_{axis} {ns}.data -= @s {ns}.record_block_{axis}
execute store result storage {recording} event.{axis} int 1 run scoreboard players get #hit_{axis} {ns}.data
"""
	write_versioned_function("record/store_hit_position", f"""
# block hit by the ray, relative to the start block of the recording
{hit_position}""")

	write_versioned_function("record/drop_state", f"$data remove storage {ns}:in_progress players.p$(player_id)")

	removed_items: str = ""
	for item in ("stop", "menu"):
		for hand in ("mainhand", "offhand"):
			removed_items += f'execute if data storage {recording} equipment.{hand}.components."minecraft:custom_data"{{{ns}:{{{item}:1b}}}} run data remove storage {recording} equipment.{hand}\n'
	stripped: str = ""
	for slot in RECORDED_SLOTS:
		for component in STRIPPED_COMPONENTS:
			stripped += f'data remove storage {recording} equipment.{slot}.components."minecraft:{component}"\n'
	write_versioned_function("record/capture_equipment", f"""
data modify storage {recording} equipment set value {{}}
data modify storage {recording} equipment set from entity @s equipment
data modify storage {recording} equipment.mainhand set from entity @s SelectedItem
{removed_items}{stripped}function {functions}/record/note_equipment_change with storage {storage.recorder}
""")

	write_versioned_function("record/note_equipment_change", f"""
$execute store success score #equipment_changed {ns}.data run data modify storage {ns}:in_progress players.p$(player_id).equipment set from storage {recording} equipment
$execute if score #equipment_changed {ns}.data matches 1 run data modify storage {ns}:in_progress players.p$(player_id).e append value {{k:0,v:{{}}}}
$execute if score #equipment_changed {ns}.data matches 1 store result storage {ns}:in_progress players.p$(player_id).e[-1].k int 1 run scoreboard players get @s {ns}.recorded_keyframes
$execute if score #equipment_changed {ns}.data matches 1 run data modify storage {ns}:in_progress players.p$(player_id).e[-1].v set from storage {recording} equipment
""")

	write_versioned_function("record/push_event", f"$data modify storage {ns}:in_progress players.p$(player_id).a append from storage {recording} event")

	## Export: one copy button per command block
	export_info: str = ""
	for key in ("name", "keyframe_step", "yaw", "pitch", "start_x", "start_y", "start_z"):
		export_info += f"data modify storage {recording} export.{key} set from storage {recording} meta.{key}\n"
	write_versioned_function("record/export_block", f"""
data modify storage {recording} export set value {{}}
{export_info}data modify storage {recording} export.group set value ""
data modify storage {recording} export.group_radius set value 50
data modify storage {recording} export.group set from storage {recording} meta.group
data modify storage {recording} export.group_radius set from storage {recording} meta.group_radius
execute store result storage {recording} export.block_number int 1 run scoreboard players get #block_number {ns}.data
data modify storage {recording} export.block_kind set value "chaîne"
data modify storage {recording} export.block_color set value "green"
execute if score #block_number {ns}.data matches 1 run data modify storage {recording} export.block_kind set value "impulsion"
execute if score #block_number {ns}.data matches 1 run data modify storage {recording} export.block_color set value "gold"
scoreboard players set #is_first {ns}.data 0
execute if score #block_number {ns}.data matches 1 run scoreboard players set #is_first {ns}.data 1
execute store result storage {recording} export.is_first int 1 run scoreboard players get #is_first {ns}.data
scoreboard players set #is_events_block {ns}.data 0
execute if score #is_split {ns}.data matches 1 if score #block_number {ns}.data = #chunk_count {ns}.data run scoreboard players set #is_events_block {ns}.data 1
execute if score #is_events_block {ns}.data matches 1 run function {functions}/record/export_events_part
execute if score #is_events_block {ns}.data matches 0 if score #block_number {ns}.data < #block_count {ns}.data run function {functions}/record/export_keyframes_part
execute if score #is_events_block {ns}.data matches 0 if score #block_number {ns}.data >= #block_count {ns}.data run function {functions}/record/export_last_part
scoreboard players add #block_number {ns}.data 1
execute if score #block_number {ns}.data <= #block_count {ns}.data run function {functions}/record/export_block
""")

	write_versioned_function("record/export_keyframes_part", f"""
data modify storage {recording} export.keyframes set from storage {recording} chunks[0]
data remove storage {recording} chunks[0]
function {functions}/record/show_part_button with storage {recording} export
""")

	event_lists: dict[str, str] = {"equipment": "e", "swings": "s", "actions": "a"}
	events_part: str = ""
	empty_events: str = ""
	unsplit_events: str = ""
	for export_key, key in event_lists.items():
		events_part += f"data modify storage {recording} export.{export_key} set from storage {recording} {key}\n"
		empty_events += f"data modify storage {recording} export.{export_key} set value []\n"
		unsplit_events += f"execute if score #is_split {ns}.data matches 0 run data modify storage {recording} export.{export_key} set from storage {recording} {key}\n"
	write_versioned_function("record/export_events_part", f"""
{events_part}function {functions}/record/show_events_button with storage {recording} export
""")
	write_versioned_function("record/show_events_button", copy_block(
		f"function {api}/part {{with:{{f:$(is_first),d:[],e:$(equipment),s:$(swings),a:$(actions)}}}}", " · équipement et gestes",
	))

	write_versioned_function("record/export_last_part", f"""
data modify storage {recording} export.keyframes set from storage {recording} chunks[0]
data remove storage {recording} chunks[0]
{empty_events}{unsplit_events}function {functions}/record/show_playback_button with storage {recording} export
""")

	recorded: dict[str, str] = {
		"name": '"$(name)"', "pos": '"$(start_x) $(start_y) $(start_z)"', "group": '"$(group)"', "group_radius": "$(group_radius)",
		"data": "{f:$(is_first),n:$(keyframe_step),y:$(yaw),p:$(pitch),d:$(keyframes),e:$(equipment),s:$(swings),a:$(actions)}",
	}
	playback_buttons: str = "$" + say(*block_kind, text(" · lecture, choisis l'entité qui rejoue :", "gray")) + "\n"
	for profile in PLAYBACK_PROFILES:
		command: str = f"function {api}/play {{with:{compound({**profile.fields(), **recorded})}}}"
		button: str = copy(f"[Copier $(block_number) · {profile.label}]", command, COPY_HOVER, extra="bold:true")
		playback_buttons += "$" + (say(button, text(f"  {profile.hint}", "gray")) if profile.hint else say(button)) + "\n"
	write_versioned_function("record/show_playback_button", playback_buttons)
	write_versioned_function("record/show_part_button", copy_block(f"function {api}/part {{with:{{f:$(is_first),d:$(keyframes)}}}}"))

	write_versioned_function("record/export", f"""
{SEPARATOR}
{say(text("Séquence ", "green"), f'{{storage:"{recording}",nbt:"meta.name",color:"gold"}}', text(" prête à copier :", "green"))}
execute store result score #chunk_count {ns}.data run data get storage {recording} chunks
scoreboard players set #equipment_count {ns}.data 0
scoreboard players set #swing_count {ns}.data 0
execute store result score #equipment_count {ns}.data run data get storage {recording} e
execute store result score #swing_count {ns}.data run data get storage {recording} s
scoreboard players set #action_count {ns}.data 0
execute store result score #action_count {ns}.data run data get storage {recording} a
# many events get a command block of their own, so the playback command stays under the size limit
scoreboard players set #is_split {ns}.data 0
execute if score #action_count {ns}.data matches 30.. run scoreboard players set #is_split {ns}.data 1
execute if score #equipment_count {ns}.data matches 4.. run scoreboard players set #is_split {ns}.data 1
execute if score #swing_count {ns}.data matches 150.. run scoreboard players set #is_split {ns}.data 1
scoreboard players operation #block_count {ns}.data = #chunk_count {ns}.data
scoreboard players operation #block_count {ns}.data += #is_split {ns}.data
scoreboard players set #block_number {ns}.data 1
function {functions}/record/export_block
execute if score #block_count {ns}.data matches 1 run {say(text("Colle-la dans un command block ", "green"), text("impulsion", "gold"), text(".", "green"))}
execute if score #block_count {ns}.data matches 2.. run {say(
	text("Colle les blocs dans l'ordre : le 1 en ", "green"), text("impulsion", "gold"), text(", les suivants en ", "green"),
	text("chaîne", "green", "underlined:true"), text(" (toujours actif).", "green"),
)}
{SEPARATOR}
""")

	write_versioned_function("record/finish", f"""
tag @s remove {ns}.recording
function {functions}/record/restore_world
function {functions}/record/pull_state
function {functions}/record/drop_state with storage {storage.recorder}
function {functions}/record/cleanup
function {api}/signals/on_record_stop
execute if score #keyframe_count {ns}.data matches 0 run return run {info("Séquence vide, rien à exporter.", "red")}
execute if score #chunk_keyframes {ns}.data matches 1.. run data modify storage {recording} chunks append from storage {recording} d
function {functions}/record/save
function {functions}/record/export
""")

	tries: str = ""
	for slot in STOP_ITEM_SLOTS:
		tries += f'execute unless items entity @s {slot} * run return run function {functions}/record/give_stop_item_in {{slot:"{slot}"}}\n'
	write_versioned_function("record/give_stop_item", f"""
# in the main hand when it is empty, else in the first empty slot
{tries}{info("Inventaire plein : pas d'objet d'arrêt, utilise le bouton rouge.")}
""")

	write_versioned_function("record/give_stop_item_in", f"""
$item replace entity @s $(slot) with {STOP_ITEM.format(ns=ns)}
execute if items entity @s weapon.mainhand {stop_match} run return run {info("Barrière en main : clic droit = stop.")}
{info("Barrière ajoutée à ton inventaire : prends-la en main, clic droit = stop.")}
""")

	write_versioned_function("record/show_hud", f"""
execute if score @s {ns}.is_challenge matches 1 run return run function {functions}/challenge/show_hud
scoreboard players operation #seconds {ns}.data = @s {ns}.record_tick
{timer(ns, f'{text("● ", "red")},{text("ENREGISTREMENT EN COURS ", "white", "bold:true")}', 'color:"yellow"')}
""")

	player_being_read: str = f"{ns}.position_being_read"
	read_player_position: str = f"""# read on a marker in the place of the player: reading the player itself would serialize its whole inventory, 5 times
tag @s add {player_being_read}
execute at @s summon minecraft:marker run function {functions}/record/read_player_position
tag @s remove {player_being_read}"""
	previous: str = ""
	for name in DIMENSIONS:
		previous += f"scoreboard players operation @s {ns}.recorded_{name} = #current_{name} {ns}.data\n"
	start_copies: str = ""
	for axis in AXES:
		start_copies += f"execute store result storage {recording} meta.start_{axis} double 0.001 run scoreboard players get @s {ns}.recorded_{axis}\n"
	origin: str = ""
	for name in DIMENSIONS:
		origin += f"scoreboard players operation @s {ns}.record_start_{name} = @s {ns}.recorded_{name}\n"
	write_versioned_function("record/init", f"""
# starts a recording for @s; {recording} meta = {{name, n}} set by the caller
execute unless score @s {ns}.player_id matches 1.. run function {functions}/player/new_id
function {functions}/record/store_player_id
tag @s add {ns}.recording
scoreboard players set @s {ns}.is_challenge 0
execute store result score @s {ns}.keyframe_step run data get storage {recording} meta.keyframe_step
scoreboard players set @s {ns}.chunk_keyframes 0
scoreboard players set @s {ns}.recorded_keyframes 0
scoreboard players set @s {ns}.ticks_since_keyframe 0
scoreboard players set @s {ns}.record_tick 0
scoreboard players set @s {ns}.last_swing_tick -1
{read_player_position}
{previous}{origin}execute store result storage {recording} meta.yaw int 1 run scoreboard players get @s {ns}.recorded_yaw
execute store result storage {recording} meta.pitch int 1 run scoreboard players get @s {ns}.recorded_pitch
{start_copies}function {functions}/record/init_state with storage {storage.recorder}
function {functions}/record/init_actions
scoreboard players set @s {ns}.item_uses 0
function {functions}/record/capture_equipment
""")

	start_block: str = ""
	for index, axis in enumerate(AXES):
		start_block += f"execute store result score @s {ns}.record_block_{axis} run data get entity @s Pos[{index}]\n"
	statistics: str = ""
	for statistic in STATISTICS:
		statistics += f"scoreboard players add @s {ns}.{statistic} 0\n"
		statistics += f"scoreboard players operation @s {ns}.previous_{statistic} = @s {ns}.{statistic}\n"
	markers: str = ""
	for role in ("look_marker", "ray_marker"):
		markers += f'execute at @s run summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.recorder_marker","{ns}.{role}","{ns}.new_recorder_marker","smithed.entity","smithed.strict"]}}\n'
	write_versioned_function("record/init_actions", f"""
# markers of the look ray, start block, and the vault cube (chunk 2) holding what the player looks at
scoreboard players operation #player_id {ns}.data = @s {ns}.player_id
function {functions}/record/kill_markers
{markers}scoreboard players operation @e[type=minecraft:marker,tag={ns}.new_recorder_marker] {ns}.player_id = #player_id {ns}.data
tag @e[type=minecraft:marker,tag={ns}.new_recorder_marker] remove {ns}.new_recorder_marker
{start_block}scoreboard players set @s {ns}.is_looking_at_block 0
scoreboard players set @s {ns}.has_pending_use 0
scoreboard players set @s {ns}.has_placed 0
scoreboard players set @s {ns}.last_hit_tick -1
scoreboard players operation #cube_index {ns}.data = @s {ns}.player_id
scoreboard players operation #cube_index {ns}.data %= #1536 {ns}.data
function {functions}/record/find_cube_corner
scoreboard players operation @s {ns}.look_cube_x = #cube_x {ns}.data
scoreboard players add @s {ns}.look_cube_x 16
scoreboard players operation @s {ns}.look_cube_y = #cube_y {ns}.data
scoreboard players operation @s {ns}.look_cube_z = #cube_z {ns}.data
{statistics}""")

	new_lists: str = ""
	for key in ("d", "chunks", "e", "s", "a", "world_backups"):
		new_lists += f"$data modify storage {ns}:in_progress players.p$(player_id).{key} set value []\n"
	write_versioned_function("record/init_state", f"""
$data modify storage {ns}:in_progress players.p$(player_id).meta set from storage {recording} meta
$data remove storage {ns}:in_progress players.p$(player_id).equipment
{new_lists}""")

	current: str = ""
	for index, axis in enumerate(AXES):
		current += f"execute store result score #current_{axis} {ns}.data run data get entity @s Pos[{index}] 1000\n"
	deltas: str = ""
	for name in DIMENSIONS:
		deltas += f"""scoreboard players operation #delta_{name} {ns}.data = #current_{name} {ns}.data
scoreboard players operation #delta_{name} {ns}.data -= @s {ns}.recorded_{name}
"""
		if name == "yaw":
			deltas += wrap_yaw(f"#delta_yaw {ns}.data") + "\n"
	write_versioned_function("record/capture_keyframe", f"""
scoreboard players set @s {ns}.ticks_since_keyframe 0
{read_player_position}
{deltas}{previous}function {functions}/record/append_keyframe
""")
	write_versioned_function("record/read_player_position", f"""
tp @s @a[tag={player_being_read},limit=1]
{current}execute store result score #current_yaw {ns}.data run data get entity @s Rotation[0] 100
execute store result score #current_pitch {ns}.data run data get entity @s Rotation[1] 100
kill @s
""")

	write_versioned_function("record/kill_markers", f"execute as @e[type=minecraft:marker,tag={ns}.recorder_marker] if score @s {ns}.player_id = #player_id {ns}.data run kill @s")

	write_versioned_function("record/launch_armed", f"""
tag @s remove {ns}.armed
title @s actionbar {{text:""}}
function {functions}/record/store_player_id
function {functions}/record/load_armed_info with storage {storage.recorder}
function {functions}/record/begin
""")

	looked_cube: str = ""
	for axis in AXES:
		looked_cube += f"execute store result storage {recording} looked_cube.{axis} int 1 run scoreboard players get @s {ns}.look_cube_{axis}\n"
	write_versioned_function("record/copy_looked_cube", f"""
{looked_cube}function {functions}/record/copy_looked_cube_to with storage {recording} looked_cube
""")
	write_versioned_function("record/copy_looked_cube_to", f"$execute at {cursor} run clone ~-1 ~-1 ~-1 ~1 ~1 ~1 to {ns}:vault $(x) $(y) $(z) strict")

	write_versioned_function("record/look", f"""
# a block looked at last tick that is now air was broken by the player
scoreboard players operation #player_id {ns}.data = @s {ns}.player_id
execute as @e[type=minecraft:marker,tag={ns}.look_marker] if score @s {ns}.player_id = #player_id {ns}.data run tag @s add {ns}.ray_cursor
scoreboard players set #has_broken {ns}.data 0
execute if score @s {ns}.is_looking_at_block matches 1 at {cursor} if block ~ ~ ~ #minecraft:air run scoreboard players set #has_broken {ns}.data 1
execute if score #has_broken {ns}.data matches 1 run function {functions}/record/note_break
scoreboard players set @s {ns}.is_looking_at_block 0
scoreboard players set #ray_steps {ns}.data 0
scoreboard players set #ray_hit {ns}.data 0
execute anchored eyes positioned ^ ^ ^ run function {functions}/record/ray_step
execute if score #ray_hit {ns}.data matches 1 run scoreboard players set @s {ns}.is_looking_at_block 1
execute if score #ray_hit {ns}.data matches 1 if data storage {ns}:config are_cubes_ready run function {functions}/record/copy_looked_cube
tag @e[type=minecraft:marker,tag={ns}.ray_cursor] remove {ns}.ray_cursor
""")

	write_versioned_function("record/show_start_marker", """
particle minecraft:happy_villager ~ ~-1.2 ~ 0.35 0 0.35 0 6 normal @a[distance=..48]
particle minecraft:end_rod ~ ~-1.2 ~ 0 0.8 0 0.01 2 normal @a[distance=..48]
""")

	write_versioned_function("record/note_place", f"""
scoreboard players set @s {ns}.has_placed 1
function {functions}/record/store_player_id
function {functions}/record/snapshot_looked_cube
function {functions}/record/cast_from_eyes
execute if score #ray_hit {ns}.data matches 1 at {cursor} run function {functions}/record/note_placed_block
tag @e[type=minecraft:marker,tag={ns}.ray_cursor] remove {ns}.ray_cursor
""")

	write_versioned_function("record/note_placed_block", f"""
function {functions}/block/read
execute if data storage {storage.block} {{id:""}} run return 0
data modify storage {recording} event set value {{t:0,k:3,x:0,y:0,z:0,b:""}}
execute store result storage {recording} event.t int 1 run scoreboard players get @s {ns}.record_tick
function {functions}/record/store_hit_position
function {functions}/block/store_state
data modify storage {recording} event.b set from storage {storage.block} state
function {functions}/block/find_other_half
execute if score #is_pair {ns}.data matches 1 run function {functions}/record/note_other_half
function {functions}/record/push_event with storage {storage.recorder}
""")

	other_half: str = ""
	for axis in AXES:
		other_half += f"""scoreboard players operation #hit_{axis} {ns}.data += #pair_{axis} {ns}.data
execute store result storage {recording} event.p.{axis} int 1 run scoreboard players get #hit_{axis} {ns}.data
execute store result storage {recording} pair_offset.{axis} int 1 run scoreboard players get #pair_{axis} {ns}.data
"""
	write_versioned_function("record/note_other_half", f"""
data modify storage {recording} event.p set value {{x:0,y:0,z:0,b:""}}
{other_half}function {functions}/record/read_other_half_at with storage {recording} pair_offset
""")

	write_versioned_function("record/read_other_half_at", f"$execute positioned ~$(x) ~$(y) ~$(z) run function {functions}/record/read_other_half")

	write_versioned_function("record/read_other_half", f"""
function {functions}/block/read
execute if data storage {storage.block} {{id:""}} run return run data remove storage {recording} event.p
function {functions}/block/store_state
data modify storage {recording} event.p.b set from storage {storage.block} state
""")

	write_versioned_function("record/pull_state", f"""
# copies the recording of the player to {recording} (and {storage.challenge} for a challenge) before the export
function {functions}/record/store_player_id
data modify storage {recording} a set value []
function {functions}/record/pull_state_of with storage {storage.recorder}
scoreboard players operation #keyframe_count {ns}.data = @s {ns}.recorded_keyframes
scoreboard players operation #chunk_keyframes {ns}.data = @s {ns}.chunk_keyframes
""")

	pulls: str = ""
	for key in ("meta", "d", "chunks", "e", "s", "a"):
		pulls += f"$data modify storage {recording} {key} set from storage {ns}:in_progress players.p$(player_id).{key}\n"
	for key in CHALLENGE_FIELDS:
		pulls += f"$data modify storage {storage.challenge} {key} set from storage {ns}:in_progress players.p$(player_id).challenge.{key}\n"
	write_versioned_function("record/pull_state_of", pulls)

	write_versioned_function("record/push_keyframe", f"$data modify storage {ns}:in_progress players.p$(player_id).d append from storage {recording} keyframe")

	write_versioned_function("record/ray_step", f"""
# steps of 0.2 block, 5 blocks at most; the {ns}.ray_cursor marker goes to the block hit
scoreboard players add #ray_steps {ns}.data 1
execute unless block ~ ~ ~ #{ns}:ray_pass run return run function {functions}/record/ray_hit
execute if score #ray_steps {ns}.data matches 26.. run return 0
execute positioned ^ ^ ^0.2 run function {functions}/record/ray_step
""")

	write_versioned_function("record/ray_hit", f"""
execute align xyz run tp {cursor} ~ ~ ~
scoreboard players set #ray_hit {ns}.data 1
""")

	write_versioned_function("record/on_rejoin", f"""
# a recording is cancelled when its player comes back after a disconnection
scoreboard players set @s {ns}.left_game 0
execute unless entity @s[tag={ns}.recording] unless entity @s[tag={ns}.armed] run return 0
function {functions}/record/abort
{info("Ton enregistrement a été annulé (déconnexion).", "yellow")}
""")

	saved: str = ""
	for key in ("meta", "chunks", "e", "s", "a"):
		saved += f"data modify storage {recording} saved.{key} set from storage {recording} {key}\n"
	write_versioned_function("record/save", f"""
# kept in the world: played by its name, exported again from the menu
data modify storage {recording} saved set value {{}}
{saved}data modify storage {recording} keyframes set value []
data modify storage {recording} keyframes append from storage {recording} chunks[][]
{build_sequence(ns)}
data remove storage {recording} keyframes
function {functions}/record/save_named with storage {recording} meta
execute store result storage {ns}:library names[-1].player_id int 1 run scoreboard players get @s {ns}.player_id
""")

	write_versioned_function("record/save_named", f"""
$data modify storage {ns}:library recordings.$(name) set from storage {recording} saved
$data modify storage {ns}:data seqs.$(name) set from storage {recording} sequence
$data remove storage {ns}:library names[{{name:"$(name)"}}]
$data modify storage {ns}:library names append value {{name:"$(name)",player_id:0}}
""")

	look_cube: str = ""
	for axis in AXES:
		look_cube += f"""execute store result storage {recording} snapshot.look_{axis} int 1 run scoreboard players get @s {ns}.look_cube_{axis}
scoreboard players operation #cube_index {ns}.data = @s {ns}.look_cube_{axis}
execute store result storage {recording} snapshot.look_end_{axis} int 1 run scoreboard players add #cube_index {ns}.data 2
"""
	write_versioned_function("record/snapshot_looked_cube", f"""
# the player has just broken, placed or used a block: keep the state before, the cube copied last tick
execute unless data storage {ns}:config are_cubes_ready run return 0
execute unless score @s {ns}.is_looking_at_block matches 1 run return 0
data modify storage {recording} snapshot set value {{}}
scoreboard players operation #player_id {ns}.data = @s {ns}.player_id
execute as @e[type=minecraft:marker,tag={ns}.look_marker] if score @s {ns}.player_id = #player_id {ns}.data run function {functions}/record/snapshot_position
execute unless data storage {recording} snapshot.x run return 0
execute store result storage {recording} snapshot.player_id int 1 run scoreboard players get @s {ns}.player_id
# the first copy of a cube during this recording is the one to restore
scoreboard players set #has_snapshot {ns}.data 0
function {functions}/record/has_snapshot with storage {recording} snapshot
execute if score #has_snapshot {ns}.data matches 1 run return 0
execute if data storage {ns}:config free_cube_slots[0] run function {functions}/record/reuse_snapshot_slot
execute unless data storage {recording} snapshot.cube_x run function {functions}/record/allocate_snapshot_slot
{look_cube}function {functions}/record/store_snapshot with storage {recording} snapshot
""")

	write_versioned_function("record/store_snapshot", f"""
$execute in {ns}:vault run clone $(look_x) $(look_y) $(look_z) $(look_end_x) $(look_end_y) $(look_end_z) $(cube_x) $(cube_y) $(cube_z) strict
$data modify storage {ns}:in_progress players.p$(player_id).world_backups append value {{cube_x:$(cube_x),cube_y:$(cube_y),cube_z:$(cube_z),cube_end_x:$(cube_end_x),cube_end_y:$(cube_end_y),cube_end_z:$(cube_end_z),x:$(x),y:$(y),z:$(z)}}
""")

	write_versioned_function("record/has_snapshot", f"$execute if data storage {ns}:in_progress players.p$(player_id).world_backups[{{x:$(x),y:$(y),z:$(z)}}] run scoreboard players set #has_snapshot {ns}.data 1")

	slot_corner: str = ""
	for axis in AXES:
		slot_corner += f"execute store result storage {recording} snapshot.cube_{axis} int 1 run scoreboard players get #cube_{axis} {ns}.data\n"
	for axis in AXES:
		slot_corner += f"execute store result storage {recording} snapshot.cube_end_{axis} int 1 run scoreboard players add #cube_{axis} {ns}.data 2\n"
	write_versioned_function("record/allocate_snapshot_slot", f"""
scoreboard players operation #cube_index {ns}.data = #next_cube_slot {ns}.data
function {functions}/record/find_cube_corner
scoreboard players add #next_cube_slot {ns}.data 1
execute if score #next_cube_slot {ns}.data matches 1536.. run scoreboard players set #next_cube_slot {ns}.data 0
{slot_corner}""")

	snapshot_position: str = ""
	for index, axis in enumerate(AXES):
		snapshot_position += f"""execute store result score #snapshot_{axis} {ns}.data run data get entity @s Pos[{index}]
execute store result storage {recording} snapshot.{axis} int 1 run scoreboard players remove #snapshot_{axis} {ns}.data 1
"""
	write_versioned_function("record/snapshot_position", snapshot_position)

	reused: str = ""
	for key in ("cube_x", "cube_y", "cube_z", "cube_end_x", "cube_end_y", "cube_end_z"):
		reused += f"data modify storage {recording} snapshot.{key} set from storage {ns}:config free_cube_slots[-1].{key}\n"
	write_versioned_function("record/reuse_snapshot_slot", f"""
{reused}data remove storage {ns}:config free_cube_slots[-1]
""")

	write_versioned_function("record/note_swing", f"""
execute if score @s {ns}.last_swing_tick = @s {ns}.record_tick run return 0
scoreboard players operation @s {ns}.last_swing_tick = @s {ns}.record_tick
function {functions}/record/store_player_id
function {functions}/record/push_swing with storage {storage.recorder}
""")

	write_versioned_function("record/push_swing", f"""
$data modify storage {ns}:in_progress players.p$(player_id).s append value 0
$execute store result storage {ns}:in_progress players.p$(player_id).s[-1] int 1 run scoreboard players get @s {ns}.record_tick
""")

	flags: str = ""
	for statistic, flag in STATISTIC_FLAGS:
		flags += f"execute if score @s {ns}.{statistic} > @s {ns}.previous_{statistic} run scoreboard players add #flags {ns}.data {flag}\n"
	for statistic in STATISTICS:
		flags += f"scoreboard players operation @s {ns}.previous_{statistic} = @s {ns}.{statistic}\n"
	periodic: str = ""
	for period, target in ((10, "show_hud"), (20, "capture_equipment")):
		periodic += f"""scoreboard players operation #tick_mod {ns}.data = @s {ns}.record_tick
scoreboard players operation #tick_mod {ns}.data %= #{period} {ns}.data
execute if score #tick_mod {ns}.data matches 0 run function {functions}/record/{target}
"""
	write_versioned_function("record/tick", f"""
function {functions}/record/store_player_id
execute if score @s {ns}.has_pending_use matches 1 run function {functions}/record/push_use
scoreboard players set @s {ns}.has_placed 0
function {functions}/record/look
scoreboard players set #flags {ns}.data 0
scoreboard players set #is_sneaking {ns}.data 0
execute if score @s {ns}.sneak_time > @s {ns}.previous_sneak_time run scoreboard players set #is_sneaking {ns}.data 1
execute if score #is_sneaking {ns}.data matches 1 run scoreboard players add #flags {ns}.data 1
{flags}execute unless score @s {ns}.is_challenge matches 1 if score @s {ns}.item_uses matches 1.. if items entity @s weapon.* {stop_match} run return run function {functions}/record/on_stop_item_click
scoreboard players set @s {ns}.item_uses 0
scoreboard players add @s {ns}.record_tick 1
execute if score @s {ns}.is_challenge matches 1 if score @s {ns}.record_tick >= @s {ns}.challenge_ticks run return run function {functions}/challenge/end
{periodic}scoreboard players add @s {ns}.ticks_since_keyframe 1
execute if score @s {ns}.ticks_since_keyframe >= @s {ns}.keyframe_step run function {functions}/record/capture_keyframe
""")

	write_versioned_function("record/note_use", f"""
function {functions}/record/cast_from_eyes
execute if score #ray_hit {ns}.data matches 1 at {cursor} if block ~ ~ ~ #{ns}:interactive run function {functions}/record/note_used_block
tag @e[type=minecraft:marker,tag={ns}.ray_cursor] remove {ns}.ray_cursor
""")

	used_block: str = ""
	for index, axis in enumerate(AXES):
		used_block += f"execute store result score @s {ns}.used_block_{axis} run data get entity {cursor} Pos[{index}]\n"
	write_versioned_function("record/note_used_block", f"""
# pushed next tick by record/push_use, unless the use placed a block
{used_block}scoreboard players operation @s {ns}.used_tick = @s {ns}.record_tick
scoreboard players set @s {ns}.has_pending_use 1
""")

	use_position: str = ""
	for axis in AXES:
		use_position += f"""scoreboard players operation #hit_{axis} {ns}.data = @s {ns}.used_block_{axis}
scoreboard players operation #hit_{axis} {ns}.data -= @s {ns}.record_block_{axis}
execute store result storage {recording} event.{axis} int 1 run scoreboard players get #hit_{axis} {ns}.data
"""
	write_versioned_function("record/push_use", f"""
scoreboard players set @s {ns}.has_pending_use 0
execute if score @s {ns}.has_placed matches 1 run return 0
function {functions}/record/snapshot_looked_cube
data modify storage {recording} event set value {{t:0,k:2,x:0,y:0,z:0}}
execute store result storage {recording} event.t int 1 run scoreboard players get @s {ns}.used_tick
{use_position}function {functions}/record/push_event with storage {storage.recorder}
""")

	## The world put back as it was before the recording, from the cube copies
	write_versioned_function("record/pull_world_backups", f"""
$data modify storage {recording} world_backups set from storage {ns}:in_progress players.p$(player_id).world_backups
$data modify storage {ns}:in_progress players.p$(player_id).world_backups set value []
""")

	write_versioned_function("record/restore_next_backup", f"""
function {functions}/record/restore_backup with storage {recording} world_backups[-1]
data remove storage {recording} world_backups[-1]
execute if data storage {recording} world_backups[0] run function {functions}/record/restore_next_backup
""")

	write_versioned_function("record/restore_backup", f"""
$clone from {ns}:vault $(cube_x) $(cube_y) $(cube_z) $(cube_end_x) $(cube_end_y) $(cube_end_z) $(x) $(y) $(z)
$execute in {ns}:vault run fill $(cube_x) $(cube_y) $(cube_z) $(cube_end_x) $(cube_end_y) $(cube_end_z) minecraft:barrier strict
$data modify storage {ns}:config free_cube_slots append value {{cube_x:$(cube_x),cube_y:$(cube_y),cube_z:$(cube_z),cube_end_x:$(cube_end_x),cube_end_y:$(cube_end_y),cube_end_z:$(cube_end_z)}}
""")

	write_versioned_function("record/restore_world", f"""
function {functions}/record/store_player_id
data modify storage {recording} world_backups set value []
function {functions}/record/pull_world_backups with storage {storage.recorder}
execute if data storage {recording} world_backups[0] at @s run function {functions}/record/restore_next_backup
""")

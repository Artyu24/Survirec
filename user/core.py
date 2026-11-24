""" Management functions called by the entry points: names, sequences, kills, ranges, groups, reset, start and stop. """
# Imports
import string

from stewbeet import Mem, write_versioned_function

from .common import NOT_RECORDING, Storages, info, kill_tagged, say, text

# Constants
NAME_CHARACTERS: str = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_"
""" Characters allowed in a name (name, id, group, tag), checked one by one. """

IMPORT_LISTS: dict[str, str] = {"keyframes": "d", "equipment": "e", "swings": "s", "actions": "a"}
""" Lists of <ns>:import collecting the parts of a long sequence -> key of a part (and of the sequence). """

STOPS: dict[str, str] = {"stop": "record/finish", "stop_loop": "record/stop_with_walk_back"}
""" Stop entry point -> how the recording of a player ends. """


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	functions: str = f"{ns}:v{version}"
	api: str = f"#{ns}:v{version.split('.')[0]}"
	storage: Storages = Storages(ns)
	call: str = storage.call

	write_versioned_function("record/abort_from_call", f"""
# a player cancels their own recording, a command block or the console cancels them all
execute if entity @s[type=minecraft:player] unless entity @s[tag={ns}.recording] unless entity @s[tag={ns}.armed] run return run {info(NOT_RECORDING, "red")}
execute if entity @s[type=minecraft:player] run function {functions}/record/abort
execute if entity @s[type=minecraft:player] run return run {info("Enregistrement annulé.", "yellow")}
execute as @a[tag={ns}.recording] run function {functions}/record/abort
execute as @a[tag={ns}.armed] run function {functions}/record/abort
""")

	write_versioned_function("spawn/from_options", f"""
data modify storage {call} spawn set from storage {call} options
$execute positioned $(pos) run function {functions}/spawn/summon
""")

	write_versioned_function("name/report_invalid", say(
		text("Nom invalide : ", "red"), text("lettres, chiffres et _ uniquement", "gold", "bold:true"), text(" (1 à 32 caractères).", "red"),
	))

	write_versioned_function("challenge/start_from_call", f"""
$data merge storage {storage.challenge_call} {{id:"$(id)",time:$(time),group:"$(group)",sync:$(sync),tp_back:$(tp_back)}}
function {functions}/challenge/start
""")

	def score(holder: str, objective: str, color: str = "aqua", extra: str = "") -> str:
		return f'{{score:{{name:"{holder}",objective:"{ns}.{objective}"}},color:"{color}"{"," + extra if extra else ""}}}'
	write_versioned_function("debug/show", f"""
tag @s add {ns}.debug_viewer
{say(text("diagnostic", "gold", "bold:true"))}
execute store result score #debug_recording {ns}.data if entity @a[tag={ns}.recording]
execute store result score #debug_armed {ns}.data if entity @a[tag={ns}.armed]
tellraw @s [{text("  Enregistrements : ", "gray")},{score("#debug_recording", "data")},{text("   armés : ", "gray")},{score("#debug_armed", "data")}]
execute as @a[tag={ns}.recording] run tellraw @a[tag={ns}.debug_viewer] [{text("  ● ", "red")},{{selector:"@s",color:"white"}},{text("  ", "gray")},{score("@s", "record_tick")},{text(" ticks, ", "gray")},{score("@s", "recorded_keyframes")},{text(" keyframes", "gray")}]
execute as @a[tag={ns}.armed] run tellraw @a[tag={ns}.debug_viewer] [{text("  ⏳ ", "gold")},{{selector:"@s",color:"white"}},{text("  attend le groupe ", "gray")},{score("@s", "waited_group")}]
execute store result score #debug_entities {ns}.data if entity @e[tag={ns}.instance]
tellraw @s [{text("  Entités animées : ", "gray")},{score("#debug_entities", "data")}]
execute as @e[tag={ns}.instance] run tellraw @a[tag={ns}.debug_viewer] [{text("  • groupe ", "gray")},{score("@s", "group_id", "gold", "bold:true")},{text("  en lecture ", "gray")},{score("@s", "play_state", "gold", "bold:true")},{text("  ", "gray")},{{nbt:"Tags",entity:"@s",color:"aqua"}}]
tag @s remove {ns}.debug_viewer
""")

	pull_saved: str = ""
	for key in ("meta", "chunks", "e", "s"):
		pull_saved += f"$data modify storage {storage.recording} {key} set from storage {ns}:library recordings.$(name).{key}\n"
	write_versioned_function("record/export_saved", f"""
$execute unless data storage {ns}:library recordings.$(name) run return run {say(text("Aucun enregistrement nommé ", "red"), text("$(name)", "gold"), text(".", "red"))}
{pull_saved}data modify storage {storage.recording} a set value []
$data modify storage {storage.recording} a set from storage {ns}:library recordings.$(name).a
function {functions}/record/export
""")

	write_versioned_function("sequence/forget", f"""
$data remove storage {ns}:data seqs.$(name)
$data remove storage {ns}:library recordings.$(name)
$data remove storage {ns}:library names[{{name:"$(name)"}}]
${say(text("Séquence ", "green"), text("$(name)", "gold"), text(" supprimée.", "green"))}
""")

	write_versioned_function("group/restart_from_call", f"""
# radius 0 restarts every scene of that name, any other radius the nearest one only
$execute if data storage {call} options{{radius:0}} as @e[tag={ns}.instance,tag={ns}.group.$(group)] run scoreboard players set @s {ns}.restart_pending 1
scoreboard players set #found_group {ns}.data 0
$execute unless data storage {call} options{{radius:0}} as @e[tag={ns}.instance,tag={ns}.group.$(group),distance=..$(radius),sort=nearest,limit=1] run scoreboard players operation #found_group {ns}.data = @s {ns}.group_id
execute if score #found_group {ns}.data matches 1.. as @e[tag={ns}.instance] if score @s {ns}.group_id = #found_group {ns}.data run scoreboard players set @s {ns}.restart_pending 1
function {functions}/group/restart_pending
""")

	## Long sequences, one part per command block of the chain
	new_lists: str = ""
	missing_lists: str = ""
	appends: str = ""
	for list_name, key in IMPORT_LISTS.items():
		new_lists += f"execute if data storage {call} part{{f:1}} run data modify storage {storage.import_parts} {list_name} set value []\n"
		missing_lists += f"execute unless data storage {storage.import_parts} {list_name} run data modify storage {storage.import_parts} {list_name} set value []\n"
		appends += f"data modify storage {storage.import_parts} {list_name} append from storage {call} part.{key}[]\n"
	write_versioned_function("sequence/collect_part", f"""
# {call} part = {{f,d,e,s,a}}, f:1 on the first part of the chain
{new_lists}{missing_lists}{appends}""")

	copies: str = ""
	cleanup: str = ""
	for key in "nyp":
		copies += f"data modify storage {call} sequence.{key} set from storage {call} options.data.{key}\n"
	for list_name, key in IMPORT_LISTS.items():
		copies += f"data modify storage {call} sequence.{key} set from storage {storage.import_parts} {list_name}\n"
		cleanup += f"data remove storage {storage.import_parts} {list_name}\n"
	write_versioned_function("sequence/import", f"""
data modify storage {call} part set from storage {call} options.data
function {functions}/sequence/collect_part
data modify storage {call} sequence set value {{}}
{copies}function {functions}/sequence/store with storage {call} options
{cleanup}""")
	write_versioned_function("sequence/store", f"$data modify storage {ns}:data seqs.$(name) set from storage {call} sequence")

	## Removing playback entities
	write_versioned_function("kill/by_tag", kill_tagged(ns, functions, f"{ns}.tag.$(tag)"))
	write_versioned_function("kill/by_name", kill_tagged(ns, functions, f"{ns}.sequence.$(name)"))
	write_versioned_function("kill/all", f"""
scoreboard players set #restore_on_kill {ns}.data 1
execute as @e[tag={ns}.entity] run function {functions}/playback/delete
scoreboard players set #restore_on_kill {ns}.data 0
execute if data storage {ns}:config are_blocks_ready in {ns}:vault if loaded 0 0 0 run function {functions}/vault/wipe
""")

	## An entity only moves while a player is within its range
	write_versioned_function("range/check_global", f"$execute as @e[tag={ns}.instance,tag=!{ns}.has_own_range] at @s store success score @s {ns}.is_near if entity @a[distance=..$(range)]")
	write_versioned_function("range/check_own", f"""
execute store result storage {storage.playback} range int 1 run scoreboard players get @s {ns}.own_range
function {functions}/range/check_own_distance with storage {storage.playback}
""")
	write_versioned_function("range/check_own_distance", f"$execute store success score @s {ns}.is_near if entity @a[distance=..$(range)]")
	write_versioned_function("range/set_global", f"$data modify storage {ns}:config range set value $(r)")

	write_versioned_function("group/prepare_local", f"""
# the group id is resolved when the entity appears, from the entities of the same group nearby
data modify storage {call} options.group_id set value -1
data modify storage {call} options.group_loop set from storage {call} options.loop
data modify storage {call} options.loop set value 0
""")

	write_versioned_function("reset", f"""
execute as @a[tag={ns}.recording] run function {api}/signals/on_record_stop
execute as @a[tag={ns}.recording] at @s run function {functions}/record/restore_world
tag @a remove {ns}.recording
tag @a remove {ns}.armed
execute as @a run function {functions}/record/cleanup
scoreboard players set @a {ns}.is_challenge 0
kill @e[type=minecraft:text_display,tag={ns}.start_marker]
kill @e[type=minecraft:marker,tag={ns}.recorder_marker]
execute as @e[type=minecraft:marker,tag={ns}.pulse_marker] at @s run function {functions}/pulse/stop
scoreboard players set #pulse_count {ns}.data 0
data remove storage {ns}:in_progress players
{info("État réinitialisé.")}
""")

	## Recordings started and stopped by the entry points
	write_versioned_function("record/start_from_call", f"""
execute unless entity @s[type=minecraft:player] run return fail
execute if entity @s[tag={ns}.recording] run return run {say(text("Tu es déjà en train d'enregistrer (", "red"), text(f"{api}/stop", "gold"), text(").", "red"))}
execute if entity @s[tag={ns}.armed] run return run {say(text("Ton enregistrement est déjà armé (", "red"), text(f"{api}/abort", "gold"), text(" pour l'annuler).", "red"))}
$scoreboard players set #keyframe_step {ns}.data $(every)
execute unless score #keyframe_step {ns}.data matches 1..100 run return run {info("every doit être entre 1 et 100.", "red")}
$data modify storage {storage.recording} meta set value {{name:"$(name)",keyframe_step:$(every),group:"$(group)",group_radius:$(group_radius)}}
execute if data storage {call} options{{group:""}} run return run function {functions}/record/begin
function {functions}/record/arm_with_nearest_group with storage {call} options
""")

	for name, ending in STOPS.items():
		write_versioned_function(f"record/{name}_from_call", f"""
# a player stops their own recording, a command block or the console stops them all
execute if entity @s[type=minecraft:player,tag={ns}.recording] run return run function {functions}/record/{name}_player
execute if entity @s[type=minecraft:player] run return run {info(NOT_RECORDING, "red")}
execute as @a[tag={ns}.recording] run function {functions}/record/{name}_player
""")
		write_versioned_function(f"record/{name}_player", f"""
# a challenge is not stopped by hand, it is cancelled
execute if score @s {ns}.is_challenge matches 1 run return run function {functions}/record/abort
function {functions}/{ending}
""")

	## Names: letters, digits and _, 1 to 32 characters
	write_versioned_function("name/validate", f"""
# checks {storage.name_check} text, #is_valid_name 1 or 0
scoreboard players set #is_valid_name {ns}.data 1
scoreboard players set #name_length {ns}.data 0
execute store result score #name_length {ns}.data run data get storage {storage.name_check} text
execute unless score #name_length {ns}.data matches 1..32 run return run scoreboard players set #is_valid_name {ns}.data 0
scoreboard players set #character_index {ns}.data 0
function {functions}/name/check_next_character
""")

	character_tests: str = ""
	for character in NAME_CHARACTERS:
		character_tests += f'execute if data storage {storage.name_check} {{character:"{character}"}} run scoreboard players set #is_allowed_character {ns}.data 1\n'
	write_versioned_function("name/check_character", f"""
data remove storage {storage.name_check} character
$data modify storage {storage.name_check} character set string storage {storage.name_check} text $(start) $(end)
scoreboard players set #is_allowed_character {ns}.data 0
{character_tests}execute if score #is_allowed_character {ns}.data matches 0 run scoreboard players set #is_valid_name {ns}.data 0
""")

	write_versioned_function("name/check_next_character", f"""
execute store result storage {storage.name_check} bounds.start int 1 run scoreboard players get #character_index {ns}.data
scoreboard players add #character_index {ns}.data 1
execute store result storage {storage.name_check} bounds.end int 1 run scoreboard players get #character_index {ns}.data
function {functions}/name/check_character with storage {storage.name_check} bounds
execute if score #is_valid_name {ns}.data matches 1 if score #character_index {ns}.data < #name_length {ns}.data run function {functions}/name/check_next_character
""")

	write_versioned_function("name/check_optional", f"""
# an empty optional field is valid
$execute unless data storage {call} options{{$(field):""}} run function {functions}/name/check_required with storage {storage.name_check} request
""")

	write_versioned_function("name/check_required", f"""
data remove storage {storage.name_check} text
$data modify storage {storage.name_check} text set from storage {call} options.$(field)
function {functions}/name/validate
execute if score #is_valid_name {ns}.data matches 0 run scoreboard players set #has_bad_name {ns}.data 1
""")

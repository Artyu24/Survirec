""" Challenges: timed recordings that spawn a double of the player when the time is up. """
# Imports
from stewbeet import Mem, write_versioned_function

from .common import ARMED, DIMENSIONS, TELEPORT_SCALES, Storages, build_sequence, check_group_alive, info, kill_tagged, say, text, timer

# Constants
CHALLENGE_INPUT: tuple[str, ...] = ("id", "time", "group", "sync", "tp_back")
""" Fields of #survirec:v1/challenge, copied to <ns>:challenge when the challenge starts. """


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	functions: str = f"{ns}:v{version}"
	api: str = f"#{ns}:v{version.split('.')[0]}"
	storage: Storages = Storages(ns)
	challenge: str = storage.challenge
	recording: str = storage.recording

	write_versioned_function("challenge/arm", f"""
execute store result score @s {ns}.waited_group run data get storage {challenge} group_id
scoreboard players operation #waited_group {ns}.data = @s {ns}.waited_group
{check_group_alive(ns)}
execute if score #group_alive {ns}.data matches 0 run return run function {functions}/challenge/launch
tag @s add {ns}.armed
{info(ARMED)}
""")

	write_versioned_function("challenge/check_armed", f"""
title @s actionbar [{text("⏳ ", "gold")},{text("EN ATTENTE DU PROCHAIN CYCLE ", "white", "bold:true")},{text("du groupe", "gray")}]
scoreboard players operation #waited_group {ns}.data = @s {ns}.waited_group
{check_group_alive(ns)}
execute if score #group_alive {ns}.data matches 0 run function {functions}/challenge/launch
""")

	write_versioned_function("challenge/begin", f"""
function {functions}/record/init
scoreboard players set @s {ns}.is_challenge 1
function {api}/signals/on_record_start
""")

	write_versioned_function("challenge/end", f"""
tag @s remove {ns}.recording
scoreboard players set @s {ns}.is_challenge 0
function {functions}/record/restore_world
function {functions}/record/pull_state
function {functions}/record/drop_state with storage {storage.recorder}
title @s actionbar {{text:""}}
scoreboard players operation #player_id {ns}.data = @s {ns}.player_id
function {functions}/record/kill_markers
data modify storage {recording} keyframes set value []
data modify storage {recording} keyframes append from storage {recording} chunks[][]
data modify storage {recording} keyframes append from storage {recording} d[]
{build_sequence(ns)}
function {functions}/challenge/store_sequence with storage {challenge}
data modify storage {storage.call} profile set value {{}}
data modify storage {storage.call} profile.id set from entity @s UUID
scoreboard players set #group_alive {ns}.data 0
function {functions}/challenge/spawn_double with storage {challenge}
execute if score #group_alive {ns}.data matches 1 run {info("Terminé ! Ton double démarrera quand les autres auront fini leur cycle.")}
execute unless score #group_alive {ns}.data matches 1 run {say(text("Terminé ! Ton double rejoue ton parcours en boucle. ", "green"), text("Recommence en réactivant l'épreuve.", "gold"))}
execute store result score #teleport_back {ns}.data run data get storage {challenge} tp_back
execute if score #teleport_back {ns}.data matches 1 run function {functions}/challenge/teleport_back
function {api}/signals/on_record_stop
""")

	write_versioned_function("challenge/resolve_group", f"""
# one group id per player and group name
$execute unless data storage {ns}:challenge_groups ids.p$(player_id)_$(group) run function {functions}/challenge/new_group_id with storage {challenge}
$execute store result score #group {ns}.data run data get storage {ns}:challenge_groups ids.p$(player_id)_$(group)
""")

	write_versioned_function("challenge/show_hud", f"""
scoreboard players operation #seconds {ns}.data = @s {ns}.challenge_ticks
scoreboard players operation #seconds {ns}.data -= @s {ns}.record_tick
scoreboard players add #seconds {ns}.data 19
{timer(ns, f'{text("● ", "red")},{text("ENREGISTREMENT  ", "white", "bold:true")},{text("Temps restant : ", "gray")}', 'color:"gold",bold:true')}
""")

	write_versioned_function("challenge/launch", f"""
execute if score @s {ns}.armed_kind matches 1 run return run function {functions}/record/launch_armed
tag @s remove {ns}.armed
title @s actionbar {{text:""}}
data modify storage {recording} meta set value {{name:"ch",keyframe_step:4}}
function {functions}/challenge/begin
scoreboard players operation #challenge_seconds {ns}.data = @s {ns}.challenge_ticks
scoreboard players operation #challenge_seconds {ns}.data /= #20 {ns}.data
{say(text("Épreuve ! Tu as ", "green"), f'{{score:{{name:"#challenge_seconds",objective:"{ns}.data"}},color:"gold",bold:true}}', text(" secondes.", "green"))}
""")

	write_versioned_function("challenge/new_group_id", f"""
scoreboard players add #next_group_id {ns}.data 1
$execute store result storage {ns}:challenge_groups ids.p$(player_id)_$(group) int 1 run scoreboard players get #next_group_id {ns}.data
""")

	write_versioned_function("player/new_id", f"""
scoreboard players add #next_player_id {ns}.data 1
scoreboard players operation @s {ns}.player_id = #next_player_id {ns}.data
""")

	write_versioned_function("challenge/spawn_double", f"""
$data modify storage {storage.call} spawn set value {{name:"ch_$(id)_$(player_id)",entity:"minecraft:mannequin",range:0,size:1,loop:0,group_id:$(group_id),speed:100,delay:0,tag:"sv_$(id)_$(player_id)",pose:"",skin:"",texture:"",head:"",chest:"",legs:"",feet:"",mainhand:"",offhand:""}}
function {functions}/challenge/spawn_at_start with storage {recording} meta
""")

	write_versioned_function("challenge/kill_previous_double", kill_tagged(ns, functions, f"{ns}.tag.sv_$(id)_$(player_id)"))
	write_versioned_function("challenge/save_settings", f"$data modify storage {ns}:in_progress players.p$(player_id).challenge set from storage {challenge}")
	write_versioned_function("challenge/spawn_at_start", f"$execute positioned $(start_x) $(start_y) $(start_z) run function {functions}/spawn/summon")

	copies: str = ""
	for key in CHALLENGE_INPUT:
		copies += f"data modify storage {challenge} {key} set from storage {storage.challenge_call} {key}\n"
	write_versioned_function("challenge/start", f"""
execute unless entity @s[type=minecraft:player] run return fail
# a pressure plate fires again and again: ignored without a message
execute if entity @s[tag={ns}.recording] run return 0
execute if entity @s[tag={ns}.armed] run return 0
{copies}execute store result score @s {ns}.challenge_ticks run data get storage {challenge} time 20
execute unless score @s {ns}.challenge_ticks matches 20.. run return run tellraw @s {text("[Survirec] time doit être d'au moins 1 seconde.", "red")}
execute unless score @s {ns}.player_id matches 1.. run function {functions}/player/new_id
execute store result storage {challenge} player_id int 1 run scoreboard players get @s {ns}.player_id
function {functions}/challenge/resolve_group with storage {challenge}
execute store result storage {challenge} group_id int 1 run scoreboard players get #group {ns}.data
function {functions}/challenge/kill_previous_double with storage {challenge}
function {functions}/group/check
function {functions}/record/store_player_id
function {functions}/challenge/save_settings with storage {storage.recorder}
scoreboard players set @s {ns}.armed_kind 0
execute store result score #is_synced {ns}.data run data get storage {challenge} sync
execute if score #is_synced {ns}.data matches 1 run return run function {functions}/challenge/arm
function {functions}/challenge/launch
""")

	write_versioned_function("challenge/store_sequence", f"$data modify storage {ns}:data seqs.ch_$(id)_$(player_id) set from storage {recording} sequence")

	start_point: str = ""
	for name in DIMENSIONS:
		start_point += f"execute store result storage {recording} start_point.{name} double {TELEPORT_SCALES[name]} run scoreboard players get @s {ns}.record_start_{name}\n"
	write_versioned_function("challenge/teleport_back", f"""
{start_point}function {functions}/playback/teleport with storage {recording} start_point
""")

""" Challenges: timed recordings that spawn a double of the player. """
# Imports
from stewbeet import Mem, write_versioned_function


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	major: str = version.split(".")[0]

	write_versioned_function("challenge/arm", f"""
execute store result score @s {ns}.rwg run data get storage {ns}:c gid
scoreboard players operation #wg {ns}.data = @s {ns}.rwg
scoreboard players set #alive {ns}.data 0
execute as @e[tag={ns}.m] if score @s {ns}.grp = #wg {ns}.data run scoreboard players set #alive {ns}.data 1
execute if score #alive {ns}.data matches 0 run return run function {ns}:v{version}/challenge/launch
tag @s add {ns}.armed
tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Enregistrement armé : il démarre au prochain cycle du groupe.",color:"green"}}]
""")

	write_versioned_function("challenge/armchk", f"""
title @s actionbar [{{text:"⏳ ",color:"gold"}},{{text:"EN ATTENTE DU PROCHAIN CYCLE ",color:"white",bold:true}},{{text:"du groupe",color:"gray"}}]
scoreboard players operation #wg {ns}.data = @s {ns}.rwg
scoreboard players set #alive {ns}.data 0
execute as @e[tag={ns}.m] if score @s {ns}.grp = #wg {ns}.data run scoreboard players set #alive {ns}.data 1
execute if score #alive {ns}.data matches 0 run function {ns}:v{version}/challenge/launch
""")

	write_versioned_function("challenge/begin", f"""
function {ns}:v{version}/record/init
scoreboard players set @s {ns}.rchal 1
function #{ns}:v{major}/signals/on_record_start
""")

	write_versioned_function("challenge/end", f"""
tag @s remove {ns}.on
scoreboard players set @s {ns}.rchal 0
function {ns}:v{version}/record/wrestore
function {ns}:v{version}/record/pull
function {ns}:v{version}/record/drop with storage {ns}:ctx
title @s actionbar {{text:""}}
scoreboard players operation #me {ns}.data = @s {ns}.pid
function {ns}:v{version}/record/killmk
data modify storage {ns}:tmp all set value []
data modify storage {ns}:tmp all append from storage {ns}:tmp chunks[][]
data modify storage {ns}:tmp all append from storage {ns}:tmp d[]
data modify storage {ns}:tmp seq set value {{}}
data modify storage {ns}:tmp seq.n set from storage {ns}:tmp meta.n
data modify storage {ns}:tmp seq.y set from storage {ns}:tmp meta.y
data modify storage {ns}:tmp seq.p set from storage {ns}:tmp meta.p
data modify storage {ns}:tmp seq.e set from storage {ns}:tmp e
data modify storage {ns}:tmp seq.s set from storage {ns}:tmp s
data modify storage {ns}:tmp seq.a set from storage {ns}:tmp a
data modify storage {ns}:tmp seq.d set from storage {ns}:tmp all
function {ns}:v{version}/challenge/store with storage {ns}:c
data modify storage {ns}:in prof set value {{}}
data modify storage {ns}:in prof.id set from entity @s UUID
scoreboard players set #alive {ns}.data 0
function {ns}:v{version}/challenge/play with storage {ns}:c
execute if score #alive {ns}.data matches 1 run tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Terminé ! Ton double démarrera quand les autres auront fini leur cycle.",color:"green"}}]
execute unless score #alive {ns}.data matches 1 run tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Terminé ! Ton double rejoue ton parcours en boucle. ",color:"green"}},{{text:"Recommence en réactivant l'épreuve.",color:"gold"}}]
execute store result score #tpb {ns}.data run data get storage {ns}:c tp_back
execute if score #tpb {ns}.data matches 1 run function {ns}:v{version}/challenge/tpback
function #{ns}:v{major}/signals/on_record_stop
""")

	write_versioned_function("challenge/gid", f"""
$execute unless data storage {ns}:grp map.p$(pid)_$(group) run function {ns}:v{version}/challenge/newgid with storage {ns}:c
$execute store result score #g {ns}.data run data get storage {ns}:grp map.p$(pid)_$(group)
""")

	write_versioned_function("challenge/hud", f"""
scoreboard players operation #s {ns}.data = @s {ns}.rcdur
scoreboard players operation #s {ns}.data -= @s {ns}.rtime
scoreboard players add #s {ns}.data 19
scoreboard players operation #s {ns}.data /= #20 {ns}.data
scoreboard players operation #mn {ns}.data = #s {ns}.data
scoreboard players operation #mn {ns}.data /= #60 {ns}.data
scoreboard players operation #s {ns}.data %= #60 {ns}.data
execute if score #s {ns}.data matches 10.. run title @s actionbar [{{text:"● ",color:"red"}},{{text:"ENREGISTREMENT  ",color:"white",bold:true}},{{text:"Temps restant : ",color:"gray"}},{{score:{{name:"#mn",objective:"{ns}.data"}},color:"gold",bold:true}},{{text:":",color:"gold",bold:true}},{{score:{{name:"#s",objective:"{ns}.data"}},color:"gold",bold:true}}]
execute if score #s {ns}.data matches ..9 run title @s actionbar [{{text:"● ",color:"red"}},{{text:"ENREGISTREMENT  ",color:"white",bold:true}},{{text:"Temps restant : ",color:"gray"}},{{score:{{name:"#mn",objective:"{ns}.data"}},color:"gold",bold:true}},{{text:":0",color:"gold",bold:true}},{{score:{{name:"#s",objective:"{ns}.data"}},color:"gold",bold:true}}]
""")

	write_versioned_function("challenge/launch", f"""
execute if score @s {ns}.ratype matches 1 run return run function {ns}:v{version}/record/launch
tag @s remove {ns}.armed
title @s actionbar {{text:""}}
data modify storage {ns}:tmp meta set value {{name:"ch",n:4}}
function {ns}:v{version}/challenge/begin
scoreboard players operation #csec {ns}.data = @s {ns}.rcdur
scoreboard players operation #csec {ns}.data /= #20 {ns}.data
tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Épreuve ! Tu as ",color:"green"}},{{score:{{name:"#csec",objective:"{ns}.data"}},color:"gold",bold:true}},{{text:" secondes.",color:"green"}}]
""")

	write_versioned_function("challenge/newgid", f"""
scoreboard players add #gid {ns}.data 1
$execute store result storage {ns}:grp map.p$(pid)_$(group) int 1 run scoreboard players get #gid {ns}.data
""")

	write_versioned_function("challenge/newpid", f"""
scoreboard players add #pid {ns}.data 1
scoreboard players operation @s {ns}.pid = #pid {ns}.data
""")

	write_versioned_function("challenge/play", f"""
$data modify storage {ns}:in a set value {{name:"ch_$(id)_$(pid)",entity:"minecraft:mannequin",range:0,size:1,loop:0,grp:$(gid),speed:100,offset:0,tag:"sv_$(id)_$(pid)",pose:"",skin:"",texture:"",head:"",chest:"",legs:"",feet:"",mainhand:"",offhand:""}}
function {ns}:v{version}/challenge/spawn with storage {ns}:tmp meta
""")

	write_versioned_function("challenge/prekill", f"""
scoreboard players set #kres {ns}.data 1
$execute as @e[tag={ns}.t.sv_$(id)_$(pid)] run function {ns}:v{version}/playback/delete
scoreboard players set #kres {ns}.data 0
""")

	write_versioned_function("challenge/save", f"""
$data modify storage {ns}:rec p.p$(pid).c set from storage {ns}:c
""")

	write_versioned_function("challenge/spawn", f"""
$execute positioned $(sx) $(sy) $(sz) run function {ns}:v{version}/spawn/spawn
""")

	write_versioned_function("challenge/start", f"""
execute unless entity @s[type=minecraft:player] run return fail
# une plaque de pression redéclenche en continu : on ignore sans message
execute if entity @s[tag={ns}.on] run return 0
execute if entity @s[tag={ns}.armed] run return 0
data modify storage {ns}:c id set from storage {ns}:cin id
data modify storage {ns}:c time set from storage {ns}:cin time
data modify storage {ns}:c group set from storage {ns}:cin group
data modify storage {ns}:c sync set from storage {ns}:cin sync
data modify storage {ns}:c tp_back set from storage {ns}:cin tp_back
execute store result score @s {ns}.rcdur run data get storage {ns}:c time 20
execute unless score @s {ns}.rcdur matches 20.. run return run tellraw @s {{text:"[Survirec] time doit être d'au moins 1 seconde.",color:"red"}}
execute unless score @s {ns}.pid matches 1.. run function {ns}:v{version}/challenge/newpid
execute store result storage {ns}:c pid int 1 run scoreboard players get @s {ns}.pid
function {ns}:v{version}/challenge/gid with storage {ns}:c
execute store result storage {ns}:c gid int 1 run scoreboard players get #g {ns}.data
function {ns}:v{version}/challenge/prekill with storage {ns}:c
function {ns}:v{version}/playback/grpcheck
function {ns}:v{version}/record/ctx
function {ns}:v{version}/challenge/save with storage {ns}:ctx
scoreboard players set @s {ns}.ratype 0
execute store result score #sync {ns}.data run data get storage {ns}:c sync
execute if score #sync {ns}.data matches 1 run return run function {ns}:v{version}/challenge/arm
function {ns}:v{version}/challenge/launch
""")

	write_versioned_function("challenge/store", f"""
$data modify storage {ns}:data seqs.ch_$(id)_$(pid) set from storage {ns}:tmp seq
""")

	write_versioned_function("challenge/tpback", f"""
execute store result storage {ns}:tmp tpb.x double 0.001 run scoreboard players get @s {ns}.rox
execute store result storage {ns}:tmp tpb.y double 0.001 run scoreboard players get @s {ns}.roy
execute store result storage {ns}:tmp tpb.z double 0.001 run scoreboard players get @s {ns}.roz
execute store result storage {ns}:tmp tpb.yaw double 0.01 run scoreboard players get @s {ns}.royw
execute store result storage {ns}:tmp tpb.pitch double 0.01 run scoreboard players get @s {ns}.ropt
function {ns}:v{version}/challenge/tpback2 with storage {ns}:tmp tpb
""")

	write_versioned_function("challenge/tpback2", f"""
$tp @s $(x) $(y) $(z) $(yaw) $(pitch)
""")

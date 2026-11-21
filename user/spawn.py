""" Spawning a playback entity from the merged playback fields. """
# Imports
from stewbeet import Mem, write_versioned_function


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	major: str = version.split(".")[0]

	write_versioned_function("spawn/cbpos", f"""
execute store result storage {ns}:in cfg.cbx int 1 run data get entity @s Pos[0]
execute store result storage {ns}:in cfg.cby int 1 run data get entity @s Pos[1]
execute store result storage {ns}:in cfg.cbz int 1 run data get entity @s Pos[2]
kill @s
""")

	write_versioned_function("spawn/cfg", f"""
$execute store result score @s {ns}.n100 run data get storage {ns}:data seqs.$(name).n 100
$execute store result score @s {ns}.yw0 run data get storage {ns}:data seqs.$(name).y
$execute store result score @s {ns}.pt0 run data get storage {ns}:data seqs.$(name).p
$execute store result score @s {ns}.len run data get storage {ns}:data seqs.$(name).d
$execute store result score @s {ns}.hs run data get storage {ns}:data seqs.$(name).s
$execute store result score @s {ns}.ha run data get storage {ns}:data seqs.$(name).a
""")

	write_versioned_function("spawn/gjoin", f"""
# rejoint le groupe du même nom le plus proche (à moins de gr blocs), sinon en crée un nouveau
scoreboard players set #found {ns}.data 0
$execute as @e[tag={ns}.m,tag={ns}.g.$(group),distance=..$(gr),sort=nearest,limit=1] run scoreboard players operation #found {ns}.data = @s {ns}.grp
execute if score #found {ns}.data matches ..0 run scoreboard players add #gid {ns}.data 1
execute if score #found {ns}.data matches ..0 run scoreboard players operation #found {ns}.data = #gid {ns}.data
scoreboard players operation @s {ns}.grp = #found {ns}.data
$tag @s add {ns}.g.$(group)
""")

	write_versioned_function("spawn/init", f"""
tag @s remove {ns}.new
scoreboard players operation @s {ns}.id = #id {ns}.data
execute store result score @s {ns}.ax run data get entity @s Pos[0] 1000
execute store result score @s {ns}.ay run data get entity @s Pos[1] 1000
execute store result score @s {ns}.az run data get entity @s Pos[2] 1000
execute store result storage {ns}:in a.id int 1 run scoreboard players get @s {ns}.id
function {ns}:v{version}/spawn/reg with storage {ns}:in a
function {ns}:v{version}/spawn/ntag with storage {ns}:in a
execute unless data storage {ns}:in a{{tag:""}} run function {ns}:v{version}/spawn/utag with storage {ns}:in a
scoreboard players set @s {ns}.grp 0
execute if data storage {ns}:in a.grp store result score @s {ns}.grp run data get storage {ns}:in a.grp
execute if score @s {ns}.grp matches -1 run function {ns}:v{version}/spawn/gjoin with storage {ns}:in a
scoreboard players set @s {ns}.gloop 1
scoreboard players set @s {ns}.gs -1
execute if data storage {ns}:in a.gl store result score @s {ns}.gloop run data get storage {ns}:in a.gl
scoreboard players set @s {ns}.rs 0
scoreboard players set @s {ns}.hs 0
scoreboard players set @s {ns}.ha 0
function {ns}:v{version}/spawn/cfg with storage {ns}:in a
execute if score @s {ns}.hs matches 1.. run scoreboard players set @s {ns}.hs 1
execute if score @s {ns}.ha matches 1.. run scoreboard players set @s {ns}.ha 1
scoreboard players set @s {ns}.rst 1
execute if data storage {ns}:in a.restore store result score @s {ns}.rst run data get storage {ns}:in a.restore
scoreboard players set @s {ns}.hitp 0
execute if data storage {ns}:in a.hitp store result score @s {ns}.hitp run data get storage {ns}:in a.hitp
scoreboard players set @s {ns}.rlt -1
scoreboard players set @s {ns}.rsb 0
execute if data storage {ns}:in a.rsb store result score @s {ns}.rsb run data get storage {ns}:in a.rsb
execute if score @s {ns}.rsb matches 1 store result score @s {ns}.cbx run data get storage {ns}:in a.cbx
execute if score @s {ns}.rsb matches 1 store result score @s {ns}.cby run data get storage {ns}:in a.cby
execute if score @s {ns}.rsb matches 1 store result score @s {ns}.cbz run data get storage {ns}:in a.cbz
execute store result score @s {ns}.bbx run data get entity @s Pos[0]
execute store result score @s {ns}.bby run data get entity @s Pos[1]
execute store result score @s {ns}.bbz run data get entity @s Pos[2]
function {ns}:v{version}/spawn/size with storage {ns}:in a
execute unless score @s {ns}.n100 matches 1.. run scoreboard players set @s {ns}.len 0
scoreboard players operation @s {ns}.dv = @s {ns}.n100
execute store result score @s {ns}.lp run data get storage {ns}:in a.loop
execute store result score @s {ns}.spd run data get storage {ns}:in a.speed
scoreboard players operation @s {ns}.bx = @s {ns}.ax
scoreboard players operation @s {ns}.by = @s {ns}.ay
scoreboard players operation @s {ns}.bz = @s {ns}.az
scoreboard players operation @s {ns}.byw = @s {ns}.yw0
scoreboard players operation @s {ns}.bpt = @s {ns}.pt0
scoreboard players set @s {ns}.st 0
scoreboard players set @s {ns}.pl 0
scoreboard players set @s {ns}.near 1
scoreboard players set @s {ns}.rng 0
execute store result score @s {ns}.rng run data get storage {ns}:in a.range
execute if score @s {ns}.rng matches 1.. run tag @s add {ns}.rg
scoreboard players set @s {ns}.seg 0
scoreboard players set @s {ns}.ei 0
scoreboard players set @s {ns}.ek 0
scoreboard players set @s {ns}.ov 0
scoreboard players set @s {ns}.fl -1
scoreboard players set @s {ns}.fx 0
execute unless entity @s[type=minecraft:mannequin] run scoreboard players set @s {ns}.fx 1
scoreboard players set @s {ns}.rb 0
scoreboard players set @s {ns}.run 0
execute if score @s {ns}.len matches 1.. run scoreboard players set @s {ns}.run 1
execute if score @s {ns}.run matches 1 run function {ns}:v{version}/playback/load
execute if score @s {ns}.grp matches 1.. run function {ns}:v{version}/playback/grpinit
function {ns}:v{version}/spawn/ovr
execute if entity @s[type=minecraft:mannequin] if data storage {ns}:in prof run data modify entity @s profile set from storage {ns}:in prof
data remove storage {ns}:in prof
execute if entity @s[type=minecraft:mannequin] unless data storage {ns}:in a{{skin:""}} run function {ns}:v{version}/spawn/skin with storage {ns}:in a
execute if entity @s[type=minecraft:mannequin] if data storage {ns}:in a{{skin:""}} unless data storage {ns}:in a{{texture:""}} run function {ns}:v{version}/spawn/tex with storage {ns}:in a
execute unless data storage {ns}:in a{{pose:""}} run function {ns}:v{version}/spawn/pose_fix with storage {ns}:in a
execute store result score @s {ns}.pr run data get storage {ns}:in a.offset 100
scoreboard players operation #t {ns}.data = @s {ns}.len
scoreboard players operation #t {ns}.data *= @s {ns}.n100
execute if score #t {ns}.data matches 1.. run scoreboard players operation @s {ns}.pr %= #t {ns}.data
execute if score @s {ns}.run matches 1 if score @s {ns}.pr >= @s {ns}.n100 run function {ns}:v{version}/playback/adv
execute if score @s {ns}.hs matches 1 run scoreboard players set @s {ns}.si 0
execute if score @s {ns}.hs matches 1 run function {ns}:v{version}/playback/swload
execute if score @s {ns}.hs matches 1 run function {ns}:v{version}/playback/swskip
execute if score @s {ns}.ha matches 1 run scoreboard players set @s {ns}.ai 0
execute if score @s {ns}.ha matches 1 run function {ns}:v{version}/playback/acload
execute if score @s {ns}.ha matches 1 run function {ns}:v{version}/playback/acskip
function {ns}:v{version}/playback/move
function #{ns}:v{major}/signals/on_spawn
""")

	write_versioned_function("spawn/killtag", f"""
scoreboard players set #kres {ns}.data 1
$execute as @e[tag={ns}.t.$(tag)] run function {ns}:v{version}/playback/delete
scoreboard players set #kres {ns}.data 0
""")

	write_versioned_function("spawn/ntag", f"""
$tag @s add {ns}.n.$(name)
""")

	write_versioned_function("spawn/ovr", f"""
# Équipement imposé depuis le command block : si un champ est rempli, l'équipement enregistré ne change plus après le départ
execute unless data storage {ns}:in a{{head:""}} run data modify storage {ns}:in s set value {{slot:"armor.head"}}
execute unless data storage {ns}:in a{{head:""}} run data modify storage {ns}:in s.item set from storage {ns}:in a.head
execute unless data storage {ns}:in a{{head:""}} run function {ns}:v{version}/spawn/slot with storage {ns}:in s
execute unless data storage {ns}:in a{{head:""}} run scoreboard players set @s {ns}.ov 1
execute unless data storage {ns}:in a{{chest:""}} run data modify storage {ns}:in s set value {{slot:"armor.chest"}}
execute unless data storage {ns}:in a{{chest:""}} run data modify storage {ns}:in s.item set from storage {ns}:in a.chest
execute unless data storage {ns}:in a{{chest:""}} run function {ns}:v{version}/spawn/slot with storage {ns}:in s
execute unless data storage {ns}:in a{{chest:""}} run scoreboard players set @s {ns}.ov 1
execute unless data storage {ns}:in a{{legs:""}} run data modify storage {ns}:in s set value {{slot:"armor.legs"}}
execute unless data storage {ns}:in a{{legs:""}} run data modify storage {ns}:in s.item set from storage {ns}:in a.legs
execute unless data storage {ns}:in a{{legs:""}} run function {ns}:v{version}/spawn/slot with storage {ns}:in s
execute unless data storage {ns}:in a{{legs:""}} run scoreboard players set @s {ns}.ov 1
execute unless data storage {ns}:in a{{feet:""}} run data modify storage {ns}:in s set value {{slot:"armor.feet"}}
execute unless data storage {ns}:in a{{feet:""}} run data modify storage {ns}:in s.item set from storage {ns}:in a.feet
execute unless data storage {ns}:in a{{feet:""}} run function {ns}:v{version}/spawn/slot with storage {ns}:in s
execute unless data storage {ns}:in a{{feet:""}} run scoreboard players set @s {ns}.ov 1
execute unless data storage {ns}:in a{{mainhand:""}} run data modify storage {ns}:in s set value {{slot:"weapon.mainhand"}}
execute unless data storage {ns}:in a{{mainhand:""}} run data modify storage {ns}:in s.item set from storage {ns}:in a.mainhand
execute unless data storage {ns}:in a{{mainhand:""}} run function {ns}:v{version}/spawn/slot with storage {ns}:in s
execute unless data storage {ns}:in a{{mainhand:""}} run scoreboard players set @s {ns}.ov 1
execute unless data storage {ns}:in a{{offhand:""}} run data modify storage {ns}:in s set value {{slot:"weapon.offhand"}}
execute unless data storage {ns}:in a{{offhand:""}} run data modify storage {ns}:in s.item set from storage {ns}:in a.offhand
execute unless data storage {ns}:in a{{offhand:""}} run function {ns}:v{version}/spawn/slot with storage {ns}:in s
execute unless data storage {ns}:in a{{offhand:""}} run scoreboard players set @s {ns}.ov 1
""")

	write_versioned_function("spawn/pose_fix", f"""
$data modify entity @s pose set value "$(pose)"
execute if data storage {ns}:in a{{pose:"fall_flying"}} run data modify entity @s OnGround set value 0b
execute if data storage {ns}:in a{{pose:"fall_flying"}} run data modify entity @s FallFlying set value 1b
scoreboard players set @s {ns}.fx 1
""")

	write_versioned_function("spawn/reg", f"""
$data modify storage {ns}:inst i$(id) set value {{name:"$(name)"}}
""")

	write_versioned_function("spawn/size", f"""
$attribute @s minecraft:scale base set $(size)
""")

	write_versioned_function("spawn/skin", f"""
$data modify entity @s profile set value "$(skin)"
""")

	write_versioned_function("spawn/slot", f"""
$item replace entity @s $(slot) with $(item)
""")

	write_versioned_function("spawn/spawn", f"""
execute unless data storage {ns}:in a{{tag:""}} run function {ns}:v{version}/spawn/killtag with storage {ns}:in a
execute if data storage {ns}:in a{{entity:""}} run function {ns}:v{version}/spawn/sum_m
execute if data storage {ns}:in a{{entity:"minecraft:mannequin"}} run function {ns}:v{version}/spawn/sum_m
execute if data storage {ns}:in a{{entity:"mannequin"}} run function {ns}:v{version}/spawn/sum_m
execute unless data storage {ns}:in a{{entity:""}} unless data storage {ns}:in a{{entity:"minecraft:mannequin"}} unless data storage {ns}:in a{{entity:"mannequin"}} run function {ns}:v{version}/spawn/sum_o with storage {ns}:in a
scoreboard players add #id {ns}.data 1
execute as @e[tag={ns}.new,sort=nearest,limit=1] run function {ns}:v{version}/spawn/init
""")

	write_versioned_function("spawn/sum_m", f"""
summon minecraft:mannequin ~ ~ ~ {{Tags:["{ns}.m","{ns}.x","{ns}.new","smithed.entity","smithed.strict"],immovable:true,hide_description:true,Invulnerable:1b,Silent:1b,NoGravity:1b}}
""")

	write_versioned_function("spawn/sum_o", f"""
$summon $(entity) ~ ~ ~ {{Tags:["{ns}.m","{ns}.x","{ns}.new","smithed.entity","smithed.strict"],NoAI:1b,Silent:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b}}
""")

	write_versioned_function("spawn/tex", f"""
$data modify entity @s profile set value {{properties:[{{name:"textures",value:"$(texture)"}}]}}
""")

	write_versioned_function("spawn/utag", f"""
$tag @s add {ns}.t.$(tag)
""")

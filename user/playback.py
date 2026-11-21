""" Playback of the instances: interpolation, equipment, swings, actions and groups. """
# Imports
from stewbeet import Mem, write_versioned_function


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("playback/a_at", f"""
$execute at @s positioned $(x) $(y) $(z) run function {ns}:v{version}/playback/a_go
""")

	write_versioned_function("playback/a_bkpair", f"""
data modify storage {ns}:t pd set value {{x:0,y:0,z:0}}
execute store result storage {ns}:t pd.x int 1 run scoreboard players get #pdx {ns}.data
execute store result storage {ns}:t pd.y int 1 run scoreboard players get #pdy {ns}.data
execute store result storage {ns}:t pd.z int 1 run scoreboard players get #pdz {ns}.data
function {ns}:v{version}/playback/a_bkpair2 with storage {ns}:t pd
""")

	write_versioned_function("playback/a_bkpair2", f"""
$execute positioned ~$(x) ~$(y) ~$(z) run function {ns}:v{version}/vault/here
""")

	write_versioned_function("playback/a_break", f"""
function {ns}:v{version}/block/read
function {ns}:v{version}/block/pair
scoreboard players operation #bkm {ns}.data = #pair {ns}.data
function {ns}:v{version}/vault/here
execute if score #pair {ns}.data matches 1 run function {ns}:v{version}/playback/a_bkpair
setblock ~ ~ ~ minecraft:air destroy
execute align xyz positioned ~0.5 ~0.5 ~0.5 run kill @e[type=minecraft:item,distance=..1.6,nbt={{Age:0s}}]
execute align xyz positioned ~0.5 ~0.5 ~0.5 run kill @e[type=minecraft:experience_orb,distance=..1.6]
swing @s mainhand
""")

	write_versioned_function("playback/a_go", f"""
execute if score #ek {ns}.data matches 2 run return run function {ns}:v{version}/playback/a_use
execute if score #ek {ns}.data matches 3 run return run function {ns}:v{version}/playback/a_place
execute if score #ek {ns}.data matches 4 run return run function {ns}:v{version}/playback/a_break
""")

	write_versioned_function("playback/a_hit2", f"""
$execute as @e[distance=..1.6,tag=!{ns}.m,tag=!smithed.strict,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker] run damage @s $(d) minecraft:mob_attack by @e[tag={ns}.hitter,limit=1]
$execute if score @e[tag={ns}.hitter,limit=1] {ns}.hitp matches 1 as @a[distance=..1.6,gamemode=!spectator] run damage @s $(d) minecraft:mob_attack by @e[tag={ns}.hitter,limit=1]
""")

	write_versioned_function("playback/a_place", f"""
scoreboard players set #bkm {ns}.data 0
execute if data storage {ns}:t ev.p run scoreboard players set #bkm {ns}.data 1
function {ns}:v{version}/vault/here
execute if score #bkm {ns}.data matches 1 run function {ns}:v{version}/playback/a_place2
execute if score #bkm {ns}.data matches 0 run function {ns}:v{version}/playback/setb with storage {ns}:t ev
execute if score #bkm {ns}.data matches 1 run function {ns}:v{version}/playback/setbs with storage {ns}:t ev
playsound minecraft:block.stone.place block @a ~ ~ ~
""")

	write_versioned_function("playback/a_place2", f"""
# autre moitié : sauvegarde puis pose
data modify storage {ns}:t pp set value {{x:0,y:0,z:0,b:""}}
data modify storage {ns}:t pp.b set from storage {ns}:t ev.p.b
execute store result score #px {ns}.data run data get storage {ns}:t ev.p.x
execute store result score #py {ns}.data run data get storage {ns}:t ev.p.y
execute store result score #pz {ns}.data run data get storage {ns}:t ev.p.z
scoreboard players operation #px {ns}.data += @s {ns}.bbx
scoreboard players operation #py {ns}.data += @s {ns}.bby
scoreboard players operation #pz {ns}.data += @s {ns}.bbz
execute store result storage {ns}:t pp.x int 1 run scoreboard players get #px {ns}.data
execute store result storage {ns}:t pp.y int 1 run scoreboard players get #py {ns}.data
execute store result storage {ns}:t pp.z int 1 run scoreboard players get #pz {ns}.data
function {ns}:v{version}/playback/a_place3 with storage {ns}:t pp
""")

	write_versioned_function("playback/a_place3", f"""
$execute positioned $(x) $(y) $(z) run function {ns}:v{version}/vault/here
$setblock $(x) $(y) $(z) $(b) strict
""")

	write_versioned_function("playback/a_use", f"""
function {ns}:v{version}/block/read
execute if data storage {ns}:bk r{{id:""}} run return 0
execute if block ~ ~ ~ #minecraft:buttons run return run function {ns}:v{version}/playback/u_button
execute if block ~ ~ ~ minecraft:lever run return run function {ns}:v{version}/playback/u_lever
execute if block ~ ~ ~ #{ns}:doors_open run return run function {ns}:v{version}/playback/u_door
execute if block ~ ~ ~ #{ns}:trapdoors_open run return run function {ns}:v{version}/playback/u_open
execute if block ~ ~ ~ #minecraft:fence_gates run return run function {ns}:v{version}/playback/u_open
""")

	write_versioned_function("playback/ac1", f"""
$data modify storage {ns}:t name set from storage {ns}:inst i$(id).name
function {ns}:v{version}/playback/ac2 with storage {ns}:t
""")

	write_versioned_function("playback/ac2", f"""
$execute if data storage {ns}:data seqs.$(name).a[$(aj)] store result score @s {ns}.ak run data get storage {ns}:data seqs.$(name).a[$(aj)].t 100
""")

	write_versioned_function("playback/acchk", f"""
scoreboard players operation #tm {ns}.data = @s {ns}.seg
scoreboard players operation #tm {ns}.data *= @s {ns}.n100
scoreboard players operation #tm {ns}.data += @s {ns}.pr
execute if score #tm {ns}.data >= @s {ns}.ak run function {ns}:v{version}/playback/acdo
""")

	write_versioned_function("playback/acdo", f"""
execute store result storage {ns}:t id int 1 run scoreboard players get @s {ns}.id
execute store result storage {ns}:t aj int 1 run scoreboard players get @s {ns}.ai
function {ns}:v{version}/playback/acget1 with storage {ns}:t
function {ns}:v{version}/playback/acrun
scoreboard players add @s {ns}.ai 1
function {ns}:v{version}/playback/acload
execute if score #tm {ns}.data >= @s {ns}.ak run function {ns}:v{version}/playback/acdo
""")

	write_versioned_function("playback/acget1", f"""
$data modify storage {ns}:t name set from storage {ns}:inst i$(id).name
function {ns}:v{version}/playback/acget2 with storage {ns}:t
""")

	write_versioned_function("playback/acget2", f"""
$data modify storage {ns}:t ev set from storage {ns}:data seqs.$(name).a[$(aj)]
""")

	write_versioned_function("playback/acload", f"""
execute store result storage {ns}:t id int 1 run scoreboard players get @s {ns}.id
execute store result storage {ns}:t aj int 1 run scoreboard players get @s {ns}.ai
scoreboard players set @s {ns}.ak 999999999
function {ns}:v{version}/playback/ac1 with storage {ns}:t
""")

	write_versioned_function("playback/acrun", f"""
execute store result score #ek {ns}.data run data get storage {ns}:t ev.k
execute if score #ek {ns}.data matches 1 run return run function {ns}:v{version}/playback/a_hit
# position absolue du bloc = point de départ de l'entité + décalage enregistré
execute store result score #ax {ns}.data run data get storage {ns}:t ev.x
execute store result score #ay {ns}.data run data get storage {ns}:t ev.y
execute store result score #az {ns}.data run data get storage {ns}:t ev.z
scoreboard players operation #ax {ns}.data += @s {ns}.bbx
scoreboard players operation #ay {ns}.data += @s {ns}.bby
scoreboard players operation #az {ns}.data += @s {ns}.bbz
data modify storage {ns}:t at set value {{x:0,y:0,z:0}}
execute store result storage {ns}:t at.x int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:t at.y int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:t at.z int 1 run scoreboard players get #az {ns}.data
execute if score #ek {ns}.data matches 2 run return run function {ns}:v{version}/playback/a_at with storage {ns}:t at
execute if score #ek {ns}.data matches 3 run return run function {ns}:v{version}/playback/a_at with storage {ns}:t at
execute if score #ek {ns}.data matches 4 run return run function {ns}:v{version}/playback/a_at with storage {ns}:t at
""")

	write_versioned_function("playback/acskip", f"""
scoreboard players operation #tm {ns}.data = @s {ns}.seg
scoreboard players operation #tm {ns}.data *= @s {ns}.n100
scoreboard players operation #tm {ns}.data += @s {ns}.pr
execute if score #tm {ns}.data > @s {ns}.ak run function {ns}:v{version}/playback/acskip1
""")

	write_versioned_function("playback/acskip1", f"""
scoreboard players add @s {ns}.ai 1
function {ns}:v{version}/playback/acload
execute if score #tm {ns}.data > @s {ns}.ak run function {ns}:v{version}/playback/acskip1
""")

	write_versioned_function("playback/adv", f"""
scoreboard players operation @s {ns}.pr -= @s {ns}.n100
scoreboard players operation @s {ns}.bx += @s {ns}.dx
scoreboard players operation @s {ns}.by += @s {ns}.dy
scoreboard players operation @s {ns}.bz += @s {ns}.dz
scoreboard players operation @s {ns}.byw += @s {ns}.dyw
scoreboard players operation @s {ns}.bpt += @s {ns}.dpt
scoreboard players add @s {ns}.seg 1
execute if score @s {ns}.seg >= @s {ns}.len run function {ns}:v{version}/playback/end
execute if score @s {ns}.run matches 1 run function {ns}:v{version}/playback/load
execute if score @s {ns}.run matches 1 if score @s {ns}.pr >= @s {ns}.n100 run function {ns}:v{version}/playback/adv
""")

	write_versioned_function("playback/body", f"""
$data modify entity @s Rotation set value [$(yaw)f,$(pitch)f]
execute if score @s {ns}.dyw matches 0 run scoreboard players set @s {ns}.rb 0
""")

	write_versioned_function("playback/delete", f"""
scoreboard players set @s {ns}.run 0
function {ns}:v{version}/playback/relall
execute if score @s {ns}.rst matches 2 run function {ns}:v{version}/vault/restore
execute if score @s {ns}.rst matches 1 if score #kres {ns}.data matches 1 run function {ns}:v{version}/vault/restore
function {ns}:v{version}/vault/free
execute store result storage {ns}:t id int 1 run scoreboard players get @s {ns}.id
function {ns}:v{version}/playback/unreg with storage {ns}:t
tag @s remove {ns}.m
# rien ne doit se voir ni tomber : on vide l'équipement et on envoie l'entité sous le monde avant de la retirer
item replace entity @s armor.head with minecraft:air
item replace entity @s armor.chest with minecraft:air
item replace entity @s armor.legs with minecraft:air
item replace entity @s armor.feet with minecraft:air
item replace entity @s weapon.mainhand with minecraft:air
item replace entity @s weapon.offhand with minecraft:air
effect give @s minecraft:invisibility infinite 0 true
tp @s ~ -1000 ~
kill @s
""")

	write_versioned_function("playback/end", f"""
execute if score @s {ns}.rsb matches 1 if score @s {ns}.grp matches 0 run function {ns}:v{version}/playback/pulse
execute if score @s {ns}.lp matches 1 run function {ns}:v{version}/playback/restart
execute unless score @s {ns}.lp matches 0..2 run function {ns}:v{version}/playback/restart
execute if score @s {ns}.lp matches 0 run function {ns}:v{version}/playback/freeze
execute if score @s {ns}.lp matches 2 run function {ns}:v{version}/playback/delete
""")

	write_versioned_function("playback/ev", f"""
execute store result storage {ns}:t id int 1 run scoreboard players get @s {ns}.id
execute store result storage {ns}:t ei int 1 run scoreboard players get @s {ns}.ei
scoreboard players add @s {ns}.ei 1
execute store result storage {ns}:t ej int 1 run scoreboard players get @s {ns}.ei
scoreboard players set @s {ns}.ek 999999999
function {ns}:v{version}/playback/ev1 with storage {ns}:t
execute if score @s {ns}.seg >= @s {ns}.ek run function {ns}:v{version}/playback/ev
""")

	write_versioned_function("playback/ev1", f"""
$data modify storage {ns}:t name set from storage {ns}:inst i$(id).name
function {ns}:v{version}/playback/ev2 with storage {ns}:t
""")

	write_versioned_function("playback/ev2", f"""
$data modify entity @s equipment set from storage {ns}:data seqs.$(name).e[$(ei)].v
$execute if data storage {ns}:data seqs.$(name).e[$(ej)] store result score @s {ns}.ek run data get storage {ns}:data seqs.$(name).e[$(ej)].k
""")

	write_versioned_function("playback/freeze", f"""
scoreboard players set @s {ns}.dx 0
scoreboard players set @s {ns}.dy 0
scoreboard players set @s {ns}.dz 0
scoreboard players set @s {ns}.dyw 0
scoreboard players set @s {ns}.dpt 0
scoreboard players set @s {ns}.pr 0
scoreboard players set @s {ns}.run 0
execute if score @s {ns}.grp matches 0 if score @s {ns}.rst matches 2 run function {ns}:v{version}/vault/restore
function {ns}:v{version}/playback/move
execute if score @s {ns}.grp matches 1.. run function {ns}:v{version}/playback/grpfreeze
""")

	write_versioned_function("playback/grpcheck", f"""
function {ns}:v{version}/playback/grpmark
execute if score #pend {ns}.data matches 1 run function {ns}:v{version}/playback/grpfire
""")

	write_versioned_function("playback/grpfire", f"""
scoreboard players set #pend {ns}.data 0
execute as @e[tag={ns}.m,scores={{{ns}.rs=1}}] run function {ns}:v{version}/playback/regrp
""")

	write_versioned_function("playback/grpfreeze", f"""
scoreboard players operation #g {ns}.data = @s {ns}.grp
function {ns}:v{version}/playback/grpmark
""")

	write_versioned_function("playback/grpinit", f"""
tag @s add {ns}.me
scoreboard players operation #g {ns}.data = @s {ns}.grp
scoreboard players set #alive {ns}.data 0
scoreboard players set #same {ns}.data 0
execute as @e[tag={ns}.m,tag=!{ns}.me] if score @s {ns}.grp = #g {ns}.data if score @s {ns}.run matches 1..2 run scoreboard players set #alive {ns}.data 1
execute as @e[tag={ns}.m,tag=!{ns}.me] if score @s {ns}.grp = #g {ns}.data if score @s {ns}.run matches 1 if score @s {ns}.gs = #gt {ns}.data run scoreboard players set #same {ns}.data 1
tag @s remove {ns}.me
execute if score #alive {ns}.data matches 1 unless score #same {ns}.data matches 1 run scoreboard players set @s {ns}.run 0
execute unless score @s {ns}.run matches 0 run scoreboard players operation @s {ns}.gs = #gt {ns}.data
""")

	write_versioned_function("playback/grpmark", f"""
scoreboard players set #alive {ns}.data 0
execute as @e[tag={ns}.m] if score @s {ns}.grp = #g {ns}.data if score @s {ns}.run matches 1..2 run scoreboard players set #alive {ns}.data 1
execute if score #alive {ns}.data matches 0 as @e[tag={ns}.m] if score @s {ns}.grp = #g {ns}.data unless score @s {ns}.gloop matches 0 unless score @s {ns}.gloop matches 2 run scoreboard players set @s {ns}.rs 1
execute if score #alive {ns}.data matches 0 as @e[tag={ns}.m] if score @s {ns}.grp = #g {ns}.data if score @s {ns}.rsb matches 1 run function {ns}:v{version}/playback/pulse
execute if score #alive {ns}.data matches 0 as @e[tag={ns}.m] if score @s {ns}.grp = #g {ns}.data if score @s {ns}.gloop matches 2 run function {ns}:v{version}/playback/delete
execute if score #alive {ns}.data matches 0 as @e[tag={ns}.m] if score @s {ns}.grp = #g {ns}.data if score @s {ns}.gloop matches 0 if score @s {ns}.rst matches 2 run function {ns}:v{version}/vault/restore
execute if score #alive {ns}.data matches 0 run scoreboard players set #pend {ns}.data 1
""")

	write_versioned_function("playback/kick", f"""
# positionné sur le bloc support : on le remplace un instant puis on le remet avec mise à jour,
# pour que les blocs autour (command block, redstone) voient le courant comme avec un vrai joueur
execute unless data storage {ns}:cfg vault run return 0
clone ~ ~ ~ ~ ~ ~ to {ns}:vault 15 319 15 strict
setblock ~ ~ ~ minecraft:barrier strict
clone from {ns}:vault 15 319 15 15 319 15 ~ ~ ~
""")

	write_versioned_function("playback/kickat", f"""
$execute positioned ~$(x) ~$(y) ~$(z) run function {ns}:v{version}/playback/kick
""")

	write_versioned_function("playback/kickmk", f"""
$execute positioned ~$(x) ~$(y) ~$(z) summon minecraft:marker run function {ns}:v{version}/playback/kickpos
""")

	write_versioned_function("playback/kickoff", f"""
# positionné sur un bouton ou un levier (drapeaux de bk/read) : décalage vers le bloc support dans {ns}:t kd
data modify storage {ns}:t kd set value {{x:0,y:0,z:0}}
execute if score #bfa {ns}.data matches 1 run data modify storage {ns}:t kd.y set value -1
execute if score #bfa {ns}.data matches 2 run data modify storage {ns}:t kd.y set value 1
execute if score #bfa {ns}.data matches 3 if score #bfc {ns}.data matches 1 run data modify storage {ns}:t kd.z set value 1
execute if score #bfa {ns}.data matches 3 if score #bfc {ns}.data matches 2 run data modify storage {ns}:t kd.z set value -1
execute if score #bfa {ns}.data matches 3 if score #bfc {ns}.data matches 3 run data modify storage {ns}:t kd.x set value -1
execute if score #bfa {ns}.data matches 3 if score #bfc {ns}.data matches 4 run data modify storage {ns}:t kd.x set value 1
""")

	write_versioned_function("playback/kickpos", f"""
execute store result storage {ns}:t rel.kx int 1 run data get entity @s Pos[0]
execute store result storage {ns}:t rel.ky int 1 run data get entity @s Pos[1]
execute store result storage {ns}:t rel.kz int 1 run data get entity @s Pos[2]
kill @s
""")

	write_versioned_function("playback/load", f"""
execute store result storage {ns}:t id int 1 run scoreboard players get @s {ns}.id
execute store result storage {ns}:t s int 1 run scoreboard players get @s {ns}.seg
function {ns}:v{version}/playback/load1 with storage {ns}:t
execute if score @s {ns}.ov matches 0 if score @s {ns}.seg >= @s {ns}.ek run function {ns}:v{version}/playback/ev
""")

	write_versioned_function("playback/load1", f"""
$data modify storage {ns}:t name set from storage {ns}:inst i$(id).name
function {ns}:v{version}/playback/load2 with storage {ns}:t
""")

	write_versioned_function("playback/load2", f"""
$data modify storage {ns}:t row set from storage {ns}:data seqs.$(name).d[$(s)]
execute store result score @s {ns}.dx run data get storage {ns}:t row[0]
execute store result score @s {ns}.dy run data get storage {ns}:t row[1]
execute store result score @s {ns}.dz run data get storage {ns}:t row[2]
execute store result score @s {ns}.dyw run data get storage {ns}:t row[3]
execute store result score @s {ns}.dpt run data get storage {ns}:t row[4]
execute store result score @s {ns}.fn run data get storage {ns}:t row[5]
scoreboard players operation #ost {ns}.data = @s {ns}.st
scoreboard players set @s {ns}.st 0
execute if score @s {ns}.dx matches 0 if score @s {ns}.dy matches 0 if score @s {ns}.dz matches 0 if score @s {ns}.dyw matches 0 if score @s {ns}.dpt matches 0 run scoreboard players set @s {ns}.st 1
execute unless score @s {ns}.st matches 1 run scoreboard players set @s {ns}.pl 0
execute unless score #ost {ns}.data matches 1 run scoreboard players set @s {ns}.pl 0
scoreboard players set @s {ns}.rb 0
execute if score @s {ns}.fx matches 0 if score @s {ns}.fn matches 2..7 unless score @s {ns}.dyw matches 0 run scoreboard players set @s {ns}.rb 1
execute if score @s {ns}.fx matches 0 if score @s {ns}.fn matches 2..7 unless score @s {ns}.fn = @s {ns}.fl run scoreboard players set @s {ns}.rb 1
execute if score @s {ns}.rb matches 1 run scoreboard players set @s {ns}.pl 0
execute if score @s {ns}.fx matches 0 unless score @s {ns}.fn = @s {ns}.fl run function {ns}:v{version}/playback/pose
""")

	write_versioned_function("playback/move", f"""
scoreboard players operation #t {ns}.data = @s {ns}.dx
scoreboard players operation #t {ns}.data *= @s {ns}.pr
scoreboard players operation #t {ns}.data /= @s {ns}.dv
scoreboard players operation #t {ns}.data += @s {ns}.bx
execute store result storage {ns}:t x double 0.001 run scoreboard players get #t {ns}.data
scoreboard players operation #t {ns}.data = @s {ns}.dy
scoreboard players operation #t {ns}.data *= @s {ns}.pr
scoreboard players operation #t {ns}.data /= @s {ns}.dv
scoreboard players operation #t {ns}.data += @s {ns}.by
execute store result storage {ns}:t y double 0.001 run scoreboard players get #t {ns}.data
scoreboard players operation #t {ns}.data = @s {ns}.dz
scoreboard players operation #t {ns}.data *= @s {ns}.pr
scoreboard players operation #t {ns}.data /= @s {ns}.dv
scoreboard players operation #t {ns}.data += @s {ns}.bz
execute store result storage {ns}:t z double 0.001 run scoreboard players get #t {ns}.data
scoreboard players operation #t {ns}.data = @s {ns}.dyw
scoreboard players operation #t {ns}.data *= @s {ns}.pr
scoreboard players operation #t {ns}.data /= @s {ns}.dv
scoreboard players operation #t {ns}.data += @s {ns}.byw
execute store result storage {ns}:t yaw double 0.01 run scoreboard players get #t {ns}.data
scoreboard players operation #t {ns}.data = @s {ns}.dpt
scoreboard players operation #t {ns}.data *= @s {ns}.pr
scoreboard players operation #t {ns}.data /= @s {ns}.dv
scoreboard players operation #t {ns}.data += @s {ns}.bpt
execute if score #t {ns}.data matches 9001.. run scoreboard players set #t {ns}.data 9000
execute if score #t {ns}.data matches ..-9001 run scoreboard players set #t {ns}.data -9000
execute store result storage {ns}:t pitch double 0.01 run scoreboard players get #t {ns}.data
function {ns}:v{version}/playback/tp with storage {ns}:t
execute if score @s {ns}.rb matches 1 run function {ns}:v{version}/playback/body with storage {ns}:t
execute if score @s {ns}.st matches 1 run scoreboard players set @s {ns}.pl 1
""")

	write_versioned_function("playback/pose", f"""
scoreboard players operation @s {ns}.fl = @s {ns}.fn
execute if score @s {ns}.fl matches 0 run data modify entity @s pose set value "standing"
execute if score @s {ns}.fl matches 1 run data modify entity @s pose set value "crouching"
execute if score @s {ns}.fl matches 2..3 run data modify entity @s pose set value "swimming"
execute if score @s {ns}.fl matches 4..7 run data modify entity @s pose set value "fall_flying"
execute if score @s {ns}.fl matches 4..7 run data modify entity @s OnGround set value 0b
execute if score @s {ns}.fl matches 4..7 run data modify entity @s FallFlying set value 1b
execute unless score @s {ns}.fl matches 4..7 run data modify entity @s FallFlying set value 0b
""")

	write_versioned_function("playback/pulse", f"""
# bloc de redstone posé 2 blocs au-dessus du command block (1 bloc d'écart, sinon il se réactive lui-même) qui a lancé la séquence, retiré 4 ticks plus tard
execute store result storage {ns}:t pu.x int 1 run scoreboard players get @s {ns}.cbx
execute store result storage {ns}:t pu.y int 1 run scoreboard players get @s {ns}.cby
execute store result storage {ns}:t pu.z int 1 run scoreboard players get @s {ns}.cbz
function {ns}:v{version}/playback/pulse2 with storage {ns}:t pu
""")

	write_versioned_function("playback/pulse2", f"""
$execute at @s positioned $(x) $(y) $(z) positioned ~ ~2 ~ run function {ns}:v{version}/playback/pulse3
""")

	write_versioned_function("playback/pulse3", f"""
# on ne remplace jamais un bloc existant
execute unless block ~ ~ ~ #minecraft:air run return 0
setblock ~ ~ ~ minecraft:redstone_block
execute align xyz positioned ~0.5 ~0.5 ~0.5 summon minecraft:marker run function {ns}:v{version}/playback/pulse4
""")

	write_versioned_function("playback/pulse4", f"""
tag @s add {ns}.pulse
tag @s add smithed.entity
tag @s add smithed.strict
scoreboard players operation @s {ns}.due = #now {ns}.data
scoreboard players add @s {ns}.due 4
scoreboard players add #npulse {ns}.data 1
""")

	write_versioned_function("playback/pulseoff", f"""
execute if block ~ ~ ~ minecraft:redstone_block run setblock ~ ~ ~ minecraft:air
scoreboard players remove #npulse {ns}.data 1
kill @s
""")

	write_versioned_function("playback/regrp", f"""
scoreboard players set @s {ns}.rs 0
execute if score @s {ns}.rst matches 1.. run function {ns}:v{version}/vault/restore
execute unless score @s {ns}.len matches 1.. run return 0
scoreboard players operation @s {ns}.dx = @s {ns}.ax
scoreboard players operation @s {ns}.dx -= @s {ns}.bx
scoreboard players operation @s {ns}.dy = @s {ns}.ay
scoreboard players operation @s {ns}.dy -= @s {ns}.by
scoreboard players operation @s {ns}.dz = @s {ns}.az
scoreboard players operation @s {ns}.dz -= @s {ns}.bz
scoreboard players operation @s {ns}.dyw = @s {ns}.yw0
scoreboard players operation @s {ns}.dyw -= @s {ns}.byw
execute if score @s {ns}.dyw matches 18001.. run scoreboard players remove @s {ns}.dyw 36000
execute if score @s {ns}.dyw matches ..-18001 run scoreboard players add @s {ns}.dyw 36000
scoreboard players operation @s {ns}.dpt = @s {ns}.pt0
scoreboard players operation @s {ns}.dpt -= @s {ns}.bpt
scoreboard players set @s {ns}.dv 40
scoreboard players set @s {ns}.pr 0
scoreboard players set @s {ns}.st 0
scoreboard players set @s {ns}.pl 0
scoreboard players set @s {ns}.fn 0
execute if score @s {ns}.fx matches 0 unless score @s {ns}.fn = @s {ns}.fl run function {ns}:v{version}/playback/pose
scoreboard players set @s {ns}.run 2
""")

	write_versioned_function("playback/rel", f"""
execute store result storage {ns}:t rv.id int 1 run scoreboard players get @s {ns}.id
function {ns}:v{version}/playback/rel1 with storage {ns}:t rv
scoreboard players set @s {ns}.rlt -1
execute if data storage {ns}:t rll[0] at @s run function {ns}:v{version}/playback/rel2
""")

	write_versioned_function("playback/rel1", f"""
data modify storage {ns}:t rll set value []
$data modify storage {ns}:t rll set from storage {ns}:inst i$(id).rl
$data modify storage {ns}:inst i$(id).rl set value []
""")

	write_versioned_function("playback/rel2", f"""
execute store result score #rt {ns}.data run data get storage {ns}:t rll[0].t
execute if score #rall {ns}.data matches 1 run scoreboard players set #rt {ns}.data -1
execute if score #rt {ns}.data <= #now {ns}.data run function {ns}:v{version}/playback/rel3 with storage {ns}:t rll[0]
execute if score #rt {ns}.data > #now {ns}.data run function {ns}:v{version}/playback/relkeep
data remove storage {ns}:t rll[0]
execute if data storage {ns}:t rll[0] run function {ns}:v{version}/playback/rel2
""")

	write_versioned_function("playback/rel3", f"""
$setblock $(x) $(y) $(z) $(b)
$execute positioned $(kx) $(ky) $(kz) run function {ns}:v{version}/playback/kick
$playsound minecraft:block.stone_button.click_off block @a $(x) $(y) $(z)
""")

	write_versioned_function("playback/relall", f"""
scoreboard players set #rall {ns}.data 1
function {ns}:v{version}/playback/rel
scoreboard players set #rall {ns}.data 0
""")

	write_versioned_function("playback/relkeep", f"""
data modify storage {ns}:t rel set from storage {ns}:t rll[0]
function {ns}:v{version}/playback/rladd
""")

	write_versioned_function("playback/relpos", f"""
execute store result storage {ns}:t rel.x int 1 run data get entity @s Pos[0]
execute store result storage {ns}:t rel.y int 1 run data get entity @s Pos[1]
execute store result storage {ns}:t rel.z int 1 run data get entity @s Pos[2]
kill @s
""")

	write_versioned_function("playback/rend", f"""
scoreboard players operation @s {ns}.gs = #gt {ns}.data
scoreboard players operation @s {ns}.dv = @s {ns}.n100
scoreboard players set @s {ns}.pr 0
scoreboard players set @s {ns}.fl -1
scoreboard players set @s {ns}.pl 0
function {ns}:v{version}/playback/restart
scoreboard players set @s {ns}.run 1
function {ns}:v{version}/playback/load
function {ns}:v{version}/playback/move
scoreboard players operation #rg {ns}.data = @s {ns}.grp
execute as @a[tag={ns}.armed] if score @s {ns}.rwg = #rg {ns}.data run function {ns}:v{version}/challenge/launch
""")

	write_versioned_function("playback/restart", f"""
execute if score @s {ns}.rst matches 1.. run function {ns}:v{version}/vault/restore
scoreboard players set @s {ns}.seg 0
scoreboard players operation @s {ns}.bx = @s {ns}.ax
scoreboard players operation @s {ns}.by = @s {ns}.ay
scoreboard players operation @s {ns}.bz = @s {ns}.az
scoreboard players operation @s {ns}.byw = @s {ns}.yw0
scoreboard players operation @s {ns}.bpt = @s {ns}.pt0
scoreboard players set @s {ns}.st 0
scoreboard players set @s {ns}.ei 0
scoreboard players set @s {ns}.ek 0
execute if score @s {ns}.hs matches 1 run scoreboard players set @s {ns}.si 0
execute if score @s {ns}.hs matches 1 run function {ns}:v{version}/playback/swload
execute if score @s {ns}.ha matches 1 run scoreboard players set @s {ns}.ai 0
execute if score @s {ns}.ha matches 1 run function {ns}:v{version}/playback/acload
""")

	write_versioned_function("playback/rladd", f"""
execute store result storage {ns}:t rel.id int 1 run scoreboard players get @s {ns}.id
function {ns}:v{version}/playback/rladd2 with storage {ns}:t rel
execute if score @s {ns}.rlt matches -1 run scoreboard players operation @s {ns}.rlt = #rt {ns}.data
execute if score #rt {ns}.data < @s {ns}.rlt run scoreboard players operation @s {ns}.rlt = #rt {ns}.data
""")

	write_versioned_function("playback/rladd2", f"""
$data modify storage {ns}:inst i$(id).rl append value {{t:$(t),x:$(x),y:$(y),z:$(z),b:"$(b)",kx:$(kx),ky:$(ky),kz:$(kz)}}
""")

	write_versioned_function("playback/rtick", f"""
execute unless score @s {ns}.near matches 1 run return 0
scoreboard players add @s {ns}.pr 1
execute if score @s {ns}.pr >= @s {ns}.dv run return run function {ns}:v{version}/playback/rend
execute if function {ns}:v{version}/playback/turn run function {ns}:v{version}/playback/move
""")

	write_versioned_function("playback/setb", f"""
$setblock ~ ~ ~ $(b)
""")

	write_versioned_function("playback/setbs", f"""
$setblock ~ ~ ~ $(b) strict
""")

	write_versioned_function("playback/setfull", f"""
$setblock ~ ~ ~ $(full)
""")

	write_versioned_function("playback/setfulls", f"""
$setblock ~ ~ ~ $(full) strict
""")

	write_versioned_function("playback/sw", f"""
swing @s mainhand
scoreboard players add @s {ns}.si 1
function {ns}:v{version}/playback/swload
execute if score #tm {ns}.data >= @s {ns}.sk run function {ns}:v{version}/playback/sw
""")

	write_versioned_function("playback/sw1", f"""
$data modify storage {ns}:t name set from storage {ns}:inst i$(id).name
function {ns}:v{version}/playback/sw2 with storage {ns}:t
""")

	write_versioned_function("playback/sw2", f"""
$execute if data storage {ns}:data seqs.$(name).s[$(sj)] store result score @s {ns}.sk run data get storage {ns}:data seqs.$(name).s[$(sj)] 100
""")

	write_versioned_function("playback/swchk", f"""
scoreboard players operation #tm {ns}.data = @s {ns}.seg
scoreboard players operation #tm {ns}.data *= @s {ns}.n100
scoreboard players operation #tm {ns}.data += @s {ns}.pr
execute if score #tm {ns}.data >= @s {ns}.sk run function {ns}:v{version}/playback/sw
""")

	write_versioned_function("playback/swload", f"""
execute store result storage {ns}:t id int 1 run scoreboard players get @s {ns}.id
execute store result storage {ns}:t sj int 1 run scoreboard players get @s {ns}.si
scoreboard players set @s {ns}.sk 999999999
function {ns}:v{version}/playback/sw1 with storage {ns}:t
""")

	write_versioned_function("playback/swskip", f"""
scoreboard players operation #tm {ns}.data = @s {ns}.seg
scoreboard players operation #tm {ns}.data *= @s {ns}.n100
scoreboard players operation #tm {ns}.data += @s {ns}.pr
execute if score #tm {ns}.data > @s {ns}.sk run function {ns}:v{version}/playback/swskip1
""")

	write_versioned_function("playback/swskip1", f"""
scoreboard players add @s {ns}.si 1
function {ns}:v{version}/playback/swload
execute if score #tm {ns}.data > @s {ns}.sk run function {ns}:v{version}/playback/swskip1
""")

	write_versioned_function("playback/tick", f"""
execute if score @s {ns}.rlt matches 0.. if score #now {ns}.data >= @s {ns}.rlt run function {ns}:v{version}/playback/rel
execute if score @s {ns}.run matches 2 run return run function {ns}:v{version}/playback/rtick
execute unless score @s {ns}.run matches 1 run return 0
execute unless score @s {ns}.near matches 1 run return 0
scoreboard players operation @s {ns}.pr += @s {ns}.spd
execute if score @s {ns}.pr >= @s {ns}.n100 run function {ns}:v{version}/playback/adv
execute unless score @s {ns}.run matches 1 run return 0
execute if score @s {ns}.hs matches 1 run function {ns}:v{version}/playback/swchk
execute if score @s {ns}.ha matches 1 run function {ns}:v{version}/playback/acchk
execute if score @s {ns}.st matches 1 if score @s {ns}.pl matches 1 run return 0
execute if function {ns}:v{version}/playback/turn run function {ns}:v{version}/playback/move
""")

	write_versioned_function("playback/tp", f"""
$tp @s $(x) $(y) $(z) $(yaw) $(pitch)
""")

	write_versioned_function("playback/turn", f"""
# vrai si c'est le tour de cette entité de bouger (une entité sur #step à chaque tick, en alternance)
scoreboard players operation #ph {ns}.data = @s {ns}.id
scoreboard players operation #ph {ns}.data += #gt {ns}.data
scoreboard players operation #ph {ns}.data %= #step {ns}.data
execute if score #ph {ns}.data matches 0 run return 1
return fail
""")

	write_versioned_function("playback/u_button", f"""
execute if score #bpw {ns}.data matches 1 run return 0
scoreboard players set #bkm {ns}.data 0
function {ns}:v{version}/vault/here
function #bs.block:replace_properties {{properties:[{{name:"powered",value:"true"}}]}}
function {ns}:v{version}/block/full
function {ns}:v{version}/playback/setfull with storage {ns}:bk
function {ns}:v{version}/playback/kickoff
function {ns}:v{version}/playback/kickat with storage {ns}:t kd
playsound minecraft:block.stone_button.click_on block @a ~ ~ ~
# relâché après le délai normal (1 s pierre, 1,5 s bois)
function #bs.block:replace_properties {{properties:[{{name:"powered",value:"false"}}]}}
function {ns}:v{version}/block/full
data modify storage {ns}:t rel set value {{t:0,x:0,y:0,z:0,b:"",kx:0,ky:0,kz:0}}
function {ns}:v{version}/playback/kickmk with storage {ns}:t kd
data modify storage {ns}:t rel.b set from storage {ns}:bk full
scoreboard players operation #rt {ns}.data = #now {ns}.data
scoreboard players add #rt {ns}.data 20
execute if block ~ ~ ~ #minecraft:wooden_buttons run scoreboard players add #rt {ns}.data 10
execute store result storage {ns}:t rel.t int 1 run scoreboard players get #rt {ns}.data
execute summon minecraft:marker run function {ns}:v{version}/playback/relpos
function {ns}:v{version}/playback/rladd
""")

	write_versioned_function("playback/u_door", f"""
# porte : les deux moitiés, posées sans mise à jour pour qu'elles ne se recopient pas l'une l'autre
scoreboard players set #nop {ns}.data 1
execute if score #bop {ns}.data matches 1 run scoreboard players set #nop {ns}.data 0
function {ns}:v{version}/block/pair
scoreboard players set #bkm {ns}.data 1
function {ns}:v{version}/vault/here
function {ns}:v{version}/playback/u_openex
function {ns}:v{version}/block/full
function {ns}:v{version}/playback/setfulls with storage {ns}:bk
execute if score #pair {ns}.data matches 1 run function {ns}:v{version}/playback/u_door2
execute if score #nop {ns}.data matches 1 run playsound minecraft:block.wooden_door.open block @a ~ ~ ~
execute if score #nop {ns}.data matches 0 run playsound minecraft:block.wooden_door.close block @a ~ ~ ~
""")

	write_versioned_function("playback/u_door2", f"""
data modify storage {ns}:t pd set value {{x:0,y:0,z:0}}
execute store result storage {ns}:t pd.y int 1 run scoreboard players get #pdy {ns}.data
function {ns}:v{version}/playback/u_door3 with storage {ns}:t pd
""")

	write_versioned_function("playback/u_door3", f"""
$execute positioned ~ ~$(y) ~ run function {ns}:v{version}/playback/u_door4
""")

	write_versioned_function("playback/u_door4", f"""
scoreboard players operation #keep {ns}.data = #nop {ns}.data
function {ns}:v{version}/block/read
execute if data storage {ns}:bk r{{id:""}} run return 0
scoreboard players operation #nop {ns}.data = #keep {ns}.data
scoreboard players set #bkm {ns}.data 1
function {ns}:v{version}/vault/here
function {ns}:v{version}/playback/u_openex
function {ns}:v{version}/block/full
function {ns}:v{version}/playback/setfulls with storage {ns}:bk
""")

	write_versioned_function("playback/u_lever", f"""
scoreboard players set #bkm {ns}.data 0
function {ns}:v{version}/vault/here
execute if score #bpw {ns}.data matches 0 run function #bs.block:replace_properties {{properties:[{{name:"powered",value:"true"}}]}}
execute if score #bpw {ns}.data matches 1 run function #bs.block:replace_properties {{properties:[{{name:"powered",value:"false"}}]}}
function {ns}:v{version}/block/full
function {ns}:v{version}/playback/setfull with storage {ns}:bk
function {ns}:v{version}/playback/kickoff
function {ns}:v{version}/playback/kickat with storage {ns}:t kd
playsound minecraft:block.lever.click block @a ~ ~ ~
""")

	write_versioned_function("playback/u_open", f"""
# trappe ou portillon : bascule open, garde le reste
scoreboard players set #bkm {ns}.data 0
function {ns}:v{version}/vault/here
scoreboard players set #nop {ns}.data 1
execute if score #bop {ns}.data matches 1 run scoreboard players set #nop {ns}.data 0
function {ns}:v{version}/playback/u_openex
function {ns}:v{version}/block/full
function {ns}:v{version}/playback/setfull with storage {ns}:bk
execute if block ~ ~ ~ #minecraft:fence_gates if score #bop {ns}.data matches 0 run playsound minecraft:block.fence_gate.open block @a ~ ~ ~
execute if block ~ ~ ~ #minecraft:fence_gates if score #bop {ns}.data matches 1 run playsound minecraft:block.fence_gate.close block @a ~ ~ ~
execute unless block ~ ~ ~ #minecraft:fence_gates if score #bop {ns}.data matches 0 run playsound minecraft:block.wooden_trapdoor.open block @a ~ ~ ~
execute unless block ~ ~ ~ #minecraft:fence_gates if score #bop {ns}.data matches 1 run playsound minecraft:block.wooden_trapdoor.close block @a ~ ~ ~
""")

	write_versioned_function("playback/u_openex", f"""
# bascule open, garde le reste de l'état
execute if score #nop {ns}.data matches 1 run function #bs.block:replace_properties {{properties:[{{name:"open",value:"true"}}]}}
execute if score #nop {ns}.data matches 0 run function #bs.block:replace_properties {{properties:[{{name:"open",value:"false"}}]}}
""")

	write_versioned_function("playback/unreg", f"""
$data remove storage {ns}:inst i$(id)
""")

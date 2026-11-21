""" Recording: per player state, keyframes, equipment, swings and actions (hits, use, place, break). """
# Imports
from stewbeet import Mem, write_versioned_function


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	major: str = version.split(".")[0]

	write_versioned_function("record/abort1", f"""
execute if entity @s[tag={ns}.on] run function #{ns}:v{major}/signals/on_record_stop
execute if entity @s[tag={ns}.on] run tag @s add {ns}.wasrec
tag @s remove {ns}.on
tag @s remove {ns}.armed
scoreboard players set @s {ns}.rchal 0
function {ns}:v{version}/record/cleanup
execute if entity @s[tag={ns}.wasrec] run function {ns}:v{version}/record/wrestore
tag @s remove {ns}.wasrec
function {ns}:v{version}/record/ctx
function {ns}:v{version}/record/drop with storage {ns}:ctx
""")

	write_versioned_function("record/append", f"""
data modify storage {ns}:tmp row set value [0,0,0,0,0,0]
execute unless score #dx {ns}.data matches 0 store result storage {ns}:tmp row[0] int 1 run scoreboard players get #dx {ns}.data
execute unless score #dy {ns}.data matches 0 store result storage {ns}:tmp row[1] int 1 run scoreboard players get #dy {ns}.data
execute unless score #dz {ns}.data matches 0 store result storage {ns}:tmp row[2] int 1 run scoreboard players get #dz {ns}.data
execute unless score #dyw {ns}.data matches 0 store result storage {ns}:tmp row[3] int 1 run scoreboard players get #dyw {ns}.data
execute unless score #dpt {ns}.data matches 0 store result storage {ns}:tmp row[4] int 1 run scoreboard players get #dpt {ns}.data
execute unless score #fl {ns}.data matches 0 store result storage {ns}:tmp row[5] int 1 run scoreboard players get #fl {ns}.data
function {ns}:v{version}/record/push with storage {ns}:ctx
scoreboard players add @s {ns}.rkt 1
scoreboard players add @s {ns}.rkf 1
execute if score @s {ns}.rkf matches 300.. run function {ns}:v{version}/record/chunk with storage {ns}:ctx
""")

	write_versioned_function("record/arm", f"""
execute store result score @s {ns}.rwg run data get storage {ns}:in cfg.grp
scoreboard players operation #wg {ns}.data = @s {ns}.rwg
scoreboard players set #alive {ns}.data 0
execute as @e[tag={ns}.m] if score @s {ns}.grp = #wg {ns}.data run scoreboard players set #alive {ns}.data 1
execute if score #alive {ns}.data matches 0 run return run function {ns}:v{version}/record/begin
execute unless score @s {ns}.pid matches 1.. run function {ns}:v{version}/challenge/newpid
function {ns}:v{version}/record/ctx
function {ns}:v{version}/record/armsave with storage {ns}:ctx
scoreboard players set @s {ns}.ratype 1
tag @s add {ns}.armed
tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Enregistrement armé : il démarre au prochain cycle du groupe.",color:"green"}}]
""")

	write_versioned_function("record/armg", f"""
# cherche le groupe du même nom le plus proche du joueur ; aucun -> l'enregistrement démarre tout de suite
scoreboard players set #found {ns}.data 0
$execute at @s as @e[tag={ns}.m,tag={ns}.g.$(group),distance=..$(group_radius),sort=nearest,limit=1] run scoreboard players operation #found {ns}.data = @s {ns}.grp
execute if score #found {ns}.data matches ..0 run return run function {ns}:v{version}/record/begin
execute store result storage {ns}:in cfg.grp int 1 run scoreboard players get #found {ns}.data
function {ns}:v{version}/record/arm
""")

	write_versioned_function("record/armload", f"""
$data modify storage {ns}:tmp meta set from storage {ns}:rec p.p$(pid).meta
""")

	write_versioned_function("record/armsave", f"""
$data modify storage {ns}:rec p.p$(pid).meta set from storage {ns}:tmp meta
""")

	write_versioned_function("record/atk", f"""
execute if score @s {ns}.ratk = @s {ns}.rtime run return 0
scoreboard players operation @s {ns}.ratk = @s {ns}.rtime
function {ns}:v{version}/record/ctx
data modify storage {ns}:tmp ev set value {{t:0,k:1}}
execute store result storage {ns}:tmp ev.t int 1 run scoreboard players get @s {ns}.rtime
function {ns}:v{version}/record/evpush with storage {ns}:ctx
""")

	write_versioned_function("record/begin", f"""
function {ns}:v{version}/record/init
scoreboard players operation #me {ns}.data = @s {ns}.pid
execute as @e[type=minecraft:text_display,tag={ns}.start] if score @s {ns}.pid = #me {ns}.data run kill @s
execute at @s run summon minecraft:text_display ~ ~1.3 ~ {{Tags:["{ns}.start","{ns}.mk","smithed.entity","smithed.strict"],text:{{text:"▶ Départ",color:"green"}},billboard:"center"}}
scoreboard players operation @e[type=minecraft:text_display,tag={ns}.mk] {ns}.pid = #me {ns}.data
tag @e[type=minecraft:text_display,tag={ns}.mk] remove {ns}.mk
tellraw @s {{text:"------------------------------------------------",color:"dark_gray"}}
tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Enregistrement ",color:"green"}},{{storage:"{ns}:tmp",nbt:"meta.name",color:"gold"}},{{text:" démarré.",color:"green"}}]
function {ns}:v{version}/record/give
tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"[■ STOP]",color:"red",bold:true,click_event:{{action:"run_command",command:"/function #{ns}:v{major}/stop"}},hover_event:{{action:"show_text",value:"Arrêter l'enregistrement"}}}},{{text:"   "}},{{text:"[↺ STOP + retour au départ]",color:"red",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/stop_loop"}},hover_event:{{action:"show_text",value:"Arrêter et ramener au point de départ (boucle propre)"}}}}]
tellraw @s {{text:"------------------------------------------------",color:"dark_gray"}}
function #{ns}:v{major}/signals/on_record_start
""")

	write_versioned_function("record/brk", f"""
function {ns}:v{version}/record/snap
data modify storage {ns}:tmp ev set value {{t:0,k:4,x:0,y:0,z:0}}
execute store result storage {ns}:tmp ev.t int 1 run scoreboard players get @s {ns}.rtime
function {ns}:v{version}/record/curpos
function {ns}:v{version}/record/evpush with storage {ns}:ctx
""")

	write_versioned_function("record/cast", f"""
# rayon avec le marqueur d'événements du joueur (@s, à sa position)
scoreboard players operation #me {ns}.data = @s {ns}.pid
execute as @e[type=minecraft:marker,tag={ns}.ray] if score @s {ns}.pid = #me {ns}.data run tag @s add {ns}.cur
scoreboard players set #rs {ns}.data 0
scoreboard players set #hit {ns}.data 0
execute anchored eyes positioned ^ ^ ^ run function {ns}:v{version}/record/ray
""")

	write_versioned_function("record/chunk", f"""
$data modify storage {ns}:rec p.p$(pid).chunks append from storage {ns}:rec p.p$(pid).d
$data modify storage {ns}:rec p.p$(pid).d set value []
scoreboard players set @s {ns}.rkf 0
""")

	write_versioned_function("record/cleanup", f"""
scoreboard players operation #me {ns}.data = @s {ns}.pid
execute as @e[type=minecraft:text_display,tag={ns}.start] if score @s {ns}.pid = #me {ns}.data run kill @s
clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}]
title @s actionbar {{text:""}}
function {ns}:v{version}/record/killmk
""")

	write_versioned_function("record/click", f"""
scoreboard players set @s {ns}.use 0
execute if score #sk {ns}.data matches 1 run return run function {ns}:v{version}/record/close
function {ns}:v{version}/record/finish
""")

	write_versioned_function("record/close", f"""
function {ns}:v{version}/record/closeprep
function {ns}:v{version}/record/finish
""")

	write_versioned_function("record/closeloop", f"""
scoreboard players operation #dx {ns}.data = #rx {ns}.data
scoreboard players operation #dx {ns}.data /= #cs {ns}.data
scoreboard players operation #dy {ns}.data = #ry {ns}.data
scoreboard players operation #dy {ns}.data /= #cs {ns}.data
scoreboard players operation #dz {ns}.data = #rz {ns}.data
scoreboard players operation #dz {ns}.data /= #cs {ns}.data
scoreboard players operation #dyw {ns}.data = #ryw {ns}.data
scoreboard players operation #dyw {ns}.data /= #cs {ns}.data
scoreboard players operation #dpt {ns}.data = #rpt {ns}.data
scoreboard players operation #dpt {ns}.data /= #cs {ns}.data
scoreboard players operation #rx {ns}.data -= #dx {ns}.data
scoreboard players operation #ry {ns}.data -= #dy {ns}.data
scoreboard players operation #rz {ns}.data -= #dz {ns}.data
scoreboard players operation #ryw {ns}.data -= #dyw {ns}.data
scoreboard players operation #rpt {ns}.data -= #dpt {ns}.data
function {ns}:v{version}/record/append
scoreboard players remove #cs {ns}.data 1
execute if score #cs {ns}.data matches 1.. run function {ns}:v{version}/record/closeloop
""")

	write_versioned_function("record/closeprep", f"""
function {ns}:v{version}/record/ctx
scoreboard players set #fl {ns}.data 0
scoreboard players operation #rx {ns}.data = @s {ns}.rox
scoreboard players operation #rx {ns}.data -= @s {ns}.rpx
scoreboard players operation #ry {ns}.data = @s {ns}.roy
scoreboard players operation #ry {ns}.data -= @s {ns}.rpy
scoreboard players operation #rz {ns}.data = @s {ns}.roz
scoreboard players operation #rz {ns}.data -= @s {ns}.rpz
scoreboard players operation #ryw {ns}.data = @s {ns}.royw
scoreboard players operation #ryw {ns}.data -= @s {ns}.rpyw
execute if score #ryw {ns}.data matches 18001.. run scoreboard players remove #ryw {ns}.data 36000
execute if score #ryw {ns}.data matches ..-18001 run scoreboard players add #ryw {ns}.data 36000
scoreboard players operation #rpt {ns}.data = @s {ns}.ropt
scoreboard players operation #rpt {ns}.data -= @s {ns}.rppt
scoreboard players set #cs {ns}.data 10
function {ns}:v{version}/record/closeloop
""")

	write_versioned_function("record/ctx", f"""
execute store result storage {ns}:ctx pid int 1 run scoreboard players get @s {ns}.pid
""")

	write_versioned_function("record/cubexyz", f"""
# index #c7 -> coin d'un cube 3x3x3 isolé par des barrières, dans la zone 1 (x 17..31) : #cx #cy #cz
scoreboard players operation #cx {ns}.data = #c7 {ns}.data
scoreboard players operation #cx {ns}.data %= #4 {ns}.data
scoreboard players operation #cx {ns}.data *= #4 {ns}.data
scoreboard players add #cx {ns}.data 17
scoreboard players operation #cz {ns}.data = #c7 {ns}.data
scoreboard players operation #cz {ns}.data /= #4 {ns}.data
scoreboard players operation #cz {ns}.data %= #4 {ns}.data
scoreboard players operation #cz {ns}.data *= #4 {ns}.data
scoreboard players add #cz {ns}.data 1
scoreboard players operation #cy {ns}.data = #c7 {ns}.data
scoreboard players operation #cy {ns}.data /= #16 {ns}.data
scoreboard players operation #cy {ns}.data *= #4 {ns}.data
scoreboard players remove #cy {ns}.data 63
""")

	write_versioned_function("record/curpos", f"""
# position du bloc touché, relative au point de départ de l'enregistrement
execute store result score #hx {ns}.data run data get entity @e[type=minecraft:marker,tag={ns}.cur,limit=1] Pos[0]
execute store result score #hy {ns}.data run data get entity @e[type=minecraft:marker,tag={ns}.cur,limit=1] Pos[1]
execute store result score #hz {ns}.data run data get entity @e[type=minecraft:marker,tag={ns}.cur,limit=1] Pos[2]
scoreboard players operation #hx {ns}.data -= @s {ns}.rbx
scoreboard players operation #hy {ns}.data -= @s {ns}.rby
scoreboard players operation #hz {ns}.data -= @s {ns}.rbz
execute store result storage {ns}:tmp ev.x int 1 run scoreboard players get #hx {ns}.data
execute store result storage {ns}:tmp ev.y int 1 run scoreboard players get #hy {ns}.data
execute store result storage {ns}:tmp ev.z int 1 run scoreboard players get #hz {ns}.data
""")

	write_versioned_function("record/drop", f"""
$data remove storage {ns}:rec p.p$(pid)
""")

	write_versioned_function("record/eq", f"""
data modify storage {ns}:tmp neweq set value {{}}
data modify storage {ns}:tmp neweq set from entity @s equipment
data modify storage {ns}:tmp neweq.mainhand set from entity @s SelectedItem
execute if data storage {ns}:tmp neweq.mainhand.components."minecraft:custom_data"{{{ns}:{{stop:1b}}}} run data remove storage {ns}:tmp neweq.mainhand
execute if data storage {ns}:tmp neweq.offhand.components."minecraft:custom_data"{{{ns}:{{stop:1b}}}} run data remove storage {ns}:tmp neweq.offhand
execute if data storage {ns}:tmp neweq.mainhand.components."minecraft:custom_data"{{{ns}:{{menu:1b}}}} run data remove storage {ns}:tmp neweq.mainhand
execute if data storage {ns}:tmp neweq.offhand.components."minecraft:custom_data"{{{ns}:{{menu:1b}}}} run data remove storage {ns}:tmp neweq.offhand
# retire noms, lore, livres et données custom : invisibles sur l'entité, et ils casseraient la commande exportée (guillemets, apostrophes, taille)
data remove storage {ns}:tmp neweq.head.components."minecraft:custom_name"
data remove storage {ns}:tmp neweq.head.components."minecraft:item_name"
data remove storage {ns}:tmp neweq.head.components."minecraft:lore"
data remove storage {ns}:tmp neweq.head.components."minecraft:written_book_content"
data remove storage {ns}:tmp neweq.head.components."minecraft:writable_book_content"
data remove storage {ns}:tmp neweq.head.components."minecraft:container"
data remove storage {ns}:tmp neweq.head.components."minecraft:bundle_contents"
data remove storage {ns}:tmp neweq.head.components."minecraft:custom_data"
data remove storage {ns}:tmp neweq.chest.components."minecraft:custom_name"
data remove storage {ns}:tmp neweq.chest.components."minecraft:item_name"
data remove storage {ns}:tmp neweq.chest.components."minecraft:lore"
data remove storage {ns}:tmp neweq.chest.components."minecraft:written_book_content"
data remove storage {ns}:tmp neweq.chest.components."minecraft:writable_book_content"
data remove storage {ns}:tmp neweq.chest.components."minecraft:container"
data remove storage {ns}:tmp neweq.chest.components."minecraft:bundle_contents"
data remove storage {ns}:tmp neweq.chest.components."minecraft:custom_data"
data remove storage {ns}:tmp neweq.legs.components."minecraft:custom_name"
data remove storage {ns}:tmp neweq.legs.components."minecraft:item_name"
data remove storage {ns}:tmp neweq.legs.components."minecraft:lore"
data remove storage {ns}:tmp neweq.legs.components."minecraft:written_book_content"
data remove storage {ns}:tmp neweq.legs.components."minecraft:writable_book_content"
data remove storage {ns}:tmp neweq.legs.components."minecraft:container"
data remove storage {ns}:tmp neweq.legs.components."minecraft:bundle_contents"
data remove storage {ns}:tmp neweq.legs.components."minecraft:custom_data"
data remove storage {ns}:tmp neweq.feet.components."minecraft:custom_name"
data remove storage {ns}:tmp neweq.feet.components."minecraft:item_name"
data remove storage {ns}:tmp neweq.feet.components."minecraft:lore"
data remove storage {ns}:tmp neweq.feet.components."minecraft:written_book_content"
data remove storage {ns}:tmp neweq.feet.components."minecraft:writable_book_content"
data remove storage {ns}:tmp neweq.feet.components."minecraft:container"
data remove storage {ns}:tmp neweq.feet.components."minecraft:bundle_contents"
data remove storage {ns}:tmp neweq.feet.components."minecraft:custom_data"
data remove storage {ns}:tmp neweq.mainhand.components."minecraft:custom_name"
data remove storage {ns}:tmp neweq.mainhand.components."minecraft:item_name"
data remove storage {ns}:tmp neweq.mainhand.components."minecraft:lore"
data remove storage {ns}:tmp neweq.mainhand.components."minecraft:written_book_content"
data remove storage {ns}:tmp neweq.mainhand.components."minecraft:writable_book_content"
data remove storage {ns}:tmp neweq.mainhand.components."minecraft:container"
data remove storage {ns}:tmp neweq.mainhand.components."minecraft:bundle_contents"
data remove storage {ns}:tmp neweq.mainhand.components."minecraft:custom_data"
data remove storage {ns}:tmp neweq.offhand.components."minecraft:custom_name"
data remove storage {ns}:tmp neweq.offhand.components."minecraft:item_name"
data remove storage {ns}:tmp neweq.offhand.components."minecraft:lore"
data remove storage {ns}:tmp neweq.offhand.components."minecraft:written_book_content"
data remove storage {ns}:tmp neweq.offhand.components."minecraft:writable_book_content"
data remove storage {ns}:tmp neweq.offhand.components."minecraft:container"
data remove storage {ns}:tmp neweq.offhand.components."minecraft:bundle_contents"
data remove storage {ns}:tmp neweq.offhand.components."minecraft:custom_data"
data remove storage {ns}:tmp neweq.body.components."minecraft:custom_name"
data remove storage {ns}:tmp neweq.body.components."minecraft:item_name"
data remove storage {ns}:tmp neweq.body.components."minecraft:lore"
data remove storage {ns}:tmp neweq.body.components."minecraft:written_book_content"
data remove storage {ns}:tmp neweq.body.components."minecraft:writable_book_content"
data remove storage {ns}:tmp neweq.body.components."minecraft:container"
data remove storage {ns}:tmp neweq.body.components."minecraft:bundle_contents"
data remove storage {ns}:tmp neweq.body.components."minecraft:custom_data"
data remove storage {ns}:tmp neweq.saddle.components."minecraft:custom_name"
data remove storage {ns}:tmp neweq.saddle.components."minecraft:item_name"
data remove storage {ns}:tmp neweq.saddle.components."minecraft:lore"
data remove storage {ns}:tmp neweq.saddle.components."minecraft:written_book_content"
data remove storage {ns}:tmp neweq.saddle.components."minecraft:writable_book_content"
data remove storage {ns}:tmp neweq.saddle.components."minecraft:container"
data remove storage {ns}:tmp neweq.saddle.components."minecraft:bundle_contents"
data remove storage {ns}:tmp neweq.saddle.components."minecraft:custom_data"
function {ns}:v{version}/record/eqcmp with storage {ns}:ctx
""")

	write_versioned_function("record/eqcmp", f"""
$execute store success score #ch {ns}.data run data modify storage {ns}:rec p.p$(pid).eq set from storage {ns}:tmp neweq
$execute if score #ch {ns}.data matches 1 run data modify storage {ns}:rec p.p$(pid).e append value {{k:0,v:{{}}}}
$execute if score #ch {ns}.data matches 1 store result storage {ns}:rec p.p$(pid).e[-1].k int 1 run scoreboard players get @s {ns}.rkt
$execute if score #ch {ns}.data matches 1 run data modify storage {ns}:rec p.p$(pid).e[-1].v set from storage {ns}:tmp neweq
""")

	write_versioned_function("record/evpush", f"""
$data modify storage {ns}:rec p.p$(pid).a append from storage {ns}:tmp ev
""")

	write_versioned_function("record/exp", f"""
data modify storage {ns}:tmp ex set value {{}}
data modify storage {ns}:tmp ex.name set from storage {ns}:tmp meta.name
data modify storage {ns}:tmp ex.n set from storage {ns}:tmp meta.n
data modify storage {ns}:tmp ex.y set from storage {ns}:tmp meta.y
data modify storage {ns}:tmp ex.p set from storage {ns}:tmp meta.p
data modify storage {ns}:tmp ex.sx set from storage {ns}:tmp meta.sx
data modify storage {ns}:tmp ex.sy set from storage {ns}:tmp meta.sy
data modify storage {ns}:tmp ex.sz set from storage {ns}:tmp meta.sz
data modify storage {ns}:tmp ex.g set value ""
data modify storage {ns}:tmp ex.gr set value 50
data modify storage {ns}:tmp ex.g set from storage {ns}:tmp meta.g
data modify storage {ns}:tmp ex.gr set from storage {ns}:tmp meta.gr
execute store result storage {ns}:tmp ex.j int 1 run scoreboard players get #j {ns}.data
execute store result storage {ns}:tmp ex.m int 1 run scoreboard players get #m {ns}.data
data modify storage {ns}:tmp ex.k set value "chaîne"
data modify storage {ns}:tmp ex.kc set value "green"
execute if score #j {ns}.data matches 1 run data modify storage {ns}:tmp ex.k set value "impulsion"
execute if score #j {ns}.data matches 1 run data modify storage {ns}:tmp ex.kc set value "gold"
scoreboard players set #f {ns}.data 0
execute if score #j {ns}.data matches 1 run scoreboard players set #f {ns}.data 1
execute store result storage {ns}:tmp ex.f int 1 run scoreboard players get #f {ns}.data
scoreboard players set #isf {ns}.data 0
execute if score #split {ns}.data matches 1 if score #j {ns}.data = #c {ns}.data run scoreboard players set #isf {ns}.data 1
execute if score #isf {ns}.data matches 1 run function {ns}:v{version}/record/exp_es
execute if score #isf {ns}.data matches 0 if score #j {ns}.data < #m {ns}.data run function {ns}:v{version}/record/exp_d
execute if score #isf {ns}.data matches 0 if score #j {ns}.data >= #m {ns}.data run function {ns}:v{version}/record/exp_fin
scoreboard players add #j {ns}.data 1
execute if score #j {ns}.data <= #m {ns}.data run function {ns}:v{version}/record/exp
""")

	write_versioned_function("record/exp_d", f"""
data modify storage {ns}:tmp ex.d set from storage {ns}:tmp chunks[0]
data remove storage {ns}:tmp chunks[0]
function {ns}:v{version}/record/exp_part with storage {ns}:tmp ex
""")

	write_versioned_function("record/exp_es", f"""
data modify storage {ns}:tmp ex.e set from storage {ns}:tmp e
data modify storage {ns}:tmp ex.s set from storage {ns}:tmp s
data modify storage {ns}:tmp ex.a set from storage {ns}:tmp a
function {ns}:v{version}/record/exp_espart with storage {ns}:tmp ex
""")

	write_versioned_function("record/exp_espart", f"""
$tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"[Copier $(j)]",color:"yellow",bold:true,click_event:{{action:"copy_to_clipboard",value:'function #{ns}:v{major}/part {{with:{{f:$(f),d:[],e:$(e),s:$(s),a:$(a)}}}}'}},hover_event:{{action:"show_text",value:"Clique pour copier, puis colle dans un command block"}}}},{{text:"  → command block $(j) · ",color:"gray"}},{{text:"$(k)",color:"$(kc)"}},{{text:" · équipement et gestes",color:"gray"}}]
""")

	write_versioned_function("record/exp_fin", f"""
data modify storage {ns}:tmp ex.d set from storage {ns}:tmp chunks[0]
data remove storage {ns}:tmp chunks[0]
data modify storage {ns}:tmp ex.e set value []
data modify storage {ns}:tmp ex.s set value []
data modify storage {ns}:tmp ex.a set value []
execute if score #split {ns}.data matches 0 run data modify storage {ns}:tmp ex.a set from storage {ns}:tmp a
execute if score #split {ns}.data matches 0 run data modify storage {ns}:tmp ex.e set from storage {ns}:tmp e
execute if score #split {ns}.data matches 0 run data modify storage {ns}:tmp ex.s set from storage {ns}:tmp s
function {ns}:v{version}/record/exp_final with storage {ns}:tmp ex
""")

	write_versioned_function("record/exp_final", f"""
$tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"[Copier $(j)]",color:"yellow",bold:true,click_event:{{action:"copy_to_clipboard",value:'function #{ns}:v{major}/play {{with:{{name:"$(name)",pos:"$(sx) $(sy) $(sz)",entity:"minecraft:mannequin",range:0,size:1,loop:1,redstone:0,restore:1,hit_players:0,speed:100,delay:0,tag:"",group:"$(g)",group_radius:$(gr),pose:"",skin:"",texture:"",head:"",chest:"",legs:"",feet:"",mainhand:"",offhand:"",data:{{f:$(f),n:$(n),y:$(y),p:$(p),d:$(d),e:$(e),s:$(s),a:$(a)}}}}}}'}},hover_event:{{action:"show_text",value:"Clique pour copier, puis colle dans un command block"}}}},{{text:"  → command block $(j) · ",color:"gray"}},{{text:"$(k)",color:"$(kc)"}},{{text:" · lecture",color:"gray"}}]
""")

	write_versioned_function("record/exp_part", f"""
$tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"[Copier $(j)]",color:"yellow",bold:true,click_event:{{action:"copy_to_clipboard",value:'function #{ns}:v{major}/part {{with:{{f:$(f),d:$(d)}}}}'}},hover_event:{{action:"show_text",value:"Clique pour copier, puis colle dans un command block"}}}},{{text:"  → command block $(j) · ",color:"gray"}},{{text:"$(k)",color:"$(kc)"}}]
""")

	write_versioned_function("record/export", f"""
tellraw @s {{text:"------------------------------------------------",color:"dark_gray"}}
tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Séquence ",color:"green"}},{{storage:"{ns}:tmp",nbt:"meta.name",color:"gold"}},{{text:" prête à copier :",color:"green"}}]
execute store result score #c {ns}.data run data get storage {ns}:tmp chunks
scoreboard players set #ne {ns}.data 0
scoreboard players set #ns {ns}.data 0
execute store result score #ne {ns}.data run data get storage {ns}:tmp e
execute store result score #ns {ns}.data run data get storage {ns}:tmp s
scoreboard players set #na {ns}.data 0
execute store result score #na {ns}.data run data get storage {ns}:tmp a
scoreboard players set #split {ns}.data 0
execute if score #na {ns}.data matches 30.. run scoreboard players set #split {ns}.data 1
execute if score #ne {ns}.data matches 4.. run scoreboard players set #split {ns}.data 1
execute if score #ns {ns}.data matches 150.. run scoreboard players set #split {ns}.data 1
scoreboard players operation #m {ns}.data = #c {ns}.data
scoreboard players operation #m {ns}.data += #split {ns}.data
scoreboard players set #j {ns}.data 1
function {ns}:v{version}/record/exp
execute if score #m {ns}.data matches 1 run tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Colle-la dans un command block ",color:"green"}},{{text:"impulsion",color:"gold"}},{{text:".",color:"green"}}]
execute if score #m {ns}.data matches 2.. run tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Colle les blocs dans l'ordre : le 1 en ",color:"green"}},{{text:"impulsion",color:"gold"}},{{text:", les suivants en ",color:"green"}},{{text:"chaîne",color:"green",underlined:true}},{{text:" (toujours actif).",color:"green"}}]
tellraw @s {{text:"------------------------------------------------",color:"dark_gray"}}
""")

	write_versioned_function("record/finish", f"""
tag @s remove {ns}.on
function {ns}:v{version}/record/wrestore
function {ns}:v{version}/record/pull
function {ns}:v{version}/record/drop with storage {ns}:ctx
function {ns}:v{version}/record/cleanup
function #{ns}:v{major}/signals/on_record_stop
execute if score #kt {ns}.data matches 0 run return run tellraw @s {{text:"[Survirec] Séquence vide, rien à exporter.",color:"red"}}
execute if score #kf {ns}.data matches 1.. run data modify storage {ns}:tmp chunks append from storage {ns}:tmp d
function {ns}:v{version}/record/save
function {ns}:v{version}/record/export
""")

	write_versioned_function("record/give", f"""
scoreboard players set #given {ns}.data 0
scoreboard players set #hand {ns}.data 0
execute unless items entity @s weapon.mainhand * run item replace entity @s weapon.mainhand with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 1 run scoreboard players set #hand {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s hotbar.0 * run item replace entity @s hotbar.0 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s hotbar.0 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s hotbar.1 * run item replace entity @s hotbar.1 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s hotbar.1 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s hotbar.2 * run item replace entity @s hotbar.2 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s hotbar.2 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s hotbar.3 * run item replace entity @s hotbar.3 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s hotbar.3 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s hotbar.4 * run item replace entity @s hotbar.4 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s hotbar.4 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s hotbar.5 * run item replace entity @s hotbar.5 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s hotbar.5 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s hotbar.6 * run item replace entity @s hotbar.6 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s hotbar.6 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s hotbar.7 * run item replace entity @s hotbar.7 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s hotbar.7 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s hotbar.8 * run item replace entity @s hotbar.8 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s hotbar.8 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.0 * run item replace entity @s inventory.0 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.0 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.1 * run item replace entity @s inventory.1 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.1 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.2 * run item replace entity @s inventory.2 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.2 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.3 * run item replace entity @s inventory.3 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.3 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.4 * run item replace entity @s inventory.4 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.4 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.5 * run item replace entity @s inventory.5 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.5 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.6 * run item replace entity @s inventory.6 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.6 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.7 * run item replace entity @s inventory.7 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.7 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.8 * run item replace entity @s inventory.8 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.8 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.9 * run item replace entity @s inventory.9 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.9 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.10 * run item replace entity @s inventory.10 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.10 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.11 * run item replace entity @s inventory.11 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.11 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.12 * run item replace entity @s inventory.12 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.12 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.13 * run item replace entity @s inventory.13 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.13 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.14 * run item replace entity @s inventory.14 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.14 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.15 * run item replace entity @s inventory.15 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.15 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.16 * run item replace entity @s inventory.16 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.16 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.17 * run item replace entity @s inventory.17 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.17 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.18 * run item replace entity @s inventory.18 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.18 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.19 * run item replace entity @s inventory.19 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.19 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.20 * run item replace entity @s inventory.20 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.20 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.21 * run item replace entity @s inventory.21 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.21 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.22 * run item replace entity @s inventory.22 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.22 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.23 * run item replace entity @s inventory.23 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.23 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.24 * run item replace entity @s inventory.24 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.24 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.25 * run item replace entity @s inventory.25 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.25 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #given {ns}.data matches 0 unless items entity @s inventory.26 * run item replace entity @s inventory.26 with minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{stop:1b}},smithed:{{ignore:{{everything:1b}}}}}},minecraft:item_name={{text:"Arrêter l'enregistrement",color:"red"}},minecraft:item_model="minecraft:barrier"]
execute if score #given {ns}.data matches 0 if items entity @s inventory.26 minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run scoreboard players set #given {ns}.data 1
execute if score #hand {ns}.data matches 1 run tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Barrière en main : clic droit = stop.",color:"green"}}]
execute if score #hand {ns}.data matches 0 if score #given {ns}.data matches 1 run tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Barrière ajoutée à ton inventaire : prends-la en main, clic droit = stop.",color:"green"}}]
execute if score #given {ns}.data matches 0 run tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Inventaire plein : pas d'objet d'arrêt, utilise le bouton rouge.",color:"green"}}]
""")

	write_versioned_function("record/hud", f"""
execute if score @s {ns}.rchal matches 1 run return run function {ns}:v{version}/challenge/hud
scoreboard players operation #s {ns}.data = @s {ns}.rtime
scoreboard players operation #s {ns}.data /= #20 {ns}.data
scoreboard players operation #mn {ns}.data = #s {ns}.data
scoreboard players operation #mn {ns}.data /= #60 {ns}.data
scoreboard players operation #s {ns}.data %= #60 {ns}.data
execute if score #s {ns}.data matches 10.. run title @s actionbar [{{text:"● ",color:"red"}},{{text:"ENREGISTREMENT EN COURS ",color:"white",bold:true}},{{score:{{name:"#mn",objective:"{ns}.data"}},color:"yellow"}},{{text:":",color:"yellow"}},{{score:{{name:"#s",objective:"{ns}.data"}},color:"yellow"}}]
execute if score #s {ns}.data matches ..9 run title @s actionbar [{{text:"● ",color:"red"}},{{text:"ENREGISTREMENT EN COURS ",color:"white",bold:true}},{{score:{{name:"#mn",objective:"{ns}.data"}},color:"yellow"}},{{text:":0",color:"yellow"}},{{score:{{name:"#s",objective:"{ns}.data"}},color:"yellow"}}]
""")

	write_versioned_function("record/init", f"""
# démarre un enregistrement pour @s ; {ns}:tmp meta = {{name, n}} posé par l'appelant
execute unless score @s {ns}.pid matches 1.. run function {ns}:v{version}/challenge/newpid
function {ns}:v{version}/record/ctx
tag @s add {ns}.on
scoreboard players set @s {ns}.rchal 0
execute store result score @s {ns}.revery run data get storage {ns}:tmp meta.n
scoreboard players set @s {ns}.rkf 0
scoreboard players set @s {ns}.rkt 0
scoreboard players set @s {ns}.rtk 0
scoreboard players set @s {ns}.rtime 0
scoreboard players set @s {ns}.rlsw -1
execute store result score @s {ns}.rpx run data get entity @s Pos[0] 1000
execute store result score @s {ns}.rpy run data get entity @s Pos[1] 1000
execute store result score @s {ns}.rpz run data get entity @s Pos[2] 1000
execute store result score @s {ns}.rpyw run data get entity @s Rotation[0] 100
execute store result score @s {ns}.rppt run data get entity @s Rotation[1] 100
scoreboard players operation @s {ns}.rox = @s {ns}.rpx
scoreboard players operation @s {ns}.roy = @s {ns}.rpy
scoreboard players operation @s {ns}.roz = @s {ns}.rpz
scoreboard players operation @s {ns}.royw = @s {ns}.rpyw
scoreboard players operation @s {ns}.ropt = @s {ns}.rppt
execute store result storage {ns}:tmp meta.y int 1 run scoreboard players get @s {ns}.rpyw
execute store result storage {ns}:tmp meta.p int 1 run scoreboard players get @s {ns}.rppt
execute store result storage {ns}:tmp meta.sx double 0.001 run scoreboard players get @s {ns}.rpx
execute store result storage {ns}:tmp meta.sy double 0.001 run scoreboard players get @s {ns}.rpy
execute store result storage {ns}:tmp meta.sz double 0.001 run scoreboard players get @s {ns}.rpz
function {ns}:v{version}/record/initstore with storage {ns}:ctx
scoreboard players operation #me {ns}.data = @s {ns}.pid
function {ns}:v{version}/record/killmk
execute at @s run summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.rk","{ns}.eye","{ns}.mk2","smithed.entity","smithed.strict"]}}
execute at @s run summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.rk","{ns}.ray","{ns}.mk2","smithed.entity","smithed.strict"]}}
scoreboard players operation @e[type=minecraft:marker,tag={ns}.mk2] {ns}.pid = #me {ns}.data
tag @e[type=minecraft:marker,tag={ns}.mk2] remove {ns}.mk2
execute store result score @s {ns}.rbx run data get entity @s Pos[0]
execute store result score @s {ns}.rby run data get entity @s Pos[1]
execute store result score @s {ns}.rbz run data get entity @s Pos[2]
scoreboard players set @s {ns}.rlk 0
scoreboard players set @s {ns}.ruf 0
scoreboard players set @s {ns}.rplf 0
scoreboard players set @s {ns}.ratk -1
# emplacement du cube regardé (zone 2), propre à ce joueur
scoreboard players operation #c7 {ns}.data = @s {ns}.pid
scoreboard players operation #c7 {ns}.data %= #1536 {ns}.data
function {ns}:v{version}/record/cubexyz
scoreboard players operation @s {ns}.rlkx = #cx {ns}.data
scoreboard players add @s {ns}.rlkx 16
scoreboard players operation @s {ns}.rlky = #cy {ns}.data
scoreboard players operation @s {ns}.rlkz = #cz {ns}.data
scoreboard players add @s {ns}.sn 0
scoreboard players add @s {ns}.sw 0
scoreboard players add @s {ns}.gl 0
scoreboard players operation @s {ns}.snp = @s {ns}.sn
scoreboard players operation @s {ns}.swp = @s {ns}.sw
scoreboard players operation @s {ns}.glp = @s {ns}.gl
scoreboard players set @s {ns}.use 0
function {ns}:v{version}/record/eq
""")

	write_versioned_function("record/initstore", f"""
$data modify storage {ns}:rec p.p$(pid).meta set from storage {ns}:tmp meta
$data modify storage {ns}:rec p.p$(pid).d set value []
$data modify storage {ns}:rec p.p$(pid).chunks set value []
$data modify storage {ns}:rec p.p$(pid).e set value []
$data modify storage {ns}:rec p.p$(pid).s set value []
$data remove storage {ns}:rec p.p$(pid).eq
$data modify storage {ns}:rec p.p$(pid).a set value []
$data modify storage {ns}:rec p.p$(pid).wb set value []
""")

	write_versioned_function("record/key", f"""
scoreboard players set @s {ns}.rtk 0
execute store result score #cx {ns}.data run data get entity @s Pos[0] 1000
execute store result score #cy {ns}.data run data get entity @s Pos[1] 1000
execute store result score #cz {ns}.data run data get entity @s Pos[2] 1000
execute store result score #cyw {ns}.data run data get entity @s Rotation[0] 100
execute store result score #cpt {ns}.data run data get entity @s Rotation[1] 100
scoreboard players operation #dx {ns}.data = #cx {ns}.data
scoreboard players operation #dx {ns}.data -= @s {ns}.rpx
scoreboard players operation #dy {ns}.data = #cy {ns}.data
scoreboard players operation #dy {ns}.data -= @s {ns}.rpy
scoreboard players operation #dz {ns}.data = #cz {ns}.data
scoreboard players operation #dz {ns}.data -= @s {ns}.rpz
scoreboard players operation #dyw {ns}.data = #cyw {ns}.data
scoreboard players operation #dyw {ns}.data -= @s {ns}.rpyw
execute if score #dyw {ns}.data matches 18001.. run scoreboard players remove #dyw {ns}.data 36000
execute if score #dyw {ns}.data matches ..-18001 run scoreboard players add #dyw {ns}.data 36000
scoreboard players operation #dpt {ns}.data = #cpt {ns}.data
scoreboard players operation #dpt {ns}.data -= @s {ns}.rppt
scoreboard players operation @s {ns}.rpx = #cx {ns}.data
scoreboard players operation @s {ns}.rpy = #cy {ns}.data
scoreboard players operation @s {ns}.rpz = #cz {ns}.data
scoreboard players operation @s {ns}.rpyw = #cyw {ns}.data
scoreboard players operation @s {ns}.rppt = #cpt {ns}.data
function {ns}:v{version}/record/append
""")

	write_versioned_function("record/killmk", f"""
execute as @e[type=minecraft:marker,tag={ns}.rk] if score @s {ns}.pid = #me {ns}.data run kill @s
""")

	write_versioned_function("record/launch", f"""
tag @s remove {ns}.armed
title @s actionbar {{text:""}}
function {ns}:v{version}/record/ctx
function {ns}:v{version}/record/armload with storage {ns}:ctx
function {ns}:v{version}/record/begin
""")

	write_versioned_function("record/lkcopy", f"""
execute store result storage {ns}:tmp lk.x int 1 run scoreboard players get @s {ns}.rlkx
execute store result storage {ns}:tmp lk.y int 1 run scoreboard players get @s {ns}.rlky
execute store result storage {ns}:tmp lk.z int 1 run scoreboard players get @s {ns}.rlkz
function {ns}:v{version}/record/lkcopy2 with storage {ns}:tmp lk
""")

	write_versioned_function("record/lkcopy2", f"""
$execute at @e[type=minecraft:marker,tag={ns}.cur,limit=1] run clone ~-1 ~-1 ~-1 ~1 ~1 ~1 to {ns}:vault $(x) $(y) $(z) strict
""")

	write_versioned_function("record/look", f"""
scoreboard players operation #me {ns}.data = @s {ns}.pid
execute as @e[type=minecraft:marker,tag={ns}.eye] if score @s {ns}.pid = #me {ns}.data run tag @s add {ns}.cur
scoreboard players set #brk {ns}.data 0
execute if score @s {ns}.rlk matches 1 at @e[type=minecraft:marker,tag={ns}.cur,limit=1] if block ~ ~ ~ #minecraft:air run scoreboard players set #brk {ns}.data 1
execute if score #brk {ns}.data matches 1 run function {ns}:v{version}/record/brk
scoreboard players set @s {ns}.rlk 0
scoreboard players set #rs {ns}.data 0
scoreboard players set #hit {ns}.data 0
execute anchored eyes positioned ^ ^ ^ run function {ns}:v{version}/record/ray
execute if score #hit {ns}.data matches 1 run scoreboard players set @s {ns}.rlk 1
execute if score #hit {ns}.data matches 1 if data storage {ns}:cfg vault2 run function {ns}:v{version}/record/lkcopy
tag @e[type=minecraft:marker,tag={ns}.cur] remove {ns}.cur
""")

	write_versioned_function("record/marker", f"""
particle minecraft:happy_villager ~ ~-1.2 ~ 0.35 0 0.35 0 6
particle minecraft:end_rod ~ ~-1.2 ~ 0 0.8 0 0.01 2
""")

	write_versioned_function("record/place", f"""
scoreboard players set @s {ns}.rplf 1
function {ns}:v{version}/record/ctx
function {ns}:v{version}/record/snap
function {ns}:v{version}/record/cast
execute if score #hit {ns}.data matches 1 at @e[type=minecraft:marker,tag={ns}.cur,limit=1] run function {ns}:v{version}/record/place2
tag @e[type=minecraft:marker,tag={ns}.cur] remove {ns}.cur
""")

	write_versioned_function("record/place2", f"""
function {ns}:v{version}/block/read
execute if data storage {ns}:bk r{{id:""}} run return 0
data modify storage {ns}:tmp ev set value {{t:0,k:3,x:0,y:0,z:0,b:""}}
execute store result storage {ns}:tmp ev.t int 1 run scoreboard players get @s {ns}.rtime
function {ns}:v{version}/record/curpos
function {ns}:v{version}/block/full
data modify storage {ns}:tmp ev.b set from storage {ns}:bk full
function {ns}:v{version}/block/pair
execute if score #pair {ns}.data matches 1 run function {ns}:v{version}/record/place3
function {ns}:v{version}/record/evpush with storage {ns}:ctx
""")

	write_versioned_function("record/place3", f"""
# l'autre moitié d'un bloc double
scoreboard players operation #hx {ns}.data += #pdx {ns}.data
scoreboard players operation #hy {ns}.data += #pdy {ns}.data
scoreboard players operation #hz {ns}.data += #pdz {ns}.data
data modify storage {ns}:tmp ev.p set value {{x:0,y:0,z:0,b:""}}
execute store result storage {ns}:tmp ev.p.x int 1 run scoreboard players get #hx {ns}.data
execute store result storage {ns}:tmp ev.p.y int 1 run scoreboard players get #hy {ns}.data
execute store result storage {ns}:tmp ev.p.z int 1 run scoreboard players get #hz {ns}.data
execute store result storage {ns}:tmp pd.x int 1 run scoreboard players get #pdx {ns}.data
execute store result storage {ns}:tmp pd.y int 1 run scoreboard players get #pdy {ns}.data
execute store result storage {ns}:tmp pd.z int 1 run scoreboard players get #pdz {ns}.data
function {ns}:v{version}/record/place4 with storage {ns}:tmp pd
""")

	write_versioned_function("record/place4", f"""
$execute positioned ~$(x) ~$(y) ~$(z) run function {ns}:v{version}/record/place5
""")

	write_versioned_function("record/place5", f"""
function {ns}:v{version}/block/read
execute if data storage {ns}:bk r{{id:""}} run return run data remove storage {ns}:tmp ev.p
function {ns}:v{version}/block/full
data modify storage {ns}:tmp ev.p.b set from storage {ns}:bk full
""")

	write_versioned_function("record/pull", f"""
# copie l'enregistrement du joueur vers {ns}:tmp (et {ns}:c pour une épreuve) avant l'export
function {ns}:v{version}/record/ctx
data modify storage {ns}:tmp a set value []
function {ns}:v{version}/record/pull2 with storage {ns}:ctx
scoreboard players operation #kt {ns}.data = @s {ns}.rkt
scoreboard players operation #kf {ns}.data = @s {ns}.rkf
""")

	write_versioned_function("record/pull2", f"""
$data modify storage {ns}:tmp meta set from storage {ns}:rec p.p$(pid).meta
$data modify storage {ns}:tmp d set from storage {ns}:rec p.p$(pid).d
$data modify storage {ns}:tmp chunks set from storage {ns}:rec p.p$(pid).chunks
$data modify storage {ns}:tmp e set from storage {ns}:rec p.p$(pid).e
$data modify storage {ns}:tmp s set from storage {ns}:rec p.p$(pid).s
$data modify storage {ns}:c id set from storage {ns}:rec p.p$(pid).c.id
$data modify storage {ns}:c time set from storage {ns}:rec p.p$(pid).c.time
$data modify storage {ns}:c group set from storage {ns}:rec p.p$(pid).c.group
$data modify storage {ns}:c sync set from storage {ns}:rec p.p$(pid).c.sync
$data modify storage {ns}:c tp_back set from storage {ns}:rec p.p$(pid).c.tp_back
$data modify storage {ns}:c pid set from storage {ns}:rec p.p$(pid).c.pid
$data modify storage {ns}:c gid set from storage {ns}:rec p.p$(pid).c.gid
$data modify storage {ns}:tmp a set from storage {ns}:rec p.p$(pid).a
""")

	write_versioned_function("record/push", f"""
$data modify storage {ns}:rec p.p$(pid).d append from storage {ns}:tmp row
""")

	write_versioned_function("record/ray", f"""
# lancer de rayon depuis le regard (pas de 0,2 bloc, 5 blocs max) : le marqueur {ns}.cur va sur le bloc touché
scoreboard players add #rs {ns}.data 1
execute unless block ~ ~ ~ #{ns}:ray_pass run return run function {ns}:v{version}/record/rayhit
execute if score #rs {ns}.data matches 26.. run return 0
execute positioned ^ ^ ^0.2 run function {ns}:v{version}/record/ray
""")

	write_versioned_function("record/rayhit", f"""
execute align xyz run tp @e[type=minecraft:marker,tag={ns}.cur,limit=1] ~ ~ ~
scoreboard players set #hit {ns}.data 1
""")

	write_versioned_function("record/rejoin", f"""
# le joueur revient après une déconnexion : son enregistrement est abandonné
scoreboard players set @s {ns}.left 0
execute unless entity @s[tag={ns}.on] unless entity @s[tag={ns}.armed] run return 0
function {ns}:v{version}/record/abort1
tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Ton enregistrement a été annulé (déconnexion).",color:"yellow"}}]
""")

	write_versioned_function("record/save", f"""
# garde l'enregistrement dans le monde : rejouable par son nom, et réexportable depuis le menu
data modify storage {ns}:tmp rec set value {{}}
data modify storage {ns}:tmp rec.meta set from storage {ns}:tmp meta
data modify storage {ns}:tmp rec.chunks set from storage {ns}:tmp chunks
data modify storage {ns}:tmp rec.e set from storage {ns}:tmp e
data modify storage {ns}:tmp rec.s set from storage {ns}:tmp s
data modify storage {ns}:tmp rec.a set from storage {ns}:tmp a
data modify storage {ns}:tmp all set value []
data modify storage {ns}:tmp all append from storage {ns}:tmp chunks[][]
data modify storage {ns}:tmp seq set value {{}}
data modify storage {ns}:tmp seq.n set from storage {ns}:tmp meta.n
data modify storage {ns}:tmp seq.y set from storage {ns}:tmp meta.y
data modify storage {ns}:tmp seq.p set from storage {ns}:tmp meta.p
data modify storage {ns}:tmp seq.e set from storage {ns}:tmp e
data modify storage {ns}:tmp seq.s set from storage {ns}:tmp s
data modify storage {ns}:tmp seq.a set from storage {ns}:tmp a
data modify storage {ns}:tmp seq.d set from storage {ns}:tmp all
data remove storage {ns}:tmp all
function {ns}:v{version}/record/save2 with storage {ns}:tmp meta
execute store result storage {ns}:lib names[-1].pid int 1 run scoreboard players get @s {ns}.pid
""")

	write_versioned_function("record/save2", f"""
$data modify storage {ns}:lib recs.$(name) set from storage {ns}:tmp rec
$data modify storage {ns}:data seqs.$(name) set from storage {ns}:tmp seq
$data remove storage {ns}:lib names[{{name:"$(name)"}}]
$data modify storage {ns}:lib names append value {{name:"$(name)",pid:0}}
""")

	write_versioned_function("record/snap", f"""
# le joueur vient de casser, poser ou actionner : on garde l'état d'avant (cube copié au tick précédent)
execute unless data storage {ns}:cfg vault2 run return 0
execute unless score @s {ns}.rlk matches 1 run return 0
data modify storage {ns}:tmp sn set value {{}}
scoreboard players operation #me {ns}.data = @s {ns}.pid
execute as @e[type=minecraft:marker,tag={ns}.eye] if score @s {ns}.pid = #me {ns}.data run function {ns}:v{version}/record/snappos
execute unless data storage {ns}:tmp sn.x run return 0
execute store result storage {ns}:tmp sn.pid int 1 run scoreboard players get @s {ns}.pid
# même cube déjà gardé pendant cet enregistrement : la copie d'origine suffit
scoreboard players set #has {ns}.data 0
function {ns}:v{version}/record/snaphas with storage {ns}:tmp sn
execute if score #has {ns}.data matches 1 run return 0
execute if data storage {ns}:cfg cfree[0] run function {ns}:v{version}/record/snapreuse
execute unless data storage {ns}:tmp sn.bx run function {ns}:v{version}/record/snapnew
execute store result storage {ns}:tmp sn.lx int 1 run scoreboard players get @s {ns}.rlkx
execute store result storage {ns}:tmp sn.ly int 1 run scoreboard players get @s {ns}.rlky
execute store result storage {ns}:tmp sn.lz int 1 run scoreboard players get @s {ns}.rlkz
scoreboard players operation #c7 {ns}.data = @s {ns}.rlkx
execute store result storage {ns}:tmp sn.lx2 int 1 run scoreboard players add #c7 {ns}.data 2
scoreboard players operation #c7 {ns}.data = @s {ns}.rlky
execute store result storage {ns}:tmp sn.ly2 int 1 run scoreboard players add #c7 {ns}.data 2
scoreboard players operation #c7 {ns}.data = @s {ns}.rlkz
execute store result storage {ns}:tmp sn.lz2 int 1 run scoreboard players add #c7 {ns}.data 2
execute store result storage {ns}:tmp sn.pid int 1 run scoreboard players get @s {ns}.pid
function {ns}:v{version}/record/snap2 with storage {ns}:tmp sn
""")

	write_versioned_function("record/snap2", f"""
$execute in {ns}:vault run clone $(lx) $(ly) $(lz) $(lx2) $(ly2) $(lz2) $(bx) $(by) $(bz) strict
$data modify storage {ns}:rec p.p$(pid).wb append value {{bx:$(bx),by:$(by),bz:$(bz),bx2:$(bx2),by2:$(by2),bz2:$(bz2),x:$(x),y:$(y),z:$(z)}}
""")

	write_versioned_function("record/snaphas", f"""
$execute if data storage {ns}:rec p.p$(pid).wb[{{x:$(x),y:$(y),z:$(z)}}] run scoreboard players set #has {ns}.data 1
""")

	write_versioned_function("record/snapnew", f"""
scoreboard players operation #c7 {ns}.data = #cs {ns}.data
function {ns}:v{version}/record/cubexyz
scoreboard players add #cs {ns}.data 1
execute if score #cs {ns}.data matches 1536.. run scoreboard players set #cs {ns}.data 0
execute store result storage {ns}:tmp sn.bx int 1 run scoreboard players get #cx {ns}.data
execute store result storage {ns}:tmp sn.by int 1 run scoreboard players get #cy {ns}.data
execute store result storage {ns}:tmp sn.bz int 1 run scoreboard players get #cz {ns}.data
execute store result storage {ns}:tmp sn.bx2 int 1 run scoreboard players add #cx {ns}.data 2
execute store result storage {ns}:tmp sn.by2 int 1 run scoreboard players add #cy {ns}.data 2
execute store result storage {ns}:tmp sn.bz2 int 1 run scoreboard players add #cz {ns}.data 2
""")

	write_versioned_function("record/snappos", f"""
execute store result score #sx {ns}.data run data get entity @s Pos[0]
execute store result score #sy {ns}.data run data get entity @s Pos[1]
execute store result score #sz {ns}.data run data get entity @s Pos[2]
execute store result storage {ns}:tmp sn.x int 1 run scoreboard players remove #sx {ns}.data 1
execute store result storage {ns}:tmp sn.y int 1 run scoreboard players remove #sy {ns}.data 1
execute store result storage {ns}:tmp sn.z int 1 run scoreboard players remove #sz {ns}.data 1
""")

	write_versioned_function("record/snapreuse", f"""
data modify storage {ns}:tmp sn.bx set from storage {ns}:cfg cfree[-1].bx
data modify storage {ns}:tmp sn.by set from storage {ns}:cfg cfree[-1].by
data modify storage {ns}:tmp sn.bz set from storage {ns}:cfg cfree[-1].bz
data modify storage {ns}:tmp sn.bx2 set from storage {ns}:cfg cfree[-1].bx2
data modify storage {ns}:tmp sn.by2 set from storage {ns}:cfg cfree[-1].by2
data modify storage {ns}:tmp sn.bz2 set from storage {ns}:cfg cfree[-1].bz2
data remove storage {ns}:cfg cfree[-1]
""")

	write_versioned_function("record/swing", f"""
execute if score @s {ns}.rlsw = @s {ns}.rtime run return 0
scoreboard players operation @s {ns}.rlsw = @s {ns}.rtime
function {ns}:v{version}/record/ctx
function {ns}:v{version}/record/swpush with storage {ns}:ctx
""")

	write_versioned_function("record/swpush", f"""
$data modify storage {ns}:rec p.p$(pid).s append value 0
$execute store result storage {ns}:rec p.p$(pid).s[-1] int 1 run scoreboard players get @s {ns}.rtime
""")

	write_versioned_function("record/tick", f"""
function {ns}:v{version}/record/ctx
execute if score @s {ns}.ruf matches 1 run function {ns}:v{version}/record/usego
scoreboard players set @s {ns}.rplf 0
function {ns}:v{version}/record/look
scoreboard players set #fl {ns}.data 0
scoreboard players set #sk {ns}.data 0
execute if score @s {ns}.sn > @s {ns}.snp run scoreboard players set #sk {ns}.data 1
execute if score #sk {ns}.data matches 1 run scoreboard players add #fl {ns}.data 1
execute if score @s {ns}.sw > @s {ns}.swp run scoreboard players add #fl {ns}.data 2
execute if score @s {ns}.gl > @s {ns}.glp run scoreboard players add #fl {ns}.data 4
scoreboard players operation @s {ns}.snp = @s {ns}.sn
scoreboard players operation @s {ns}.swp = @s {ns}.sw
scoreboard players operation @s {ns}.glp = @s {ns}.gl
execute unless score @s {ns}.rchal matches 1 if score @s {ns}.use matches 1.. if items entity @s weapon.* minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{stop:1b}}}}] run return run function {ns}:v{version}/record/click
scoreboard players set @s {ns}.use 0
scoreboard players add @s {ns}.rtime 1
execute if score @s {ns}.rchal matches 1 if score @s {ns}.rtime >= @s {ns}.rcdur run return run function {ns}:v{version}/challenge/end
scoreboard players operation #q {ns}.data = @s {ns}.rtime
scoreboard players operation #q {ns}.data %= #10 {ns}.data
execute if score #q {ns}.data matches 0 run function {ns}:v{version}/record/hud
scoreboard players operation #q {ns}.data = @s {ns}.rtime
scoreboard players operation #q {ns}.data %= #20 {ns}.data
execute if score #q {ns}.data matches 0 run function {ns}:v{version}/record/eq
scoreboard players add @s {ns}.rtk 1
execute if score @s {ns}.rtk >= @s {ns}.revery run function {ns}:v{version}/record/key
""")

	write_versioned_function("record/use", f"""
function {ns}:v{version}/record/cast
execute if score #hit {ns}.data matches 1 at @e[type=minecraft:marker,tag={ns}.cur,limit=1] if block ~ ~ ~ #{ns}:interactive run function {ns}:v{version}/record/use2
tag @e[type=minecraft:marker,tag={ns}.cur] remove {ns}.cur
""")

	write_versioned_function("record/use2", f"""
execute store result score @s {ns}.rux run data get entity @e[type=minecraft:marker,tag={ns}.cur,limit=1] Pos[0]
execute store result score @s {ns}.ruy run data get entity @e[type=minecraft:marker,tag={ns}.cur,limit=1] Pos[1]
execute store result score @s {ns}.ruz run data get entity @e[type=minecraft:marker,tag={ns}.cur,limit=1] Pos[2]
scoreboard players operation @s {ns}.rut = @s {ns}.rtime
scoreboard players set @s {ns}.ruf 1
""")

	write_versioned_function("record/usego", f"""
scoreboard players set @s {ns}.ruf 0
execute if score @s {ns}.rplf matches 1 run return 0
function {ns}:v{version}/record/snap
data modify storage {ns}:tmp ev set value {{t:0,k:2,x:0,y:0,z:0}}
execute store result storage {ns}:tmp ev.t int 1 run scoreboard players get @s {ns}.rut
scoreboard players operation #hx {ns}.data = @s {ns}.rux
scoreboard players operation #hx {ns}.data -= @s {ns}.rbx
scoreboard players operation #hy {ns}.data = @s {ns}.ruy
scoreboard players operation #hy {ns}.data -= @s {ns}.rby
scoreboard players operation #hz {ns}.data = @s {ns}.ruz
scoreboard players operation #hz {ns}.data -= @s {ns}.rbz
execute store result storage {ns}:tmp ev.x int 1 run scoreboard players get #hx {ns}.data
execute store result storage {ns}:tmp ev.y int 1 run scoreboard players get #hy {ns}.data
execute store result storage {ns}:tmp ev.z int 1 run scoreboard players get #hz {ns}.data
function {ns}:v{version}/record/evpush with storage {ns}:ctx
""")

	write_versioned_function("record/wr0", f"""
$data modify storage {ns}:tmp wbl set from storage {ns}:rec p.p$(pid).wb
$data modify storage {ns}:rec p.p$(pid).wb set value []
""")

	write_versioned_function("record/wr1", f"""
function {ns}:v{version}/record/wr2 with storage {ns}:tmp wbl[-1]
data remove storage {ns}:tmp wbl[-1]
execute if data storage {ns}:tmp wbl[0] run function {ns}:v{version}/record/wr1
""")

	write_versioned_function("record/wr2", f"""
$clone from {ns}:vault $(bx) $(by) $(bz) $(bx2) $(by2) $(bz2) $(x) $(y) $(z)
$execute in {ns}:vault run fill $(bx) $(by) $(bz) $(bx2) $(by2) $(bz2) minecraft:barrier strict
$data modify storage {ns}:cfg cfree append value {{bx:$(bx),by:$(by),bz:$(bz),bx2:$(bx2),by2:$(by2),bz2:$(bz2)}}
""")

	write_versioned_function("record/wrestore", f"""
# remet le monde comme avant l'enregistrement (en tant que joueur)
function {ns}:v{version}/record/ctx
data modify storage {ns}:tmp wbl set value []
function {ns}:v{version}/record/wr0 with storage {ns}:ctx
execute if data storage {ns}:tmp wbl[0] at @s run function {ns}:v{version}/record/wr1
""")

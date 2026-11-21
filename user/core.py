""" Management functions shared by the entry points (validation, kill, reset, groups, export...). """
# Imports
from stewbeet import Mem, write_versioned_function


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	major: str = version.split(".")[0]

	write_versioned_function("abort", f"""
# joueur : annule son propre enregistrement. command block / console : annule tous les enregistrements
execute if entity @s[type=minecraft:player] unless entity @s[tag={ns}.on] unless entity @s[tag={ns}.armed] run return run tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Tu n'as aucun enregistrement en cours.",color:"red"}}]
execute if entity @s[type=minecraft:player] run function {ns}:v{version}/record/abort1
execute if entity @s[type=minecraft:player] run return run tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Enregistrement annulé.",color:"yellow"}}]
execute as @a[tag={ns}.on] run function {ns}:v{version}/record/abort1
execute as @a[tag={ns}.armed] run function {ns}:v{version}/record/abort1
""")

	write_versioned_function("again", f"""
# Relance une séquence déjà chargée dans CE monde (sans les données)
$data modify storage {ns}:in a set value {{name:"$(name)",entity:"$(entity)",range:$(range),grp:$(grp),gl:$(gl),group:"$(group)",gr:$(group_radius),size:$(size),loop:$(loop),rsb:$(redstone),cbx:$(cbx),cby:$(cby),cbz:$(cbz),restore:$(restore),hitp:$(hit_players),speed:$(speed),offset:$(delay),tag:"$(tag)",pose:"$(pose)",skin:"$(skin)",texture:"$(texture)",head:"$(head)",chest:"$(chest)",legs:"$(legs)",feet:"$(feet)",mainhand:"$(mainhand)",offhand:"$(offhand)"}}
$execute positioned $(pos) run function {ns}:v{version}/spawn/spawn
""")

	write_versioned_function("badname", f"""
tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Nom invalide : ",color:"red"}},{{text:"lettres, chiffres et _ uniquement",color:"gold",bold:true}},{{text:" (1 à 32 caractères).",color:"red"}}]
""")

	write_versioned_function("challenge", f"""
# execute as @p run function #{ns}:v{major}/challenge {{with:{{id:"a",time:5,group:"salle1",sync:0,tp_back:1}}}}
$data merge storage {ns}:cin {{id:"$(id)",time:$(time),group:"$(group)",sync:$(sync),tp_back:$(tp_back)}}
function {ns}:v{version}/challenge/start
""")

	write_versioned_function("debug", f"""
tag @s add {ns}.dbg
tellraw @s {{text:"[Survirec] diagnostic",color:"gold",bold:true}}
execute store result score #dbg {ns}.data if entity @a[tag={ns}.on]
execute store result score #dbg2 {ns}.data if entity @a[tag={ns}.armed]
tellraw @s [{{text:"  Enregistrements : ",color:"gray"}},{{score:{{name:"#dbg",objective:"{ns}.data"}},color:"aqua"}},{{text:"   armés : ",color:"gray"}},{{score:{{name:"#dbg2",objective:"{ns}.data"}},color:"aqua"}}]
execute as @a[tag={ns}.on] run tellraw @a[tag={ns}.dbg] [{{text:"  ● ",color:"red"}},{{selector:"@s",color:"white"}},{{text:"  ",color:"gray"}},{{score:{{name:"@s",objective:"{ns}.rtime"}},color:"aqua"}},{{text:" ticks, ",color:"gray"}},{{score:{{name:"@s",objective:"{ns}.rkt"}},color:"aqua"}},{{text:" keyframes",color:"gray"}}]
execute as @a[tag={ns}.armed] run tellraw @a[tag={ns}.dbg] [{{text:"  ⏳ ",color:"gold"}},{{selector:"@s",color:"white"}},{{text:"  attend le groupe ",color:"gray"}},{{score:{{name:"@s",objective:"{ns}.rwg"}},color:"aqua"}}]
execute store result score #dbg {ns}.data if entity @e[tag={ns}.m]
tellraw @s [{{text:"  Entités animées : ",color:"gray"}},{{score:{{name:"#dbg",objective:"{ns}.data"}},color:"aqua"}}]
execute as @e[tag={ns}.m] run tellraw @a[tag={ns}.dbg] [{{text:"  • groupe ",color:"gray"}},{{score:{{name:"@s",objective:"{ns}.grp"}},color:"gold",bold:true}},{{text:"  en lecture ",color:"gray"}},{{score:{{name:"@s",objective:"{ns}.run"}},color:"gold",bold:true}},{{text:"  ",color:"gray"}},{{nbt:"Tags",entity:"@s",color:"aqua"}}]
tag @s remove {ns}.dbg
""")

	write_versioned_function("export", f"""
$execute unless data storage {ns}:lib recs.$(name) run return run tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Aucun enregistrement nommé ",color:"red"}},{{text:"$(name)",color:"gold"}},{{text:".",color:"red"}}]
$data modify storage {ns}:tmp meta set from storage {ns}:lib recs.$(name).meta
$data modify storage {ns}:tmp chunks set from storage {ns}:lib recs.$(name).chunks
$data modify storage {ns}:tmp e set from storage {ns}:lib recs.$(name).e
$data modify storage {ns}:tmp s set from storage {ns}:lib recs.$(name).s
data modify storage {ns}:tmp a set value []
$data modify storage {ns}:tmp a set from storage {ns}:lib recs.$(name).a
function {ns}:v{version}/record/export
""")

	write_versioned_function("forget", f"""
# Supprime une séquence du monde (données de lecture et enregistrement gardé)
$data remove storage {ns}:data seqs.$(name)
$data remove storage {ns}:lib recs.$(name)
$data remove storage {ns}:lib names[{{name:"$(name)"}}]
$tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Séquence ",color:"green"}},{{text:"$(name)",color:"gold"}},{{text:" supprimée.",color:"green"}}]
""")

	write_versioned_function("group_restart", f"""
# radius > 0 : relance la scène de ce nom la plus proche. radius 0 : relance toutes les scènes de ce nom
$execute if data storage {ns}:in cfg{{radius:0}} as @e[tag={ns}.m,tag={ns}.g.$(group)] run scoreboard players set @s {ns}.rs 1
scoreboard players set #found {ns}.data 0
$execute unless data storage {ns}:in cfg{{radius:0}} as @e[tag={ns}.m,tag={ns}.g.$(group),distance=..$(radius),sort=nearest,limit=1] run scoreboard players operation #found {ns}.data = @s {ns}.grp
execute if score #found {ns}.data matches 1.. as @e[tag={ns}.m] if score @s {ns}.grp = #found {ns}.data run scoreboard players set @s {ns}.rs 1
function {ns}:v{version}/playback/grpfire
""")

	write_versioned_function("help", f"""
tellraw @s {{text:"══ SURVIREC · AIDE ══",color:"gold"}}
tellraw @s [{{text:"   "}},{{text:"[🎬 Ouvrir le menu]",color:"gold",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/menu"}},hover_event:{{action:"show_text",value:"Interface Survirec"}}}},{{text:"  "}},{{text:"[Recevoir l'objet]",color:"yellow",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/menu_item"}},hover_event:{{action:"show_text",value:"Objet qui ouvre le menu d'un clic droit"}}}}]
tellraw @s [{{text:"   "}},{{text:"[1] Enregistrer",color:"aqua",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help_page {{with:{{page:1}}}}"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}}]
tellraw @s [{{text:"   "}},{{text:"[2] Lancer",color:"aqua",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help_page {{with:{{page:2}}}}"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}}]
tellraw @s [{{text:"   "}},{{text:"[3] Champs",color:"aqua",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help_page {{with:{{page:3}}}}"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}}]
tellraw @s [{{text:"   "}},{{text:"[4] Épreuve",color:"aqua",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help_page {{with:{{page:4}}}}"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}}]
tellraw @s [{{text:"   "}},{{text:"[5] Gérer",color:"aqua",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help_page {{with:{{page:5}}}}"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}}]
""")

	write_versioned_function("import", f"""
execute if data storage {ns}:in cfg.data{{f:1}} run data modify storage {ns}:t pend set value []
execute if data storage {ns}:in cfg.data{{f:1}} run data modify storage {ns}:t pend_e set value []
execute if data storage {ns}:in cfg.data{{f:1}} run data modify storage {ns}:t pend_s set value []
execute if data storage {ns}:in cfg.data{{f:1}} run data modify storage {ns}:t pend_a set value []
execute unless data storage {ns}:t pend run data modify storage {ns}:t pend set value []
execute unless data storage {ns}:t pend_e run data modify storage {ns}:t pend_e set value []
execute unless data storage {ns}:t pend_s run data modify storage {ns}:t pend_s set value []
execute unless data storage {ns}:t pend_a run data modify storage {ns}:t pend_a set value []
data modify storage {ns}:t pend append from storage {ns}:in cfg.data.d[]
data modify storage {ns}:t pend_e append from storage {ns}:in cfg.data.e[]
data modify storage {ns}:t pend_s append from storage {ns}:in cfg.data.s[]
data modify storage {ns}:t pend_a append from storage {ns}:in cfg.data.a[]
data modify storage {ns}:in seq set value {{}}
data modify storage {ns}:in seq.n set from storage {ns}:in cfg.data.n
data modify storage {ns}:in seq.y set from storage {ns}:in cfg.data.y
data modify storage {ns}:in seq.p set from storage {ns}:in cfg.data.p
data modify storage {ns}:in seq.e set from storage {ns}:t pend_e
data modify storage {ns}:in seq.s set from storage {ns}:t pend_s
data modify storage {ns}:in seq.a set from storage {ns}:t pend_a
data modify storage {ns}:in seq.d set from storage {ns}:t pend
function {ns}:v{version}/store_seq with storage {ns}:in cfg
data remove storage {ns}:t pend
data remove storage {ns}:t pend_e
data remove storage {ns}:t pend_s
data remove storage {ns}:t pend_a
""")

	write_versioned_function("kill", f"""
scoreboard players set #kres {ns}.data 1
# function {ns}:v{version}/kill {{tag:"porte_nord"}}
$execute as @e[tag={ns}.t.$(tag)] run function {ns}:v{version}/playback/delete
scoreboard players set #kres {ns}.data 0
""")

	write_versioned_function("kill_all", f"""
scoreboard players set #kres {ns}.data 1
execute as @e[tag={ns}.x] run function {ns}:v{version}/playback/delete
scoreboard players set #kres {ns}.data 0
execute if data storage {ns}:cfg vault in {ns}:vault if loaded 0 0 0 run function {ns}:v{version}/vault/wipe
""")

	write_versioned_function("kill_name", f"""
scoreboard players set #kres {ns}.data 1
# function {ns}:v{version}/kill_name {{name:"walk"}}
$execute as @e[tag={ns}.n.$(name)] run function {ns}:v{version}/playback/delete
scoreboard players set #kres {ns}.data 0
""")

	write_versioned_function("near", f"""
# Toutes les 10 ticks : un mannequin n'est animé que si un joueur est à moins de r blocs
$execute as @e[tag={ns}.m,tag=!{ns}.rg] at @s store success score @s {ns}.near if entity @a[distance=..$(r)]
""")

	write_versioned_function("pgroup", f"""
# groupe local : l'identifiant est résolu à l'apparition (p/gjoin), selon les entités du même groupe à proximité
data modify storage {ns}:in cfg.grp set value -1
data modify storage {ns}:in cfg.gl set from storage {ns}:in cfg.loop
data modify storage {ns}:in cfg.loop set value 0
""")

	write_versioned_function("range", f"""
# function {ns}:v{version}/range {{r:128}}
$data modify storage {ns}:cfg r set value $(r)
""")

	write_versioned_function("reset", f"""
execute as @a[tag={ns}.on] run function #{ns}:v{major}/signals/on_record_stop
execute as @a[tag={ns}.on] at @s run function {ns}:v{version}/record/wrestore
tag @a remove {ns}.on
tag @a remove {ns}.armed
execute as @a run function {ns}:v{version}/record/cleanup
scoreboard players set @a {ns}.rchal 0
kill @e[type=minecraft:text_display,tag={ns}.start]
kill @e[type=minecraft:marker,tag={ns}.rk]
execute as @e[type=minecraft:marker,tag={ns}.pulse] at @s run function {ns}:v{version}/playback/pulseoff
scoreboard players set #npulse {ns}.data 0
data remove storage {ns}:rec p
tellraw @s {{text:"[Survirec] État réinitialisé.",color:"green"}}
""")

	write_versioned_function("rngchk", f"""
execute store result storage {ns}:t rng int 1 run scoreboard players get @s {ns}.rng
function {ns}:v{version}/rngchk2 with storage {ns}:t
""")

	write_versioned_function("rngchk2", f"""
$execute store success score @s {ns}.near if entity @a[distance=..$(rng)]
""")

	write_versioned_function("start", f"""
# function {ns}:v{version}/start {{name:"walk",every:4}}
execute unless entity @s[type=minecraft:player] run return fail
execute if entity @s[tag={ns}.on] run return run tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Tu es déjà en train d'enregistrer (",color:"red"}},{{text:"#{ns}:v{major}/stop",color:"gold"}},{{text:").",color:"red"}}]
execute if entity @s[tag={ns}.armed] run return run tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Ton enregistrement est déjà armé (",color:"red"}},{{text:"#{ns}:v{major}/abort",color:"gold"}},{{text:" pour l'annuler).",color:"red"}}]
$scoreboard players set #n {ns}.data $(every)
execute unless score #n {ns}.data matches 1..100 run return run tellraw @s {{text:"[Survirec] every doit être entre 1 et 100.",color:"red"}}
$data modify storage {ns}:tmp meta set value {{name:"$(name)",n:$(every),g:"$(group)",gr:$(group_radius)}}
execute if data storage {ns}:in cfg{{group:""}} run return run function {ns}:v{version}/record/begin
function {ns}:v{version}/record/armg with storage {ns}:in cfg
""")

	write_versioned_function("stop", f"""
# joueur : arrête son propre enregistrement. command block / console : arrête tous les enregistrements
execute if entity @s[type=minecraft:player,tag={ns}.on] run return run function {ns}:v{version}/stop1
execute if entity @s[type=minecraft:player] run return run tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Tu n'as aucun enregistrement en cours.",color:"red"}}]
execute as @a[tag={ns}.on] run function {ns}:v{version}/stop1
""")

	write_versioned_function("stop1", f"""
# une épreuve ne s'arrête pas à la main : elle est annulée
execute if score @s {ns}.rchal matches 1 run return run function {ns}:v{version}/record/abort1
function {ns}:v{version}/record/finish
""")

	write_versioned_function("stop_loop", f"""
# joueur : arrête son propre enregistrement. command block / console : arrête tous les enregistrements
execute if entity @s[type=minecraft:player,tag={ns}.on] run return run function {ns}:v{version}/stop_loop1
execute if entity @s[type=minecraft:player] run return run tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Tu n'as aucun enregistrement en cours.",color:"red"}}]
execute as @a[tag={ns}.on] run function {ns}:v{version}/stop_loop1
""")

	write_versioned_function("stop_loop1", f"""
# une épreuve ne s'arrête pas à la main : elle est annulée
execute if score @s {ns}.rchal matches 1 run return run function {ns}:v{version}/record/abort1
function {ns}:v{version}/record/close
""")

	write_versioned_function("store_seq", f"""
$data modify storage {ns}:data seqs.$(name) set from storage {ns}:in seq
""")

	write_versioned_function("validate", f"""
# Valide la chaîne de {ns}:v s : lettres, chiffres et _ , 1 à 32 caractères. Résultat : #valid 1 ou 0
scoreboard players set #valid {ns}.data 1
scoreboard players set #vlen {ns}.data 0
execute store result score #vlen {ns}.data run data get storage {ns}:v s
execute unless score #vlen {ns}.data matches 1..32 run return run scoreboard players set #valid {ns}.data 0
scoreboard players set #vi {ns}.data 0
function {ns}:v{version}/vloop
""")

	write_versioned_function("vchar", f"""
data remove storage {ns}:v c
$data modify storage {ns}:v c set string storage {ns}:v s $(i) $(j)
scoreboard players set #ok {ns}.data 0
execute if data storage {ns}:v {{c:"a"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"b"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"c"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"d"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"e"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"f"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"g"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"h"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"i"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"j"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"k"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"l"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"m"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"n"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"o"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"p"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"q"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"r"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"s"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"t"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"u"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"v"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"w"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"x"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"y"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"z"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"A"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"B"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"C"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"D"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"E"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"F"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"G"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"H"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"I"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"J"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"K"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"L"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"M"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"N"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"O"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"P"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"Q"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"R"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"S"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"T"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"U"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"V"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"W"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"X"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"Y"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"Z"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"0"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"1"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"2"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"3"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"4"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"5"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"6"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"7"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"8"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"9"}} run scoreboard players set #ok {ns}.data 1
execute if data storage {ns}:v {{c:"_"}} run scoreboard players set #ok {ns}.data 1
execute if score #ok {ns}.data matches 0 run scoreboard players set #valid {ns}.data 0
""")

	write_versioned_function("vloop", f"""
execute store result storage {ns}:v idx.i int 1 run scoreboard players get #vi {ns}.data
scoreboard players add #vi {ns}.data 1
execute store result storage {ns}:v idx.j int 1 run scoreboard players get #vi {ns}.data
function {ns}:v{version}/vchar with storage {ns}:v idx
execute if score #valid {ns}.data matches 1 if score #vi {ns}.data < #vlen {ns}.data run function {ns}:v{version}/vloop
""")

	write_versioned_function("vopt", f"""
# comme vreq, mais un champ vide est accepté
$execute unless data storage {ns}:in cfg{{$(f):""}} run function {ns}:v{version}/vreq with storage {ns}:v q
""")

	write_versioned_function("vreq", f"""
# $(f) = champ de {ns}:in cfg à valider (obligatoire)
data remove storage {ns}:v s
$data modify storage {ns}:v s set from storage {ns}:in cfg.$(f)
function {ns}:v{version}/validate
execute if score #valid {ns}.data matches 0 run scoreboard players set #bad {ns}.data 1
""")

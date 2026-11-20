tag @s remove survirec.on
scoreboard players set @s survirec.rchal 0
function survirec:v1/private/r/wrestore
function survirec:v1/private/r/pull
function survirec:v1/private/r/drop with storage survirec:ctx
title @s actionbar {text:""}
scoreboard players operation #me survirec.v = @s survirec.pid
function survirec:v1/private/r/killmk
data modify storage survirec:tmp all set value []
data modify storage survirec:tmp all append from storage survirec:tmp chunks[][]
data modify storage survirec:tmp all append from storage survirec:tmp d[]
data modify storage survirec:tmp seq set value {}
data modify storage survirec:tmp seq.n set from storage survirec:tmp meta.n
data modify storage survirec:tmp seq.y set from storage survirec:tmp meta.y
data modify storage survirec:tmp seq.p set from storage survirec:tmp meta.p
data modify storage survirec:tmp seq.e set from storage survirec:tmp e
data modify storage survirec:tmp seq.s set from storage survirec:tmp s
data modify storage survirec:tmp seq.a set from storage survirec:tmp a
data modify storage survirec:tmp seq.d set from storage survirec:tmp all
function survirec:v1/private/c/store with storage survirec:c
data modify storage survirec:in prof set value {}
data modify storage survirec:in prof.id set from entity @s UUID
scoreboard players set #alive survirec.v 0
function survirec:v1/private/c/play with storage survirec:c
execute if score #alive survirec.v matches 1 run tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Terminé ! Ton double démarrera quand les autres auront fini leur cycle.",color:"green"}]
execute unless score #alive survirec.v matches 1 run tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Terminé ! Ton double rejoue ton parcours en boucle. ",color:"green"},{text:"Recommence en réactivant l'épreuve.",color:"gold"}]
execute store result score #tpb survirec.v run data get storage survirec:c tp_back
execute if score #tpb survirec.v matches 1 run function survirec:v1/private/c/tpback
function #survirec:v1/signals/on_record_stop

tag @s remove survirec.on
scoreboard players set #rec survirec.v 0
scoreboard players set #chal survirec.v 0
title @s actionbar {text:""}
data modify storage survirec:tmp all set value []
data modify storage survirec:tmp all append from storage survirec:tmp chunks[][]
data modify storage survirec:tmp all append from storage survirec:tmp d[]
data modify storage survirec:tmp seq set value {}
data modify storage survirec:tmp seq.n set from storage survirec:tmp meta.n
data modify storage survirec:tmp seq.y set from storage survirec:tmp meta.y
data modify storage survirec:tmp seq.p set from storage survirec:tmp meta.p
data modify storage survirec:tmp seq.e set from storage survirec:tmp e
data modify storage survirec:tmp seq.s set from storage survirec:tmp s
data modify storage survirec:tmp seq.d set from storage survirec:tmp all
function survirec:c/store with storage survirec:c
data modify storage survirec:in prof set value {}
data modify storage survirec:in prof.id set from entity @s UUID
scoreboard players set #alive survirec.v 0
function survirec:c/play with storage survirec:c
execute if score #alive survirec.v matches 1 run tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Terminé ! Ton double démarrera quand les autres auront fini leur cycle.",color:"green"}]
execute unless score #alive survirec.v matches 1 run tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Terminé ! Ton double rejoue ton parcours en boucle. ",color:"green"},{text:"Recommence en réactivant l'épreuve.",color:"gold"}]
function #survirec:v1/signals/on_record_stop

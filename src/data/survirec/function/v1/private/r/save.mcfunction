# garde l'enregistrement dans le monde : rejouable par son nom, et réexportable depuis le menu
data modify storage survirec:tmp rec set value {}
data modify storage survirec:tmp rec.meta set from storage survirec:tmp meta
data modify storage survirec:tmp rec.chunks set from storage survirec:tmp chunks
data modify storage survirec:tmp rec.e set from storage survirec:tmp e
data modify storage survirec:tmp rec.s set from storage survirec:tmp s
data modify storage survirec:tmp rec.a set from storage survirec:tmp a
data modify storage survirec:tmp all set value []
data modify storage survirec:tmp all append from storage survirec:tmp chunks[][]
data modify storage survirec:tmp seq set value {}
data modify storage survirec:tmp seq.n set from storage survirec:tmp meta.n
data modify storage survirec:tmp seq.y set from storage survirec:tmp meta.y
data modify storage survirec:tmp seq.p set from storage survirec:tmp meta.p
data modify storage survirec:tmp seq.e set from storage survirec:tmp e
data modify storage survirec:tmp seq.s set from storage survirec:tmp s
data modify storage survirec:tmp seq.a set from storage survirec:tmp a
data modify storage survirec:tmp seq.d set from storage survirec:tmp all
data remove storage survirec:tmp all
function survirec:v1/private/r/save2 with storage survirec:tmp meta
execute store result storage survirec:lib names[-1].pid int 1 run scoreboard players get @s survirec.pid

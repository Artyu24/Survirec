data modify storage survirec:tmp ex.d set from storage survirec:tmp chunks[0]
data remove storage survirec:tmp chunks[0]
data modify storage survirec:tmp ex.e set value []
data modify storage survirec:tmp ex.s set value []
data modify storage survirec:tmp ex.a set value []
execute if score #split survirec.v matches 0 run data modify storage survirec:tmp ex.a set from storage survirec:tmp a
execute if score #split survirec.v matches 0 run data modify storage survirec:tmp ex.e set from storage survirec:tmp e
execute if score #split survirec.v matches 0 run data modify storage survirec:tmp ex.s set from storage survirec:tmp s
function survirec:v1/private/r/exp_final with storage survirec:tmp ex

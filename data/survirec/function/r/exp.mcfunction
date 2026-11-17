data modify storage survirec:tmp ex set value {}
data modify storage survirec:tmp ex.name set from storage survirec:tmp meta.name
data modify storage survirec:tmp ex.n set from storage survirec:tmp meta.n
data modify storage survirec:tmp ex.y set from storage survirec:tmp meta.y
data modify storage survirec:tmp ex.p set from storage survirec:tmp meta.p
data modify storage survirec:tmp ex.sx set from storage survirec:tmp meta.sx
data modify storage survirec:tmp ex.sy set from storage survirec:tmp meta.sy
data modify storage survirec:tmp ex.sz set from storage survirec:tmp meta.sz
data modify storage survirec:tmp ex.d set from storage survirec:tmp chunks[0]
data remove storage survirec:tmp chunks[0]
execute store result storage survirec:tmp ex.j int 1 run scoreboard players get #j survirec.v
execute store result storage survirec:tmp ex.m int 1 run scoreboard players get #m survirec.v
data modify storage survirec:tmp ex.k set value "chaîne"
execute if score #j survirec.v matches 1 run data modify storage survirec:tmp ex.k set value "impulsion"
scoreboard players set #f survirec.v 0
execute if score #j survirec.v matches 1 run scoreboard players set #f survirec.v 1
execute store result storage survirec:tmp ex.f int 1 run scoreboard players get #f survirec.v
execute if score #j survirec.v < #m survirec.v run function survirec:r/exp_part with storage survirec:tmp ex
execute if score #j survirec.v >= #m survirec.v run data modify storage survirec:tmp ex.e set from storage survirec:tmp e
execute if score #j survirec.v >= #m survirec.v run data modify storage survirec:tmp ex.s set from storage survirec:tmp s
execute if score #j survirec.v >= #m survirec.v run function survirec:r/exp_final with storage survirec:tmp ex
scoreboard players add #j survirec.v 1
execute if score #j survirec.v <= #m survirec.v run function survirec:r/exp

data modify storage survirec:tmp ex set value {}
data modify storage survirec:tmp ex.name set from storage survirec:tmp meta.name
data modify storage survirec:tmp ex.n set from storage survirec:tmp meta.n
data modify storage survirec:tmp ex.y set from storage survirec:tmp meta.y
data modify storage survirec:tmp ex.p set from storage survirec:tmp meta.p
data modify storage survirec:tmp ex.sx set from storage survirec:tmp meta.sx
data modify storage survirec:tmp ex.sy set from storage survirec:tmp meta.sy
data modify storage survirec:tmp ex.sz set from storage survirec:tmp meta.sz
data modify storage survirec:tmp ex.g set value ""
data modify storage survirec:tmp ex.gr set value 50
data modify storage survirec:tmp ex.g set from storage survirec:tmp meta.g
data modify storage survirec:tmp ex.gr set from storage survirec:tmp meta.gr
execute store result storage survirec:tmp ex.j int 1 run scoreboard players get #j survirec.v
execute store result storage survirec:tmp ex.m int 1 run scoreboard players get #m survirec.v
data modify storage survirec:tmp ex.k set value "chaîne"
data modify storage survirec:tmp ex.kc set value "green"
execute if score #j survirec.v matches 1 run data modify storage survirec:tmp ex.k set value "impulsion"
execute if score #j survirec.v matches 1 run data modify storage survirec:tmp ex.kc set value "gold"
scoreboard players set #f survirec.v 0
execute if score #j survirec.v matches 1 run scoreboard players set #f survirec.v 1
execute store result storage survirec:tmp ex.f int 1 run scoreboard players get #f survirec.v
scoreboard players set #isf survirec.v 0
execute if score #split survirec.v matches 1 if score #j survirec.v = #c survirec.v run scoreboard players set #isf survirec.v 1
execute if score #isf survirec.v matches 1 run function survirec:v1/private/r/exp_es
execute if score #isf survirec.v matches 0 if score #j survirec.v < #m survirec.v run function survirec:v1/private/r/exp_d
execute if score #isf survirec.v matches 0 if score #j survirec.v >= #m survirec.v run function survirec:v1/private/r/exp_fin
scoreboard players add #j survirec.v 1
execute if score #j survirec.v <= #m survirec.v run function survirec:v1/private/r/exp

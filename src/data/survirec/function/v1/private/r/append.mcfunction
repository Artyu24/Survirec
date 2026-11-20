data modify storage survirec:tmp row set value [0,0,0,0,0,0]
execute unless score #dx survirec.v matches 0 store result storage survirec:tmp row[0] int 1 run scoreboard players get #dx survirec.v
execute unless score #dy survirec.v matches 0 store result storage survirec:tmp row[1] int 1 run scoreboard players get #dy survirec.v
execute unless score #dz survirec.v matches 0 store result storage survirec:tmp row[2] int 1 run scoreboard players get #dz survirec.v
execute unless score #dyw survirec.v matches 0 store result storage survirec:tmp row[3] int 1 run scoreboard players get #dyw survirec.v
execute unless score #dpt survirec.v matches 0 store result storage survirec:tmp row[4] int 1 run scoreboard players get #dpt survirec.v
execute unless score #fl survirec.v matches 0 store result storage survirec:tmp row[5] int 1 run scoreboard players get #fl survirec.v
function survirec:v1/private/r/push with storage survirec:ctx
scoreboard players add @s survirec.rkt 1
scoreboard players add @s survirec.rkf 1
execute if score @s survirec.rkf matches 300.. run function survirec:v1/private/r/chunk with storage survirec:ctx

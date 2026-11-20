execute store result storage survirec:t rel.id int 1 run scoreboard players get @s survirec.id
function survirec:v1/private/i/rladd2 with storage survirec:t rel
execute if score @s survirec.rlt matches -1 run scoreboard players operation @s survirec.rlt = #rt survirec.v
execute if score #rt survirec.v < @s survirec.rlt run scoreboard players operation @s survirec.rlt = #rt survirec.v

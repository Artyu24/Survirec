execute store result storage survirec:v idx.i int 1 run scoreboard players get #vi survirec.v
scoreboard players add #vi survirec.v 1
execute store result storage survirec:v idx.j int 1 run scoreboard players get #vi survirec.v
function survirec:v1/private/vchar with storage survirec:v idx
execute if score #valid survirec.v matches 1 if score #vi survirec.v < #vlen survirec.v run function survirec:v1/private/vloop

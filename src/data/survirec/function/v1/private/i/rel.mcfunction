execute store result storage survirec:t rv.id int 1 run scoreboard players get @s survirec.id
function survirec:v1/private/i/rel1 with storage survirec:t rv
scoreboard players set @s survirec.rlt -1
execute if data storage survirec:t rll[0] at @s run function survirec:v1/private/i/rel2

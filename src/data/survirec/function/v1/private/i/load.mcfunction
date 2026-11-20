execute store result storage survirec:t id int 1 run scoreboard players get @s survirec.id
execute store result storage survirec:t s int 1 run scoreboard players get @s survirec.seg
function survirec:v1/private/i/load1 with storage survirec:t
execute if score @s survirec.ov matches 0 if score @s survirec.seg >= @s survirec.ek run function survirec:v1/private/i/ev

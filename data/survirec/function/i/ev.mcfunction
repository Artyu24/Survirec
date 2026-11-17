execute store result storage survirec:t id int 1 run scoreboard players get @s survirec.id
execute store result storage survirec:t ei int 1 run scoreboard players get @s survirec.ei
scoreboard players add @s survirec.ei 1
execute store result storage survirec:t ej int 1 run scoreboard players get @s survirec.ei
scoreboard players set @s survirec.ek 999999999
function survirec:i/ev1 with storage survirec:t
execute if score @s survirec.seg >= @s survirec.ek run function survirec:i/ev

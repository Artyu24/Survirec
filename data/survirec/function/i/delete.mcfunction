scoreboard players set @s survirec.run 0
execute store result storage survirec:t id int 1 run scoreboard players get @s survirec.id
function survirec:i/unreg with storage survirec:t
tag @s remove survirec.m
kill @s

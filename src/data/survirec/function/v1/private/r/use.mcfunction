function survirec:v1/private/r/cast
execute if score #hit survirec.v matches 1 at @e[type=minecraft:marker,tag=survirec.cur,limit=1] if block ~ ~ ~ #survirec:interactive run function survirec:v1/private/r/use2
tag @e[type=minecraft:marker,tag=survirec.cur] remove survirec.cur

scoreboard players set @s survirec.rplf 1
function survirec:v1/private/r/ctx
function survirec:v1/private/r/snap
function survirec:v1/private/r/cast
execute if score #hit survirec.v matches 1 at @e[type=minecraft:marker,tag=survirec.cur,limit=1] run function survirec:v1/private/r/place2
tag @e[type=minecraft:marker,tag=survirec.cur] remove survirec.cur

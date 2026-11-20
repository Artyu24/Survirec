scoreboard players operation #me survirec.v = @s survirec.pid
execute as @e[type=minecraft:marker,tag=survirec.eye] if score @s survirec.pid = #me survirec.v run tag @s add survirec.cur
scoreboard players set #brk survirec.v 0
execute if score @s survirec.rlk matches 1 at @e[type=minecraft:marker,tag=survirec.cur,limit=1] if block ~ ~ ~ #survirec:air run scoreboard players set #brk survirec.v 1
execute if score #brk survirec.v matches 1 run function survirec:v1/private/r/brk
scoreboard players set @s survirec.rlk 0
scoreboard players set #rs survirec.v 0
scoreboard players set #hit survirec.v 0
execute anchored eyes positioned ^ ^ ^ run function survirec:v1/private/r/ray
execute if score #hit survirec.v matches 1 run scoreboard players set @s survirec.rlk 1
execute if score #hit survirec.v matches 1 if data storage survirec:cfg vault2 run function survirec:v1/private/r/lkcopy
tag @e[type=minecraft:marker,tag=survirec.cur] remove survirec.cur

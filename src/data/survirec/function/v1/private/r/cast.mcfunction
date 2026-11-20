# rayon avec le marqueur d'événements du joueur (@s, à sa position)
scoreboard players operation #me survirec.v = @s survirec.pid
execute as @e[type=minecraft:marker,tag=survirec.ray] if score @s survirec.pid = #me survirec.v run tag @s add survirec.cur
scoreboard players set #rs survirec.v 0
scoreboard players set #hit survirec.v 0
execute anchored eyes positioned ^ ^ ^ run function survirec:v1/private/r/ray

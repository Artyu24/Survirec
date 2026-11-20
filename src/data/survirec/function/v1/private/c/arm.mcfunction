execute store result score @s survirec.rwg run data get storage survirec:c gid
scoreboard players operation #wg survirec.v = @s survirec.rwg
scoreboard players set #alive survirec.v 0
execute as @e[tag=survirec.m] if score @s survirec.grp = #wg survirec.v run scoreboard players set #alive survirec.v 1
execute if score #alive survirec.v matches 0 run return run function survirec:v1/private/c/launch
tag @s add survirec.armed
tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Enregistrement armé : il démarre au prochain cycle du groupe.",color:"green"}]

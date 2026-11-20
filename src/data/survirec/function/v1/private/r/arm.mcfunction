execute store result score @s survirec.rwg run data get storage survirec:in cfg.grp
scoreboard players operation #wg survirec.v = @s survirec.rwg
scoreboard players set #alive survirec.v 0
execute as @e[tag=survirec.m] if score @s survirec.grp = #wg survirec.v run scoreboard players set #alive survirec.v 1
execute if score #alive survirec.v matches 0 run return run function survirec:v1/private/r/begin
execute unless score @s survirec.pid matches 1.. run function survirec:v1/private/c/newpid
function survirec:v1/private/r/ctx
function survirec:v1/private/r/armsave with storage survirec:ctx
scoreboard players set @s survirec.ratype 1
tag @s add survirec.armed
tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Enregistrement armé : il démarre au prochain cycle du groupe.",color:"green"}]

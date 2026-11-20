execute unless entity @s[type=minecraft:player] run return fail
# une plaque de pression redéclenche en continu : on ignore sans message
execute if entity @s[tag=survirec.on] run return 0
execute if entity @s[tag=survirec.armed] run return 0
data modify storage survirec:c id set from storage survirec:cin id
data modify storage survirec:c time set from storage survirec:cin time
data modify storage survirec:c group set from storage survirec:cin group
data modify storage survirec:c sync set from storage survirec:cin sync
data modify storage survirec:c tp_back set from storage survirec:cin tp_back
execute store result score @s survirec.rcdur run data get storage survirec:c time 20
execute unless score @s survirec.rcdur matches 20.. run return run tellraw @s {text:"[Survirec] time doit être d'au moins 1 seconde.",color:"red"}
execute unless score @s survirec.pid matches 1.. run function survirec:v1/private/c/newpid
execute store result storage survirec:c pid int 1 run scoreboard players get @s survirec.pid
function survirec:v1/private/c/gid with storage survirec:c
execute store result storage survirec:c gid int 1 run scoreboard players get #g survirec.v
function survirec:v1/private/c/prekill with storage survirec:c
function survirec:v1/private/i/grpcheck
function survirec:v1/private/r/ctx
function survirec:v1/private/c/save with storage survirec:ctx
scoreboard players set @s survirec.ratype 0
execute store result score #sync survirec.v run data get storage survirec:c sync
execute if score #sync survirec.v matches 1 run return run function survirec:v1/private/c/arm
function survirec:v1/private/c/launch

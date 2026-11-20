execute store result score #ek survirec.v run data get storage survirec:t ev.k
execute if score #ek survirec.v matches 1 run return run function survirec:v1/private/i/a_hit
# position absolue du bloc = point de départ de l'entité + décalage enregistré
execute store result score #ax survirec.v run data get storage survirec:t ev.x
execute store result score #ay survirec.v run data get storage survirec:t ev.y
execute store result score #az survirec.v run data get storage survirec:t ev.z
scoreboard players operation #ax survirec.v += @s survirec.bbx
scoreboard players operation #ay survirec.v += @s survirec.bby
scoreboard players operation #az survirec.v += @s survirec.bbz
data modify storage survirec:t at set value {x:0,y:0,z:0}
execute store result storage survirec:t at.x int 1 run scoreboard players get #ax survirec.v
execute store result storage survirec:t at.y int 1 run scoreboard players get #ay survirec.v
execute store result storage survirec:t at.z int 1 run scoreboard players get #az survirec.v
execute if score #ek survirec.v matches 2 run return run function survirec:v1/private/i/a_at with storage survirec:t at
execute if score #ek survirec.v matches 3 run return run function survirec:v1/private/i/a_at with storage survirec:t at
execute if score #ek survirec.v matches 4 run return run function survirec:v1/private/i/a_at with storage survirec:t at

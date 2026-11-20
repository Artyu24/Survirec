# autre moitié : sauvegarde puis pose
data modify storage survirec:t pp set value {x:0,y:0,z:0,b:""}
data modify storage survirec:t pp.b set from storage survirec:t ev.p.b
execute store result score #px survirec.v run data get storage survirec:t ev.p.x
execute store result score #py survirec.v run data get storage survirec:t ev.p.y
execute store result score #pz survirec.v run data get storage survirec:t ev.p.z
scoreboard players operation #px survirec.v += @s survirec.bbx
scoreboard players operation #py survirec.v += @s survirec.bby
scoreboard players operation #pz survirec.v += @s survirec.bbz
execute store result storage survirec:t pp.x int 1 run scoreboard players get #px survirec.v
execute store result storage survirec:t pp.y int 1 run scoreboard players get #py survirec.v
execute store result storage survirec:t pp.z int 1 run scoreboard players get #pz survirec.v
function survirec:v1/private/i/a_place3 with storage survirec:t pp

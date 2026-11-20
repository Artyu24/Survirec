# l'autre moitié d'un bloc double
scoreboard players operation #hx survirec.v += #pdx survirec.v
scoreboard players operation #hy survirec.v += #pdy survirec.v
scoreboard players operation #hz survirec.v += #pdz survirec.v
data modify storage survirec:tmp ev.p set value {x:0,y:0,z:0,b:""}
execute store result storage survirec:tmp ev.p.x int 1 run scoreboard players get #hx survirec.v
execute store result storage survirec:tmp ev.p.y int 1 run scoreboard players get #hy survirec.v
execute store result storage survirec:tmp ev.p.z int 1 run scoreboard players get #hz survirec.v
execute store result storage survirec:tmp pd.x int 1 run scoreboard players get #pdx survirec.v
execute store result storage survirec:tmp pd.y int 1 run scoreboard players get #pdy survirec.v
execute store result storage survirec:tmp pd.z int 1 run scoreboard players get #pdz survirec.v
function survirec:v1/private/r/place4 with storage survirec:tmp pd

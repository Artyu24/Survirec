data modify storage survirec:t pd set value {x:0,y:0,z:0}
execute store result storage survirec:t pd.x int 1 run scoreboard players get #pdx survirec.v
execute store result storage survirec:t pd.y int 1 run scoreboard players get #pdy survirec.v
execute store result storage survirec:t pd.z int 1 run scoreboard players get #pdz survirec.v
function survirec:v1/private/i/a_bkpair2 with storage survirec:t pd

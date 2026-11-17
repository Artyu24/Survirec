scoreboard players operation #dx survirec.v = #rx survirec.v
scoreboard players operation #dx survirec.v /= #cs survirec.v
scoreboard players operation #dy survirec.v = #ry survirec.v
scoreboard players operation #dy survirec.v /= #cs survirec.v
scoreboard players operation #dz survirec.v = #rz survirec.v
scoreboard players operation #dz survirec.v /= #cs survirec.v
scoreboard players operation #dyw survirec.v = #ryw survirec.v
scoreboard players operation #dyw survirec.v /= #cs survirec.v
scoreboard players operation #dpt survirec.v = #rpt survirec.v
scoreboard players operation #dpt survirec.v /= #cs survirec.v
scoreboard players operation #rx survirec.v -= #dx survirec.v
scoreboard players operation #ry survirec.v -= #dy survirec.v
scoreboard players operation #rz survirec.v -= #dz survirec.v
scoreboard players operation #ryw survirec.v -= #dyw survirec.v
scoreboard players operation #rpt survirec.v -= #dpt survirec.v
function survirec:r/append
scoreboard players remove #cs survirec.v 1
execute if score #cs survirec.v matches 1.. run function survirec:r/closeloop

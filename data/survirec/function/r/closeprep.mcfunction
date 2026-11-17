scoreboard players set #fl survirec.v 0
scoreboard players operation #rx survirec.v = #ox survirec.v
scoreboard players operation #rx survirec.v -= #px survirec.v
scoreboard players operation #ry survirec.v = #oy survirec.v
scoreboard players operation #ry survirec.v -= #py survirec.v
scoreboard players operation #rz survirec.v = #oz survirec.v
scoreboard players operation #rz survirec.v -= #pz survirec.v
scoreboard players operation #ryw survirec.v = #oyw survirec.v
scoreboard players operation #ryw survirec.v -= #pyw survirec.v
execute if score #ryw survirec.v matches 18001.. run scoreboard players remove #ryw survirec.v 36000
execute if score #ryw survirec.v matches ..-18001 run scoreboard players add #ryw survirec.v 36000
scoreboard players operation #rpt survirec.v = #opt survirec.v
scoreboard players operation #rpt survirec.v -= #ppt survirec.v
scoreboard players set #cs survirec.v 10
function survirec:r/closeloop

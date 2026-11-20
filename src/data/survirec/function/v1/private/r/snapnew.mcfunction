scoreboard players operation #c7 survirec.v = #cs survirec.v
function survirec:v1/private/r/cubexyz
scoreboard players add #cs survirec.v 1
execute if score #cs survirec.v matches 1536.. run scoreboard players set #cs survirec.v 0
execute store result storage survirec:tmp sn.bx int 1 run scoreboard players get #cx survirec.v
execute store result storage survirec:tmp sn.by int 1 run scoreboard players get #cy survirec.v
execute store result storage survirec:tmp sn.bz int 1 run scoreboard players get #cz survirec.v
execute store result storage survirec:tmp sn.bx2 int 1 run scoreboard players add #cx survirec.v 2
execute store result storage survirec:tmp sn.by2 int 1 run scoreboard players add #cy survirec.v 2
execute store result storage survirec:tmp sn.bz2 int 1 run scoreboard players add #cz survirec.v 2

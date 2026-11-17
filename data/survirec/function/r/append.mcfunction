data modify storage survirec:tmp d append value [0,0,0,0,0,0]
execute unless score #dx survirec.v matches 0 store result storage survirec:tmp d[-1][0] int 1 run scoreboard players get #dx survirec.v
execute unless score #dy survirec.v matches 0 store result storage survirec:tmp d[-1][1] int 1 run scoreboard players get #dy survirec.v
execute unless score #dz survirec.v matches 0 store result storage survirec:tmp d[-1][2] int 1 run scoreboard players get #dz survirec.v
execute unless score #dyw survirec.v matches 0 store result storage survirec:tmp d[-1][3] int 1 run scoreboard players get #dyw survirec.v
execute unless score #dpt survirec.v matches 0 store result storage survirec:tmp d[-1][4] int 1 run scoreboard players get #dpt survirec.v
execute unless score #fl survirec.v matches 0 store result storage survirec:tmp d[-1][5] int 1 run scoreboard players get #fl survirec.v
scoreboard players add #kt survirec.v 1
scoreboard players add #kf survirec.v 1
execute if score #kf survirec.v matches 500.. run function survirec:r/chunk

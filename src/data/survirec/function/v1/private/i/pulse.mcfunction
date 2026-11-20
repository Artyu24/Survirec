# bloc de redstone posé 2 blocs au-dessus du command block (1 bloc d'écart, sinon il se réactive lui-même) qui a lancé la séquence, retiré 4 ticks plus tard
execute store result storage survirec:t pu.x int 1 run scoreboard players get @s survirec.cbx
execute store result storage survirec:t pu.y int 1 run scoreboard players get @s survirec.cby
execute store result storage survirec:t pu.z int 1 run scoreboard players get @s survirec.cbz
function survirec:v1/private/i/pulse2 with storage survirec:t pu

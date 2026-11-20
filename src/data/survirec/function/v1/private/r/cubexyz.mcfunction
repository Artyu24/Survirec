# index #c7 -> coin d'un cube 3x3x3 isolé par des barrières, dans la zone 1 (x 17..31) : #cx #cy #cz
scoreboard players operation #cx survirec.v = #c7 survirec.v
scoreboard players operation #cx survirec.v %= #4 survirec.v
scoreboard players operation #cx survirec.v *= #4 survirec.v
scoreboard players add #cx survirec.v 17
scoreboard players operation #cz survirec.v = #c7 survirec.v
scoreboard players operation #cz survirec.v /= #4 survirec.v
scoreboard players operation #cz survirec.v %= #4 survirec.v
scoreboard players operation #cz survirec.v *= #4 survirec.v
scoreboard players add #cz survirec.v 1
scoreboard players operation #cy survirec.v = #c7 survirec.v
scoreboard players operation #cy survirec.v /= #16 survirec.v
scoreboard players operation #cy survirec.v *= #4 survirec.v
scoreboard players remove #cy survirec.v 63

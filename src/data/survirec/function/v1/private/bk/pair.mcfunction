# bloc double (porte, lit, grande plante) : décalage vers l'autre moitié dans #pdx #pdy #pdz, #pair 1
scoreboard players set #pair survirec.v 0
scoreboard players set #pdx survirec.v 0
scoreboard players set #pdy survirec.v 0
scoreboard players set #pdz survirec.v 0
execute if score #bhl survirec.v matches 2 run scoreboard players set #pdy survirec.v 1
execute if score #bhl survirec.v matches 1 run scoreboard players set #pdy survirec.v -1
execute if score #bhl survirec.v matches 1..2 run scoreboard players set #pair survirec.v 1
execute if score #bpt survirec.v matches 1..2 run scoreboard players set #pair survirec.v 1
execute if score #bpt survirec.v matches 1..2 if score #bfc survirec.v matches 1 run scoreboard players set #pdz survirec.v -1
execute if score #bpt survirec.v matches 1..2 if score #bfc survirec.v matches 2 run scoreboard players set #pdz survirec.v 1
execute if score #bpt survirec.v matches 1..2 if score #bfc survirec.v matches 3 run scoreboard players set #pdx survirec.v 1
execute if score #bpt survirec.v matches 1..2 if score #bfc survirec.v matches 4 run scoreboard players set #pdx survirec.v -1
execute if score #bpt survirec.v matches 1 run scoreboard players operation #pdx survirec.v *= #m1 survirec.v
execute if score #bpt survirec.v matches 1 run scoreboard players operation #pdz survirec.v *= #m1 survirec.v

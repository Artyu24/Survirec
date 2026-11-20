# vrai si c'est le tour de cette entité de bouger (une entité sur #step à chaque tick, en alternance)
scoreboard players operation #ph survirec.v = @s survirec.id
scoreboard players operation #ph survirec.v += #gt survirec.v
scoreboard players operation #ph survirec.v %= #step survirec.v
execute if score #ph survirec.v matches 0 run return 1
return fail

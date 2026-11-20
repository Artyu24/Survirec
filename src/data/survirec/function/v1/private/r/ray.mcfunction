# lancer de rayon depuis le regard (pas de 0,2 bloc, 5 blocs max) : le marqueur survirec.cur va sur le bloc touché
scoreboard players add #rs survirec.v 1
execute unless block ~ ~ ~ #survirec:ray_pass run return run function survirec:v1/private/r/rayhit
execute if score #rs survirec.v matches 26.. run return 0
execute positioned ^ ^ ^0.2 run function survirec:v1/private/r/ray

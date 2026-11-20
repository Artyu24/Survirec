# positionné sur le bloc, en tant qu'entité. survirec:t bka = {x,y,z,m} (m = "strict" ou "replace" pour la remise en place)
# Une seule copie par bloc : celle d'origine. Elle sert à chaque remise en place, on ne la refait jamais.
execute unless score @s survirec.rst matches 1.. run return 0
execute unless data storage survirec:cfg vault run return 0
execute store result storage survirec:t bka.id int 1 run scoreboard players get @s survirec.id
scoreboard players set #has survirec.v 0
function survirec:v1/private/vault/has with storage survirec:t bka
execute if score #has survirec.v matches 1 run return 0
execute if data storage survirec:cfg vfree[0] run return run function survirec:v1/private/vault/reuse
scoreboard players operation #c7 survirec.v = #vs survirec.v
scoreboard players operation #c7 survirec.v %= #7 survirec.v
scoreboard players operation #c7 survirec.v *= #2 survirec.v
execute store result storage survirec:t bka.vx int 1 run scoreboard players add #c7 survirec.v 1
scoreboard players operation #c7 survirec.v = #vs survirec.v
scoreboard players operation #c7 survirec.v /= #7 survirec.v
scoreboard players operation #c7 survirec.v %= #7 survirec.v
scoreboard players operation #c7 survirec.v *= #2 survirec.v
execute store result storage survirec:t bka.vz int 1 run scoreboard players add #c7 survirec.v 1
scoreboard players operation #c7 survirec.v = #vs survirec.v
scoreboard players operation #c7 survirec.v /= #49 survirec.v
scoreboard players operation #c7 survirec.v *= #2 survirec.v
execute store result storage survirec:t bka.vy int 1 run scoreboard players remove #c7 survirec.v 63
scoreboard players add #vs survirec.v 1
execute if score #vs survirec.v matches 9359.. run scoreboard players set #vs survirec.v 0
function survirec:v1/private/vault/bk2 with storage survirec:t bka

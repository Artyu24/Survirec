# remet en place, dans l'ordre inverse, les blocs modifiés par cette entité
execute store result storage survirec:t rv.id int 1 run scoreboard players get @s survirec.id
function survirec:v1/private/vault/rs0 with storage survirec:t rv
execute if data storage survirec:t bkl[0] at @s run function survirec:v1/private/vault/rs1

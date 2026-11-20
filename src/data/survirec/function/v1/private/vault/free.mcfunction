# l'entité disparaît : ses emplacements redeviennent des barrières et sont réutilisables
execute store result storage survirec:t rv.id int 1 run scoreboard players get @s survirec.id
function survirec:v1/private/vault/rs0 with storage survirec:t rv
execute if data storage survirec:t bkl[0] run function survirec:v1/private/vault/free1

# remet le monde comme avant l'enregistrement (en tant que joueur)
function survirec:v1/private/r/ctx
data modify storage survirec:tmp wbl set value []
function survirec:v1/private/r/wr0 with storage survirec:ctx
execute if data storage survirec:tmp wbl[0] at @s run function survirec:v1/private/r/wr1

scoreboard players set @s survirec.run 0
function survirec:v1/private/i/relall
execute if score @s survirec.rst matches 2 run function survirec:v1/private/vault/restore
execute if score @s survirec.rst matches 1 if score #kres survirec.v matches 1 run function survirec:v1/private/vault/restore
function survirec:v1/private/vault/free
execute store result storage survirec:t id int 1 run scoreboard players get @s survirec.id
function survirec:v1/private/i/unreg with storage survirec:t
tag @s remove survirec.m
# rien ne doit se voir ni tomber : on vide l'équipement et on envoie l'entité sous le monde avant de la retirer
item replace entity @s armor.head with minecraft:air
item replace entity @s armor.chest with minecraft:air
item replace entity @s armor.legs with minecraft:air
item replace entity @s armor.feet with minecraft:air
item replace entity @s weapon.mainhand with minecraft:air
item replace entity @s weapon.offhand with minecraft:air
effect give @s minecraft:invisibility infinite 0 true
tp @s ~ -1000 ~
kill @s

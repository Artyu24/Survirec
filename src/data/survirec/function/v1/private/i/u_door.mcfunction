# porte : les deux moitiés, posées sans mise à jour pour qu'elles ne se recopient pas l'une l'autre
scoreboard players set #nop survirec.v 1
execute if score #bop survirec.v matches 1 run scoreboard players set #nop survirec.v 0
function survirec:v1/private/bk/pair
scoreboard players set #bkm survirec.v 1
function survirec:v1/private/vault/here
function survirec:v1/private/i/u_openex
function survirec:v1/private/bk/full
function survirec:v1/private/i/setfulls with storage survirec:bk
execute if score #pair survirec.v matches 1 run function survirec:v1/private/i/u_door2
execute if score #nop survirec.v matches 1 run playsound minecraft:block.wooden_door.open block @a ~ ~ ~
execute if score #nop survirec.v matches 0 run playsound minecraft:block.wooden_door.close block @a ~ ~ ~

function survirec:v1/private/bk/read
function survirec:v1/private/bk/pair
scoreboard players operation #bkm survirec.v = #pair survirec.v
function survirec:v1/private/vault/here
execute if score #pair survirec.v matches 1 run function survirec:v1/private/i/a_bkpair
setblock ~ ~ ~ minecraft:air destroy
execute align xyz positioned ~0.5 ~0.5 ~0.5 run kill @e[type=minecraft:item,distance=..1.6,nbt={Age:0s}]
execute align xyz positioned ~0.5 ~0.5 ~0.5 run kill @e[type=minecraft:experience_orb,distance=..1.6]
swing @s mainhand

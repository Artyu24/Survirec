# on ne remplace jamais un bloc existant
execute unless block ~ ~ ~ #survirec:air run return 0
setblock ~ ~ ~ minecraft:redstone_block
execute align xyz positioned ~0.5 ~0.5 ~0.5 summon minecraft:marker run function survirec:v1/private/i/pulse4

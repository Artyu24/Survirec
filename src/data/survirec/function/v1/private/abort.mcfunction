# joueur : annule son propre enregistrement. command block / console : annule tous les enregistrements
execute if entity @s[type=minecraft:player] unless entity @s[tag=survirec.on] unless entity @s[tag=survirec.armed] run return run tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Tu n'as aucun enregistrement en cours.",color:"red"}]
execute if entity @s[type=minecraft:player] run function survirec:v1/private/r/abort1
execute if entity @s[type=minecraft:player] run return run tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Enregistrement annulé.",color:"yellow"}]
execute as @a[tag=survirec.on] run function survirec:v1/private/r/abort1
execute as @a[tag=survirec.armed] run function survirec:v1/private/r/abort1

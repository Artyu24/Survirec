# joueur : arrête son propre enregistrement. command block / console : arrête tous les enregistrements
execute if entity @s[type=minecraft:player,tag=survirec.on] run return run function survirec:v1/private/stop_loop1
execute if entity @s[type=minecraft:player] run return run tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Tu n'as aucun enregistrement en cours.",color:"red"}]
execute as @a[tag=survirec.on] run function survirec:v1/private/stop_loop1

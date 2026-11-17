execute if score #chal survirec.v matches 1 run return run function survirec:abort
execute unless score #rec survirec.v matches 1 run return run tellraw @s {text:"[Survirec] Aucun enregistrement en cours.",color:"red"}
execute as @a[tag=survirec.on] run function survirec:r/finish

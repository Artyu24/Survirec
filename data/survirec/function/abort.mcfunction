execute as @a[tag=survirec.on] run function survirec:r/cleanup
tag @a remove survirec.on
scoreboard players set #rec survirec.v 0
scoreboard players set #chal survirec.v 0
tellraw @s {text:"[Survirec] Enregistrement annulé.",color:"yellow"}

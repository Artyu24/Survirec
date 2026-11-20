execute as @a[tag=survirec.on] run function #survirec:v1/signals/on_record_stop
execute as @a[tag=survirec.on] at @s run function survirec:v1/private/r/wrestore
tag @a remove survirec.on
tag @a remove survirec.armed
execute as @a run function survirec:v1/private/r/cleanup
scoreboard players set @a survirec.rchal 0
kill @e[type=minecraft:text_display,tag=survirec.start]
kill @e[type=minecraft:marker,tag=survirec.rk]
execute as @e[type=minecraft:marker,tag=survirec.pulse] at @s run function survirec:v1/private/i/pulseoff
scoreboard players set #npulse survirec.v 0
data remove storage survirec:rec p
tellraw @s {text:"[Survirec] État réinitialisé.",color:"green"}

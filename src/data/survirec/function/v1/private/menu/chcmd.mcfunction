# la durée doit être un nombre entier de secondes
$scoreboard players set #ct survirec.v $(time)
execute unless score #ct survirec.v matches 1.. run return run tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"La durée doit être un nombre de secondes (1 ou plus).",color:"red"}]
execute store result storage survirec:in cfg.time int 1 run scoreboard players get #ct survirec.v
function survirec:v1/private/menu/chcmd2 with storage survirec:in cfg

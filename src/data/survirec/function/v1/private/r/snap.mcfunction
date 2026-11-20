# le joueur vient de casser, poser ou actionner : on garde l'état d'avant (cube copié au tick précédent)
execute unless data storage survirec:cfg vault2 run return 0
execute unless score @s survirec.rlk matches 1 run return 0
data modify storage survirec:tmp sn set value {}
scoreboard players operation #me survirec.v = @s survirec.pid
execute as @e[type=minecraft:marker,tag=survirec.eye] if score @s survirec.pid = #me survirec.v run function survirec:v1/private/r/snappos
execute unless data storage survirec:tmp sn.x run return 0
execute store result storage survirec:tmp sn.pid int 1 run scoreboard players get @s survirec.pid
# même cube déjà gardé pendant cet enregistrement : la copie d'origine suffit
scoreboard players set #has survirec.v 0
function survirec:v1/private/r/snaphas with storage survirec:tmp sn
execute if score #has survirec.v matches 1 run return 0
execute if data storage survirec:cfg cfree[0] run function survirec:v1/private/r/snapreuse
execute unless data storage survirec:tmp sn.bx run function survirec:v1/private/r/snapnew
execute store result storage survirec:tmp sn.lx int 1 run scoreboard players get @s survirec.rlkx
execute store result storage survirec:tmp sn.ly int 1 run scoreboard players get @s survirec.rlky
execute store result storage survirec:tmp sn.lz int 1 run scoreboard players get @s survirec.rlkz
scoreboard players operation #c7 survirec.v = @s survirec.rlkx
execute store result storage survirec:tmp sn.lx2 int 1 run scoreboard players add #c7 survirec.v 2
scoreboard players operation #c7 survirec.v = @s survirec.rlky
execute store result storage survirec:tmp sn.ly2 int 1 run scoreboard players add #c7 survirec.v 2
scoreboard players operation #c7 survirec.v = @s survirec.rlkz
execute store result storage survirec:tmp sn.lz2 int 1 run scoreboard players add #c7 survirec.v 2
execute store result storage survirec:tmp sn.pid int 1 run scoreboard players get @s survirec.pid
function survirec:v1/private/r/snap2 with storage survirec:tmp sn

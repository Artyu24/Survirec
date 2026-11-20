title @s actionbar [{text:"⏳ ",color:"gold"},{text:"EN ATTENTE DU PROCHAIN CYCLE ",color:"white",bold:true},{text:"du groupe",color:"gray"}]
scoreboard players operation #wg survirec.v = @s survirec.rwg
scoreboard players set #alive survirec.v 0
execute as @e[tag=survirec.m] if score @s survirec.grp = #wg survirec.v run scoreboard players set #alive survirec.v 1
execute if score #alive survirec.v matches 0 run function survirec:v1/private/c/launch

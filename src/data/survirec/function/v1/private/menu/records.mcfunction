tellraw @s {text:"══ Enregistrements ══",color:"gold"}
scoreboard players operation #me survirec.v = @s survirec.pid
scoreboard players set #cnt survirec.v 0
data modify storage survirec:tmp it set value []
data modify storage survirec:tmp it set from storage survirec:lib names
execute if data storage survirec:tmp it[0] run function survirec:v1/private/menu/rloop
execute if score #cnt survirec.v matches 0 run tellraw @s {text:"   Aucun enregistrement pour l'instant.",color:"gray"}

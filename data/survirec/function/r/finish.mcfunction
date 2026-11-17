tag @s remove survirec.on
scoreboard players set #rec survirec.v 0
function survirec:r/cleanup
function #survirec:v1/signals/on_record_stop
execute if score #kt survirec.v matches 0 run return run tellraw @s {text:"[Survirec] Séquence vide, rien à exporter.",color:"red"}
execute if score #kf survirec.v matches 1.. run data modify storage survirec:tmp chunks append from storage survirec:tmp d
execute store result score #m survirec.v run data get storage survirec:tmp chunks
scoreboard players set #j survirec.v 1
function survirec:r/exp
tellraw @s {text:"[Survirec] Terminé. Clique pour copier, puis colle dans un command block (impulsion).",color:"green"}
execute if score #m survirec.v matches 2.. run tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Colle les boutons dans l'ordre, du 1 au dernier : ",color:"green"},{text:"bloc 1 en impulsion",color:"gold"},{text:", les suivants en chaîne (toujours actif).",color:"green"}]

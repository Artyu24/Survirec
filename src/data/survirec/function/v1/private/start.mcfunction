# function survirec:v1/private/start {name:"walk",every:4}
execute unless entity @s[type=minecraft:player] run return fail
execute if entity @s[tag=survirec.on] run return run tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Tu es déjà en train d'enregistrer (",color:"red"},{text:"#survirec:v1/stop",color:"gold"},{text:").",color:"red"}]
execute if entity @s[tag=survirec.armed] run return run tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Ton enregistrement est déjà armé (",color:"red"},{text:"#survirec:v1/abort",color:"gold"},{text:" pour l'annuler).",color:"red"}]
$scoreboard players set #n survirec.v $(every)
execute unless score #n survirec.v matches 1..100 run return run tellraw @s {text:"[Survirec] every doit être entre 1 et 100.",color:"red"}
$data modify storage survirec:tmp meta set value {name:"$(name)",n:$(every),g:"$(group)",gr:$(group_radius)}
execute if data storage survirec:in cfg{group:""} run return run function survirec:v1/private/r/begin
function survirec:v1/private/r/armg with storage survirec:in cfg

$data modify storage survirec:in api set value $(with)
data modify storage survirec:in cfg set value {}
data modify storage survirec:in cfg merge from storage survirec:in api
scoreboard players set #bad survirec.v 0
execute if data storage survirec:in cfg.tag run data modify storage survirec:v q set value {f:"tag"}
execute if data storage survirec:in cfg.tag run function survirec:v1/private/vreq with storage survirec:v q
execute if data storage survirec:in cfg.name run data modify storage survirec:v q set value {f:"name"}
execute if data storage survirec:in cfg.name run function survirec:v1/private/vreq with storage survirec:v q
execute if score #bad survirec.v matches 1 run return run function survirec:v1/private/badname
execute if data storage survirec:in cfg.tag run return run function survirec:v1/private/kill with storage survirec:in cfg
execute if data storage survirec:in cfg.name run return run function survirec:v1/private/kill_name with storage survirec:in cfg
tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"kill demande un filtre (tag ou name). Pour tout supprimer : ",color:"red"},{text:"#survirec:v1/kill_all",color:"gold",bold:true}]

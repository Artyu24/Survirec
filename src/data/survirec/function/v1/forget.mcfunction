$data modify storage survirec:in api set value $(with)
data modify storage survirec:in cfg set value {name:""}
data modify storage survirec:in cfg merge from storage survirec:in api
scoreboard players set #bad survirec.v 0
data modify storage survirec:v q set value {f:"name"}
function survirec:v1/private/vreq with storage survirec:v q
execute if score #bad survirec.v matches 1 run return run function survirec:v1/private/badname
function survirec:v1/private/forget with storage survirec:in cfg

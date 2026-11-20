$data modify storage survirec:in api set value $(with)
data modify storage survirec:in cfg set value {id:"default",time:30,group:"main",sync:0,tp_back:1}
data modify storage survirec:in cfg merge from storage survirec:in api
scoreboard players set #bad survirec.v 0
data modify storage survirec:v q set value {f:"id"}
function survirec:v1/private/vreq with storage survirec:v q
data modify storage survirec:v q set value {f:"group"}
function survirec:v1/private/vreq with storage survirec:v q
execute if score #bad survirec.v matches 1 run return run function survirec:v1/private/badname
function survirec:v1/private/challenge with storage survirec:in cfg

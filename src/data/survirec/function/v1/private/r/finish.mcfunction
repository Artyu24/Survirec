tag @s remove survirec.on
function survirec:v1/private/r/wrestore
function survirec:v1/private/r/pull
function survirec:v1/private/r/drop with storage survirec:ctx
function survirec:v1/private/r/cleanup
function #survirec:v1/signals/on_record_stop
execute if score #kt survirec.v matches 0 run return run tellraw @s {text:"[Survirec] Séquence vide, rien à exporter.",color:"red"}
execute if score #kf survirec.v matches 1.. run data modify storage survirec:tmp chunks append from storage survirec:tmp d
function survirec:v1/private/r/save
function survirec:v1/private/r/export

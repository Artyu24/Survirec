execute if entity @s[tag=survirec.on] run function #survirec:v1/signals/on_record_stop
execute if entity @s[tag=survirec.on] run tag @s add survirec.wasrec
tag @s remove survirec.on
tag @s remove survirec.armed
scoreboard players set @s survirec.rchal 0
function survirec:v1/private/r/cleanup
execute if entity @s[tag=survirec.wasrec] run function survirec:v1/private/r/wrestore
tag @s remove survirec.wasrec
function survirec:v1/private/r/ctx
function survirec:v1/private/r/drop with storage survirec:ctx

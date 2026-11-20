execute if score @s survirec.ratk = @s survirec.rtime run return 0
scoreboard players operation @s survirec.ratk = @s survirec.rtime
function survirec:v1/private/r/ctx
data modify storage survirec:tmp ev set value {t:0,k:1}
execute store result storage survirec:tmp ev.t int 1 run scoreboard players get @s survirec.rtime
function survirec:v1/private/r/evpush with storage survirec:ctx

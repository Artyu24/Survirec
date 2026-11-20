function survirec:v1/private/r/snap
data modify storage survirec:tmp ev set value {t:0,k:4,x:0,y:0,z:0}
execute store result storage survirec:tmp ev.t int 1 run scoreboard players get @s survirec.rtime
function survirec:v1/private/r/curpos
function survirec:v1/private/r/evpush with storage survirec:ctx

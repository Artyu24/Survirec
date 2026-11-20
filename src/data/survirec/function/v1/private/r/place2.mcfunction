function survirec:v1/private/bk/read
execute if data storage survirec:bk r{id:""} run return 0
data modify storage survirec:tmp ev set value {t:0,k:3,x:0,y:0,z:0,b:""}
execute store result storage survirec:tmp ev.t int 1 run scoreboard players get @s survirec.rtime
function survirec:v1/private/r/curpos
function survirec:v1/private/bk/fullp
data modify storage survirec:tmp ev.b set from storage survirec:bk full
function survirec:v1/private/bk/pair
execute if score #pair survirec.v matches 1 run function survirec:v1/private/r/place3
function survirec:v1/private/r/evpush with storage survirec:ctx

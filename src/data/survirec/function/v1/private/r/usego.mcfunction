scoreboard players set @s survirec.ruf 0
execute if score @s survirec.rplf matches 1 run return 0
function survirec:v1/private/r/snap
data modify storage survirec:tmp ev set value {t:0,k:2,x:0,y:0,z:0}
execute store result storage survirec:tmp ev.t int 1 run scoreboard players get @s survirec.rut
scoreboard players operation #hx survirec.v = @s survirec.rux
scoreboard players operation #hx survirec.v -= @s survirec.rbx
scoreboard players operation #hy survirec.v = @s survirec.ruy
scoreboard players operation #hy survirec.v -= @s survirec.rby
scoreboard players operation #hz survirec.v = @s survirec.ruz
scoreboard players operation #hz survirec.v -= @s survirec.rbz
execute store result storage survirec:tmp ev.x int 1 run scoreboard players get #hx survirec.v
execute store result storage survirec:tmp ev.y int 1 run scoreboard players get #hy survirec.v
execute store result storage survirec:tmp ev.z int 1 run scoreboard players get #hz survirec.v
function survirec:v1/private/r/evpush with storage survirec:ctx

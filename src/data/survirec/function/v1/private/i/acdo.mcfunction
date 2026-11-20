execute store result storage survirec:t id int 1 run scoreboard players get @s survirec.id
execute store result storage survirec:t aj int 1 run scoreboard players get @s survirec.ai
function survirec:v1/private/i/acget1 with storage survirec:t
function survirec:v1/private/i/acrun
scoreboard players add @s survirec.ai 1
function survirec:v1/private/i/acload
execute if score #tm survirec.v >= @s survirec.ak run function survirec:v1/private/i/acdo

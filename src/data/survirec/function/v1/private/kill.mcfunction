scoreboard players set #kres survirec.v 1
# function survirec:v1/private/kill {tag:"porte_nord"}
$execute as @e[tag=survirec.t.$(tag)] run function survirec:v1/private/i/delete
scoreboard players set #kres survirec.v 0

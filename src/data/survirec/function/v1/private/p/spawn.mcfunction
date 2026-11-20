execute unless data storage survirec:in a{tag:""} run function survirec:v1/private/p/killtag with storage survirec:in a
execute if data storage survirec:in a{entity:""} run function survirec:v1/private/p/sum_m
execute if data storage survirec:in a{entity:"minecraft:mannequin"} run function survirec:v1/private/p/sum_m
execute if data storage survirec:in a{entity:"mannequin"} run function survirec:v1/private/p/sum_m
execute unless data storage survirec:in a{entity:""} unless data storage survirec:in a{entity:"minecraft:mannequin"} unless data storage survirec:in a{entity:"mannequin"} run function survirec:v1/private/p/sum_o with storage survirec:in a
scoreboard players add #id survirec.v 1
execute as @e[tag=survirec.new,sort=nearest,limit=1] run function survirec:v1/private/p/init

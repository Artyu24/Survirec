execute if score #rec survirec.v matches 1 unless entity @a[tag=survirec.on] run function survirec:r/lost
scoreboard players add #gt survirec.v 1
execute if score #gt survirec.v matches 1000000.. run scoreboard players set #gt survirec.v 0
execute if score #rec survirec.v matches 1 as @a[tag=survirec.on] run function survirec:r/tick
scoreboard players operation #g survirec.v = #gt survirec.v
scoreboard players operation #g survirec.v %= #10 survirec.v
execute if score #g survirec.v matches 0 run function survirec:near with storage survirec:cfg
execute as @e[tag=survirec.m] run function survirec:i/tick
execute if score #pend survirec.v matches 1 run function survirec:i/grpfire

execute store result score #now survirec.v run time query gametime
execute unless data storage survirec:cfg vault2 run function survirec:v1/private/vault/try
scoreboard players add #gt survirec.v 1
execute if score #gt survirec.v matches 1000000.. run scoreboard players set #gt survirec.v 0
execute as @a[scores={survirec.left=1..}] run function survirec:v1/private/r/rejoin
execute as @a[scores={survirec.use=1..}] if items entity @s weapon.* minecraft:carrot_on_a_stick[minecraft:custom_data~{survirec:{menu:1b}}] run function survirec:v1/private/menu/open
execute as @a[tag=survirec.on] at @s run function survirec:v1/private/r/tick
scoreboard players operation #g survirec.v = #gt survirec.v
scoreboard players operation #g survirec.v %= #10 survirec.v
execute if score #g survirec.v matches 0 run function survirec:v1/private/near with storage survirec:cfg
execute if score #g survirec.v matches 0 as @a[tag=survirec.armed] run function survirec:v1/private/c/armchk
scoreboard players operation #h survirec.v = #gt survirec.v
scoreboard players operation #h survirec.v %= #4 survirec.v
execute if score #h survirec.v matches 0 as @e[tag=survirec.m,tag=survirec.rg] at @s run function survirec:v1/private/rngchk
scoreboard players operation #q5 survirec.v = #gt survirec.v
scoreboard players operation #q5 survirec.v %= #5 survirec.v
execute if score #q5 survirec.v matches 0 as @e[type=minecraft:text_display,tag=survirec.start] at @s run function survirec:v1/private/r/marker
execute if score #npulse survirec.v matches 1.. as @e[type=minecraft:marker,tag=survirec.pulse] if score #now survirec.v >= @s survirec.due at @s run function survirec:v1/private/i/pulseoff
execute as @e[tag=survirec.m] run function survirec:v1/private/i/tick
execute if score #pend survirec.v matches 1 run function survirec:v1/private/i/grpfire

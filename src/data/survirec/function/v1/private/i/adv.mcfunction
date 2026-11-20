scoreboard players operation @s survirec.pr -= @s survirec.n100
scoreboard players operation @s survirec.bx += @s survirec.dx
scoreboard players operation @s survirec.by += @s survirec.dy
scoreboard players operation @s survirec.bz += @s survirec.dz
scoreboard players operation @s survirec.byw += @s survirec.dyw
scoreboard players operation @s survirec.bpt += @s survirec.dpt
scoreboard players add @s survirec.seg 1
execute if score @s survirec.seg >= @s survirec.len run function survirec:v1/private/i/end
execute if score @s survirec.run matches 1 run function survirec:v1/private/i/load
execute if score @s survirec.run matches 1 if score @s survirec.pr >= @s survirec.n100 run function survirec:v1/private/i/adv

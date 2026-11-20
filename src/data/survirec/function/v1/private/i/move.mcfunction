scoreboard players operation #t survirec.v = @s survirec.dx
scoreboard players operation #t survirec.v *= @s survirec.pr
scoreboard players operation #t survirec.v /= @s survirec.dv
scoreboard players operation #t survirec.v += @s survirec.bx
execute store result storage survirec:t x double 0.001 run scoreboard players get #t survirec.v
scoreboard players operation #t survirec.v = @s survirec.dy
scoreboard players operation #t survirec.v *= @s survirec.pr
scoreboard players operation #t survirec.v /= @s survirec.dv
scoreboard players operation #t survirec.v += @s survirec.by
execute store result storage survirec:t y double 0.001 run scoreboard players get #t survirec.v
scoreboard players operation #t survirec.v = @s survirec.dz
scoreboard players operation #t survirec.v *= @s survirec.pr
scoreboard players operation #t survirec.v /= @s survirec.dv
scoreboard players operation #t survirec.v += @s survirec.bz
execute store result storage survirec:t z double 0.001 run scoreboard players get #t survirec.v
scoreboard players operation #t survirec.v = @s survirec.dyw
scoreboard players operation #t survirec.v *= @s survirec.pr
scoreboard players operation #t survirec.v /= @s survirec.dv
scoreboard players operation #t survirec.v += @s survirec.byw
execute store result storage survirec:t yaw double 0.01 run scoreboard players get #t survirec.v
scoreboard players operation #t survirec.v = @s survirec.dpt
scoreboard players operation #t survirec.v *= @s survirec.pr
scoreboard players operation #t survirec.v /= @s survirec.dv
scoreboard players operation #t survirec.v += @s survirec.bpt
execute if score #t survirec.v matches 9001.. run scoreboard players set #t survirec.v 9000
execute if score #t survirec.v matches ..-9001 run scoreboard players set #t survirec.v -9000
execute store result storage survirec:t pitch double 0.01 run scoreboard players get #t survirec.v
function survirec:v1/private/i/tp with storage survirec:t
execute if score @s survirec.rb matches 1 run function survirec:v1/private/i/body with storage survirec:t
execute if score @s survirec.st matches 1 run scoreboard players set @s survirec.pl 1

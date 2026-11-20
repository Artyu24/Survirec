function survirec:v1/private/r/ctx
scoreboard players set #fl survirec.v 0
scoreboard players operation #rx survirec.v = @s survirec.rox
scoreboard players operation #rx survirec.v -= @s survirec.rpx
scoreboard players operation #ry survirec.v = @s survirec.roy
scoreboard players operation #ry survirec.v -= @s survirec.rpy
scoreboard players operation #rz survirec.v = @s survirec.roz
scoreboard players operation #rz survirec.v -= @s survirec.rpz
scoreboard players operation #ryw survirec.v = @s survirec.royw
scoreboard players operation #ryw survirec.v -= @s survirec.rpyw
execute if score #ryw survirec.v matches 18001.. run scoreboard players remove #ryw survirec.v 36000
execute if score #ryw survirec.v matches ..-18001 run scoreboard players add #ryw survirec.v 36000
scoreboard players operation #rpt survirec.v = @s survirec.ropt
scoreboard players operation #rpt survirec.v -= @s survirec.rppt
scoreboard players set #cs survirec.v 10
function survirec:v1/private/r/closeloop

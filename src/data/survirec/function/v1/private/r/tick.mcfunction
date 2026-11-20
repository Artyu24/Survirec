function survirec:v1/private/r/ctx
execute if score @s survirec.ruf matches 1 run function survirec:v1/private/r/usego
scoreboard players set @s survirec.rplf 0
function survirec:v1/private/r/look
scoreboard players set #fl survirec.v 0
scoreboard players set #sk survirec.v 0
execute if score @s survirec.sn > @s survirec.snp run scoreboard players set #sk survirec.v 1
execute if score #sk survirec.v matches 1 run scoreboard players add #fl survirec.v 1
execute if score @s survirec.sw > @s survirec.swp run scoreboard players add #fl survirec.v 2
execute if score @s survirec.gl > @s survirec.glp run scoreboard players add #fl survirec.v 4
scoreboard players operation @s survirec.snp = @s survirec.sn
scoreboard players operation @s survirec.swp = @s survirec.sw
scoreboard players operation @s survirec.glp = @s survirec.gl
execute unless score @s survirec.rchal matches 1 if score @s survirec.use matches 1.. if items entity @s weapon.* minecraft:carrot_on_a_stick[minecraft:custom_data~{survirec:{stop:1b}}] run return run function survirec:v1/private/r/click
scoreboard players set @s survirec.use 0
scoreboard players add @s survirec.rtime 1
execute if score @s survirec.rchal matches 1 if score @s survirec.rtime >= @s survirec.rcdur run return run function survirec:v1/private/c/end
scoreboard players operation #q survirec.v = @s survirec.rtime
scoreboard players operation #q survirec.v %= #10 survirec.v
execute if score #q survirec.v matches 0 run function survirec:v1/private/r/hud
scoreboard players operation #q survirec.v = @s survirec.rtime
scoreboard players operation #q survirec.v %= #20 survirec.v
execute if score #q survirec.v matches 0 run function survirec:v1/private/r/eq
scoreboard players add @s survirec.rtk 1
execute if score @s survirec.rtk >= @s survirec.revery run function survirec:v1/private/r/key

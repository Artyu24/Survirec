scoreboard players set #fl survirec.v 0
scoreboard players set #sk survirec.v 0
execute if score @s survirec.sn > @s survirec.snp run scoreboard players set #sk survirec.v 1
execute if score #sk survirec.v matches 1 run scoreboard players add #fl survirec.v 1
execute if score @s survirec.sw > @s survirec.swp run scoreboard players add #fl survirec.v 2
execute if score @s survirec.gl > @s survirec.glp run scoreboard players add #fl survirec.v 4
scoreboard players operation @s survirec.snp = @s survirec.sn
scoreboard players operation @s survirec.swp = @s survirec.sw
scoreboard players operation @s survirec.glp = @s survirec.gl
execute if score @s survirec.trg matches 1.. run return run function survirec:r/trg
execute unless score #chal survirec.v matches 1 if score @s survirec.use matches 1.. run return run function survirec:r/click
scoreboard players add #ticks survirec.v 1
execute if score #chal survirec.v matches 1 if score #ticks survirec.v >= #cdur survirec.v run return run function survirec:c/end
scoreboard players operation #q survirec.v = #ticks survirec.v
scoreboard players operation #q survirec.v %= #5 survirec.v
execute if score #q survirec.v matches 0 at @e[type=minecraft:text_display,tag=survirec.start] run function survirec:r/marker
scoreboard players operation #q survirec.v = #ticks survirec.v
scoreboard players operation #q survirec.v %= #10 survirec.v
execute if score #q survirec.v matches 0 run function survirec:r/hud
scoreboard players operation #q survirec.v = #ticks survirec.v
scoreboard players operation #q survirec.v %= #20 survirec.v
execute if score #q survirec.v matches 0 run function survirec:r/eq
scoreboard players add #tk survirec.v 1
execute if score #tk survirec.v >= #n survirec.v run function survirec:r/key

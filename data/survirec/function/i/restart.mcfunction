scoreboard players set @s survirec.seg 0
scoreboard players operation @s survirec.bx = @s survirec.ax
scoreboard players operation @s survirec.by = @s survirec.ay
scoreboard players operation @s survirec.bz = @s survirec.az
scoreboard players operation @s survirec.byw = @s survirec.yw0
scoreboard players operation @s survirec.bpt = @s survirec.pt0
scoreboard players set @s survirec.st 0
scoreboard players set @s survirec.ei 0
scoreboard players set @s survirec.ek 0
execute if score @s survirec.hs matches 1 run scoreboard players set @s survirec.si 0
execute if score @s survirec.hs matches 1 run function survirec:i/swload

scoreboard players set @s survirec.rs 0
execute if score @s survirec.rst matches 1.. run function survirec:v1/private/vault/restore
execute unless score @s survirec.len matches 1.. run return 0
scoreboard players operation @s survirec.dx = @s survirec.ax
scoreboard players operation @s survirec.dx -= @s survirec.bx
scoreboard players operation @s survirec.dy = @s survirec.ay
scoreboard players operation @s survirec.dy -= @s survirec.by
scoreboard players operation @s survirec.dz = @s survirec.az
scoreboard players operation @s survirec.dz -= @s survirec.bz
scoreboard players operation @s survirec.dyw = @s survirec.yw0
scoreboard players operation @s survirec.dyw -= @s survirec.byw
execute if score @s survirec.dyw matches 18001.. run scoreboard players remove @s survirec.dyw 36000
execute if score @s survirec.dyw matches ..-18001 run scoreboard players add @s survirec.dyw 36000
scoreboard players operation @s survirec.dpt = @s survirec.pt0
scoreboard players operation @s survirec.dpt -= @s survirec.bpt
scoreboard players set @s survirec.dv 40
scoreboard players set @s survirec.pr 0
scoreboard players set @s survirec.st 0
scoreboard players set @s survirec.pl 0
scoreboard players set @s survirec.fn 0
execute if score @s survirec.fx matches 0 unless score @s survirec.fn = @s survirec.fl run function survirec:v1/private/i/pose
scoreboard players set @s survirec.run 2

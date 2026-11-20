execute store result score @s survirec.rux run data get entity @e[type=minecraft:marker,tag=survirec.cur,limit=1] Pos[0]
execute store result score @s survirec.ruy run data get entity @e[type=minecraft:marker,tag=survirec.cur,limit=1] Pos[1]
execute store result score @s survirec.ruz run data get entity @e[type=minecraft:marker,tag=survirec.cur,limit=1] Pos[2]
scoreboard players operation @s survirec.rut = @s survirec.rtime
scoreboard players set @s survirec.ruf 1

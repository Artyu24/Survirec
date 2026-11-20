execute store result score #sx survirec.v run data get entity @s Pos[0]
execute store result score #sy survirec.v run data get entity @s Pos[1]
execute store result score #sz survirec.v run data get entity @s Pos[2]
execute store result storage survirec:tmp sn.x int 1 run scoreboard players remove #sx survirec.v 1
execute store result storage survirec:tmp sn.y int 1 run scoreboard players remove #sy survirec.v 1
execute store result storage survirec:tmp sn.z int 1 run scoreboard players remove #sz survirec.v 1

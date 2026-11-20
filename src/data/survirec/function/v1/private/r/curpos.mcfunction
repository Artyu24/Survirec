# position du bloc touché, relative au point de départ de l'enregistrement
execute store result score #hx survirec.v run data get entity @e[type=minecraft:marker,tag=survirec.cur,limit=1] Pos[0]
execute store result score #hy survirec.v run data get entity @e[type=minecraft:marker,tag=survirec.cur,limit=1] Pos[1]
execute store result score #hz survirec.v run data get entity @e[type=minecraft:marker,tag=survirec.cur,limit=1] Pos[2]
scoreboard players operation #hx survirec.v -= @s survirec.rbx
scoreboard players operation #hy survirec.v -= @s survirec.rby
scoreboard players operation #hz survirec.v -= @s survirec.rbz
execute store result storage survirec:tmp ev.x int 1 run scoreboard players get #hx survirec.v
execute store result storage survirec:tmp ev.y int 1 run scoreboard players get #hy survirec.v
execute store result storage survirec:tmp ev.z int 1 run scoreboard players get #hz survirec.v

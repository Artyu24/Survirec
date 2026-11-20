# démarre un enregistrement pour @s ; survirec:tmp meta = {name, n} posé par l'appelant
execute unless score @s survirec.pid matches 1.. run function survirec:v1/private/c/newpid
function survirec:v1/private/r/ctx
tag @s add survirec.on
scoreboard players set @s survirec.rchal 0
execute store result score @s survirec.revery run data get storage survirec:tmp meta.n
scoreboard players set @s survirec.rkf 0
scoreboard players set @s survirec.rkt 0
scoreboard players set @s survirec.rtk 0
scoreboard players set @s survirec.rtime 0
scoreboard players set @s survirec.rlsw -1
execute store result score @s survirec.rpx run data get entity @s Pos[0] 1000
execute store result score @s survirec.rpy run data get entity @s Pos[1] 1000
execute store result score @s survirec.rpz run data get entity @s Pos[2] 1000
execute store result score @s survirec.rpyw run data get entity @s Rotation[0] 100
execute store result score @s survirec.rppt run data get entity @s Rotation[1] 100
scoreboard players operation @s survirec.rox = @s survirec.rpx
scoreboard players operation @s survirec.roy = @s survirec.rpy
scoreboard players operation @s survirec.roz = @s survirec.rpz
scoreboard players operation @s survirec.royw = @s survirec.rpyw
scoreboard players operation @s survirec.ropt = @s survirec.rppt
execute store result storage survirec:tmp meta.y int 1 run scoreboard players get @s survirec.rpyw
execute store result storage survirec:tmp meta.p int 1 run scoreboard players get @s survirec.rppt
execute store result storage survirec:tmp meta.sx double 0.001 run scoreboard players get @s survirec.rpx
execute store result storage survirec:tmp meta.sy double 0.001 run scoreboard players get @s survirec.rpy
execute store result storage survirec:tmp meta.sz double 0.001 run scoreboard players get @s survirec.rpz
function survirec:v1/private/r/initstore with storage survirec:ctx
scoreboard players operation #me survirec.v = @s survirec.pid
function survirec:v1/private/r/killmk
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["survirec.rk","survirec.eye","survirec.mk2","smithed.entity","smithed.strict"]}
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["survirec.rk","survirec.ray","survirec.mk2","smithed.entity","smithed.strict"]}
scoreboard players operation @e[type=minecraft:marker,tag=survirec.mk2] survirec.pid = #me survirec.v
tag @e[type=minecraft:marker,tag=survirec.mk2] remove survirec.mk2
execute store result score @s survirec.rbx run data get entity @s Pos[0]
execute store result score @s survirec.rby run data get entity @s Pos[1]
execute store result score @s survirec.rbz run data get entity @s Pos[2]
scoreboard players set @s survirec.rlk 0
scoreboard players set @s survirec.ruf 0
scoreboard players set @s survirec.rplf 0
scoreboard players set @s survirec.ratk -1
# emplacement du cube regardé (zone 2), propre à ce joueur
scoreboard players operation #c7 survirec.v = @s survirec.pid
scoreboard players operation #c7 survirec.v %= #1536 survirec.v
function survirec:v1/private/r/cubexyz
scoreboard players operation @s survirec.rlkx = #cx survirec.v
scoreboard players add @s survirec.rlkx 16
scoreboard players operation @s survirec.rlky = #cy survirec.v
scoreboard players operation @s survirec.rlkz = #cz survirec.v
scoreboard players add @s survirec.sn 0
scoreboard players add @s survirec.sw 0
scoreboard players add @s survirec.gl 0
scoreboard players operation @s survirec.snp = @s survirec.sn
scoreboard players operation @s survirec.swp = @s survirec.sw
scoreboard players operation @s survirec.glp = @s survirec.gl
scoreboard players set @s survirec.use 0
function survirec:v1/private/r/eq

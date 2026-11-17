scoreboard players set #rec survirec.v 1
tag @s add survirec.on
data modify storage survirec:tmp d set value []
data modify storage survirec:tmp chunks set value []
data modify storage survirec:tmp e set value []
data modify storage survirec:tmp s set value []
scoreboard players set #lsw survirec.v -1
data remove storage survirec:tmp eq
scoreboard players set #kf survirec.v 0
scoreboard players set #kt survirec.v 0
scoreboard players set #tk survirec.v 0
scoreboard players set #ticks survirec.v 0
execute store result score #px survirec.v run data get entity @s Pos[0] 1000
execute store result score #py survirec.v run data get entity @s Pos[1] 1000
execute store result score #pz survirec.v run data get entity @s Pos[2] 1000
execute store result score #pyw survirec.v run data get entity @s Rotation[0] 100
execute store result score #ppt survirec.v run data get entity @s Rotation[1] 100
scoreboard players operation #ox survirec.v = #px survirec.v
scoreboard players operation #oy survirec.v = #py survirec.v
scoreboard players operation #oz survirec.v = #pz survirec.v
scoreboard players operation #oyw survirec.v = #pyw survirec.v
scoreboard players operation #opt survirec.v = #ppt survirec.v
execute store result storage survirec:tmp meta.y int 1 run scoreboard players get #pyw survirec.v
execute store result storage survirec:tmp meta.p int 1 run scoreboard players get #ppt survirec.v
execute store result storage survirec:tmp meta.sx double 0.001 run scoreboard players get #px survirec.v
execute store result storage survirec:tmp meta.sy double 0.001 run scoreboard players get #py survirec.v
execute store result storage survirec:tmp meta.sz double 0.001 run scoreboard players get #pz survirec.v
scoreboard players add @s survirec.sn 0
scoreboard players add @s survirec.sw 0
scoreboard players add @s survirec.gl 0
scoreboard players operation @s survirec.snp = @s survirec.sn
scoreboard players operation @s survirec.swp = @s survirec.sw
scoreboard players operation @s survirec.glp = @s survirec.gl
scoreboard players set @s survirec.use 0
function survirec:r/eq
function #survirec:v1/signals/on_record_start

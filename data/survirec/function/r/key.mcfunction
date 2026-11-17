scoreboard players set #tk survirec.v 0
execute store result score #cx survirec.v run data get entity @s Pos[0] 1000
execute store result score #cy survirec.v run data get entity @s Pos[1] 1000
execute store result score #cz survirec.v run data get entity @s Pos[2] 1000
execute store result score #cyw survirec.v run data get entity @s Rotation[0] 100
execute store result score #cpt survirec.v run data get entity @s Rotation[1] 100
scoreboard players operation #dx survirec.v = #cx survirec.v
scoreboard players operation #dx survirec.v -= #px survirec.v
scoreboard players operation #dy survirec.v = #cy survirec.v
scoreboard players operation #dy survirec.v -= #py survirec.v
scoreboard players operation #dz survirec.v = #cz survirec.v
scoreboard players operation #dz survirec.v -= #pz survirec.v
scoreboard players operation #dyw survirec.v = #cyw survirec.v
scoreboard players operation #dyw survirec.v -= #pyw survirec.v
execute if score #dyw survirec.v matches 18001.. run scoreboard players remove #dyw survirec.v 36000
execute if score #dyw survirec.v matches ..-18001 run scoreboard players add #dyw survirec.v 36000
scoreboard players operation #dpt survirec.v = #cpt survirec.v
scoreboard players operation #dpt survirec.v -= #ppt survirec.v
scoreboard players operation #px survirec.v = #cx survirec.v
scoreboard players operation #py survirec.v = #cy survirec.v
scoreboard players operation #pz survirec.v = #cz survirec.v
scoreboard players operation #pyw survirec.v = #cyw survirec.v
scoreboard players operation #ppt survirec.v = #cpt survirec.v
function survirec:r/append

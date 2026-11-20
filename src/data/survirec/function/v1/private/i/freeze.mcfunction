scoreboard players set @s survirec.dx 0
scoreboard players set @s survirec.dy 0
scoreboard players set @s survirec.dz 0
scoreboard players set @s survirec.dyw 0
scoreboard players set @s survirec.dpt 0
scoreboard players set @s survirec.pr 0
scoreboard players set @s survirec.run 0
execute if score @s survirec.grp matches 0 if score @s survirec.rst matches 2 run function survirec:v1/private/vault/restore
function survirec:v1/private/i/move
execute if score @s survirec.grp matches 1.. run function survirec:v1/private/i/grpfreeze

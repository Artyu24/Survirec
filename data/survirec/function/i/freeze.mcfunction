scoreboard players set @s survirec.dx 0
scoreboard players set @s survirec.dy 0
scoreboard players set @s survirec.dz 0
scoreboard players set @s survirec.dyw 0
scoreboard players set @s survirec.dpt 0
scoreboard players set @s survirec.pr 0
scoreboard players set @s survirec.run 0
function survirec:i/move
execute if score @s survirec.grp matches 1.. run function survirec:i/grpfreeze

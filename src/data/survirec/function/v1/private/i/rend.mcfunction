scoreboard players operation @s survirec.gs = #gt survirec.v
scoreboard players operation @s survirec.dv = @s survirec.n100
scoreboard players set @s survirec.pr 0
scoreboard players set @s survirec.fl -1
scoreboard players set @s survirec.pl 0
function survirec:v1/private/i/restart
scoreboard players set @s survirec.run 1
function survirec:v1/private/i/load
function survirec:v1/private/i/move
scoreboard players operation #rg survirec.v = @s survirec.grp
execute as @a[tag=survirec.armed] if score @s survirec.rwg = #rg survirec.v run function survirec:v1/private/c/launch

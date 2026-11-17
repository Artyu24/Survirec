execute unless score @s survirec.near matches 1 run return 0
scoreboard players operation @s survirec.pr += @s survirec.spd
execute if score @s survirec.pr >= @s survirec.dv run return run function survirec:i/rend
function survirec:i/move

execute unless score @s survirec.near matches 1 run return 0
scoreboard players add @s survirec.pr 1
execute if score @s survirec.pr >= @s survirec.dv run return run function survirec:v1/private/i/rend
execute if function survirec:v1/private/i/turn run function survirec:v1/private/i/move

execute if score @s survirec.run matches 2 run return run function survirec:i/rtick
execute unless score @s survirec.run matches 1 run return 0
execute unless score @s survirec.near matches 1 run return 0
scoreboard players operation @s survirec.pr += @s survirec.spd
execute if score @s survirec.pr >= @s survirec.n100 run function survirec:i/adv
execute unless score @s survirec.run matches 1 run return 0
execute if score @s survirec.hs matches 1 run function survirec:i/swchk
execute if score @s survirec.st matches 1 if score @s survirec.pl matches 1 run return 0
function survirec:i/move

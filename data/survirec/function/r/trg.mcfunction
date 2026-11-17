scoreboard players operation #tg survirec.v = @s survirec.trg
scoreboard players set @s survirec.trg 0
execute if score #tg survirec.v matches 2 run return run function survirec:r/close
function survirec:r/finish

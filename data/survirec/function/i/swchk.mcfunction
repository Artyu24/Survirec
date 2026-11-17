scoreboard players operation #tm survirec.v = @s survirec.seg
scoreboard players operation #tm survirec.v *= @s survirec.n100
scoreboard players operation #tm survirec.v += @s survirec.pr
execute if score #tm survirec.v >= @s survirec.sk run function survirec:i/sw

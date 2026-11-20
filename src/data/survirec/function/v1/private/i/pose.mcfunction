scoreboard players operation @s survirec.fl = @s survirec.fn
execute if score @s survirec.fl matches 0 run data modify entity @s pose set value "standing"
execute if score @s survirec.fl matches 1 run data modify entity @s pose set value "crouching"
execute if score @s survirec.fl matches 2..3 run data modify entity @s pose set value "swimming"
execute if score @s survirec.fl matches 4..7 run data modify entity @s pose set value "fall_flying"
execute if score @s survirec.fl matches 4..7 run data modify entity @s OnGround set value 0b
execute if score @s survirec.fl matches 4..7 run data modify entity @s FallFlying set value 1b
execute unless score @s survirec.fl matches 4..7 run data modify entity @s FallFlying set value 0b

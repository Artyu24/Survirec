$data modify entity @s pose set value "$(pose)"
execute if data storage survirec:in a{pose:"fall_flying"} run data modify entity @s OnGround set value 0b
execute if data storage survirec:in a{pose:"fall_flying"} run data modify entity @s FallFlying set value 1b
scoreboard players set @s survirec.fx 1

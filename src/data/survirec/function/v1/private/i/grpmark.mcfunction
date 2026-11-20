scoreboard players set #alive survirec.v 0
execute as @e[tag=survirec.m] if score @s survirec.grp = #g survirec.v if score @s survirec.run matches 1..2 run scoreboard players set #alive survirec.v 1
execute if score #alive survirec.v matches 0 as @e[tag=survirec.m] if score @s survirec.grp = #g survirec.v unless score @s survirec.gloop matches 0 unless score @s survirec.gloop matches 2 run scoreboard players set @s survirec.rs 1
execute if score #alive survirec.v matches 0 as @e[tag=survirec.m] if score @s survirec.grp = #g survirec.v if score @s survirec.rsb matches 1 run function survirec:v1/private/i/pulse
execute if score #alive survirec.v matches 0 as @e[tag=survirec.m] if score @s survirec.grp = #g survirec.v if score @s survirec.gloop matches 2 run function survirec:v1/private/i/delete
execute if score #alive survirec.v matches 0 as @e[tag=survirec.m] if score @s survirec.grp = #g survirec.v if score @s survirec.gloop matches 0 if score @s survirec.rst matches 2 run function survirec:v1/private/vault/restore
execute if score #alive survirec.v matches 0 run scoreboard players set #pend survirec.v 1

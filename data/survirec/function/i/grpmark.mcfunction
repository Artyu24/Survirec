scoreboard players set #alive survirec.v 0
execute as @e[tag=survirec.m] if score @s survirec.grp = #g survirec.v if score @s survirec.run matches 1..2 run scoreboard players set #alive survirec.v 1
execute if score #alive survirec.v matches 0 as @e[tag=survirec.m] if score @s survirec.grp = #g survirec.v run scoreboard players set @s survirec.rs 1
execute if score #alive survirec.v matches 0 run scoreboard players set #pend survirec.v 1

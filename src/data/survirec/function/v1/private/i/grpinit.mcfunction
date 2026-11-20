tag @s add survirec.me
scoreboard players operation #g survirec.v = @s survirec.grp
scoreboard players set #alive survirec.v 0
scoreboard players set #same survirec.v 0
execute as @e[tag=survirec.m,tag=!survirec.me] if score @s survirec.grp = #g survirec.v if score @s survirec.run matches 1..2 run scoreboard players set #alive survirec.v 1
execute as @e[tag=survirec.m,tag=!survirec.me] if score @s survirec.grp = #g survirec.v if score @s survirec.run matches 1 if score @s survirec.gs = #gt survirec.v run scoreboard players set #same survirec.v 1
tag @s remove survirec.me
execute if score #alive survirec.v matches 1 unless score #same survirec.v matches 1 run scoreboard players set @s survirec.run 0
execute unless score @s survirec.run matches 0 run scoreboard players operation @s survirec.gs = #gt survirec.v

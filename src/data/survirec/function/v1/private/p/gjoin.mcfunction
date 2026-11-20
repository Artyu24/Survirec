# rejoint le groupe du même nom le plus proche (à moins de gr blocs), sinon en crée un nouveau
scoreboard players set #found survirec.v 0
$execute as @e[tag=survirec.m,tag=survirec.g.$(group),distance=..$(gr),sort=nearest,limit=1] run scoreboard players operation #found survirec.v = @s survirec.grp
execute if score #found survirec.v matches ..0 run scoreboard players add #gid survirec.v 1
execute if score #found survirec.v matches ..0 run scoreboard players operation #found survirec.v = #gid survirec.v
scoreboard players operation @s survirec.grp = #found survirec.v
$tag @s add survirec.g.$(group)

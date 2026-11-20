# cherche le groupe du même nom le plus proche du joueur ; aucun -> l'enregistrement démarre tout de suite
scoreboard players set #found survirec.v 0
$execute at @s as @e[tag=survirec.m,tag=survirec.g.$(group),distance=..$(group_radius),sort=nearest,limit=1] run scoreboard players operation #found survirec.v = @s survirec.grp
execute if score #found survirec.v matches ..0 run return run function survirec:v1/private/r/begin
execute store result storage survirec:in cfg.grp int 1 run scoreboard players get #found survirec.v
function survirec:v1/private/r/arm

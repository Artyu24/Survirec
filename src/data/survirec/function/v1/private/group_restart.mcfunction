# radius > 0 : relance la scène de ce nom la plus proche. radius 0 : relance toutes les scènes de ce nom
$execute if data storage survirec:in cfg{radius:0} as @e[tag=survirec.m,tag=survirec.g.$(group)] run scoreboard players set @s survirec.rs 1
scoreboard players set #found survirec.v 0
$execute unless data storage survirec:in cfg{radius:0} as @e[tag=survirec.m,tag=survirec.g.$(group),distance=..$(radius),sort=nearest,limit=1] run scoreboard players operation #found survirec.v = @s survirec.grp
execute if score #found survirec.v matches 1.. as @e[tag=survirec.m] if score @s survirec.grp = #found survirec.v run scoreboard players set @s survirec.rs 1
function survirec:v1/private/i/grpfire

# le joueur revient après une déconnexion : son enregistrement est abandonné
scoreboard players set @s survirec.left 0
execute unless entity @s[tag=survirec.on] unless entity @s[tag=survirec.armed] run return 0
function survirec:v1/private/r/abort1
tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Ton enregistrement a été annulé (déconnexion).",color:"yellow"}]

# copie l'enregistrement du joueur vers survirec:tmp (et survirec:c pour une épreuve) avant l'export
function survirec:v1/private/r/ctx
data modify storage survirec:tmp a set value []
function survirec:v1/private/r/pull2 with storage survirec:ctx
scoreboard players operation #kt survirec.v = @s survirec.rkt
scoreboard players operation #kf survirec.v = @s survirec.rkf

# function survirec:start {name:"walk",every:4}
execute if score #rec survirec.v matches 1 run return run tellraw @s {text:"[Survirec] Un enregistrement est déjà en cours (function survirec:stop).",color:"red"}
$scoreboard players set #n survirec.v $(every)
execute unless score #n survirec.v matches 1..100 run return run tellraw @s {text:"[Survirec] every doit être entre 1 et 100.",color:"red"}
$data modify storage survirec:tmp meta set value {name:"$(name)",n:$(every)}
function survirec:r/begin

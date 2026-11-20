# $(f) = champ de survirec:in cfg à valider (obligatoire)
data remove storage survirec:v s
$data modify storage survirec:v s set from storage survirec:in cfg.$(f)
function survirec:v1/private/validate
execute if score #valid survirec.v matches 0 run scoreboard players set #bad survirec.v 1

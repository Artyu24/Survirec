$execute unless data storage survirec:lib recs.$(name) run return run tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Aucun enregistrement nommé ",color:"red"},{text:"$(name)",color:"gold"},{text:".",color:"red"}]
$data modify storage survirec:tmp meta set from storage survirec:lib recs.$(name).meta
$data modify storage survirec:tmp chunks set from storage survirec:lib recs.$(name).chunks
$data modify storage survirec:tmp e set from storage survirec:lib recs.$(name).e
$data modify storage survirec:tmp s set from storage survirec:lib recs.$(name).s
data modify storage survirec:tmp a set value []
$data modify storage survirec:tmp a set from storage survirec:lib recs.$(name).a
function survirec:v1/private/r/export

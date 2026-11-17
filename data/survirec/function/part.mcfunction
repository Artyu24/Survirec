# Partie intermédiaire d'une longue séquence (chaîne de command blocks)
$scoreboard players set #f survirec.v $(f)
execute if score #f survirec.v matches 1 run data modify storage survirec:t pend set value []
$data modify storage survirec:t chunk set value $(d)
data modify storage survirec:t pend append from storage survirec:t chunk[]
data remove storage survirec:t chunk

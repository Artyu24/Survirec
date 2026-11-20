# Supprime une séquence du monde (données de lecture et enregistrement gardé)
$data remove storage survirec:data seqs.$(name)
$data remove storage survirec:lib recs.$(name)
$data remove storage survirec:lib names[{name:"$(name)"}]
$tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Séquence ",color:"green"},{text:"$(name)",color:"gold"},{text:" supprimée.",color:"green"}]

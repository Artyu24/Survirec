# Valide la chaîne de survirec:v s : lettres, chiffres et _ , 1 à 32 caractères. Résultat : #valid 1 ou 0
scoreboard players set #valid survirec.v 1
scoreboard players set #vlen survirec.v 0
execute store result score #vlen survirec.v run data get storage survirec:v s
execute unless score #vlen survirec.v matches 1..32 run return run scoreboard players set #valid survirec.v 0
scoreboard players set #vi survirec.v 0
function survirec:v1/private/vloop

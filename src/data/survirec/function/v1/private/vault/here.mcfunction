# sauvegarde le bloc courant ; #bkm 1 = remise en place sans mise à jour (blocs doubles)
data modify storage survirec:t bka set value {x:0,y:0,z:0,m:"replace"}
execute if score #bkm survirec.v matches 1 run data modify storage survirec:t bka.m set value "strict"
execute summon minecraft:marker run function survirec:v1/private/vault/herepos
function survirec:v1/private/vault/bk

# positionné sur le bloc support : on le remplace un instant puis on le remet avec mise à jour,
# pour que les blocs autour (command block, redstone) voient le courant comme avec un vrai joueur
execute unless data storage survirec:cfg vault run return 0
clone ~ ~ ~ ~ ~ ~ to survirec:vault 15 319 15 strict
setblock ~ ~ ~ minecraft:barrier strict
clone from survirec:vault 15 319 15 15 319 15 ~ ~ ~

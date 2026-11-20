# cage de barrières : chaque copie est isolée (ni chute, ni écoulement, ni mise à jour entre copies)
execute in survirec:vault run fill 0 -64 0 15 31 15 minecraft:barrier strict
execute in survirec:vault run fill 0 32 0 15 127 15 minecraft:barrier strict
execute in survirec:vault run fill 0 128 0 15 223 15 minecraft:barrier strict
execute in survirec:vault run fill 0 224 0 15 319 15 minecraft:barrier strict
data modify storage survirec:cfg vault set value 1b

# Toutes les 10 ticks : un mannequin n'est animé que si un joueur est à moins de r blocs
$execute as @e[tag=survirec.m] at @s store success score @s survirec.near if entity @a[distance=..$(r)]

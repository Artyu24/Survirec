$clone from survirec:vault $(bx) $(by) $(bz) $(bx2) $(by2) $(bz2) $(x) $(y) $(z)
$execute in survirec:vault run fill $(bx) $(by) $(bz) $(bx2) $(by2) $(bz2) minecraft:barrier strict
$data modify storage survirec:cfg cfree append value {bx:$(bx),by:$(by),bz:$(bz),bx2:$(bx2),by2:$(by2),bz2:$(bz2)}

$execute in survirec:vault run clone $(lx) $(ly) $(lz) $(lx2) $(ly2) $(lz2) $(bx) $(by) $(bz) strict
$data modify storage survirec:rec p.p$(pid).wb append value {bx:$(bx),by:$(by),bz:$(bz),bx2:$(bx2),by2:$(by2),bz2:$(bz2),x:$(x),y:$(y),z:$(z)}

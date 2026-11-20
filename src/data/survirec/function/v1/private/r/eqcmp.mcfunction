$execute store success score #ch survirec.v run data modify storage survirec:rec p.p$(pid).eq set from storage survirec:tmp neweq
$execute if score #ch survirec.v matches 1 run data modify storage survirec:rec p.p$(pid).e append value {k:0,v:{}}
$execute if score #ch survirec.v matches 1 store result storage survirec:rec p.p$(pid).e[-1].k int 1 run scoreboard players get @s survirec.rkt
$execute if score #ch survirec.v matches 1 run data modify storage survirec:rec p.p$(pid).e[-1].v set from storage survirec:tmp neweq

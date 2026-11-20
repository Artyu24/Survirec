$data modify storage survirec:rec p.p$(pid).s append value 0
$execute store result storage survirec:rec p.p$(pid).s[-1] int 1 run scoreboard players get @s survirec.rtime

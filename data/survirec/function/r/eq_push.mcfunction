data modify storage survirec:tmp e append value {k:0,v:{}}
execute store result storage survirec:tmp e[-1].k int 1 run scoreboard players get #kt survirec.v
data modify storage survirec:tmp e[-1].v set from storage survirec:tmp neweq

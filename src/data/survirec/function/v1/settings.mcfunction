$data modify storage survirec:in api set value $(with)
data modify storage survirec:in cfg set value {range:128,move_every:2}
data modify storage survirec:in cfg.range set from storage survirec:cfg r
execute store result storage survirec:in cfg.move_every int 1 run scoreboard players get #step survirec.v
data modify storage survirec:in cfg merge from storage survirec:in api
data modify storage survirec:cfg r set from storage survirec:in cfg.range
execute store result score #step survirec.v run data get storage survirec:in cfg.move_every
execute unless score #step survirec.v matches 1..20 run scoreboard players set #step survirec.v 2
tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Portée : ",color:"green"},{storage:"survirec:cfg",nbt:"r",color:"gold"},{text:" blocs · position mise à jour tous les ",color:"green"},{score:{name:"#step",objective:"survirec.v"},color:"gold"},{text:" ticks",color:"green"}]

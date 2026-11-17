execute if score #lsw survirec.v = #ticks survirec.v run return 0
scoreboard players operation #lsw survirec.v = #ticks survirec.v
data modify storage survirec:tmp s append value 0
execute store result storage survirec:tmp s[-1] int 1 run scoreboard players get #ticks survirec.v

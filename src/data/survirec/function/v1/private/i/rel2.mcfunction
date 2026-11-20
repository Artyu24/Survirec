execute store result score #rt survirec.v run data get storage survirec:t rll[0].t
execute if score #rall survirec.v matches 1 run scoreboard players set #rt survirec.v -1
execute if score #rt survirec.v <= #now survirec.v run function survirec:v1/private/i/rel3 with storage survirec:t rll[0]
execute if score #rt survirec.v > #now survirec.v run function survirec:v1/private/i/relkeep
data remove storage survirec:t rll[0]
execute if data storage survirec:t rll[0] run function survirec:v1/private/i/rel2

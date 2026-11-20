scoreboard players set #ep survirec.v -1
execute store result score #ep survirec.v run data get storage survirec:tmp it[0].pid
execute if score #ep survirec.v = #me survirec.v run function survirec:v1/private/menu/rline with storage survirec:tmp it[0]
data remove storage survirec:tmp it[0]
execute if data storage survirec:tmp it[0] run function survirec:v1/private/menu/rloop

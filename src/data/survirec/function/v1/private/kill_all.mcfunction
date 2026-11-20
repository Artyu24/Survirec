scoreboard players set #kres survirec.v 1
execute as @e[tag=survirec.x] run function survirec:v1/private/i/delete
scoreboard players set #kres survirec.v 0
execute if data storage survirec:cfg vault in survirec:vault if loaded 0 0 0 run function survirec:v1/private/vault/wipe

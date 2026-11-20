function survirec:v1/private/vault/rs2 with storage survirec:t bkl[-1]
data remove storage survirec:t bkl[-1]
execute if data storage survirec:t bkl[0] run function survirec:v1/private/vault/rs1

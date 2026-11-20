function survirec:v1/private/r/wr2 with storage survirec:tmp wbl[-1]
data remove storage survirec:tmp wbl[-1]
execute if data storage survirec:tmp wbl[0] run function survirec:v1/private/r/wr1

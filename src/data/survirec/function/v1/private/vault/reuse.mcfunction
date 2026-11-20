# emplacement libéré par une entité disparue
data modify storage survirec:t bka.vx set from storage survirec:cfg vfree[-1].vx
data modify storage survirec:t bka.vy set from storage survirec:cfg vfree[-1].vy
data modify storage survirec:t bka.vz set from storage survirec:cfg vfree[-1].vz
data remove storage survirec:cfg vfree[-1]
function survirec:v1/private/vault/bk2 with storage survirec:t bka

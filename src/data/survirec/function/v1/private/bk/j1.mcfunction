data modify storage survirec:bk j.p set from storage survirec:bk jl[0]
data remove storage survirec:bk jl[0]
function survirec:v1/private/bk/j2 with storage survirec:bk j
execute if data storage survirec:bk jl[0] run function survirec:v1/private/bk/j1

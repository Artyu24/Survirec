# survirec:bk full = "id[propriétés + ex]"
data modify storage survirec:bk jl set from storage survirec:bk pl
data modify storage survirec:bk jl append from storage survirec:bk ex[]
data modify storage survirec:bk j set value {s:"",p:""}
data modify storage survirec:bk j.id set from storage survirec:bk r.id
execute if data storage survirec:bk jl[0] run function survirec:v1/private/bk/j0
execute if data storage survirec:bk j{s:""} run return run data modify storage survirec:bk full set from storage survirec:bk r.id
function survirec:v1/private/bk/jfin with storage survirec:bk j

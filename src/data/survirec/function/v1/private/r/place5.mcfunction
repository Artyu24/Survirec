function survirec:v1/private/bk/read
execute if data storage survirec:bk r{id:""} run return run data remove storage survirec:tmp ev.p
function survirec:v1/private/bk/fullp
data modify storage survirec:tmp ev.p.b set from storage survirec:bk full

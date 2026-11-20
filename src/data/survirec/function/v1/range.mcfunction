$data modify storage survirec:in api set value $(with)
data modify storage survirec:in cfg set value {r:128}
data modify storage survirec:in cfg merge from storage survirec:in api
function survirec:v1/private/range with storage survirec:in cfg

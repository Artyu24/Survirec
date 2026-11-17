$data modify storage survirec:in api set value $(with)
data modify storage survirec:in cfg set value {name:"rec",every:4}
data modify storage survirec:in cfg merge from storage survirec:in api
function survirec:start with storage survirec:in cfg

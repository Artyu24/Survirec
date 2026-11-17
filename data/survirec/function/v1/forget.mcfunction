$data modify storage survirec:in api set value $(with)
data modify storage survirec:in cfg set value {name:""}
data modify storage survirec:in cfg merge from storage survirec:in api
function survirec:forget with storage survirec:in cfg

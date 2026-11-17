$data modify storage survirec:in api set value $(with)
data modify storage survirec:in cfg set value {}
data modify storage survirec:in cfg merge from storage survirec:in api
execute if data storage survirec:in cfg.tag run return run function survirec:kill with storage survirec:in cfg
execute if data storage survirec:in cfg.name run return run function survirec:kill_name with storage survirec:in cfg
function survirec:kill_all

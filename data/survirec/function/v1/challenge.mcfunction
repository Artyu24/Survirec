$data modify storage survirec:in api set value $(with)
data modify storage survirec:in cfg set value {id:"default",time:30,group:"main"}
data modify storage survirec:in cfg merge from storage survirec:in api
function survirec:challenge_g with storage survirec:in cfg

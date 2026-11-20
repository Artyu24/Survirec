$data modify storage survirec:in api set value $(with)
data modify storage survirec:in cfg set value {f:0,d:[],e:[],s:[],a:[]}
data modify storage survirec:in cfg merge from storage survirec:in api
execute if data storage survirec:in cfg{f:1} run data modify storage survirec:t pend set value []
execute if data storage survirec:in cfg{f:1} run data modify storage survirec:t pend_e set value []
execute if data storage survirec:in cfg{f:1} run data modify storage survirec:t pend_s set value []
execute if data storage survirec:in cfg{f:1} run data modify storage survirec:t pend_a set value []
execute unless data storage survirec:t pend run data modify storage survirec:t pend set value []
execute unless data storage survirec:t pend_e run data modify storage survirec:t pend_e set value []
execute unless data storage survirec:t pend_s run data modify storage survirec:t pend_s set value []
execute unless data storage survirec:t pend_a run data modify storage survirec:t pend_a set value []
data modify storage survirec:t pend append from storage survirec:in cfg.d[]
data modify storage survirec:t pend_e append from storage survirec:in cfg.e[]
data modify storage survirec:t pend_s append from storage survirec:in cfg.s[]
data modify storage survirec:t pend_a append from storage survirec:in cfg.a[]

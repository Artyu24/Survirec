execute if data storage survirec:in cfg.data{f:1} run data modify storage survirec:t pend set value []
execute if data storage survirec:in cfg.data{f:1} run data modify storage survirec:t pend_e set value []
execute if data storage survirec:in cfg.data{f:1} run data modify storage survirec:t pend_s set value []
execute if data storage survirec:in cfg.data{f:1} run data modify storage survirec:t pend_a set value []
execute unless data storage survirec:t pend run data modify storage survirec:t pend set value []
execute unless data storage survirec:t pend_e run data modify storage survirec:t pend_e set value []
execute unless data storage survirec:t pend_s run data modify storage survirec:t pend_s set value []
execute unless data storage survirec:t pend_a run data modify storage survirec:t pend_a set value []
data modify storage survirec:t pend append from storage survirec:in cfg.data.d[]
data modify storage survirec:t pend_e append from storage survirec:in cfg.data.e[]
data modify storage survirec:t pend_s append from storage survirec:in cfg.data.s[]
data modify storage survirec:t pend_a append from storage survirec:in cfg.data.a[]
data modify storage survirec:in seq set value {}
data modify storage survirec:in seq.n set from storage survirec:in cfg.data.n
data modify storage survirec:in seq.y set from storage survirec:in cfg.data.y
data modify storage survirec:in seq.p set from storage survirec:in cfg.data.p
data modify storage survirec:in seq.e set from storage survirec:t pend_e
data modify storage survirec:in seq.s set from storage survirec:t pend_s
data modify storage survirec:in seq.a set from storage survirec:t pend_a
data modify storage survirec:in seq.d set from storage survirec:t pend
function survirec:v1/private/store_seq with storage survirec:in cfg
data remove storage survirec:t pend
data remove storage survirec:t pend_e
data remove storage survirec:t pend_s
data remove storage survirec:t pend_a

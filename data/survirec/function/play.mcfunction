$scoreboard players set #f survirec.v $(f)
execute if score #f survirec.v matches 1 run data modify storage survirec:t pend set value []
$data modify storage survirec:t chunk set value $(d)
data modify storage survirec:t pend append from storage survirec:t chunk[]
data remove storage survirec:t chunk
$data modify storage survirec:data seqs.$(name) set value {n:$(n),y:$(y),p:$(p),e:$(e),s:$(s)}
$data modify storage survirec:data seqs.$(name).d set from storage survirec:t pend
data remove storage survirec:t pend
$data modify storage survirec:in a set value {name:"$(name)",entity:"$(entity)",size:$(size),loop:$(loop),speed:$(speed),offset:$(offset),tag:"$(tag)",pose:"$(pose)",skin:"$(skin)",texture:"$(texture)",head:"$(head)",chest:"$(chest)",legs:"$(legs)",feet:"$(feet)",mainhand:"$(mainhand)",offhand:"$(offhand)"}
$execute positioned $(pos) run function survirec:p/spawn

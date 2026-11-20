execute if score @s survirec.ratype matches 1 run return run function survirec:v1/private/r/launch
tag @s remove survirec.armed
title @s actionbar {text:""}
data modify storage survirec:tmp meta set value {name:"ch",n:4}
function survirec:v1/private/c/begin
scoreboard players operation #csec survirec.v = @s survirec.rcdur
scoreboard players operation #csec survirec.v /= #20 survirec.v
tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Épreuve ! Tu as ",color:"green"},{score:{name:"#csec",objective:"survirec.v"},color:"gold",bold:true},{text:" secondes.",color:"green"}]

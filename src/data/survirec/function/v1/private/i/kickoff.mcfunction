# positionné sur un bouton ou un levier (drapeaux de bk/read) : décalage vers le bloc support dans survirec:t kd
data modify storage survirec:t kd set value {x:0,y:0,z:0}
execute if score #bfa survirec.v matches 1 run data modify storage survirec:t kd.y set value -1
execute if score #bfa survirec.v matches 2 run data modify storage survirec:t kd.y set value 1
execute if score #bfa survirec.v matches 3 if score #bfc survirec.v matches 1 run data modify storage survirec:t kd.z set value 1
execute if score #bfa survirec.v matches 3 if score #bfc survirec.v matches 2 run data modify storage survirec:t kd.z set value -1
execute if score #bfa survirec.v matches 3 if score #bfc survirec.v matches 3 run data modify storage survirec:t kd.x set value -1
execute if score #bfa survirec.v matches 3 if score #bfc survirec.v matches 4 run data modify storage survirec:t kd.x set value 1

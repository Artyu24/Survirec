data modify storage survirec:tmp neweq set value {}
data modify storage survirec:tmp neweq set from entity @s equipment
data modify storage survirec:tmp neweq.mainhand set from entity @s SelectedItem
execute if data storage survirec:tmp neweq.mainhand.components."minecraft:custom_data"{survirec:{stop:1b}} run data remove storage survirec:tmp neweq.mainhand
execute if data storage survirec:tmp neweq.offhand.components."minecraft:custom_data"{survirec:{stop:1b}} run data remove storage survirec:tmp neweq.offhand
execute store success score #ch survirec.v run data modify storage survirec:tmp eq set from storage survirec:tmp neweq
execute if score #ch survirec.v matches 1 run function survirec:r/eq_push

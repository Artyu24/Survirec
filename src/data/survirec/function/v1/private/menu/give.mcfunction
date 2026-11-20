execute unless entity @s[type=minecraft:player] run return fail
clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{survirec:{menu:1b}}]
execute if data storage survirec:cfg menu{texture:""} run return run function survirec:v1/private/menu/give_plain
function survirec:v1/private/menu/give_head with storage survirec:cfg menu

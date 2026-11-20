scoreboard players operation #me survirec.v = @s survirec.pid
execute as @e[type=minecraft:text_display,tag=survirec.start] if score @s survirec.pid = #me survirec.v run kill @s
clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{survirec:{stop:1b}}]
title @s actionbar {text:""}
function survirec:v1/private/r/killmk

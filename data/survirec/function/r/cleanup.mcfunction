clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{survirec:{stop:1b}}]
kill @e[type=minecraft:text_display,tag=survirec.start]
scoreboard players reset @s survirec.trg
title @s actionbar {text:""}

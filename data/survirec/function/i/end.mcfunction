execute if score @s survirec.lp matches 1 run function survirec:i/restart
execute unless score @s survirec.lp matches 0..2 run function survirec:i/restart
execute if score @s survirec.lp matches 0 run function survirec:i/freeze
execute if score @s survirec.lp matches 2 run function survirec:i/delete

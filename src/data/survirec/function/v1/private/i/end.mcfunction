execute if score @s survirec.rsb matches 1 if score @s survirec.grp matches 0 run function survirec:v1/private/i/pulse
execute if score @s survirec.lp matches 1 run function survirec:v1/private/i/restart
execute unless score @s survirec.lp matches 0..2 run function survirec:v1/private/i/restart
execute if score @s survirec.lp matches 0 run function survirec:v1/private/i/freeze
execute if score @s survirec.lp matches 2 run function survirec:v1/private/i/delete

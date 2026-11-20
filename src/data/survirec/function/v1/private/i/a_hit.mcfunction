scoreboard players set #dmg survirec.v 10
execute if items entity @s weapon.mainhand #survirec:dmg/d20 run scoreboard players set #dmg survirec.v 20
execute if items entity @s weapon.mainhand #survirec:dmg/d25 run scoreboard players set #dmg survirec.v 25
execute if items entity @s weapon.mainhand #survirec:dmg/d30 run scoreboard players set #dmg survirec.v 30
execute if items entity @s weapon.mainhand #survirec:dmg/d35 run scoreboard players set #dmg survirec.v 35
execute if items entity @s weapon.mainhand #survirec:dmg/d40 run scoreboard players set #dmg survirec.v 40
execute if items entity @s weapon.mainhand #survirec:dmg/d45 run scoreboard players set #dmg survirec.v 45
execute if items entity @s weapon.mainhand #survirec:dmg/d50 run scoreboard players set #dmg survirec.v 50
execute if items entity @s weapon.mainhand #survirec:dmg/d55 run scoreboard players set #dmg survirec.v 55
execute if items entity @s weapon.mainhand #survirec:dmg/d60 run scoreboard players set #dmg survirec.v 60
execute if items entity @s weapon.mainhand #survirec:dmg/d65 run scoreboard players set #dmg survirec.v 65
execute if items entity @s weapon.mainhand #survirec:dmg/d70 run scoreboard players set #dmg survirec.v 70
execute if items entity @s weapon.mainhand #survirec:dmg/d80 run scoreboard players set #dmg survirec.v 80
execute if items entity @s weapon.mainhand #survirec:dmg/d90 run scoreboard players set #dmg survirec.v 90
execute if items entity @s weapon.mainhand #survirec:dmg/d100 run scoreboard players set #dmg survirec.v 100
execute store result storage survirec:t hit.d float 0.1 run scoreboard players get #dmg survirec.v
tag @s add survirec.hitter
execute at @s anchored eyes positioned ^ ^-0.6 ^1 run function survirec:v1/private/i/a_hit2 with storage survirec:t hit
tag @s remove survirec.hitter

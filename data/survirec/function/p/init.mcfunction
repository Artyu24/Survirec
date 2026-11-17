tag @s remove survirec.new
scoreboard players operation @s survirec.id = #id survirec.v
execute store result score @s survirec.ax run data get entity @s Pos[0] 1000
execute store result score @s survirec.ay run data get entity @s Pos[1] 1000
execute store result score @s survirec.az run data get entity @s Pos[2] 1000
execute store result storage survirec:in a.id int 1 run scoreboard players get @s survirec.id
function survirec:p/reg with storage survirec:in a
function survirec:p/ntag with storage survirec:in a
execute unless data storage survirec:in a{tag:""} run function survirec:p/utag with storage survirec:in a
scoreboard players set @s survirec.grp 0
execute if data storage survirec:in a.grp store result score @s survirec.grp run data get storage survirec:in a.grp
scoreboard players set @s survirec.rs 0
scoreboard players set @s survirec.hs 0
function survirec:p/cfg with storage survirec:in a
execute if score @s survirec.hs matches 1.. run scoreboard players set @s survirec.hs 1
function survirec:p/size with storage survirec:in a
execute unless score @s survirec.n100 matches 1.. run scoreboard players set @s survirec.len 0
scoreboard players operation @s survirec.dv = @s survirec.n100
execute store result score @s survirec.lp run data get storage survirec:in a.loop
execute store result score @s survirec.spd run data get storage survirec:in a.speed
scoreboard players operation @s survirec.bx = @s survirec.ax
scoreboard players operation @s survirec.by = @s survirec.ay
scoreboard players operation @s survirec.bz = @s survirec.az
scoreboard players operation @s survirec.byw = @s survirec.yw0
scoreboard players operation @s survirec.bpt = @s survirec.pt0
scoreboard players set @s survirec.st 0
scoreboard players set @s survirec.pl 0
scoreboard players set @s survirec.near 1
scoreboard players set @s survirec.seg 0
scoreboard players set @s survirec.ei 0
scoreboard players set @s survirec.ek 0
scoreboard players set @s survirec.ov 0
scoreboard players set @s survirec.fl -1
scoreboard players set @s survirec.fx 0
execute unless entity @s[type=minecraft:mannequin] run scoreboard players set @s survirec.fx 1
scoreboard players set @s survirec.rb 0
scoreboard players set @s survirec.run 0
execute if score @s survirec.len matches 1.. run scoreboard players set @s survirec.run 1
execute if score @s survirec.run matches 1 run function survirec:i/load
execute if score @s survirec.grp matches 1.. run function survirec:i/grpinit
function survirec:p/ovr
execute if entity @s[type=minecraft:mannequin] if data storage survirec:in prof run data modify entity @s profile set from storage survirec:in prof
data remove storage survirec:in prof
execute if entity @s[type=minecraft:mannequin] unless data storage survirec:in a{skin:""} run function survirec:p/skin with storage survirec:in a
execute if entity @s[type=minecraft:mannequin] if data storage survirec:in a{skin:""} unless data storage survirec:in a{texture:""} run function survirec:p/tex with storage survirec:in a
execute unless data storage survirec:in a{pose:""} run function survirec:p/pose_fix with storage survirec:in a
execute store result score @s survirec.pr run data get storage survirec:in a.offset 100
scoreboard players operation #t survirec.v = @s survirec.len
scoreboard players operation #t survirec.v *= @s survirec.n100
execute if score #t survirec.v matches 1.. run scoreboard players operation @s survirec.pr %= #t survirec.v
execute if score @s survirec.run matches 1 if score @s survirec.pr >= @s survirec.n100 run function survirec:i/adv
execute if score @s survirec.hs matches 1 run scoreboard players set @s survirec.si 0
execute if score @s survirec.hs matches 1 run function survirec:i/swload
execute if score @s survirec.hs matches 1 run function survirec:i/swskip
function survirec:i/move
function #survirec:v1/signals/on_spawn

tag @s remove survirec.new
scoreboard players operation @s survirec.id = #id survirec.v
execute store result score @s survirec.ax run data get entity @s Pos[0] 1000
execute store result score @s survirec.ay run data get entity @s Pos[1] 1000
execute store result score @s survirec.az run data get entity @s Pos[2] 1000
execute store result storage survirec:in a.id int 1 run scoreboard players get @s survirec.id
function survirec:v1/private/p/reg with storage survirec:in a
function survirec:v1/private/p/ntag with storage survirec:in a
execute unless data storage survirec:in a{tag:""} run function survirec:v1/private/p/utag with storage survirec:in a
scoreboard players set @s survirec.grp 0
execute if data storage survirec:in a.grp store result score @s survirec.grp run data get storage survirec:in a.grp
execute if score @s survirec.grp matches -1 run function survirec:v1/private/p/gjoin with storage survirec:in a
scoreboard players set @s survirec.gloop 1
scoreboard players set @s survirec.gs -1
execute if data storage survirec:in a.gl store result score @s survirec.gloop run data get storage survirec:in a.gl
scoreboard players set @s survirec.rs 0
scoreboard players set @s survirec.hs 0
scoreboard players set @s survirec.ha 0
function survirec:v1/private/p/cfg with storage survirec:in a
execute if score @s survirec.hs matches 1.. run scoreboard players set @s survirec.hs 1
execute if score @s survirec.ha matches 1.. run scoreboard players set @s survirec.ha 1
scoreboard players set @s survirec.rst 1
execute if data storage survirec:in a.restore store result score @s survirec.rst run data get storage survirec:in a.restore
scoreboard players set @s survirec.hitp 0
execute if data storage survirec:in a.hitp store result score @s survirec.hitp run data get storage survirec:in a.hitp
scoreboard players set @s survirec.rlt -1
scoreboard players set @s survirec.rsb 0
execute if data storage survirec:in a.rsb store result score @s survirec.rsb run data get storage survirec:in a.rsb
execute if score @s survirec.rsb matches 1 store result score @s survirec.cbx run data get storage survirec:in a.cbx
execute if score @s survirec.rsb matches 1 store result score @s survirec.cby run data get storage survirec:in a.cby
execute if score @s survirec.rsb matches 1 store result score @s survirec.cbz run data get storage survirec:in a.cbz
execute store result score @s survirec.bbx run data get entity @s Pos[0]
execute store result score @s survirec.bby run data get entity @s Pos[1]
execute store result score @s survirec.bbz run data get entity @s Pos[2]
function survirec:v1/private/p/size with storage survirec:in a
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
scoreboard players set @s survirec.rng 0
execute store result score @s survirec.rng run data get storage survirec:in a.range
execute if score @s survirec.rng matches 1.. run tag @s add survirec.rg
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
execute if score @s survirec.run matches 1 run function survirec:v1/private/i/load
execute if score @s survirec.grp matches 1.. run function survirec:v1/private/i/grpinit
function survirec:v1/private/p/ovr
execute if entity @s[type=minecraft:mannequin] if data storage survirec:in prof run data modify entity @s profile set from storage survirec:in prof
data remove storage survirec:in prof
execute if entity @s[type=minecraft:mannequin] unless data storage survirec:in a{skin:""} run function survirec:v1/private/p/skin with storage survirec:in a
execute if entity @s[type=minecraft:mannequin] if data storage survirec:in a{skin:""} unless data storage survirec:in a{texture:""} run function survirec:v1/private/p/tex with storage survirec:in a
execute unless data storage survirec:in a{pose:""} run function survirec:v1/private/p/pose_fix with storage survirec:in a
execute store result score @s survirec.pr run data get storage survirec:in a.offset 100
scoreboard players operation #t survirec.v = @s survirec.len
scoreboard players operation #t survirec.v *= @s survirec.n100
execute if score #t survirec.v matches 1.. run scoreboard players operation @s survirec.pr %= #t survirec.v
execute if score @s survirec.run matches 1 if score @s survirec.pr >= @s survirec.n100 run function survirec:v1/private/i/adv
execute if score @s survirec.hs matches 1 run scoreboard players set @s survirec.si 0
execute if score @s survirec.hs matches 1 run function survirec:v1/private/i/swload
execute if score @s survirec.hs matches 1 run function survirec:v1/private/i/swskip
execute if score @s survirec.ha matches 1 run scoreboard players set @s survirec.ai 0
execute if score @s survirec.ha matches 1 run function survirec:v1/private/i/acload
execute if score @s survirec.ha matches 1 run function survirec:v1/private/i/acskip
function survirec:v1/private/i/move
function #survirec:v1/signals/on_spawn

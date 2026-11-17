execute if entity @s[tag=survirec.on] if score #rec survirec.v matches 1 run return 0
tag @s remove survirec.on
execute if score #rec survirec.v matches 1 run return run tellraw @s {text:"[Survirec] Un enregistrement est déjà en cours, patiente un instant.",color:"red"}
execute store result score #csec survirec.v run data get storage survirec:c time
execute unless score #csec survirec.v matches 1.. run return run tellraw @s {text:"[Survirec] time doit être d'au moins 1 seconde.",color:"red"}
scoreboard players operation #cdur survirec.v = #csec survirec.v
scoreboard players operation #cdur survirec.v *= #20 survirec.v
execute unless score @s survirec.pid matches 1.. run function survirec:c/newpid
execute store result storage survirec:c pid int 1 run scoreboard players get @s survirec.pid
function survirec:c/gid with storage survirec:c
execute store result storage survirec:c gid int 1 run scoreboard players get #g survirec.v
function survirec:c/prekill with storage survirec:c
function survirec:i/grpcheck
data modify storage survirec:tmp meta set value {name:"ch",n:4}
scoreboard players set #n survirec.v 4
scoreboard players set #chal survirec.v 1
function survirec:c/begin
tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Épreuve ! Tu as ",color:"green"},{score:{name:"#csec",objective:"survirec.v"},color:"gold",bold:true},{text:" secondes.",color:"green"}]

tellraw @s {text:"------------------------------------------------",color:"dark_gray"}
tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Séquence ",color:"green"},{storage:"survirec:tmp",nbt:"meta.name",color:"gold"},{text:" prête à copier :",color:"green"}]
execute store result score #c survirec.v run data get storage survirec:tmp chunks
scoreboard players set #ne survirec.v 0
scoreboard players set #ns survirec.v 0
execute store result score #ne survirec.v run data get storage survirec:tmp e
execute store result score #ns survirec.v run data get storage survirec:tmp s
scoreboard players set #na survirec.v 0
execute store result score #na survirec.v run data get storage survirec:tmp a
scoreboard players set #split survirec.v 0
execute if score #na survirec.v matches 30.. run scoreboard players set #split survirec.v 1
execute if score #ne survirec.v matches 4.. run scoreboard players set #split survirec.v 1
execute if score #ns survirec.v matches 150.. run scoreboard players set #split survirec.v 1
scoreboard players operation #m survirec.v = #c survirec.v
scoreboard players operation #m survirec.v += #split survirec.v
scoreboard players set #j survirec.v 1
function survirec:v1/private/r/exp
execute if score #m survirec.v matches 1 run tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Colle-la dans un command block ",color:"green"},{text:"impulsion",color:"gold"},{text:".",color:"green"}]
execute if score #m survirec.v matches 2.. run tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Colle les blocs dans l'ordre : le 1 en ",color:"green"},{text:"impulsion",color:"gold"},{text:", les suivants en ",color:"green"},{text:"chaîne",color:"green",underlined:true},{text:" (toujours actif).",color:"green"}]
tellraw @s {text:"------------------------------------------------",color:"dark_gray"}

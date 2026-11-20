# trappe ou portillon : bascule open, garde le reste
scoreboard players set #bkm survirec.v 0
function survirec:v1/private/vault/here
scoreboard players set #nop survirec.v 1
execute if score #bop survirec.v matches 1 run scoreboard players set #nop survirec.v 0
function survirec:v1/private/i/u_openex
function survirec:v1/private/bk/full
function survirec:v1/private/i/setfull with storage survirec:bk
execute if block ~ ~ ~ #minecraft:fence_gates if score #bop survirec.v matches 0 run playsound minecraft:block.fence_gate.open block @a ~ ~ ~
execute if block ~ ~ ~ #minecraft:fence_gates if score #bop survirec.v matches 1 run playsound minecraft:block.fence_gate.close block @a ~ ~ ~
execute unless block ~ ~ ~ #minecraft:fence_gates if score #bop survirec.v matches 0 run playsound minecraft:block.wooden_trapdoor.open block @a ~ ~ ~
execute unless block ~ ~ ~ #minecraft:fence_gates if score #bop survirec.v matches 1 run playsound minecraft:block.wooden_trapdoor.close block @a ~ ~ ~

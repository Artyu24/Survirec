scoreboard players set #bkm survirec.v 0
execute if data storage survirec:t ev.p run scoreboard players set #bkm survirec.v 1
function survirec:v1/private/vault/here
execute if score #bkm survirec.v matches 1 run function survirec:v1/private/i/a_place2
execute if score #bkm survirec.v matches 0 run function survirec:v1/private/i/setb with storage survirec:t ev
execute if score #bkm survirec.v matches 1 run function survirec:v1/private/i/setbs with storage survirec:t ev
playsound minecraft:block.stone.place block @a ~ ~ ~

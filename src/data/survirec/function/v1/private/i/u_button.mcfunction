execute if score #bpw survirec.v matches 1 run return 0
scoreboard players set #bkm survirec.v 0
function survirec:v1/private/vault/here
data modify storage survirec:bk ex set value ["powered=true"]
function survirec:v1/private/bk/full
function survirec:v1/private/i/setfull with storage survirec:bk
function survirec:v1/private/i/kickoff
function survirec:v1/private/i/kickat with storage survirec:t kd
playsound minecraft:block.stone_button.click_on block @a ~ ~ ~
# relâché après le délai normal (1 s pierre, 1,5 s bois)
data modify storage survirec:bk ex set value ["powered=false"]
function survirec:v1/private/bk/full
data modify storage survirec:t rel set value {t:0,x:0,y:0,z:0,b:"",kx:0,ky:0,kz:0}
function survirec:v1/private/i/kickmk with storage survirec:t kd
data modify storage survirec:t rel.b set from storage survirec:bk full
scoreboard players operation #rt survirec.v = #now survirec.v
scoreboard players add #rt survirec.v 20
execute if block ~ ~ ~ #minecraft:wooden_buttons run scoreboard players add #rt survirec.v 10
execute store result storage survirec:t rel.t int 1 run scoreboard players get #rt survirec.v
execute summon minecraft:marker run function survirec:v1/private/i/relpos
function survirec:v1/private/i/rladd

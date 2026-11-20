scoreboard players set #bkm survirec.v 0
function survirec:v1/private/vault/here
data modify storage survirec:bk ex set value ["powered=true"]
execute if score #bpw survirec.v matches 1 run data modify storage survirec:bk ex set value ["powered=false"]
function survirec:v1/private/bk/full
function survirec:v1/private/i/setfull with storage survirec:bk
function survirec:v1/private/i/kickoff
function survirec:v1/private/i/kickat with storage survirec:t kd
playsound minecraft:block.lever.click block @a ~ ~ ~

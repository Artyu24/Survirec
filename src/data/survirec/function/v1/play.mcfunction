$data modify storage survirec:in api set value $(with)
data modify storage survirec:in cfg set value {name:"",pos:"~ ~ ~",entity:"minecraft:mannequin",range:0,size:1,loop:1,redstone:0,restore:1,hit_players:0,speed:100,delay:0,tag:"",group:"",group_radius:50,grp:0,gl:0,pose:"",skin:"",texture:"",head:"",chest:"",legs:"",feet:"",mainhand:"",offhand:""}
data modify storage survirec:in cfg merge from storage survirec:in api
scoreboard players set #bad survirec.v 0
data modify storage survirec:v q set value {f:"name"}
function survirec:v1/private/vreq with storage survirec:v q
data modify storage survirec:v q set value {f:"tag"}
function survirec:v1/private/vopt with storage survirec:v q
data modify storage survirec:v q set value {f:"group"}
function survirec:v1/private/vopt with storage survirec:v q
execute if score #bad survirec.v matches 1 run return run function survirec:v1/private/badname
execute if data storage survirec:in cfg.data run function survirec:v1/private/import
execute unless data storage survirec:in cfg{group:""} run function survirec:v1/private/pgroup with storage survirec:in cfg
execute summon minecraft:marker run function survirec:v1/private/p/cbpos
function survirec:v1/private/again with storage survirec:in cfg

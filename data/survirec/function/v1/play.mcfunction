$data modify storage survirec:in api set value $(with)
data modify storage survirec:in cfg set value {name:"",pos:"~ ~ ~",entity:"minecraft:mannequin",size:1,loop:1,speed:100,offset:0,tag:"",pose:"",skin:"",texture:"",head:"",chest:"",legs:"",feet:"",mainhand:"",offhand:""}
data modify storage survirec:in cfg merge from storage survirec:in api
function survirec:again with storage survirec:in cfg

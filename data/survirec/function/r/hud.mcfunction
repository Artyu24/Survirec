execute if score #chal survirec.v matches 1 run return run function survirec:c/hud
scoreboard players operation #s survirec.v = #ticks survirec.v
scoreboard players operation #s survirec.v /= #20 survirec.v
scoreboard players operation #mn survirec.v = #s survirec.v
scoreboard players operation #mn survirec.v /= #60 survirec.v
scoreboard players operation #s survirec.v %= #60 survirec.v
execute if score #s survirec.v matches 10.. run title @s actionbar [{text:"● ",color:"red"},{text:"ENREGISTREMENT EN COURS ",color:"white",bold:true},{score:{name:"#mn",objective:"survirec.v"},color:"yellow"},{text:":",color:"yellow"},{score:{name:"#s",objective:"survirec.v"},color:"yellow"}]
execute if score #s survirec.v matches ..9 run title @s actionbar [{text:"● ",color:"red"},{text:"ENREGISTREMENT EN COURS ",color:"white",bold:true},{score:{name:"#mn",objective:"survirec.v"},color:"yellow"},{text:":0",color:"yellow"},{score:{name:"#s",objective:"survirec.v"},color:"yellow"}]

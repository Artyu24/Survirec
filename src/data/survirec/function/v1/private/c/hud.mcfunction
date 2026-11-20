scoreboard players operation #s survirec.v = @s survirec.rcdur
scoreboard players operation #s survirec.v -= @s survirec.rtime
scoreboard players add #s survirec.v 19
scoreboard players operation #s survirec.v /= #20 survirec.v
scoreboard players operation #mn survirec.v = #s survirec.v
scoreboard players operation #mn survirec.v /= #60 survirec.v
scoreboard players operation #s survirec.v %= #60 survirec.v
execute if score #s survirec.v matches 10.. run title @s actionbar [{text:"● ",color:"red"},{text:"ENREGISTREMENT  ",color:"white",bold:true},{text:"Temps restant : ",color:"gray"},{score:{name:"#mn",objective:"survirec.v"},color:"gold",bold:true},{text:":",color:"gold",bold:true},{score:{name:"#s",objective:"survirec.v"},color:"gold",bold:true}]
execute if score #s survirec.v matches ..9 run title @s actionbar [{text:"● ",color:"red"},{text:"ENREGISTREMENT  ",color:"white",bold:true},{text:"Temps restant : ",color:"gray"},{score:{name:"#mn",objective:"survirec.v"},color:"gold",bold:true},{text:":0",color:"gold",bold:true},{score:{name:"#s",objective:"survirec.v"},color:"gold",bold:true}]

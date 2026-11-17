tellraw @s {text:"[Survirec] diagnostic",color:"gold",bold:true}
tellraw @s [{text:"  rec = ",color:"gray"},{score:{name:"#rec",objective:"survirec.v"},color:"aqua"},{text:"   chal = ",color:"gray"},{score:{name:"#chal",objective:"survirec.v"},color:"aqua"},{text:"   ticks = ",color:"gray"},{score:{name:"#ticks",objective:"survirec.v"},color:"aqua"},{text:"   durée = ",color:"gray"},{score:{name:"#cdur",objective:"survirec.v"},color:"aqua"}]
execute if entity @s[tag=survirec.on] run tellraw @s {text:"  Tu es en cours d'enregistrement.",color:"yellow"}
execute unless entity @s[tag=survirec.on] run tellraw @s {text:"  Tu n'es pas en cours d'enregistrement.",color:"gray"}
execute store result score #dbg survirec.v if entity @e[tag=survirec.m]
tellraw @s [{text:"  Entités animées : ",color:"gray"},{score:{name:"#dbg",objective:"survirec.v"},color:"aqua"}]
execute as @e[tag=survirec.m] run tellraw @p [{text:"  • groupe ",color:"gray"},{score:{name:"@s",objective:"survirec.grp"},color:"gold",bold:true},{text:"  en lecture ",color:"gray"},{score:{name:"@s",objective:"survirec.run"},color:"gold",bold:true},{text:"  ",color:"gray"},{nbt:"Tags",entity:"@s",color:"aqua"}]

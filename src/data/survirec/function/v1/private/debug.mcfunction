tag @s add survirec.dbg
tellraw @s {text:"[Survirec] diagnostic",color:"gold",bold:true}
execute store result score #dbg survirec.v if entity @a[tag=survirec.on]
execute store result score #dbg2 survirec.v if entity @a[tag=survirec.armed]
tellraw @s [{text:"  Enregistrements : ",color:"gray"},{score:{name:"#dbg",objective:"survirec.v"},color:"aqua"},{text:"   armés : ",color:"gray"},{score:{name:"#dbg2",objective:"survirec.v"},color:"aqua"}]
execute as @a[tag=survirec.on] run tellraw @a[tag=survirec.dbg] [{text:"  ● ",color:"red"},{selector:"@s",color:"white"},{text:"  ",color:"gray"},{score:{name:"@s",objective:"survirec.rtime"},color:"aqua"},{text:" ticks, ",color:"gray"},{score:{name:"@s",objective:"survirec.rkt"},color:"aqua"},{text:" keyframes",color:"gray"}]
execute as @a[tag=survirec.armed] run tellraw @a[tag=survirec.dbg] [{text:"  ⏳ ",color:"gold"},{selector:"@s",color:"white"},{text:"  attend le groupe ",color:"gray"},{score:{name:"@s",objective:"survirec.rwg"},color:"aqua"}]
execute store result score #dbg survirec.v if entity @e[tag=survirec.m]
tellraw @s [{text:"  Entités animées : ",color:"gray"},{score:{name:"#dbg",objective:"survirec.v"},color:"aqua"}]
execute as @e[tag=survirec.m] run tellraw @a[tag=survirec.dbg] [{text:"  • groupe ",color:"gray"},{score:{name:"@s",objective:"survirec.grp"},color:"gold",bold:true},{text:"  en lecture ",color:"gray"},{score:{name:"@s",objective:"survirec.run"},color:"gold",bold:true},{text:"  ",color:"gray"},{nbt:"Tags",entity:"@s",color:"aqua"}]
tag @s remove survirec.dbg

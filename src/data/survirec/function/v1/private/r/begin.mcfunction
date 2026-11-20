function survirec:v1/private/r/init
scoreboard players operation #me survirec.v = @s survirec.pid
execute as @e[type=minecraft:text_display,tag=survirec.start] if score @s survirec.pid = #me survirec.v run kill @s
execute at @s run summon minecraft:text_display ~ ~1.3 ~ {Tags:["survirec.start","survirec.mk","smithed.entity","smithed.strict"],text:{text:"▶ Départ",color:"green"},billboard:"center"}
scoreboard players operation @e[type=minecraft:text_display,tag=survirec.mk] survirec.pid = #me survirec.v
tag @e[type=minecraft:text_display,tag=survirec.mk] remove survirec.mk
tellraw @s {text:"------------------------------------------------",color:"dark_gray"}
tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"Enregistrement ",color:"green"},{storage:"survirec:tmp",nbt:"meta.name",color:"gold"},{text:" démarré.",color:"green"}]
function survirec:v1/private/r/give
tellraw @s [{text:"[Survirec] ",color:"gray"},{text:"[■ STOP]",color:"red",bold:true,click_event:{action:"run_command",command:"/function #survirec:v1/stop"},hover_event:{action:"show_text",value:"Arrêter l'enregistrement"}},{text:"   "},{text:"[↺ STOP + retour au départ]",color:"red",click_event:{action:"run_command",command:"/function #survirec:v1/stop_loop"},hover_event:{action:"show_text",value:"Arrêter et ramener au point de départ (boucle propre)"}}]
tellraw @s {text:"------------------------------------------------",color:"dark_gray"}
function #survirec:v1/signals/on_record_start

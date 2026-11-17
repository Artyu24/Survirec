tellraw @s {text:"══════ SURVIREC · 1/5 · ENREGISTRER ══════",color:"gold",bold:true}
tellraw @s [{text:"   "},{text:'/function survirec:start {name:"walk",every:4}',color:"aqua"}]
tellraw @s [{text:"   "},{text:"[Copier l'exemple]",color:"yellow",bold:true,click_event:{action:"copy_to_clipboard",value:'/function survirec:start {name:"walk",every:4}'},hover_event:{action:"show_text",value:"Copier la commande"}}]
tellraw @s [{text:"   name",color:"gold",bold:true},{text:"  nom de la séquence",color:"gray"}]
tellraw @s [{text:"   every",color:"gold",bold:true},{text:"  4 = fluide, 2 = précis",color:"gray"}]
tellraw @s [{text:"   Arrêt : ",color:"gray"},{text:"clic droit avec la barrière",color:"red",bold:true}]
tellraw @s [{text:"   "},{text:"[Menu]",color:"gold",bold:true,click_event:{action:"run_command",command:"/function survirec:help"},hover_event:{action:"show_text",value:"Ouvrir"}},{text:"  "},{text:"[Suivant ▶]",color:"green",bold:true,click_event:{action:"run_command",command:"/function survirec:help/p2"},hover_event:{action:"show_text",value:"Ouvrir"}}]

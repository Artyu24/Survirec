tellraw @s {text:"══ SURVIREC · 1/5 · ENREGISTRER ══",color:"gold"}
tellraw @s [{text:"   "},{text:'function #survirec:v1/start {with:{name:"walk",every:4}}',color:"aqua"}]
tellraw @s [{text:"   "},{text:"[Copier l'exemple]",color:"yellow",click_event:{action:"copy_to_clipboard",value:'/function #survirec:v1/start {with:{name:"walk",every:4}}'},hover_event:{action:"show_text",value:'/function #survirec:v1/start {with:{name:"walk",every:4}}'}}]
tellraw @s [{text:"   name",color:"gold",bold:true},{text:"  nom de la séquence (lettres, chiffres, _)",color:"gray"}]
tellraw @s [{text:"   every",color:"gold",bold:true},{text:"  4 = fluide, 2 = précis",color:"gray"}]
tellraw @s [{text:"   group",color:"gold",bold:true},{text:"  démarre au prochain cycle du groupe",color:"gray"}]
tellraw @s [{text:"   Enregistré aussi : ",color:"gray"},{text:"coups, boutons, leviers, portes, blocs posés et cassés",color:"aqua"}]
tellraw @s [{text:"   Arrêt : ",color:"gray"},{text:"clic droit avec la barrière",color:"red"}]
tellraw @s [{text:"   "},{text:"[Menu]",color:"gold",click_event:{action:"run_command",command:"/function #survirec:v1/help"},hover_event:{action:"show_text",value:"Ouvrir"}},{text:"  "},{text:"[Suivant ▶]",color:"green",click_event:{action:"run_command",command:"/function survirec:v1/private/help/p2"},hover_event:{action:"show_text",value:"Ouvrir"}}]

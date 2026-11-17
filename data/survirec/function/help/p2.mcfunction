tellraw @s {text:"══════ SURVIREC · 2/5 · LANCER ══════",color:"gold",bold:true}
tellraw @s [{text:"   1. Clique sur "},{text:"[Copier la commande de lecture]",color:"yellow",bold:true}]
tellraw @s {text:"   2. Colle-la dans un command block",color:"gray"}
tellraw @s {text:"   3. Active le bloc",color:"gray"}
tellraw @s [{text:"   Les champs à modifier sont ",color:"gray"},{text:"au début",color:"gold",bold:true}]
tellraw @s [{text:"   "},{text:"[◀ Précédent]",color:"green",bold:true,click_event:{action:"run_command",command:"/function survirec:help/p1"},hover_event:{action:"show_text",value:"Ouvrir"}},{text:"  "},{text:"[Menu]",color:"gold",bold:true,click_event:{action:"run_command",command:"/function survirec:help"},hover_event:{action:"show_text",value:"Ouvrir"}},{text:"  "},{text:"[Suivant ▶]",color:"green",bold:true,click_event:{action:"run_command",command:"/function survirec:help/p3"},hover_event:{action:"show_text",value:"Ouvrir"}}]

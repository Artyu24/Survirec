tellraw @s {text:"══ SURVIREC · 2/5 · LANCER ══",color:"gold"}
tellraw @s [{text:"   1. Clique sur ",color:"gray"},{text:"[Copier 1]",color:"yellow"},{text:" à la fin de l'enregistrement",color:"gray"}]
tellraw @s [{text:"   2. Colle-la dans un command block ",color:"gray"},{text:"impulsion",color:"gold"}]
tellraw @s [{text:"   3. Active le bloc",color:"gray"}]
tellraw @s [{text:"   Les champs à modifier sont ",color:"gray"},{text:"au début",color:"gold"},{text:" de la commande",color:"gray"}]
tellraw @s [{text:"   "},{text:"[◀ Précédent]",color:"green",click_event:{action:"run_command",command:"/function survirec:v1/private/help/p1"},hover_event:{action:"show_text",value:"Ouvrir"}},{text:"  "},{text:"[Menu]",color:"gold",click_event:{action:"run_command",command:"/function #survirec:v1/help"},hover_event:{action:"show_text",value:"Ouvrir"}},{text:"  "},{text:"[Suivant ▶]",color:"green",click_event:{action:"run_command",command:"/function survirec:v1/private/help/p3"},hover_event:{action:"show_text",value:"Ouvrir"}}]

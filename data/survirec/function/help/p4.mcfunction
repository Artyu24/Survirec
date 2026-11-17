tellraw @s {text:"══════ SURVIREC · 4/5 · ÉPREUVE ══════",color:"gold",bold:true}
tellraw @s [{text:"   "},{text:'execute as @p run function survirec:challenge_g',color:"aqua"}]
tellraw @s [{text:"   "},{text:'{id:"epreuve1",time:30,group:"salle1"}',color:"aqua"}]
tellraw @s [{text:"   "},{text:"[Copier l'exemple]",color:"yellow",bold:true,click_event:{action:"copy_to_clipboard",value:'execute as @p run function survirec:challenge_g {id:"epreuve1",time:30,group:"salle1"}'},hover_event:{action:"show_text",value:"Pour un command block"}}]
tellraw @s [{text:"   id",color:"gold",bold:true},{text:"  nom de l'épreuve",color:"gray"}]
tellraw @s [{text:"   time",color:"gold",bold:true},{text:"  secondes pour s'enregistrer",color:"gray"}]
tellraw @s [{text:"   group",color:"gold",bold:true},{text:"  même nom = rec synchronisés",color:"gray"}]
tellraw @s {text:"   Command block + plaque de pression.",color:"gray"}
tellraw @s [{text:"   "},{text:"[◀ Précédent]",color:"green",bold:true,click_event:{action:"run_command",command:"/function survirec:help/p3"},hover_event:{action:"show_text",value:"Ouvrir"}},{text:"  "},{text:"[Menu]",color:"gold",bold:true,click_event:{action:"run_command",command:"/function survirec:help"},hover_event:{action:"show_text",value:"Ouvrir"}},{text:"  "},{text:"[Suivant ▶]",color:"green",bold:true,click_event:{action:"run_command",command:"/function survirec:help/p5"},hover_event:{action:"show_text",value:"Ouvrir"}}]

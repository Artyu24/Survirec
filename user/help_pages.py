""" In-game help pages. """
# Imports
from stewbeet import Mem, write_versioned_function


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	major: str = version.split(".")[0]

	write_versioned_function("help/p1", f"""
tellraw @s {{text:"══ SURVIREC · 1/5 · ENREGISTRER ══",color:"gold"}}
tellraw @s [{{text:"   "}},{{text:'function #{ns}:v{major}/start {{with:{{name:"walk",every:4}}}}',color:"aqua"}}]
tellraw @s [{{text:"   "}},{{text:"[Copier l'exemple]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/start {{with:{{name:"walk",every:4}}}}'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/start {{with:{{name:"walk",every:4}}}}'}}}}]
tellraw @s [{{text:"   name",color:"gold",bold:true}},{{text:"  nom de la séquence (lettres, chiffres, _)",color:"gray"}}]
tellraw @s [{{text:"   every",color:"gold",bold:true}},{{text:"  4 = fluide, 2 = précis",color:"gray"}}]
tellraw @s [{{text:"   group",color:"gold",bold:true}},{{text:"  démarre au prochain cycle du groupe",color:"gray"}}]
tellraw @s [{{text:"   Enregistré aussi : ",color:"gray"}},{{text:"coups, boutons, leviers, portes, blocs posés et cassés",color:"aqua"}}]
tellraw @s [{{text:"   Arrêt : ",color:"gray"}},{{text:"clic droit avec la barrière",color:"red"}}]
tellraw @s [{{text:"   "}},{{text:"[Menu]",color:"gold",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}},{{text:"  "}},{{text:"[Suivant ▶]",color:"green",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help_page {{with:{{page:2}}}}"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}}]
""")

	write_versioned_function("help/p2", f"""
tellraw @s {{text:"══ SURVIREC · 2/5 · LANCER ══",color:"gold"}}
tellraw @s [{{text:"   1. Clique sur ",color:"gray"}},{{text:"[Copier 1]",color:"yellow"}},{{text:" à la fin de l'enregistrement",color:"gray"}}]
tellraw @s [{{text:"   2. Colle-la dans un command block ",color:"gray"}},{{text:"impulsion",color:"gold"}}]
tellraw @s [{{text:"   3. Active le bloc",color:"gray"}}]
tellraw @s [{{text:"   Les champs à modifier sont ",color:"gray"}},{{text:"au début",color:"gold"}},{{text:" de la commande",color:"gray"}}]
tellraw @s [{{text:"   "}},{{text:"[◀ Précédent]",color:"green",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help_page {{with:{{page:1}}}}"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}},{{text:"  "}},{{text:"[Menu]",color:"gold",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}},{{text:"  "}},{{text:"[Suivant ▶]",color:"green",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help_page {{with:{{page:3}}}}"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}}]
""")

	write_versioned_function("help/p3", f"""
tellraw @s {{text:"══ SURVIREC · 3/5 · CHAMPS ══",color:"gold"}}
tellraw @s [{{text:"   pos",color:"gold",bold:true}},{{text:"  où ça apparaît, relatif possible (~ ~ ~ = centre du bloc)",color:"gray"}}]
tellraw @s [{{text:"   entity",color:"gold",bold:true}},{{text:"  mannequin, cat...",color:"gray"}}]
tellraw @s [{{text:"   size",color:"gold",bold:true}},{{text:"  taille (1 = normale)",color:"gray"}}]
tellraw @s [{{text:"   loop",color:"gold",bold:true}},{{text:"  1 boucle · 0 fige · 2 disparaît",color:"gray"}}]
tellraw @s [{{text:"   redstone",color:"gold",bold:true}},{{text:"  1 = bloc de redstone 2 blocs au-dessus du command block à chaque fin de boucle",color:"gray"}}]
tellraw @s [{{text:"   restore",color:"gold",bold:true}},{{text:"  monde remis en état : 1 à chaque boucle · 2 aussi à la fin · 0 jamais",color:"gray"}}]
tellraw @s [{{text:"   hit_players",color:"gold",bold:true}},{{text:"  1 = ses coups touchent aussi les joueurs",color:"gray"}}]
tellraw @s [{{text:"   speed",color:"gold",bold:true}},{{text:"  100 = normal",color:"gray"}}]
tellraw @s [{{text:"   delay",color:"gold",bold:true}},{{text:"  décalage de départ (ticks)",color:"gray"}}]
tellraw @s [{{text:"   range",color:"gold",bold:true}},{{text:"  arrêt si aucun joueur à X blocs (0 = défaut)",color:"gray"}}]
tellraw @s [{{text:"   tag",color:"gold",bold:true}},{{text:"  remplace l'ancien (unique dans tout le monde)",color:"gray"}}]
tellraw @s [{{text:"   group",color:"gold",bold:true}},{{text:"  synchronise avec le groupe",color:"gray"}}]
tellraw @s [{{text:"   group_radius",color:"gold",bold:true}},{{text:"  distance de regroupement (50 blocs)",color:"gray"}}]
tellraw @s [{{text:"   pose",color:"gold",bold:true}},{{text:"  pose forcée",color:"gray"}}]
tellraw @s [{{text:"   skin",color:"gold",bold:true}},{{text:"  pseudo d'un joueur",color:"gray"}}]
tellraw @s [{{text:"   texture",color:"gold",bold:true}},{{text:"  texture base64 (si skin vide)",color:"gray"}}]
tellraw @s [{{text:"   head chest legs feet",color:"gold",bold:true}},{{text:"  armure",color:"gray"}}]
tellraw @s [{{text:"   mainhand offhand",color:"gold",bold:true}},{{text:"  mains",color:"gray"}}]
tellraw @s [{{text:"   "}},{{text:"[◀ Précédent]",color:"green",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help_page {{with:{{page:2}}}}"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}},{{text:"  "}},{{text:"[Menu]",color:"gold",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}},{{text:"  "}},{{text:"[Suivant ▶]",color:"green",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help_page {{with:{{page:4}}}}"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}}]
""")

	write_versioned_function("help/p4", f"""
tellraw @s {{text:"══ SURVIREC · 4/5 · ÉPREUVE ══",color:"gold"}}
tellraw @s [{{text:"   "}},{{text:'execute as @p run function #{ns}:v{major}/challenge',color:"aqua"}}]
tellraw @s [{{text:"   "}},{{text:'{{with:{{id:"epreuve1",time:30,group:"salle1"}}}}',color:"aqua"}}]
tellraw @s [{{text:"   "}},{{text:"[Copier l'exemple]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'execute as @p run function #{ns}:v{major}/challenge {{with:{{id:"epreuve1",time:30,group:"salle1"}}}}'}},hover_event:{{action:"show_text",value:'execute as @p run function #{ns}:v{major}/challenge {{with:{{id:"epreuve1",time:30,group:"salle1"}}}}'}}}}]
tellraw @s [{{text:"   id",color:"gold",bold:true}},{{text:"  nom de l'épreuve",color:"gray"}}]
tellraw @s [{{text:"   time",color:"gold",bold:true}},{{text:"  secondes pour s'enregistrer",color:"gray"}}]
tellraw @s [{{text:"   group",color:"gold",bold:true}},{{text:"  même nom = rec synchronisés",color:"gray"}}]
tellraw @s [{{text:"   sync",color:"gold",bold:true}},{{text:"  1 = démarre au prochain cycle du groupe",color:"gray"}}]
tellraw @s [{{text:"   tp_back",color:"gold",bold:true}},{{text:"  1 = retour au départ à la fin (défaut), 0 = reste sur place",color:"gray"}}]
tellraw @s [{{text:"   À mettre dans un command block, derrière un bouton ou une plaque.",color:"gray"}}]
tellraw @s [{{text:"   "}},{{text:"[◀ Précédent]",color:"green",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help_page {{with:{{page:3}}}}"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}},{{text:"  "}},{{text:"[Menu]",color:"gold",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}},{{text:"  "}},{{text:"[Suivant ▶]",color:"green",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help_page {{with:{{page:5}}}}"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}}]
""")

	write_versioned_function("help/p5", f"""
tellraw @s {{text:"══ SURVIREC · 5/5 · GÉRER ══",color:"gold"}}
tellraw @s [{{text:"   kill",color:"gold",bold:true}},{{text:"  supprime les entités d'un tag ou d'une séquence  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/kill {{with:{{tag:"x"}}}}'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/kill {{with:{{tag:"x"}}}}'}}}}]
tellraw @s [{{text:"   kill_all",color:"gold",bold:true}},{{text:"  supprime toutes les entités  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/kill_all'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/kill_all'}}}}]
tellraw @s [{{text:"   group_restart",color:"gold",bold:true}},{{text:"  relance la scène d'un groupe  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/group_restart {{with:{{group:"scene1"}}}}'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/group_restart {{with:{{group:"scene1"}}}}'}}}}]
tellraw @s [{{text:"   forget",color:"gold",bold:true}},{{text:"  efface une séquence du monde  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/forget {{with:{{name:"walk"}}}}'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/forget {{with:{{name:"walk"}}}}'}}}}]
tellraw @s [{{text:"   records",color:"gold",bold:true}},{{text:"  liste tes enregistrements  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/records'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/records'}}}}]
tellraw @s [{{text:"   export",color:"gold",bold:true}},{{text:"  réaffiche les boutons de copie d'une séquence  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/export {{with:{{name:"walk"}}}}'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/export {{with:{{name:"walk"}}}}'}}}}]
tellraw @s [{{text:"   settings",color:"gold",bold:true}},{{text:"  portée (128) et fluidité : move_every 1 = fluide, 2 = défaut, 3+ = plus léger  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/settings {{with:{{range:128,move_every:2}}}}'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/settings {{with:{{range:128,move_every:2}}}}'}}}}]
tellraw @s [{{text:"   range",color:"gold",bold:true}},{{text:"  portée globale d'animation (128 blocs)  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/range {{with:{{r:128}}}}'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/range {{with:{{r:128}}}}'}}}}]
tellraw @s [{{text:"   menu_item",color:"gold",bold:true}},{{text:"  donne l'objet Survirec  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'execute as @p run function #{ns}:v{major}/menu_item'}},hover_event:{{action:"show_text",value:'execute as @p run function #{ns}:v{major}/menu_item'}}}}]
tellraw @s [{{text:"   reset",color:"gold",bold:true}},{{text:"  annule tous les enregistrements en cours  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/reset'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/reset'}}}}]
tellraw @s [{{text:"   debug",color:"gold",bold:true}},{{text:"  diagnostic  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/debug'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/debug'}}}}]
tellraw @s [{{text:"   "}},{{text:"[◀ Précédent]",color:"green",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help_page {{with:{{page:4}}}}"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}},{{text:"  "}},{{text:"[Menu]",color:"gold",click_event:{{action:"run_command",command:"/function #{ns}:v{major}/help"}},hover_event:{{action:"show_text",value:"Ouvrir"}}}}]
""")

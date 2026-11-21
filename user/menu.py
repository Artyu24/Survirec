""" Menu item, records list and copy buttons. """
# Imports
from stewbeet import Mem, write_versioned_function

# Constants
MENU_HEAD_TEXTURE: str = (
	"eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvMWI0MWQwZmZjOTg4MjVkYWM2MzZhZmJjZjYxMzU3MmRmZTBkMTg0MGYyZDA2OGZlNDNhMjViMGQzYjYwOTA4YSJ9fX0="
)
""" Base64 `textures` value of the menu item head (Camera head, minecraft-heads.com, Custom Head ID 120246).
To use another head, paste its "Value" field here. Empty string = spyglass look.
"""


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	major: str = version.split(".")[0]

	write_versioned_function("menu/chcmd", f"""
# la durée doit être un nombre entier de secondes
$scoreboard players set #ct {ns}.data $(time)
execute unless score #ct {ns}.data matches 1.. run return run tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"La durée doit être un nombre de secondes (1 ou plus).",color:"red"}}]
execute store result storage {ns}:in cfg.time int 1 run scoreboard players get #ct {ns}.data
function {ns}:v{version}/menu/chcmd2 with storage {ns}:in cfg
""")

	write_versioned_function("menu/chcmd2", f"""
tellraw @s {{text:"------------------------------------------------",color:"dark_gray"}}
$tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Épreuve ",color:"green"}},{{text:"$(id)",color:"gold"}},{{text:" · $(time) s · groupe ",color:"green"}},{{text:"$(group)",color:"gold"}}]
$tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"[Copier la commande]",color:"yellow",bold:true,click_event:{{action:"copy_to_clipboard",value:'execute as @p run function #{ns}:v{major}/challenge {{with:{{id:"$(id)",time:$(time),group:"$(group)",sync:$(sync),tp_back:$(tp_back)}}}}'}},hover_event:{{action:"show_text",value:"Colle-la dans un command block impulsion, derrière un bouton ou une plaque"}}}},{{text:"  → command block ",color:"gray"}},{{text:"impulsion",color:"gold"}}]
tellraw @s {{text:"------------------------------------------------",color:"dark_gray"}}
""")

	write_versioned_function("menu/cmds", f"""
tellraw @s {{text:"══ Commandes à copier ══",color:"gold"}}
tellraw @s [{{text:"   Enregistrer  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/start {{with:{{name:"walk",every:4}}}}'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/start {{with:{{name:"walk",every:4}}}}'}}}}]
tellraw @s [{{text:"   Rejouer ici  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/play {{with:{{name:"walk"}}}}'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/play {{with:{{name:"walk"}}}}'}}}}]
tellraw @s [{{text:"   Épreuve (command block)  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'execute as @p run function #{ns}:v{major}/challenge {{with:{{id:"epreuve1",time:30,group:"salle1"}}}}'}},hover_event:{{action:"show_text",value:'execute as @p run function #{ns}:v{major}/challenge {{with:{{id:"epreuve1",time:30,group:"salle1"}}}}'}}}}]
tellraw @s [{{text:"   Donner le menu (command block)  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'execute as @p run function #{ns}:v{major}/menu_item'}},hover_event:{{action:"show_text",value:'execute as @p run function #{ns}:v{major}/menu_item'}}}}]
tellraw @s [{{text:"   Ouvrir le menu  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/menu'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/menu'}}}}]
tellraw @s [{{text:"   Mes enregistrements  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/records'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/records'}}}}]
tellraw @s [{{text:"   Tout supprimer  ",color:"gray"}},{{text:"[Copier]",color:"yellow",click_event:{{action:"copy_to_clipboard",value:'/function #{ns}:v{major}/kill_all'}},hover_event:{{action:"show_text",value:'/function #{ns}:v{major}/kill_all'}}}}]
""")

	write_versioned_function("menu/give", f"""
execute unless entity @s[type=minecraft:player] run return fail
clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{menu:1b}}}}]
execute if data storage {ns}:cfg menu{{texture:""}} run return run function {ns}:v{version}/menu/give_plain
function {ns}:v{version}/menu/give_head with storage {ns}:cfg menu
""")

	write_versioned_function("menu/give_head", f"""
$give @s minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{menu:1b}},smithed:{{ignore:{{functionality:1b,crafting:1b}}}}}},minecraft:item_name={{text:"Survirec",color:"gold",bold:true}},minecraft:lore=[{{text:"Clic droit : ouvrir le menu",color:"gray",italic:false}}],minecraft:item_model="minecraft:player_head",minecraft:profile={{properties:[{{name:"textures",value:"$(texture)"}}]}}]
""")

	write_versioned_function("menu/give_plain", f"""
give @s minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{menu:1b}},smithed:{{ignore:{{functionality:1b,crafting:1b}}}}}},minecraft:item_name={{text:"Survirec",color:"gold",bold:true}},minecraft:lore=[{{text:"Clic droit : ouvrir le menu",color:"gray",italic:false}}],minecraft:item_model="minecraft:spyglass"]
""")

	write_versioned_function("menu/open", f"""
scoreboard players set @s {ns}.use 0
dialog show @s {ns}:menu
""")

	write_versioned_function("menu/records", f"""
tellraw @s {{text:"══ Enregistrements ══",color:"gold"}}
scoreboard players operation #me {ns}.data = @s {ns}.pid
scoreboard players set #cnt {ns}.data 0
data modify storage {ns}:tmp it set value []
data modify storage {ns}:tmp it set from storage {ns}:lib names
execute if data storage {ns}:tmp it[0] run function {ns}:v{version}/menu/rloop
execute if score #cnt {ns}.data matches 0 run tellraw @s {{text:"   Aucun enregistrement pour l'instant.",color:"gray"}}
""")

	write_versioned_function("menu/rline", f"""
scoreboard players add #cnt {ns}.data 1
$tellraw @s [{{text:"   • ",color:"gray"}},{{text:"$(name)",color:"aqua",bold:true}},{{text:"   "}},{{text:"[▶ Jouer ici]",color:"green",bold:true,click_event:{{action:"run_command",command:'/function #{ns}:v{major}/play {{with:{{name:"$(name)"}}}}'}},hover_event:{{action:"show_text",value:"Fait apparaître un mannequin à ta position"}}}},{{text:"  "}},{{text:"[📋 Copier]",color:"yellow",bold:true,click_event:{{action:"run_command",command:'/function #{ns}:v{major}/export {{with:{{name:"$(name)"}}}}'}},hover_event:{{action:"show_text",value:"Réaffiche les boutons de copie pour un command block"}}}},{{text:"  "}},{{text:"[🗑]",color:"red",bold:true,click_event:{{action:"suggest_command",command:'/function #{ns}:v{major}/forget {{with:{{name:"$(name)"}}}}'}},hover_event:{{action:"show_text",value:"Supprimer (appuie sur Entrée pour confirmer)"}}}}]
""")

	write_versioned_function("menu/rloop", f"""
scoreboard players set #ep {ns}.data -1
execute store result score #ep {ns}.data run data get storage {ns}:tmp it[0].pid
execute if score #ep {ns}.data = #me {ns}.data run function {ns}:v{version}/menu/rline with storage {ns}:tmp it[0]
data remove storage {ns}:tmp it[0]
execute if data storage {ns}:tmp it[0] run function {ns}:v{version}/menu/rloop
""")

	write_versioned_function("menu/texture", f"""
# Texture de la tête « Survirec » (MENU_HEAD_TEXTURE dans user/menu.py)
data modify storage {ns}:cfg menu.texture set value "{MENU_HEAD_TEXTURE}"
""")

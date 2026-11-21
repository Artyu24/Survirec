""" Menu item, records list and copy buttons. """
# Imports
from stewbeet import Mem, write_versioned_function

from .common import SEPARATOR, Storages, copy, info, run, say, text

# Constants
MENU_HEAD_TEXTURE: str = (
	"eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvMWI0MWQwZmZjOTg4MjVkYWM2MzZhZmJjZjYxMzU3MmRmZTBkMTg0MGYyZDA2OGZlNDNhMjViMGQzYjYwOTA4YSJ9fX0="
)
""" Base64 `textures` value of the menu item head (Camera head, minecraft-heads.com, Custom Head ID 120246).
To use another head, paste its "Value" field here. Empty string = spyglass look.
"""

MENU_ITEM: str = (
	"minecraft:carrot_on_a_stick[minecraft:custom_data={{{ns}:{{menu:1b}},smithed:{{ignore:{{functionality:1b,crafting:1b}}}}}},"
	'minecraft:item_name={{text:"Survirec",color:"gold",bold:true}},minecraft:lore=[{{text:"Clic droit : ouvrir le menu",color:"gray",italic:false}}],'
)
""" Menu item, without its look (item_model...). Right-click detected by the <ns>.use statistic. Format it with ns. """

MENU_MATCH: str = "minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{menu:1b}}}}]"
""" Item predicate matching the menu item. Format it with ns. """

COMMANDS: tuple[tuple[str, str], ...] = (
	("Enregistrer", '/function #{api}/start {{with:{{name:"walk",every:4}}}}'),
	("Rejouer ici", '/function #{api}/play {{with:{{name:"walk"}}}}'),
	("Épreuve (command block)", 'execute as @p run function #{api}/challenge {{with:{{id:"epreuve1",time:30,group:"salle1"}}}}'),
	("Donner le menu (command block)", "execute as @p run function #{api}/menu_item"),
	("Ouvrir le menu", "/function #{api}/menu"),
	("Mes enregistrements", "/function #{api}/records"),
	("Tout supprimer", "/function #{api}/kill_all"),
)
""" Useful commands shown by #survirec:v1/commands (format with api). """


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	functions: str = f"{ns}:v{version}"
	api: str = f"{ns}:v{version.split('.')[0]}"
	storage: Storages = Storages(ns)
	item: str = MENU_ITEM.format(ns=ns)

	write_versioned_function("menu/check_challenge_time", f"""
# the duration must be a whole number of seconds
$scoreboard players set #challenge_time {ns}.data $(time)
execute unless score #challenge_time {ns}.data matches 1.. run return run {info("La durée doit être un nombre de secondes (1 ou plus).", "red")}
execute store result storage {storage.call} options.time int 1 run scoreboard players get #challenge_time {ns}.data
function {functions}/menu/show_challenge_command with storage {storage.call} options
""")

	command: str = f'execute as @p run function #{api}/challenge {{with:{{id:"$(id)",time:$(time),group:"$(group)",sync:$(sync),tp_back:$(tp_back)}}}}'
	write_versioned_function("menu/show_challenge_command", f"""
{SEPARATOR}
${say(text("Épreuve ", "green"), text("$(id)", "gold"), text(" · $(time) s · groupe ", "green"), text("$(group)", "gold"))}
${say(
	copy("[Copier la commande]", command, "Colle-la dans un command block impulsion, derrière un bouton ou une plaque", extra="bold:true"),
	text("  -> command block ", "gray"), text("impulsion", "gold"),
)}
{SEPARATOR}
""")

	commands: str = f"tellraw @s {text('══ Commandes à copier ══', 'gold')}\n"
	for label, value in COMMANDS:
		commands += f"tellraw @s [{text(f'   {label}  ', 'gray')},{copy('[Copier]', value.format(api=api))}]\n"
	write_versioned_function("menu/show_commands", commands)

	write_versioned_function("menu/give_item", f"""
execute unless entity @s[type=minecraft:player] run return fail
clear @s {MENU_MATCH.format(ns=ns)}
execute if data storage {ns}:config menu{{texture:""}} run return run function {functions}/menu/give_spyglass_item
function {functions}/menu/give_head_item with storage {ns}:config menu
""")
	write_versioned_function("menu/give_head_item", f'$give @s {item}minecraft:item_model="minecraft:player_head",minecraft:profile={{properties:[{{name:"textures",value:"$(texture)"}}]}}]')
	write_versioned_function("menu/give_spyglass_item", f'give @s {item}minecraft:item_model="minecraft:spyglass"]')

	write_versioned_function("menu/open", f"""
scoreboard players set @s {ns}.item_uses 0
dialog show @s {ns}:menu
""")

	write_versioned_function("menu/list_records", f"""
tellraw @s {text("══ Enregistrements ══", "gold")}
scoreboard players operation #player_id {ns}.data = @s {ns}.player_id
scoreboard players set #record_count {ns}.data 0
data modify storage {storage.recording} names_left set value []
data modify storage {storage.recording} names_left set from storage {ns}:library names
execute if data storage {storage.recording} names_left[0] run function {functions}/menu/list_next_record
execute if score #record_count {ns}.data matches 0 run tellraw @s {text("   Aucun enregistrement pour l'instant.", "gray")}
""")

	def record_button(label: str, entry: str, color: str, hover: str, action: str = "run_command") -> str:
		return run(label, f'/function #{api}/{entry} {{with:{{name:"$(name)"}}}}', color, hover, extra="bold:true", action=action)
	write_versioned_function("menu/show_record", f"""
scoreboard players add #record_count {ns}.data 1
$tellraw @s [{",".join((
	text("   • ", "gray"), text("$(name)", "aqua", "bold:true"), text("   "),
	record_button("[Jouer ici]", "play", "green", "Fait apparaître un mannequin à ta position"), text("  "),
	record_button("[📋 Copier]", "export", "yellow", "Réaffiche les boutons de copie pour un command block"), text("  "),
	record_button("[🗑]", "forget", "red", "Supprimer (appuie sur Entrée pour confirmer)", action="suggest_command"),
))}]
""")

	write_versioned_function("menu/list_next_record", f"""
# only the recordings of this player
scoreboard players set #entry_player {ns}.data -1
execute store result score #entry_player {ns}.data run data get storage {storage.recording} names_left[0].player_id
execute if score #entry_player {ns}.data = #player_id {ns}.data run function {functions}/menu/show_record with storage {storage.recording} names_left[0]
data remove storage {storage.recording} names_left[0]
execute if data storage {storage.recording} names_left[0] run function {functions}/menu/list_next_record
""")

	write_versioned_function("menu/set_head_texture", f"""
data modify storage {ns}:config menu.texture set value "{MENU_HEAD_TEXTURE}"
""")

""" In-game help: a dialog index and one dialog per topic, opened by #survirec:v1/help and #survirec:v1/help_page. """
# Imports
from stewbeet import Mem, write_versioned_function
from stouputils.typing import JsonDict

from .dialogs import back, message, text, write

# Constants
PAGES: tuple[str, ...] = ("Enregistrer", "Lancer", "Champs", "Épreuve", "Gérer")
""" Help pages, in order: dialogs <ns>:help/page_1 to <ns>:help/page_5. """

PLAYBACK_HELP: tuple[tuple[str, str], ...] = (
	("pos", "où ça apparaît, relatif possible (~ ~ ~ = centre du bloc)"),
	("entity", "mannequin, zombie, item_display..."),
	("nbt", "NBT appliqués à l'apparition, ex : {Glowing:1b} (sauf Tags)"),
	("size", "taille (1 = normale)"),
	("loop", "1 boucle · 0 fige · 2 disparaît"),
	("redstone", "1 = bloc de redstone 2 blocs au-dessus du command block à chaque fin de boucle"),
	("restore", "monde remis en état : 1 à chaque boucle · 2 aussi à la fin · 0 jamais"),
	("speed", "100 = normal"),
	("delay", "décalage de départ (ticks)"),
	("range", "arrêt si aucun joueur à X blocs (0 = défaut)"),
	("tag", "remplace l'ancien (unique dans tout le monde)"),
	("group", "synchronise avec le groupe"),
	("group_radius", "distance de regroupement (50 blocs)"),
	("hit_players", "1 = ses coups touchent aussi les joueurs (mannequin, mob)"),
	("pose", "pose forcée (mannequin)"),
	("skin", "pseudo d'un joueur (mannequin)"),
	("texture", "texture base64 si skin vide (mannequin)"),
	("head chest legs feet", "armure (mannequin, mob)"),
	("mainhand offhand", "mains (mannequin, mob)"),
)
""" Page 3: playback fields. """

CHALLENGE_HELP: tuple[tuple[str, str], ...] = (
	("id", "nom de l'épreuve"),
	("time", "secondes pour s'enregistrer"),
	("group", "même nom = rec synchronisés"),
	("sync", "1 = démarre au prochain cycle du groupe"),
	("tp_back", "1 = retour au départ à la fin (défaut), 0 = reste sur place"),
)
""" Page 4: challenge fields. """

MANAGE_HELP: tuple[tuple[str, str, str], ...] = (
	("kill", "supprime les entités d'un tag ou d'une séquence", '/function #{api}/kill {{with:{{tag:"x"}}}}'),
	("kill_all", "supprime toutes les entités", "/function #{api}/kill_all"),
	("group_restart", "relance la scène d'un groupe", '/function #{api}/group_restart {{with:{{group:"scene1"}}}}'),
	("forget", "efface une séquence du monde", '/function #{api}/forget {{with:{{name:"walk"}}}}'),
	("records", "liste tes enregistrements", "/function #{api}/records"),
	("export", "réaffiche les boutons de copie d'une séquence", '/function #{api}/export {{with:{{name:"walk"}}}}'),
	("settings", "portée (128) et fluidité : move_every 1 = fluide, 2 = défaut, 3+ = plus léger", "/function #{api}/settings {{with:{{range:128,move_every:2}}}}"),
	("range", "portée globale d'animation (128 blocs)", "/function #{api}/range {{with:{{r:128}}}}"),
	("menu_item", "donne l'objet Survirec", "execute as @p run function #{api}/menu_item"),
	("reset", "annule tous les enregistrements en cours", "/function #{api}/reset"),
	("debug", "diagnostic", "/function #{api}/debug"),
)
""" Page 5: management entry points, with the command copied by their button (format with api). """




def field(name: str, description: str) -> JsonDict:
	""" Help line: the explained word in bold, then its description. """
	return line((name, "gold", True), (f"  {description}", "gray", False))


def line(*parts: tuple[str, str] | tuple[str, str, bool]) -> JsonDict:
	""" Help line from (text, color) or (text, color, is_bold) parts.
	The empty root keeps the parts apart: in a list, every part inherits the style of the first one.
	"""
	contents: list[str | JsonDict] = [""]
	for part in parts:
		component: JsonDict = {"text": part[0], "color": part[1]}
		if len(part) == 3 and part[2]:
			component["bold"] = True
		contents.append(component)
	return {"type": "minecraft:plain_message", "width": 300, "contents": contents}


def copy_button(label: str, command: str, width: int = 150) -> JsonDict:
	return {"label": text(label, "yellow"), "width": width, "tooltip": text(command), "action": {"type": "minecraft:copy_to_clipboard", "value": command}}


def copy_line(label: str, command: str) -> JsonDict:
	""" Body line copying a command when clicked: a button on its own row, above the action buttons. """
	return {"type": "minecraft:plain_message", "width": 300, "contents": {
		"text": label, "color": "yellow",
		"click_event": {"action": "copy_to_clipboard", "value": command}, "hover_event": {"action": "show_text", "value": command},
	}}


def page_button(ns: str, label: str, page: int) -> JsonDict:
	return {"label": text(label, "green"), "width": 150, "action": {"type": "minecraft:show_dialog", "dialog": f"{ns}:help/page_{page}"}}


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	functions: str = f"{ns}:v{version}"
	api: str = f"{ns}:v{version.split('.')[0]}"
	start_example: str = f'/function #{api}/start {{with:{{name:"walk",every:4}}}}'
	challenge_example: str = f'execute as @p run function #{api}/challenge {{with:{{id:"epreuve1",time:30,group:"salle1"}}}}'

	pages: tuple[tuple[list[JsonDict], list[JsonDict]], ...] = (
		([
			message(start_example[1:], "aqua"),
			field("name", "nom de la séquence (lettres, chiffres, _)"),
			field("every", "4 = fluide, 2 = précis"),
			field("group", "démarre au prochain cycle du groupe"),
			line(("Enregistré aussi : ", "gray"), ("coups, boutons, leviers, portes, blocs posés et cassés", "aqua")),
			line(("Arrêt : ", "gray"), ("clic droit avec la barrière", "red")),
		], [copy_button("Copier l'exemple", start_example)]),
		([
			line(("1. À la fin de l'enregistrement, clique sur ", "gray"), ("[Copier]", "yellow"), (" de l'entité voulue", "gray")),
			line(("2. Colle-la dans un command block ", "gray"), ("impulsion", "gold")),
			line(("3. Active le bloc", "gray")),
			line(("Les champs à modifier sont ", "gray"), ("au début", "gold"), (" de la commande", "gray")),
		], []),
		([field(name, description) for name, description in PLAYBACK_HELP], []),
		([
			message(challenge_example, "aqua"),
			*(field(name, description) for name, description in CHALLENGE_HELP),
			message("À mettre dans un command block, derrière un bouton ou une plaque."),
			copy_line("[Copier l'exemple]", challenge_example),
		], []),
		(
			[field(name, description) for name, description, _ in MANAGE_HELP],
			[copy_button(name, command.format(api=api)) for name, _, command in MANAGE_HELP],
		),
	)

	for page, (title, (body, actions)) in enumerate(zip(PAGES, pages, strict=True), start=1):
		navigation: list[JsonDict] = []
		if page > 1:
			navigation.append(page_button(ns, "< Précédent", page - 1))
		if page < len(PAGES):
			navigation.append(page_button(ns, "Suivant >", page + 1))
		write(f"{ns}:help/page_{page}", {
			"type": "minecraft:multi_action",
			"title": {"text": f"Aide {page}/{len(PAGES)} · {title}", "color": "gold"},
			"body": body,
			"columns": 2,
			"actions": [*actions, *navigation],
			"exit_action": back(f"{ns}:help"),
		})

	write(f"{ns}:help", {
		"type": "minecraft:multi_action",
		"title": {"text": "Aide Survirec", "color": "gold"},
		"body": [message("Choisis une page.")],
		"columns": 2,
		"actions": [
			*(page_button(ns, f"{page}. {title}", page) for page, title in enumerate(PAGES, start=1)),
			{"label": text("Recevoir l'objet", "yellow"), "width": 150, "tooltip": text("Objet qui ouvre le menu d'un clic droit"),
				"action": {"type": "minecraft:run_command", "command": f"function #{api}/menu_item"}},
		],
		"exit_action": back(f"{ns}:menu", "Menu"),
	})

	# Entry points of #survirec:v1/help and #survirec:v1/help_page (which checks the page number)
	write_versioned_function("help/open_index", f"""
execute unless entity @s[type=minecraft:player] run return fail
dialog show @s {ns}:help
""")
	write_versioned_function("help/open_page", f"""
execute unless entity @s[type=minecraft:player] run return fail
$dialog show @s {ns}:help/page_$(page)
""")

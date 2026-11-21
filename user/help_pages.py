""" In-game help: an index and one chat page per topic, linked together with the public #survirec:v1/help_page tag. """
# Imports
from stewbeet import Mem, write_versioned_function

from .common import copy, run, text

# Constants
PAGES: tuple[str, ...] = ("Enregistrer", "Lancer", "Champs", "Épreuve", "Gérer")
""" Help pages, in order (help/p1 to help/p5). """

PLAYBACK_HELP: tuple[tuple[str, str], ...] = (
	("pos", "où ça apparaît, relatif possible (~ ~ ~ = centre du bloc)"),
	("entity", "mannequin, cat..."),
	("size", "taille (1 = normale)"),
	("loop", "1 boucle · 0 fige · 2 disparaît"),
	("redstone", "1 = bloc de redstone 2 blocs au-dessus du command block à chaque fin de boucle"),
	("restore", "monde remis en état : 1 à chaque boucle · 2 aussi à la fin · 0 jamais"),
	("hit_players", "1 = ses coups touchent aussi les joueurs"),
	("speed", "100 = normal"),
	("delay", "décalage de départ (ticks)"),
	("range", "arrêt si aucun joueur à X blocs (0 = défaut)"),
	("tag", "remplace l'ancien (unique dans tout le monde)"),
	("group", "synchronise avec le groupe"),
	("group_radius", "distance de regroupement (50 blocs)"),
	("pose", "pose forcée"),
	("skin", "pseudo d'un joueur"),
	("texture", "texture base64 (si skin vide)"),
	("head chest legs feet", "armure"),
	("mainhand offhand", "mains"),
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


def field(name: str, description: str, *after: str) -> str:
	""" Help line: the explained word in bold, then its description. """
	return f"tellraw @s [{','.join((text(f'   {name}', 'gold', 'bold:true'), text(f'  {description}', 'gray'), *after))}]"


def line(*components: str) -> str:
	""" Indented help line. """
	return f"tellraw @s [{','.join((text('   '), *components))}]"


def buttons(*components: str) -> str:
	""" Indented line of buttons, two spaces apart. """
	parts: list[str] = []
	for button in components:
		if parts:
			parts.append(text("  "))
		parts.append(button)
	return line(*parts)


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	functions: str = f"{ns}:v{version}"
	api: str = f"{ns}:v{version.split('.')[0]}"
	start_example: str = f'/function #{api}/start {{with:{{name:"walk",every:4}}}}'
	challenge_example: str = f'execute as @p run function #{api}/challenge {{with:{{id:"epreuve1",time:30,group:"salle1"}}}}'

	def page_button(label: str, page: int, color: str) -> str:
		return run(label, f"/function #{api}/help_page {{with:{{page:{page}}}}}", color, "Ouvrir")

	playback_fields: str = ""
	for name, description in PLAYBACK_HELP:
		playback_fields += field(name, description) + "\n"
	challenge_fields: str = ""
	for name, description in CHALLENGE_HELP:
		challenge_fields += field(name, description) + "\n"
	manage_fields: str = ""
	for name, description, command in MANAGE_HELP:
		manage_fields += field(name, f"{description}  ", copy("[Copier]", command.format(api=api))) + "\n"

	bodies: tuple[str, ...] = (
		f"""{line(text(start_example[1:], "aqua"))}
{line(copy("[Copier l'exemple]", start_example))}
{field("name", "nom de la séquence (lettres, chiffres, _)")}
{field("every", "4 = fluide, 2 = précis")}
{field("group", "démarre au prochain cycle du groupe")}
tellraw @s [{text('   Enregistré aussi : ', 'gray')},{text('coups, boutons, leviers, portes, blocs posés et cassés', 'aqua')}]
tellraw @s [{text('   Arrêt : ', 'gray')},{text('clic droit avec la barrière', 'red')}]
""",
		f"""tellraw @s [{text('   1. Clique sur ', 'gray')},{text('[Copier 1]', 'yellow')},{text(" à la fin de l'enregistrement", 'gray')}]
tellraw @s [{text('   2. Colle-la dans un command block ', 'gray')},{text('impulsion', 'gold')}]
tellraw @s [{text('   3. Active le bloc', 'gray')}]
tellraw @s [{text('   Les champs à modifier sont ', 'gray')},{text('au début', 'gold')},{text(' de la commande', 'gray')}]
""",
		playback_fields,
		f"""{line(text(f"execute as @p run function #{api}/challenge", "aqua"))}
{line(text('{with:{id:"epreuve1",time:30,group:"salle1"}}', "aqua"))}
{line(copy("[Copier l'exemple]", challenge_example))}
{challenge_fields}tellraw @s [{text('   À mettre dans un command block, derrière un bouton ou une plaque.', 'gray')}]
""",
		manage_fields,
	)

	for page, (title, body) in enumerate(zip(PAGES, bodies, strict=True), start=1):
		navigation: list[str] = []
		if page > 1:
			navigation.append(page_button("[< Précédent]", page - 1, "green"))
		navigation.append(run("[Menu]", f"/function #{api}/help", "gold", "Ouvrir"))
		if page < len(PAGES):
			navigation.append(page_button("[Suivant >]", page + 1, "green"))
		write_versioned_function(f"help/page_{page}", f"""
tellraw @s {text(f"══ SURVIREC · {page}/{len(PAGES)} · {title.upper()} ══", "gold")}
{body}{buttons(*navigation)}
""")

	pages: str = ""
	for page, title in enumerate(PAGES, start=1):
		pages += line(page_button(f"[{page}] {title}", page, "aqua")) + "\n"
	write_versioned_function("help/index", f"""
tellraw @s {text("══ SURVIREC · AIDE ══", "gold")}
{buttons(run("[🎬 Ouvrir le menu]", f"/function #{api}/menu", "gold", "Interface Survirec"),
	run("[Recevoir l'objet]", f"/function #{api}/menu_item", "yellow", "Objet qui ouvre le menu d'un clic droit"))}
{pages}""")
	# called by the public help_page entry point, which checks the page number
	write_versioned_function("help/open_page", f"$function {functions}/help/page_$(page)")

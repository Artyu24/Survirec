""" Dialogs: the Survirec menu, its forms, and the Smithed Data Pack Menu Dialog convention.

Every button runs a public `#survirec:v<major>/...` function tag, never a versioned function:
a dialog stays the same whichever version of the library answers it.
"""
# Imports
from beet import Dialog, DialogTag
from stewbeet import Mem, set_json_encoder
from stouputils.typing import JsonDict

# Constants
REPOSITORY: str = "https://github.com/Artyu24/Survirec"
""" Project page, opened from the menu and the about dialog. """

MENU_COMMANDS: tuple[tuple[str, str, str, str], ...] = (
	("■ Arrêter", "red", "stop", "Termine ton enregistrement et affiche les boutons de copie"),
	("Arrêter + retour", "red", "stop_loop", "Termine et ajoute un retour au départ (boucle propre)"),
	("✖ Annuler", "red", "abort", "Annule ton enregistrement en cours"),
	("📂 Mes enregistrements", "", "records", "Rejouer, recopier ou supprimer tes séquences"),
	("📋 Commandes à copier", "", "commands", "Les commandes utiles, prêtes à coller"),
)
""" Menu buttons running an entry point: (label, color, entry point, tooltip). """


def text(content: str, color: str = "") -> JsonDict:
	return {"text": content, "color": color} if color else {"text": content}


def message(content: str, color: str = "gray") -> JsonDict:
	return {"type": "minecraft:plain_message", "width": 300, "contents": text(content, color)}


def back(dialog: str, label: str = "Retour") -> JsonDict:
	return {"label": text(label), "width": 200, "action": {"type": "minecraft:show_dialog", "dialog": dialog}}


def text_input(key: str, label: str, initial: str, max_length: int = 32) -> JsonDict:
	return {"type": "minecraft:text", "key": key, "label": text(label), "initial": initial, "max_length": max_length, "width": 200}


def toggle(key: str, label: str, initial: bool) -> JsonDict:
	return {"type": "minecraft:boolean", "key": key, "label": text(label), "initial": initial, "on_true": "1", "on_false": "0"}


def write(path: str, dialog: JsonDict) -> None:
	Mem.ctx.data.dialogs[path] = set_json_encoder(Dialog(dialog))


def main() -> None:
	ns: str = Mem.ctx.project_id
	major: str = Mem.ctx.project_version.split(".")[0]
	api: str = f"#{ns}:v{major}"

	write(f"{ns}:menu", {
		"type": "minecraft:multi_action",
		"title": {"text": "Survirec", "color": "gold", "bold": True},
		"body": [message("Enregistre tes mouvements et fais-les rejouer par des mannequins.")],
		"columns": 2,
		"actions": [
			{"label": text("🎥 Nouvel enregistrement", "green"), "width": 150, "tooltip": text("Choisir un nom et démarrer"),
				"action": {"type": "minecraft:show_dialog", "dialog": f"{ns}:record"}},
			{"label": text("🏁 Épreuve", "green"), "width": 150, "tooltip": text("Enregistrement chronométré, rejoué par ton double"),
				"action": {"type": "minecraft:show_dialog", "dialog": f"{ns}:challenge"}},
			*({"label": text(label, color), "width": 150, "tooltip": text(tooltip),
				"action": {"type": "minecraft:run_command", "command": f"function {api}/{entry}"}} for label, color, entry, tooltip in MENU_COMMANDS),
			{"label": text("❓ Aide"), "width": 150, "tooltip": text("Aide détaillée, page par page"),
				"action": {"type": "minecraft:show_dialog", "dialog": f"{ns}:help"}},
			{"label": text("📖 README (GitHub)", "aqua"), "width": 304, "tooltip": text("Documentation complète"),
				"action": {"type": "minecraft:open_url", "url": f"{REPOSITORY}#readme"}},
		],
		"exit_action": {"label": text("Fermer"), "width": 200},
	})

	write(f"{ns}:record", {
		"type": "minecraft:multi_action",
		"title": {"text": "🎥 Nouvel enregistrement", "color": "gold"},
		"body": [message("Nom : lettres, chiffres et _ uniquement. Un même nom remplace l'ancien enregistrement.")],
		"inputs": [
			text_input("name", "Nom", "walk"),
			{"type": "minecraft:single_option", "key": "every", "label": text("Précision"), "width": 200, "options": [
				{"id": "2", "display": text("Précise (2)")},
				{"id": "4", "display": text("Normale (4)"), "initial": True},
				{"id": "8", "display": text("Légère (8)")},
			]},
			text_input("group", "Groupe (optionnel)", ""),
		],
		"columns": 1,
		"actions": [{
			"label": text("Démarrer", "green"), "width": 200,
			"tooltip": text("Avec un groupe, l'enregistrement attend le prochain cycle du groupe"),
			"action": {"type": "minecraft:dynamic/run_command", "template": f'function {api}/start {{with:{{name:"$(name)",every:$(every),group:"$(group)"}}}}'},
		}],
		"exit_action": back(f"{ns}:menu"),
	})

	write(f"{ns}:challenge", {
		"type": "minecraft:multi_action",
		"title": {"text": "🏁 Épreuve", "color": "gold"},
		"body": [message("Prépare la commande d'une épreuve, à coller dans un command block (derrière un bouton ou une plaque).")],
		"inputs": [
			text_input("id", "Nom de l'épreuve", "epreuve1"),
			text_input("time", "Durée (secondes)", "30", max_length=5),
			text_input("group", "Groupe", "main"),
			toggle("sync", "Démarrer au prochain cycle du groupe", initial=False),
			toggle("tp_back", "Revenir au point de départ à la fin", initial=True),
		],
		"columns": 1,
		"actions": [{
			"label": text("📋 Copier la commande", "yellow"), "width": 200,
			"action": {"type": "minecraft:dynamic/run_command",
				"template": f'function {api}/challenge_cmd {{with:{{id:"$(id)",time:$(time),group:"$(group)",sync:$(sync),tp_back:$(tp_back)}}}}'},
		}],
		"exit_action": back(f"{ns}:menu"),
	})

	# Smithed Data Pack Menu Dialog convention: the shared list in the pause screen, and our entry in it
	write(f"{ns}:about", {
		"type": "minecraft:multi_action",
		"title": {"text": "Survirec", "color": "gold", "bold": True},
		"body": [
			message("Enregistre les mouvements d'un joueur et les rejoue avec des mannequins.", color=""),
			message(f"Par {Mem.ctx.project_author}"),
		],
		"actions": [
			{"label": "Ouvrir le menu", "action": {"type": "minecraft:show_dialog", "dialog": f"{ns}:menu"}},
			{"label": "GitHub", "action": {"type": "minecraft:open_url", "url": REPOSITORY}},
			{"label": "Signaler un problème", "action": {"type": "minecraft:open_url", "url": f"{REPOSITORY}/issues"}},
		],
		"exit_action": {"action": {"type": "minecraft:show_dialog", "dialog": "smithed:data_packs"}, "label": {"translate": "gui.back"}, "width": 200},
	})
	write("smithed:data_packs", {
		"type": "minecraft:dialog_list",
		"external_title": {"translate": "menu.smithed.data_packs", "fallback": "%s...", "with": [{"translate": "selectWorld.dataPacks"}]},
		"title": {"translate": "menu.smithed.data_packs.title", "fallback": "%s", "with": [{"translate": "selectWorld.dataPacks"}]},
		"dialogs": "#smithed:data_packs",
		"exit_action": {"label": {"translate": "gui.back"}, "width": 200},
	})
	Mem.ctx.data.dialogs_tags["smithed:data_packs"] = set_json_encoder(DialogTag({"values": [{"id": f"{ns}:about", "required": False}]}))
	Mem.ctx.data.dialogs_tags["minecraft:pause_screen_additions"] = set_json_encoder(DialogTag({"values": [{"id": "smithed:data_packs", "required": False}]}))

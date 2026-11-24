""" Everything that is not a function: the hidden dimension, block and item tags, advancements. """
# Imports
from beet import Advancement, BlockTag, EntityTypeTag, ItemTag
from beet.contrib.worldgen import Dimension
from stewbeet import Mem, set_json_encoder, write_versioned_function
from stouputils.typing import JsonDict

from .common import Storages

# Constants
WEAPON_DAMAGE: dict[int, tuple[str, ...]] = {
	20: ("wooden_pickaxe", "golden_pickaxe"),
	25: ("wooden_shovel", "golden_shovel"),
	30: ("stone_pickaxe", "copper_pickaxe"),
	35: ("stone_shovel", "copper_shovel"),
	40: ("wooden_sword", "golden_sword", "iron_pickaxe"),
	45: ("iron_shovel",),
	50: ("stone_sword", "copper_sword", "diamond_pickaxe"),
	55: ("diamond_shovel",),
	60: ("iron_sword", "mace", "netherite_pickaxe"),
	65: ("netherite_shovel",),
	70: ("diamond_sword", "wooden_axe", "golden_axe"),
	80: ("netherite_sword",),
	90: ("stone_axe", "copper_axe", "iron_axe", "diamond_axe", "trident"),
	100: ("netherite_axe",),
}
""" Damage of a player's hit with the held item, in tenths of a health point (fist: 10). """

FIST_DAMAGE: int = 10
""" Damage of a hit with any other item, in tenths. """

COPPER_STAGES: tuple[str, ...] = ("", "exposed_", "weathered_", "oxidized_")
""" Oxidation prefixes of the copper blocks (each one also has a waxed_ version). """

RAY_PASS: tuple[str, ...] = ("#minecraft:air", "minecraft:water", "minecraft:lava", "minecraft:bubble_column")
""" Blocks the look ray goes through (plus light blocks). """

TRIGGERS: dict[str, tuple[JsonDict, str]] = {
	"swing": ({
		"criteria": {
			"hit": {"trigger": "minecraft:player_hurt_entity"},
			"block": {"trigger": "minecraft:any_block_use"},
			"entity": {"trigger": "minecraft:player_interacted_with_entity"},
		},
		"requirements": [["hit", "block", "entity"]],
	}, "note_swing"),
	"attack": ({"criteria": {"x": {"trigger": "minecraft:player_hurt_entity"}}}, "note_hit"),
	"place": ({"criteria": {"x": {"trigger": "minecraft:placed_block"}}}, "note_place"),
	"use": ({"criteria": {"x": {"trigger": "minecraft:any_block_use"}}}, "note_use"),
}
""" Advancement name (record/trigger/<name>) -> (criteria, record/<function> run for a recording player). """


def copper(kind: str) -> list[JsonDict]:
	""" Every copper `kind` (door, trapdoor...), optional so that a version without them still loads. """
	return [{"id": f"minecraft:{waxed}{stage}copper_{kind}", "required": False} for waxed in ("", "waxed_") for stage in COPPER_STAGES]


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	major, minor, patch = version.split(".")
	data = Mem.ctx.data
	functions: str = f"{ns}:v{version}"
	playback: str = Storages(ns).playback

	# Hidden void dimension: chunk 0 = single blocks, chunk 1 = recording cubes, chunk 2 = look cubes
	data[f"{ns}:vault"] = set_json_encoder(Dimension({
		"type": "minecraft:overworld",
		"generator": {
			"type": "minecraft:flat",
			"settings": {"biome": "minecraft:the_void", "layers": [], "lakes": False, "features": False},
		},
	}))

	# Blocks a player (and so an entity) can toggle by hand
	data[ns].block_tags["doors_open"] = set_json_encoder(BlockTag({"values": ["#minecraft:wooden_doors", *copper("door")]}))
	data[ns].block_tags["trapdoors_open"] = set_json_encoder(BlockTag({"values": ["#minecraft:wooden_trapdoors", *copper("trapdoor")]}))
	data[ns].block_tags["interactive"] = set_json_encoder(BlockTag({"values": [
		"#minecraft:buttons", "minecraft:lever", f"#{ns}:doors_open", f"#{ns}:trapdoors_open", "#minecraft:fence_gates",
	]}))
	data[ns].block_tags["ray_pass"] = set_json_encoder(BlockTag({"values": [*RAY_PASS, {"id": "minecraft:light", "required": False}]}))

	# Playback entities moved and sized their own way
	data[ns].entity_type_tags["displays"] = set_json_encoder(EntityTypeTag({"values": ["minecraft:item_display", "minecraft:block_display", "minecraft:text_display"]}))

	# Damage of the hits played back, read from the held item
	for damage, items in WEAPON_DAMAGE.items():
		data[ns].item_tags[f"dmg/d{damage}"] = set_json_encoder(ItemTag({"values": [{"id": f"minecraft:{item}", "required": False} for item in items]}))
	weapon_checks: str = ""
	for damage in WEAPON_DAMAGE:
		weapon_checks += f"execute if items entity @s weapon.mainhand #{ns}:dmg/d{damage} run scoreboard players set #hit_damage {ns}.data {damage}\n"
	write_versioned_function("action/hit", f"""
scoreboard players set #hit_damage {ns}.data {FIST_DAMAGE}
{weapon_checks}execute store result storage {playback} hit.damage float 0.1 run scoreboard players get #hit_damage {ns}.data
tag @s add {ns}.hitter
execute at @s anchored eyes positioned ^ ^-0.6 ^1 run function {functions}/action/hit_in_front with storage {playback} hit
tag @s remove {ns}.hitter
""")

	# Recorded actions. Every version has its own advancements: only the resolved one records
	for name, (advancement, target) in TRIGGERS.items():
		path: str = f"v{version}/record/trigger/{name}"
		data[ns].advancements[path] = set_json_encoder(Advancement({**advancement, "rewards": {"function": f"{ns}:{path}"}}), max_level=-1)
		write_versioned_function(f"record/trigger/{name}", f"""
advancement revoke @s only {ns}:{path}
execute if score #{ns}.major load.status matches {major} if score #{ns}.minor load.status matches {minor} if score #{ns}.patch load.status matches {patch} if entity @s[tag={ns}.recording] run function {functions}/record/{target}
""")

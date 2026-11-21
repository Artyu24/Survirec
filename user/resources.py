""" Everything that is not a function: the hidden dimension, block and item tags, advancements. """
# Imports
from beet import Advancement, BlockTag, ItemTag
from beet.contrib.worldgen import Dimension
from stewbeet import Mem, set_json_encoder, write_versioned_function
from stouputils.typing import JsonDict

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
	}, "swing"),
	"attack": ({"criteria": {"x": {"trigger": "minecraft:player_hurt_entity"}}}, "atk"),
	"place": ({"criteria": {"x": {"trigger": "minecraft:placed_block"}}}, "place"),
	"use": ({"criteria": {"x": {"trigger": "minecraft:any_block_use"}}}, "use"),
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

	# Damage of the hits played back, read from the held item
	for damage, items in WEAPON_DAMAGE.items():
		data[ns].item_tags[f"dmg/d{damage}"] = set_json_encoder(ItemTag({"values": [{"id": f"minecraft:{item}", "required": False} for item in items]}))
	checks: str = "\n".join(
		f"execute if items entity @s weapon.mainhand #{ns}:dmg/d{damage} run scoreboard players set #dmg {ns}.data {damage}"
		for damage in WEAPON_DAMAGE
	)
	write_versioned_function("playback/a_hit", f"""
scoreboard players set #dmg {ns}.data {FIST_DAMAGE}
{checks}
execute store result storage {ns}:t hit.d float 0.1 run scoreboard players get #dmg {ns}.data
tag @s add {ns}.hitter
execute at @s anchored eyes positioned ^ ^-0.6 ^1 run function {ns}:v{version}/playback/a_hit2 with storage {ns}:t hit
tag @s remove {ns}.hitter
""")

	# Recorded actions. Every version has its own advancements: only the resolved one records
	for name, (advancement, target) in TRIGGERS.items():
		path: str = f"v{version}/record/trigger/{name}"
		data[ns].advancements[path] = set_json_encoder(Advancement({**advancement, "rewards": {"function": f"{ns}:{path}"}}), max_level=-1)
		write_versioned_function(f"record/trigger/{name}", f"""
advancement revoke @s only {ns}:{path}
execute if score #{ns}.major load.status matches {major} if score #{ns}.minor load.status matches {minor} if score #{ns}.patch load.status matches {patch} if entity @s[tag={ns}.on] run function {ns}:v{version}/record/{target}
""")

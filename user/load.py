""" Load, tick and unload: objectives, world state kept between versions, and the main loop. """
# Imports
from stewbeet import Mem, write_load_file, write_tick_file, write_unload_file

# Constants
DUMMY_OBJECTIVES: tuple[str, ...] = (
	# Playback instances
	"id", "run", "seg", "len", "n100", "pr", "spd", "lp", "ax", "ay", "az", "yw0", "pt0",
	"bx", "by", "bz", "byw", "bpt", "dx", "dy", "dz", "dyw", "dpt", "fl", "fn", "fx", "ek", "ei", "ov",
	"snp", "swp", "glp", "st", "pl", "near", "rb", "hs", "rng", "gloop", "gs", "si", "sk", "pid", "grp", "rs", "dv",
	# Recording state, per player
	"rpx", "rpy", "rpz", "rpyw", "rppt", "rox", "roy", "roz", "royw", "ropt",
	"rkf", "rkt", "rtk", "rtime", "revery", "rlsw", "rchal", "rcdur", "rwg", "ratype",
	# Recorded actions
	"rbx", "rby", "rbz", "rlk", "ruf", "rplf", "rux", "ruy", "ruz", "rut", "ratk", "rlkx", "rlky", "rlkz", "rsb",
	# Played back actions
	"bbx", "bby", "bbz", "ha", "ai", "ak", "rst", "hitp", "rlt", "cbx", "cby", "cbz", "due",
)
""" Dummy objectives, all prefixed with the namespace. """

CRITERIA_OBJECTIVES: dict[str, str] = {
	"sn": "minecraft.custom:minecraft.sneak_time",
	"sw": "minecraft.custom:minecraft.swim_one_cm",
	"gl": "minecraft.custom:minecraft.aviate_one_cm",
	"use": "minecraft.used:minecraft.carrot_on_a_stick",
	"left": "minecraft.custom:minecraft.leave_game",
}
""" Statistic objectives, all prefixed with the namespace. """

PERSISTENT_SCORES: dict[str, int] = {
	"#id": 0,		# next playback entity id
	"#pid": 0,		# next player id
	"#gid": 0,		# next challenge group id
	"#gt": 0,		# game tick counter
	"#pend": 0,		# a group waits for its first cycle
	"#vs": 0,		# next free block slot in the vault
	"#cs": 0,		# next free 3x3x3 cube in the vault
	"#npulse": 0,	# redstone pulses alive
	"#step": 2,		# move_every setting
}
""" Scores of `<ns>.data` that hold world state: kept on /reload, and carried over from the `<ns>.v` objective of 1.0.0. """

VAULT_CHUNKS: str = "0 0 47 15"
""" Blocks forceloaded in the survirec:vault dimension (chunks 0 to 2). """


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	objectives: str = "\n".join(f"scoreboard objectives add {ns}.{name} dummy" for name in DUMMY_OBJECTIVES)
	criteria: str = "\n".join(f"scoreboard objectives add {ns}.{name} {criterion}" for name, criterion in CRITERIA_OBJECTIVES.items())
	migrate: str = "\n".join(
		f"execute unless score {name} {ns}.data = {name} {ns}.data if score {name} {ns}.v = {name} {ns}.v "
		f"run scoreboard players operation {name} {ns}.data = {name} {ns}.v"
		for name in PERSISTENT_SCORES
	)
	defaults: str = "\n".join(
		f"execute unless score {name} {ns}.data = {name} {ns}.data run scoreboard players set {name} {ns}.data {value}"
		for name, value in PERSISTENT_SCORES.items()
	)

	write_load_file(f"""
# Objectives
{objectives}
{criteria}

# World state written by Survirec 1.0.0 in the old {ns}.v objective (empty, then removed, on every later load)
scoreboard objectives add {ns}.v dummy
{migrate}
scoreboard objectives remove {ns}.v

# World state defaults
{defaults}
execute unless data storage {ns}:cfg r run data modify storage {ns}:cfg r set value 128
function {ns}:v{version}/menu/texture

# Hidden dimension holding the block copies
execute in {ns}:vault run forceload add {VAULT_CHUNKS}
""")

	write_tick_file(f"""
execute store result score #now {ns}.data run time query gametime
execute unless data storage {ns}:cfg vault2 run function {ns}:v{version}/vault/try
scoreboard players add #gt {ns}.data 1
execute if score #gt {ns}.data matches 1000000.. run scoreboard players set #gt {ns}.data 0

# Players: rejoin, menu item, recordings
execute as @a[scores={{{ns}.left=1..}}] run function {ns}:v{version}/record/rejoin
execute as @a[scores={{{ns}.use=1..}}] if items entity @s weapon.* minecraft:carrot_on_a_stick[minecraft:custom_data~{{{ns}:{{menu:1b}}}}] run function {ns}:v{version}/menu/open
execute as @a[tag={ns}.on] at @s run function {ns}:v{version}/record/tick

# Every 10 ticks: players near the entities, armed recordings
scoreboard players operation #g {ns}.data = #gt {ns}.data
scoreboard players operation #g {ns}.data %= #10 {ns}.data
execute if score #g {ns}.data matches 0 run function {ns}:v{version}/near with storage {ns}:cfg
execute if score #g {ns}.data matches 0 as @a[tag={ns}.armed] run function {ns}:v{version}/challenge/armchk

# Every 4 ticks: per playback range
scoreboard players operation #h {ns}.data = #gt {ns}.data
scoreboard players operation #h {ns}.data %= #4 {ns}.data
execute if score #h {ns}.data matches 0 as @e[tag={ns}.m,tag={ns}.rg] at @s run function {ns}:v{version}/rngchk

# Every 5 ticks: start markers of the recordings
scoreboard players operation #q5 {ns}.data = #gt {ns}.data
scoreboard players operation #q5 {ns}.data %= #5 {ns}.data
execute if score #q5 {ns}.data matches 0 as @e[type=minecraft:text_display,tag={ns}.start] at @s run function {ns}:v{version}/record/marker

# Playback
execute if score #npulse {ns}.data matches 1.. as @e[type=minecraft:marker,tag={ns}.pulse] if score #now {ns}.data >= @s {ns}.due at @s run function {ns}:v{version}/playback/pulseoff
execute as @e[tag={ns}.m] run function {ns}:v{version}/playback/tick
execute if score #pend {ns}.data matches 1 run function {ns}:v{version}/playback/grpfire
""")

	write_unload_file(f"""
# Hidden dimension holding the block copies
execute in {ns}:vault run forceload remove {VAULT_CHUNKS}
""")

""" Public entry points: the `#survirec:v<major>/...` function tags and the signals.

Every version of the library ships its own `api/<name>` function in the same function tag.
Each one starts with a version guard, so when several versions of Survirec are embedded in the
datapacks of a world, only the newest one (the one LanternLoad resolved) runs the call.
"""
# Imports
from dataclasses import dataclass

from stewbeet import Mem, write_versioned_function

from .common import PLAYBACK_FIELDS, Storages, compound, say, text
from .help_pages import PAGES

# Constants
CHALLENGE_DEFAULTS: str = '{id:"default",time:30,group:"main",sync:0,tp_back:1}'
""" Default fields of #survirec:v1/challenge (and challenge_cmd, which shows the command instead of starting it). """

SIGNALS: tuple[str, ...] = ("on_record_start", "on_record_stop", "on_spawn")
""" Function tags the library fires, so a datapack can react to a recording or a playback entity. """


@dataclass(frozen=True, slots=True)
class EntryPoint:
	""" A public function tag and the versioned function it ends in. """

	target: str
	""" Versioned function called once the options are merged and checked (ex: "record/start_from_call"). """

	defaults: str | None = None
	""" Default `with` fields as SNBT, `None` for an entry point that reads no option (called without `with`). """

	required: tuple[str, ...] = ()
	""" Fields that must hold a valid name (letters, digits, `_`). """

	optional: tuple[str, ...] = ()
	""" Fields that must hold a valid name when not empty. """

	extra: str = ""
	""" Commands run after the checks, before the target. """


def merge(ns: str, defaults: str, target: str = "options") -> str:
	""" The `with` compound of the call merged over `defaults`, in <ns>:call <target>. """
	call: str = Storages(ns).call
	return f"""$data modify storage {call} arguments set value $(with)
data modify storage {call} {target} set value {defaults}
data modify storage {call} {target} merge from storage {call} arguments"""


def check_name(ns: str, functions: str, field: str, required: bool, condition: str = "") -> str:
	""" Sets #has_bad_name to 1 when the option `field` is not a valid name (an empty optional field is valid).
	`condition`: execute subcommands both commands run behind, ex: "if data storage survirec:call options.tag ".
	"""
	run: str = f"execute {condition}run " if condition else ""
	return f"""{run}data modify storage {Storages(ns).name_check} request set value {{field:"{field}"}}
{run}function {functions}/name/check_{"required" if required else "optional"} with storage {Storages(ns).name_check} request
"""


def body(ns: str, functions: str, entry: EntryPoint) -> str:
	""" Commands of an entry point described by an EntryPoint. """
	if entry.defaults is None:
		return f"function {functions}/{entry.target}"

	content: str = f"\n{merge(ns, entry.defaults)}\n"
	if entry.required or entry.optional:
		content += f"scoreboard players set #has_bad_name {ns}.data 0\n"
		for field in entry.required:
			content += check_name(ns, functions, field, required=True)
		for field in entry.optional:
			content += check_name(ns, functions, field, required=False)
		content += f"execute if score #has_bad_name {ns}.data matches 1 run return run function {functions}/name/report_invalid\n"
	return content + f"""{entry.extra}
function {functions}/{entry.target} with storage {Storages(ns).call} options
"""


def entry_points(ns: str, functions: str, api: str) -> dict[str, EntryPoint | str]:
	""" Public function tag name -> how its call is handled (an EntryPoint, or a hand-written body). """
	call: str = Storages(ns).call
	return {
		"start":			EntryPoint("record/start_from_call", '{name:"rec",every:4,group:"",group_radius:50}', required=("name",), optional=("group",)),
		"stop":				EntryPoint("record/stop_from_call"),
		"stop_loop":		EntryPoint("record/stop_loop_from_call"),
		"abort":			EntryPoint("record/abort_from_call"),
		"play":				EntryPoint(
			"spawn/from_options",
			compound({**PLAYBACK_FIELDS, "group_id": "0", "group_loop": "0"}),
			required=("name",), optional=("tag", "group"),
			extra=f"""execute if data storage {call} options.data run function {functions}/sequence/import
execute unless data storage {call} options{{group:""}} run function {functions}/group/prepare_local
execute summon minecraft:marker run function {functions}/spawn/store_command_block_position""",
		),
		"part": f"""
{merge(ns, "{f:0,d:[],e:[],s:[],a:[]}", "part")}
function {functions}/sequence/collect_part
""",
		"challenge":		EntryPoint("challenge/start_from_call", CHALLENGE_DEFAULTS, required=("id", "group")),
		"challenge_cmd":	EntryPoint("menu/check_challenge_time", CHALLENGE_DEFAULTS, required=("id", "group")),
		"kill": f"""
{merge(ns, "{}")}
scoreboard players set #has_bad_name {ns}.data 0
{check_name(ns, functions, "tag", required=True, condition=f"if data storage {call} options.tag ")}{check_name(ns, functions, "name", required=True, condition=f"if data storage {call} options.name ")}execute if score #has_bad_name {ns}.data matches 1 run return run function {functions}/name/report_invalid
execute if data storage {call} options.tag run return run function {functions}/kill/by_tag with storage {call} options
execute if data storage {call} options.name run return run function {functions}/kill/by_name with storage {call} options
{say(text("kill demande un filtre (tag ou name). Pour tout supprimer : ", "red"), text(f"{api}/kill_all", "gold", "bold:true"))}
""",
		"kill_all":			EntryPoint("kill/all"),
		"group_restart":	EntryPoint("group/restart_from_call", '{group:"",radius:50}'),
		"forget":			EntryPoint("sequence/forget", '{name:""}', required=("name",)),
		"export":			EntryPoint("record/export_saved", '{name:""}', required=("name",)),
		"records":			EntryPoint("menu/list_records"),
		"range":			EntryPoint("range/set_global", "{r:128}"),
		"settings": f"""
$data modify storage {call} arguments set value $(with)
data modify storage {call} options set value {{range:128,move_every:2}}
data modify storage {call} options.range set from storage {ns}:config range
execute store result storage {call} options.move_every int 1 run scoreboard players get #move_every {ns}.data
data modify storage {call} options merge from storage {call} arguments
data modify storage {ns}:config range set from storage {call} options.range
execute store result score #move_every {ns}.data run data get storage {call} options.move_every
execute unless score #move_every {ns}.data matches 1..20 run scoreboard players set #move_every {ns}.data 2
{say(text("Portée : ", "green"), f'{{storage:"{ns}:config",nbt:"range",color:"gold"}}', text(" blocs · position mise à jour tous les ", "green"),
	f'{{score:{{name:"#move_every",objective:"{ns}.data"}},color:"gold"}}', text(" ticks", "green"))}
""",
		"menu": f"""
execute unless entity @s[type=minecraft:player] run return fail
dialog show @s {ns}:menu
""",
		"menu_item":		EntryPoint("menu/give_item"),
		"commands":			EntryPoint("menu/show_commands"),
		"help":				EntryPoint("help/index"),
		"help_page": f"""
{merge(ns, "{page:1}")}
execute store result score #page {ns}.data run data get storage {call} options.page
execute unless score #page {ns}.data matches 1..{len(PAGES)} run return run function {functions}/help/index
execute store result storage {call} options.page int 1 run scoreboard players get #page {ns}.data
function {functions}/help/open_page with storage {call} options
""",
		"debug":			EntryPoint("debug/show"),
		"reset":			EntryPoint("reset"),
	}


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	major, minor, patch = version.split(".")
	functions: str = f"{ns}:v{version}"
	api: str = f"#{ns}:v{major}"

	guard: str = f"\n# Only the newest {ns} loaded in the world runs the call\n"
	for part, value in (("loaded", 1), ("major", major), ("minor", minor), ("patch", patch)):
		guard += f"execute unless score #{ns}.{part} load.status matches {value} run return fail\n"

	for name, entry in entry_points(ns, functions, api).items():
		content: str = entry if isinstance(entry, str) else body(ns, functions, entry)
		write_versioned_function(f"api/{name}", guard + content, tags=[f"{ns}:v{major}/{name}"])

	# The library owns the signal tags, datapacks add their functions to them
	for signal in SIGNALS:
		write_versioned_function(f"api/signals/{signal}", """
# Placeholder so the tag always exists. Add your own function to the tag to react to the event.
""", tags=[f"{ns}:v{major}/signals/{signal}"])

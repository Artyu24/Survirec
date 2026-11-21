""" Public entry points: the `#survirec:v<major>/...` function tags and the signals.

Every version of the library ships its own `api/<name>` function in the same function tag.
Each one starts with a version guard, so when several versions of Survirec are embedded in the
datapacks of a world, only the newest one (the one LanternLoad resolved) runs the call.
"""
# Imports
from dataclasses import dataclass

from stewbeet import Mem, write_versioned_function


@dataclass(frozen=True, slots=True)
class EntryPoint:
	""" A public function tag and the versioned function it ends in. """

	target: str
	""" Versioned function called once the options are merged and checked (ex: "start"). """

	defaults: str | None = None
	""" Default `with` fields as SNBT, `None` for an entry point that reads no option (called without `with`). """

	required: tuple[str, ...] = ()
	""" Fields that must hold a valid name (letters, digits, `_`). """

	optional: tuple[str, ...] = ()
	""" Fields that must hold a valid name when not empty. """

	extra: str = ""
	""" Commands run after the checks, before the target. """


def entry_points(ns: str, version: str, major: str) -> dict[str, EntryPoint | str]:
	""" Public function tag name -> how its call is handled (an EntryPoint, or a hand-written body). """
	v: str = f"{ns}:v{version}"
	return {
		"start":			EntryPoint("start", '{name:"rec",every:4,group:"",group_radius:50}', required=("name",), optional=("group",)),
		"stop":				EntryPoint("stop"),
		"stop_loop":		EntryPoint("stop_loop"),
		"abort":			EntryPoint("abort"),
		"play":				EntryPoint(
			"again",
			'{name:"",pos:"~ ~ ~",entity:"minecraft:mannequin",range:0,size:1,loop:1,redstone:0,restore:1,hit_players:0,speed:100,delay:0,'
			'tag:"",group:"",group_radius:50,grp:0,gl:0,pose:"",skin:"",texture:"",head:"",chest:"",legs:"",feet:"",mainhand:"",offhand:""}',
			required=("name",), optional=("tag", "group"),
			extra=f"""
execute if data storage {ns}:in cfg.data run function {v}/import
execute unless data storage {ns}:in cfg{{group:""}} run function {v}/pgroup with storage {ns}:in cfg
execute summon minecraft:marker run function {v}/spawn/cbpos""",
		),
		"part": f"""
$data modify storage {ns}:in api set value $(with)
data modify storage {ns}:in cfg set value {{f:0,d:[],e:[],s:[],a:[]}}
data modify storage {ns}:in cfg merge from storage {ns}:in api
execute if data storage {ns}:in cfg{{f:1}} run data modify storage {ns}:t pend set value []
execute if data storage {ns}:in cfg{{f:1}} run data modify storage {ns}:t pend_e set value []
execute if data storage {ns}:in cfg{{f:1}} run data modify storage {ns}:t pend_s set value []
execute if data storage {ns}:in cfg{{f:1}} run data modify storage {ns}:t pend_a set value []
execute unless data storage {ns}:t pend run data modify storage {ns}:t pend set value []
execute unless data storage {ns}:t pend_e run data modify storage {ns}:t pend_e set value []
execute unless data storage {ns}:t pend_s run data modify storage {ns}:t pend_s set value []
execute unless data storage {ns}:t pend_a run data modify storage {ns}:t pend_a set value []
data modify storage {ns}:t pend append from storage {ns}:in cfg.d[]
data modify storage {ns}:t pend_e append from storage {ns}:in cfg.e[]
data modify storage {ns}:t pend_s append from storage {ns}:in cfg.s[]
data modify storage {ns}:t pend_a append from storage {ns}:in cfg.a[]
""",
		"challenge":		EntryPoint("challenge", '{id:"default",time:30,group:"main",sync:0,tp_back:1}', required=("id", "group")),
		"challenge_cmd":	EntryPoint("menu/chcmd", '{id:"default",time:30,group:"main",sync:0,tp_back:1}', required=("id", "group")),
		"kill": f"""
$data modify storage {ns}:in api set value $(with)
data modify storage {ns}:in cfg set value {{}}
data modify storage {ns}:in cfg merge from storage {ns}:in api
scoreboard players set #bad {ns}.data 0
execute if data storage {ns}:in cfg.tag run data modify storage {ns}:v q set value {{f:"tag"}}
execute if data storage {ns}:in cfg.tag run function {v}/vreq with storage {ns}:v q
execute if data storage {ns}:in cfg.name run data modify storage {ns}:v q set value {{f:"name"}}
execute if data storage {ns}:in cfg.name run function {v}/vreq with storage {ns}:v q
execute if score #bad {ns}.data matches 1 run return run function {v}/badname
execute if data storage {ns}:in cfg.tag run return run function {v}/kill with storage {ns}:in cfg
execute if data storage {ns}:in cfg.name run return run function {v}/kill_name with storage {ns}:in cfg
tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"kill demande un filtre (tag ou name). Pour tout supprimer : ",color:"red"}},{{text:"#{ns}:v{major}/kill_all",color:"gold",bold:true}}]
""",
		"kill_all":			EntryPoint("kill_all"),
		"group_restart":	EntryPoint("group_restart", '{group:"",radius:50}'),
		"forget":			EntryPoint("forget", '{name:""}', required=("name",)),
		"export":			EntryPoint("export", '{name:""}', required=("name",)),
		"records":			EntryPoint("menu/records"),
		"range":			EntryPoint("range", "{r:128}"),
		"settings": f"""
$data modify storage {ns}:in api set value $(with)
data modify storage {ns}:in cfg set value {{range:128,move_every:2}}
data modify storage {ns}:in cfg.range set from storage {ns}:cfg r
execute store result storage {ns}:in cfg.move_every int 1 run scoreboard players get #step {ns}.data
data modify storage {ns}:in cfg merge from storage {ns}:in api
data modify storage {ns}:cfg r set from storage {ns}:in cfg.range
execute store result score #step {ns}.data run data get storage {ns}:in cfg.move_every
execute unless score #step {ns}.data matches 1..20 run scoreboard players set #step {ns}.data 2
tellraw @s [{{text:"[Survirec] ",color:"gray"}},{{text:"Portée : ",color:"green"}},{{storage:"{ns}:cfg",nbt:"r",color:"gold"}},{{text:" blocs · position mise à jour tous les ",color:"green"}},{{score:{{name:"#step",objective:"{ns}.data"}},color:"gold"}},{{text:" ticks",color:"green"}}]
""",
		"menu": f"""
execute unless entity @s[type=minecraft:player] run return fail
dialog show @s {ns}:menu
""",
		"menu_item":		EntryPoint("menu/give"),
		"commands":			EntryPoint("menu/cmds"),
		"help":				EntryPoint("help"),
		"help_page": f"""
$data modify storage {ns}:in api set value $(with)
data modify storage {ns}:in cfg set value {{page:1}}
data modify storage {ns}:in cfg merge from storage {ns}:in api
execute store result score #page {ns}.data run data get storage {ns}:in cfg.page
execute unless score #page {ns}.data matches 1..{HELP_PAGES} run return run function {v}/help
execute store result storage {ns}:in cfg.page int 1 run scoreboard players get #page {ns}.data
function {v}/help/page with storage {ns}:in cfg
""",
		"debug":			EntryPoint("debug"),
		"reset":			EntryPoint("reset"),
	}


HELP_PAGES: int = 5
""" Pages of the in-game help (help/p1 to help/p<HELP_PAGES>). """

SIGNALS: tuple[str, ...] = ("on_record_start", "on_record_stop", "on_spawn")
""" Function tags the library fires, so a datapack can react to a recording or a playback entity. """


def body(ns: str, version: str, entry: EntryPoint) -> str:
	""" Commands of an entry point described by an EntryPoint. """
	v: str = f"{ns}:v{version}"
	if entry.defaults is None:
		return f"function {v}/{entry.target}"

	checks: str = ""
	if entry.required or entry.optional:
		fields: list[str] = [f"""
data modify storage {ns}:v q set value {{f:"{field}"}}
function {v}/{check} with storage {ns}:v q""" for check, names in (("vreq", entry.required), ("vopt", entry.optional)) for field in names]
		checks = f"""
scoreboard players set #bad {ns}.data 0{"".join(fields)}
execute if score #bad {ns}.data matches 1 run return run function {v}/badname"""

	return f"""
$data modify storage {ns}:in api set value $(with)
data modify storage {ns}:in cfg set value {entry.defaults}
data modify storage {ns}:in cfg merge from storage {ns}:in api{checks}{entry.extra}
function {v}/{entry.target} with storage {ns}:in cfg
"""


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	major, minor, patch = version.split(".")

	# Only the version resolved by LanternLoad (and fully loaded) answers a call
	guard: str = f"""
# Only the newest {ns} loaded in the world runs the call
execute unless score #{ns}.loaded load.status matches 1 run return fail
execute unless score #{ns}.major load.status matches {major} run return fail
execute unless score #{ns}.minor load.status matches {minor} run return fail
execute unless score #{ns}.patch load.status matches {patch} run return fail
"""
	for name, entry in entry_points(ns, version, major).items():
		content: str = entry if isinstance(entry, str) else body(ns, version, entry)
		write_versioned_function(f"api/{name}", guard + content, tags=[f"{ns}:v{major}/{name}"])

	# Signals are extension points: the library owns the tag, datapacks add their functions to it
	for signal in SIGNALS:
		write_versioned_function(f"api/signals/{signal}", """
# Placeholder so the tag always exists. Add your own function to the tag to react to the event.
""", tags=[f"{ns}:v{major}/signals/{signal}"])

	# Help page called by the public help_page entry point (its number is checked there)
	write_versioned_function("help/page", f"$function {ns}:v{version}/help/p$(page)")

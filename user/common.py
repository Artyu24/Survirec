""" Command fragments shared by the modules. Each helper returns command text (single braces), to insert in an f-string. """
# Imports
from dataclasses import dataclass

# Constants
AXES: tuple[str, ...] = ("x", "y", "z")
""" Axes, in the order of Pos[0], Pos[1], Pos[2]. """

DIMENSIONS: tuple[str, ...] = ("x", "y", "z", "yaw", "pitch")
""" Position (thousandths of a block) and rotation (hundredths of a degree): suffix of the objectives and fake players holding them. """

TELEPORT_SCALES: dict[str, str] = {"x": "0.001", "y": "0.001", "z": "0.001", "yaw": "0.01", "pitch": "0.01"}
""" Dimension -> scale back to blocks or degrees, for the macro arguments of playback/teleport. """

PLAYBACK_FIELDS: dict[str, str] = {
	"name": '""', "pos": '"~ ~ ~"', "entity": '"minecraft:mannequin"', "range": "0", "size": "1", "loop": "1",
	"redstone": "0", "restore": "1", "hit_players": "0", "speed": "100", "delay": "0", "tag": '""', "group": '""', "group_radius": "50",
	"pose": '""', "skin": '""', "texture": '""', "head": '""', "chest": '""', "legs": '""', "feet": '""', "mainhand": '""', "offhand": '""',
}
""" Public fields of #survirec:v1/play and their defaults (SNBT), in the order of the copied playback command. """

EQUIPMENT_FIELDS: dict[str, str] = {
	"head": "armor.head", "chest": "armor.chest", "legs": "armor.legs", "feet": "armor.feet", "mainhand": "weapon.mainhand", "offhand": "weapon.offhand",
}
""" Equipment playback field -> slot of the entity. """

ARMED: str = "Enregistrement armé : il démarre au prochain cycle du groupe."
NOT_RECORDING: str = "Tu n'as aucun enregistrement en cours."


@dataclass(frozen=True, slots=True)
class Storages:
	""" Storage names of the library (namespace included). """

	ns: str

	@property
	def playback(self) -> str:
		""" Scratch of the playback entities: current event, block copy, release, pulse, keyframe. """
		return f"{self.ns}:playback"

	@property
	def recording(self) -> str:
		""" Scratch of a recording being stopped, saved or exported. """
		return f"{self.ns}:recording"

	@property
	def call(self) -> str:
		""" Arguments of the current entry point call: arguments, options, spawn settings. """
		return f"{self.ns}:call"

	@property
	def name_check(self) -> str:
		return f"{self.ns}:name_check"

	@property
	def block(self) -> str:
		""" Block read by block/read: id and state. """
		return f"{self.ns}:block"

	@property
	def recorder(self) -> str:
		""" pid of the recording player, the macro argument of the functions reading <ns>:rec p.p<pid>. """
		return f"{self.ns}:recorder"

	@property
	def challenge(self) -> str:
		""" Settings of the challenge being started, kept in <ns>:rec p.p<pid>.c. """
		return f"{self.ns}:challenge"

	@property
	def challenge_call(self) -> str:
		return f"{self.ns}:challenge_call"

	@property
	def import_parts(self) -> str:
		""" Lists collecting the parts of a long sequence, one command block after the other. """
		return f"{self.ns}:import"


def compound(fields: dict[str, str]) -> str:
	""" SNBT compound from field -> SNBT value. """
	return "{" + ",".join(f"{key}:{value}" for key, value in fields.items()) + "}"


def wrap_yaw(score: str) -> str:
	""" Keep a yaw delta in -180..180 degrees (hundredths). `score`: holder and objective, ex: "#delta_yaw survirec.data". """
	return f"""execute if score {score} matches 18001.. run scoreboard players remove {score} 36000
execute if score {score} matches ..-18001 run scoreboard players add {score} 36000"""


def store_position(path: str) -> str:
	""" Block position of @s into the storage keys `<path>x`, `<path>y` and `<path>z` (ex: "survirec:playback release."). """
	content: str = ""
	for index, axis in enumerate(AXES):
		content += f"execute store result storage {path}{axis} int 1 run data get entity @s Pos[{index}]\n"
	return content.rstrip("\n")


def kill_tagged(ns: str, functions: str, tag: str) -> str:
	""" Remove the playback entities with `tag` (macro arguments allowed), putting their world back unless restore:0. """
	return f"""
scoreboard players set #restore_on_kill {ns}.data 1
$execute as @e[tag={tag}] run function {functions}/playback/delete
scoreboard players set #restore_on_kill {ns}.data 0
"""


def build_sequence(ns: str) -> str:
	""" <ns>:recording sequence: the playable sequence of the recording in <ns>:recording, keyframes in <ns>:recording keyframes. """
	recording: str = Storages(ns).recording
	content: str = f"data modify storage {recording} sequence set value {{}}\n"
	for key, info in (("n", "keyframe_step"), ("y", "yaw"), ("p", "pitch")):
		content += f"data modify storage {recording} sequence.{key} set from storage {recording} meta.{info}\n"
	for key in "esa":
		content += f"data modify storage {recording} sequence.{key} set from storage {recording} {key}\n"
	return content + f"data modify storage {recording} sequence.d set from storage {recording} keyframes"


def check_group_alive(ns: str) -> str:
	""" #group_alive 1 when an entity of the group #waited_group still plays. """
	return f"""scoreboard players set #group_alive {ns}.data 0
execute as @e[tag={ns}.instance] if score @s {ns}.group_id = #waited_group {ns}.data run scoreboard players set #group_alive {ns}.data 1"""


## Text components
def quoted(value: str) -> str:
	""" SNBT string: double quotes, single quotes when the value holds double quotes. """
	return f"'{value}'" if '"' in value else f'"{value}"'


def text(content: str, color: str = "", extra: str = "") -> str:
	""" Text component. `extra`: more fields, ex: "bold:true". """
	fields: list[str] = [f"text:{quoted(content)}"]
	if color:
		fields.append(f'color:"{color}"')
	if extra:
		fields.append(extra)
	return "{" + ",".join(fields) + "}"


def tooltip(value: str, always_single_quotes: bool = False) -> str:
	return f"hover_event:{{action:\"show_text\",value:{f"'{value}'" if always_single_quotes else quoted(value)}}}"


def run(label: str, command: str, color: str, hover: str, extra: str = "", action: str = "run_command") -> str:
	""" Clickable text running (or suggesting) a command: a public function tag, never a versioned function. """
	click: str = f"click_event:{{action:\"{action}\",command:{quoted(command)}}}"
	return text(label, color, ",".join(field for field in (extra, click, tooltip(hover)) if field))


def copy(label: str, value: str, hover: str = "", color: str = "yellow", extra: str = "") -> str:
	""" Clickable text copying a command; the tooltip shows the command when `hover` is empty.
	Always single quotes: macro arguments put double quotes in the command.
	"""
	click: str = f"click_event:{{action:\"copy_to_clipboard\",value:'{value}'}}"
	return text(label, color, ",".join(field for field in (extra, click, tooltip(hover or value, always_single_quotes=not hover)) if field))


PREFIX: str = text("[Survirec] ", "gray")
""" Start of every chat message of the library. """

SEPARATOR: str = f"tellraw @s {text('-' * 48, 'dark_gray')}"
""" Line around a group of chat messages. """


def say(*components: str) -> str:
	""" Chat message to @s, after the Survirec prefix. """
	return f"tellraw @s [{','.join((PREFIX, *components))}]"


def info(message: str, color: str = "green") -> str:
	""" One-color chat message to @s. """
	return say(text(message, color))


def timer(ns: str, head: str, style: str) -> str:
	""" Action bar `head` then #seconds ticks as m:ss (divided by 20 here). `style`: fields of the digits, ex: 'color:"yellow"'. """
	def digits(holder: str) -> str:
		return f'{{score:{{name:"{holder}",objective:"{ns}.data"}},{style}}}'
	content: str = f"""scoreboard players operation #seconds {ns}.data /= #20 {ns}.data
scoreboard players operation #minutes {ns}.data = #seconds {ns}.data
scoreboard players operation #minutes {ns}.data /= #60 {ns}.data
scoreboard players operation #seconds {ns}.data %= #60 {ns}.data
"""
	for seconds, colon in (("10..", ":"), ("..9", ":0")):
		content += f'execute if score #seconds {ns}.data matches {seconds} run title @s actionbar [{head},{digits("#minutes")},{{text:"{colon}",{style}}},{digits("#seconds")}]\n'
	return content.rstrip("\n")

""" Copies of the blocks changed by entities, kept in the survirec:vault dimension. """
# Imports
from stewbeet import Mem, write_versioned_function

# Constants
CAGE_LAYERS: tuple[tuple[int, int], ...] = ((-64, 31), (32, 127), (128, 223), (224, 319))
""" Height ranges filled one by one (a single fill is limited to 32768 blocks). """


def cage(ns: str, chunk: int) -> str:
	""" Fill a vault chunk with barriers: every copy is isolated (no fall, no flow, no update between copies). """
	x: int = chunk * 16
	return "\n".join(f"execute in {ns}:vault run fill {x} {y1} 0 {x + 15} {y2} 15 minecraft:barrier strict" for y1, y2 in CAGE_LAYERS)


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("vault/bk", f"""
# positionné sur le bloc, en tant qu'entité. {ns}:t bka = {{x,y,z,m}} (m = "strict" ou "replace" pour la remise en place)
# Une seule copie par bloc : celle d'origine. Elle sert à chaque remise en place, on ne la refait jamais.
execute unless score @s {ns}.rst matches 1.. run return 0
execute unless data storage {ns}:cfg vault run return 0
execute store result storage {ns}:t bka.id int 1 run scoreboard players get @s {ns}.id
scoreboard players set #has {ns}.data 0
function {ns}:v{version}/vault/has with storage {ns}:t bka
execute if score #has {ns}.data matches 1 run return 0
execute if data storage {ns}:cfg vfree[0] run return run function {ns}:v{version}/vault/reuse
scoreboard players operation #c7 {ns}.data = #vs {ns}.data
scoreboard players operation #c7 {ns}.data %= #7 {ns}.data
scoreboard players operation #c7 {ns}.data *= #2 {ns}.data
execute store result storage {ns}:t bka.vx int 1 run scoreboard players add #c7 {ns}.data 1
scoreboard players operation #c7 {ns}.data = #vs {ns}.data
scoreboard players operation #c7 {ns}.data /= #7 {ns}.data
scoreboard players operation #c7 {ns}.data %= #7 {ns}.data
scoreboard players operation #c7 {ns}.data *= #2 {ns}.data
execute store result storage {ns}:t bka.vz int 1 run scoreboard players add #c7 {ns}.data 1
scoreboard players operation #c7 {ns}.data = #vs {ns}.data
scoreboard players operation #c7 {ns}.data /= #49 {ns}.data
scoreboard players operation #c7 {ns}.data *= #2 {ns}.data
execute store result storage {ns}:t bka.vy int 1 run scoreboard players remove #c7 {ns}.data 63
scoreboard players add #vs {ns}.data 1
execute if score #vs {ns}.data matches 9359.. run scoreboard players set #vs {ns}.data 0
function {ns}:v{version}/vault/bk2 with storage {ns}:t bka
""")

	write_versioned_function("vault/bk2", f"""
$clone $(x) $(y) $(z) $(x) $(y) $(z) to {ns}:vault $(vx) $(vy) $(vz) strict
$data modify storage {ns}:inst i$(id).bk append from storage {ns}:t bka
""")

	write_versioned_function("vault/free", f"""
# l'entité disparaît : ses emplacements redeviennent des barrières et sont réutilisables
execute store result storage {ns}:t rv.id int 1 run scoreboard players get @s {ns}.id
function {ns}:v{version}/vault/rs0 with storage {ns}:t rv
execute if data storage {ns}:t bkl[0] run function {ns}:v{version}/vault/free1
""")

	write_versioned_function("vault/free1", f"""
function {ns}:v{version}/vault/free2 with storage {ns}:t bkl[-1]
data remove storage {ns}:t bkl[-1]
execute if data storage {ns}:t bkl[0] run function {ns}:v{version}/vault/free1
""")

	write_versioned_function("vault/free2", f"""
$execute in {ns}:vault run setblock $(vx) $(vy) $(vz) minecraft:barrier strict
$data modify storage {ns}:cfg vfree append value {{vx:$(vx),vy:$(vy),vz:$(vz)}}
""")

	write_versioned_function("vault/has", f"""
$execute if data storage {ns}:inst i$(id).bk[{{x:$(x),y:$(y),z:$(z)}}] run scoreboard players set #has {ns}.data 1
""")

	write_versioned_function("vault/here", f"""
# sauvegarde le bloc courant ; #bkm 1 = remise en place sans mise à jour (blocs doubles)
data modify storage {ns}:t bka set value {{x:0,y:0,z:0,m:"replace"}}
execute if score #bkm {ns}.data matches 1 run data modify storage {ns}:t bka.m set value "strict"
execute summon minecraft:marker run function {ns}:v{version}/vault/herepos
function {ns}:v{version}/vault/bk
""")

	write_versioned_function("vault/herepos", f"""
execute store result storage {ns}:t bka.x int 1 run data get entity @s Pos[0]
execute store result storage {ns}:t bka.y int 1 run data get entity @s Pos[1]
execute store result storage {ns}:t bka.z int 1 run data get entity @s Pos[2]
kill @s
""")

	write_versioned_function("vault/prep", f"""
# cage de barrières : chaque copie est isolée (ni chute, ni écoulement, ni mise à jour entre copies)
{cage(ns, 0)}
data modify storage {ns}:cfg vault set value 1b
""")

	write_versioned_function("vault/prep2", f"""
{cage(ns, 1)}
{cage(ns, 2)}
data modify storage {ns}:cfg vault2 set value 1b
""")

	write_versioned_function("vault/restore", f"""
# remet en place, dans l'ordre inverse, les blocs modifiés par cette entité
execute store result storage {ns}:t rv.id int 1 run scoreboard players get @s {ns}.id
function {ns}:v{version}/vault/rs0 with storage {ns}:t rv
execute if data storage {ns}:t bkl[0] at @s run function {ns}:v{version}/vault/rs1
""")

	write_versioned_function("vault/reuse", f"""
# emplacement libéré par une entité disparue
data modify storage {ns}:t bka.vx set from storage {ns}:cfg vfree[-1].vx
data modify storage {ns}:t bka.vy set from storage {ns}:cfg vfree[-1].vy
data modify storage {ns}:t bka.vz set from storage {ns}:cfg vfree[-1].vz
data remove storage {ns}:cfg vfree[-1]
function {ns}:v{version}/vault/bk2 with storage {ns}:t bka
""")

	write_versioned_function("vault/rs0", f"""
data modify storage {ns}:t bkl set value []
$data modify storage {ns}:t bkl set from storage {ns}:inst i$(id).bk
""")

	write_versioned_function("vault/rs1", f"""
function {ns}:v{version}/vault/rs2 with storage {ns}:t bkl[-1]
data remove storage {ns}:t bkl[-1]
execute if data storage {ns}:t bkl[0] run function {ns}:v{version}/vault/rs1
""")

	write_versioned_function("vault/rs2", f"""
$clone from {ns}:vault $(vx) $(vy) $(vz) $(vx) $(vy) $(vz) $(x) $(y) $(z) $(m)
""")

	write_versioned_function("vault/try", f"""
execute unless data storage {ns}:cfg vault in {ns}:vault if loaded 0 0 0 run function {ns}:v{version}/vault/prep
execute unless data storage {ns}:cfg vault2 in {ns}:vault if loaded 16 0 0 if loaded 32 0 0 run function {ns}:v{version}/vault/prep2
""")

	write_versioned_function("vault/wipe", f"""
{cage(ns, 0)}
data modify storage {ns}:cfg vfree set value []
scoreboard players set #vs {ns}.data 0
""")

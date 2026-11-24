# 🎬 Survirec

A vanilla datapack library that **records a player's movements and replays them with a mannequin** (or any other entity: a mob, or an item, block or text display).
No mods, no resource pack: only commands.

- 🎥 Records walking, sprinting, jumping, sneaking, swimming, elytra flight, equipment changes and arm swings.
- 🧱 Records **actions** too: hitting entities, pressing buttons and levers, opening doors, trapdoors and fence gates, placing and breaking blocks. The world can be put back as it was at every loop.
- 🔁 Replays the movement in a loop, interpolated between keyframes (one keyframe every `N` ticks, so sequences stay small).
- 🧍 Mannequin by default, but any mob or display entity works. Per-playback skin, texture, size, speed, delay, pose and equipment overrides.
- 📋 The sequence is copied into **one command block command** (long ones are split in a command block chain): no file to move around.
- 🏁 **Challenge mode**: a player (even in adventure) is recorded for `X` seconds, then a double with their skin replays the run in a loop. Several recordings can be synchronized in a group.
- ⚡ Cheap playback: scores and one `tp` macro per entity and tick. Stationary entities are not teleported, and entities with no player nearby are paused.
- 🧩 Follows the [Smithed conventions](https://docs.smithed.dev/conventions/).

📦 **Embedded library**: package it inside your datapack rather than shipping it separately. Several datapacks can embed different versions of Survirec in the same world: only the newest one runs (see Conventions).
Developed for Minecraft Java **26.2**. Depends on [Bookshelf Block](https://docs.mcbookshelf.dev/en/latest/modules/block.html) (`bs.block`), already included in `Survirec_datapack_with_libs.zip`.

Made by **Artyu24**.

# ⚡ Quick start

Everything goes through the **function tags** `#survirec:v1/...`. Each one takes a single `with` compound, and every field inside is optional.

```
function #survirec:v1/start {with:{name:"walk",every:4}}
```

You get a stop item (right-click to stop, sneak + right-click to also walk back to the start) and red buttons in the chat.
When the recording ends, click the **yellow button** in the chat to copy the playback command, then paste it in a command block.
Run `function #survirec:v1/help` (as a player) for the in-game help, one dialog per topic with copy buttons.

## Entry points

| Function tag                | `with` fields (defaults)                                                         |
| --------------------------- | -------------------------------------------------------------------------------- |
| `#survirec:v1/start`        | `name` (`"rec"`), `every` (`4`), `group` (`""`), `group_radius` (`50`). Run as the player to record |
| `#survirec:v1/stop`         | none. Run by a player: stops their recording. Run by a command block: stops all of them |
| `#survirec:v1/stop_loop`    | none. Stops and walks back to the start point                                    |
| `#survirec:v1/abort`        | none. Run by a player: cancels their recording. Run by a command block: cancels all of them |
| `#survirec:v1/play`         | `name`, plus the playback fields below. Optional `data` to import a sequence     |
| `#survirec:v1/part`         | `f`, `d`. One part of a long sequence (chain of command blocks)                  |
| `#survirec:v1/challenge_cmd`| Same fields as `challenge`. Shows a button that copies the challenge command for a command block (used by the menu) |
| `#survirec:v1/challenge`    | `id` (`"default"`), `time` (`30`), `group` (`"main"`), `sync` (`0`), `tp_back` (`1`). Run as the player |
| `#survirec:v1/kill`         | `tag` or `name` (one is required). Use `kill_all` to remove everything            |
| `#survirec:v1/kill_all`     | none                                                                             |
| `#survirec:v1/group_restart`| `group`, `radius` (`50`). Restarts the nearest scene of that group; `radius:0` restarts every scene of that name |
| `#survirec:v1/forget`       | `name`. Deletes the stored sequence                                              |
| `#survirec:v1/range`        | `r` (`128`). Animation range in blocks                                           |
| `#survirec:v1/settings`     | `range` (`128`), `move_every` (`2`). Missing fields keep their value. See Performance |
| `#survirec:v1/help`         | none. Opens the help dialog (run as a player)                                    |
| `#survirec:v1/help_page`    | `page` (`1`). Opens one page of the help dialog (`1` to `5`)                     |
| `#survirec:v1/reset`        | none. Cancels every recording and clears the recording data                      |
| `#survirec:v1/debug`        | none. Lists the animated entities                                                |
| `#survirec:v1/menu`         | none. Opens the Survirec menu (run as a player)                                  |
| `#survirec:v1/menu_item`    | none. Gives the menu item to the player who runs it                              |
| `#survirec:v1/records`      | none. Lists your saved recordings in the chat                                    |
| `#survirec:v1/commands`     | none. Shows the useful commands with copy buttons                                |
| `#survirec:v1/export`       | `name`. Shows the copy buttons of a saved recording again                        |

```
execute as @p run function #survirec:v1/start {with:{name:"walk",every:4}}
execute positioned 10 64 10 run function #survirec:v1/play {with:{name:"walk",loop:1,speed:150}}
execute as @p run function #survirec:v1/challenge {with:{id:"a",time:5,group:"room1"}}
function #survirec:v1/kill {with:{tag:"door"}}
```

Following an NPC that stops when you get more than 5 blocks away: `function #survirec:v1/play {with:{name:"npc",range:5}}`.

Only the `#survirec:v1/...` function tags are public. Everything under `survirec:v<version>/` (for example `survirec:v1.2.0/`) is internal and changes with every version.

## Menu

```
execute as @p run function #survirec:v1/menu_item
```

Gives the **Survirec** item. Right-click it to open a menu: start a recording, prepare a challenge command (any duration, copied for a command block), stop or cancel it, list your recordings (play one where you stand, copy its command again, delete it), get the useful commands to copy, open the in-game help or this README.
The menu is also in the pause screen, under the Smithed *Data Packs* list.

Every finished recording is kept in the world under its name: `#survirec:v1/play {with:{name:"walk"}}` replays it without the copied data.

The item is a camera head ([minecraft-heads.com](https://minecraft-heads.com), Custom Head ID 120246). To use another head, paste its base64 `textures` value in `MENU_HEAD_TEXTURE` (`user/menu.py`) and rebuild (empty = spyglass look).

> The menu and every chat button run `/function`, so they only work for operators. A non-operator who gets the item can open the menu but no button does anything.

> Dialogs are only loaded when the world or server starts: after updating the datapack, restart instead of `/reload`.

## Playback fields

The command copied after a recording starts with these fields. Edit them before running the command block.
Its last command block has one copy button per kind of entity, holding only the fields that entity uses: **Mannequin**, **Mob** (`minecraft:zombie`, to replace with the mob you want), **Objet** (`item_display`), **Bloc** (`block_display`) and **Texte** (`text_display`). Every field still works in any command: a missing field takes its default.

| Field                                  | Meaning                                                                 |
| -------------------------------------- | ----------------------------------------------------------------------- |
| `name`                                 | Sequence name (letters, digits, `_`)                                    |
| `pos`                                  | Where the entity appears. Default: where you started recording. `"~ ~ ~"` is the **center** of the command block, `"~ ~-0.5 ~"` the floor it stands on |
| `entity`                               | `minecraft:mannequin` (default), any mob, or `minecraft:item_display`, `block_display`, `text_display` |
| `nbt`                                  | Entity NBT merged when it appears, as in a `/summon`: `{IsBaby:1b}`, `{Glowing:1b}`, `{item:{id:"minecraft:diamond_sword"}}`... Merged last, so it wins over the other fields, except `Tags` which is ignored. Default `{}` |
| `size`                                 | Scale. `1` normal, `0.5` half, `2` double (`transformation` on a display) |
| `loop`                                 | `1` loop, `0` play once and stay, `2` play once and disappear (no death animation, nothing dropped) |
| `redstone`                             | `1`: at the end of every loop, a redstone block is placed 2 blocks above the command block that started the playback (one block gap, so it does not power the launching command block again), and removed 4 ticks later (a pulse, so a command block placed right next to it fires every time). Nothing is placed if that spot is not empty. With a `group`, at the end of every group cycle. Default `0` |
| `restore`                              | World restoring: `1` at every new loop (default), `2` also when the entity ends (`loop` 0 or 2), `0` never. `kill` restores too unless `0` |
| `hit_players`                          | `1`: the entity's hits also damage players (default `0`). Mannequin and mobs |
| `speed`                                | Percent. `100` normal                                                   |
| `delay`                                | Start delay in ticks, to desynchronize several entities                 |
| `range`                                | Pause distance in blocks for this playback: the entity only moves while a player is within `range` blocks of it. `0` (default) uses the global range (`#survirec:v1/range`, 128 by default) |
| `tag`                                  | Triggering the block again replaces the entity with this tag. The tag is global to the world: use a unique one per build, otherwise two copies of a build erase each other's entities |
| `group`                                | Group name. Entities of the same group start and finish together (see below). `loop` then applies to the whole group |
| `group_radius`                         | Distance (blocks, default `50`) within which an entity joins an existing group of the same name |
| `pose`                                 | Mannequin only. Empty keeps the recorded poses. Otherwise forced: `standing`, `crouching`, `swimming`, `sleeping`, `fall_flying` |
| `skin`                                 | Player name (mannequin only)                                            |
| `texture`                              | Base64 `textures` property value, used if `skin` is empty (mannequin only) |
| `head` `chest` `legs` `feet` `mainhand` `offhand` | Item overrides. Empty keeps the recorded equipment. Mannequin and mobs |
| `data`                                 | The recorded sequence (`f`, `n`, `y`, `p`, `d`, `e`, `s`, `a`). Do not edit |

### Display entities

An `item_display`, `block_display` or `text_display` shows what its `nbt` says (`item`, `block_state`, `text`). Survirec also sets, before merging `nbt`:
- `teleport_duration` to `move_every`, so the display glides between two moves like a mob.
- `transformation` from `size`, and for a `block_display` a translation that centers the block on its position.

A `transformation` in `nbt` replaces these. Displays follow the recorded rotation, pitch included, unless their `billboard` says otherwise; swings, poses and equipment do nothing on them.

## Challenge groups

Every double belongs to a group (`main` by default). Doubles of the same player and group start and finish together:
a shorter double stays frozen on its last position until the longest one is done, then all of them walk back to their start point (2 seconds) and start again together.
Triggering a challenge again removes the player's previous double for that `id` and records a new one.
When the time is up, the player is teleported back to where the recording started, facing the same way (`tp_back:1`, default). With `tp_back:0`, they stay where they are.
Several players can record at the same time, each one their own sequence or challenge.

### Recording in sync with a group

With `sync:1`, the recording does not start immediately: it is *armed*, and starts exactly when the doubles of the group start a new cycle.
Record a second take while the first one plays, then both start together on every cycle:

```
execute as @p run function #survirec:v1/challenge {with:{id:"a",time:10,group:"scene1"}}
execute as @p run function #survirec:v1/challenge {with:{id:"b",time:10,group:"scene1",sync:1}}
```

If the group has no double yet, the recording starts at once. `#survirec:v1/abort` cancels an armed recording.

## Actions

While recording, Survirec also notes what you do to the world. During playback, the entity does it again at the same moment and at the same place (relative to its start point):

| Action | Recorded when | Played back as |
| ------ | ------------- | -------------- |
| Hit | You hit an entity | Every entity just in front of the entity takes the damage of a player holding the same weapon (fist `1`, diamond sword `7`...), with knockback. Players only with `hit_players:1` |
| Interact | You right-click a button, a lever, a door (not iron), a trapdoor (not iron) or a fence gate | The block is pressed or toggled, so redstone reacts, including through the block the button or lever is attached to (a command block behind it works). Buttons are released after 1 s (stone) or 1.5 s (wood) |
| Place | You place a block | The same block, with its orientation (doors and beds: both halves) |
| Break | A block you look at disappears | The block is broken with its particles and sound; nothing is dropped |

Pressure plates and tripwires need nothing: the entity walking on them triggers them.

**World restoring.** Before changing a block, the entity copies it into a hidden dimension of the pack (`survirec:vault`, a void world no player can reach). With `restore:1`, every copied block is put back at the start of each loop, in reverse order, so each loop starts from the same world. Only the blocks the entity changed itself are restored: blocks pushed by a piston, flowing water, mobs killed... are not.

Each entity copies a block only once, the first time it changes it: the same copy is used at every loop, so the hidden dimension does not grow while scenes loop. The copies of an entity are freed when it disappears, and `#survirec:v1/kill_all` resets the whole area.

**While recording**, your own changes are undone as soon as the recording ends or is interrupted (stop, cancel, disconnection, `reset`): the entity is the one doing them on playback. Survirec keeps a copy of the 3x3x3 blocks you are looking at, so it knows what was there before you broke, placed or used something.

> The dimension is only created when the world or server starts: after installing or updating the datapack, restart instead of `/reload`.

Limits: hits in the air and blocks broken while not looking at them are not recorded. Enchantments and attack cooldown are not taken into account. Blocks and their full state are read with Bookshelf's block module, so every block of the game version can be placed back.

## Groups for classic playback

Challenge groups belong to one player. Classic playbacks (`#survirec:v1/play`) use **local** groups: a group is a name *and* a place.

```
function #survirec:v1/play {with:{name:"a",group:"scene1"}}
function #survirec:v1/play {with:{name:"b",group:"scene1"}}
```

When an entity appears, it joins the nearest group of the same name within `group_radius` blocks (50 by default). If there is none, it starts a new group.
So the same scene pasted at two places far apart gives two independent groups, with the same command blocks. Raise `group_radius` for scenes larger than 50 blocks, and keep two copies of a scene more than `group_radius` apart.

Entities of the same group wait for the longest one. What happens next depends on `loop`:

| `loop` | When all the entities of the group have finished                                  |
| ------ | --------------------------------------------------------------------------------- |
| `1`    | They walk back to their start point (2 seconds) and start again together (default) |
| `0`    | They stay frozen on their last position                                           |
| `2`    | They disappear                                                                    |

Entities of a group that are created in the same tick (for example by command blocks triggered together) start together. One created later waits for the next cycle (for a group that does not loop, until `group_restart`).

`#survirec:v1/group_restart {with:{group:"scene1"}}` restarts the nearest `scene1` (within `radius`, 50 by default) at any time, for example to replay a group that does not loop.

To record a new take in sync with a group, give `group` to `#survirec:v1/start`:

```
function #survirec:v1/start {with:{name:"b",every:4,group:"scene1"}}
```

The recording joins the nearest `scene1` within `group_radius` blocks of the player, is armed, and starts when that group starts a new cycle. If there is no such group nearby, it starts at once. `#survirec:v1/abort` cancels it.

## Permissions

Only operators can use Survirec: every entry point is a `/function`, and the datapack has no `/trigger`.
Non-operators can only take part in a **challenge started by a command block** (button or pressure plate with `execute as @p run function #survirec:v1/challenge {...}`). A challenge cannot be stopped or cancelled by the player.

# 📡 Signals

Add your own function to these function tags.

| Tag                                      | When                                            | Runs as                                   |
| ---------------------------------------- | ----------------------------------------------- | ----------------------------------------- |
| `#survirec:v1/signals/on_record_start`   | A recording (or challenge) has just started     | the player being recorded (the real player, not the mannequin) |
| `#survirec:v1/signals/on_record_stop`    | A recording has ended                           | the player who was recorded. When a player leaves during a recording, it is sent when they come back |
| `#survirec:v1/signals/on_spawn`          | A playback entity has just been created         | the new entity (the mannequin)            |

# 🗂️ Sequence format

Sequences live in the storage `survirec:data`, under `seqs.<name>`. A datapack can ship its own in its load function:

```
data modify storage survirec:data seqs.walk set value {n:4,y:0,p:0,d:[[120,0,-340,500,0,0]],e:[],s:[]}
```

| Key | Meaning |
| --- | ------- |
| `n` | Ticks between two keyframes |
| `y` / `p` | Start yaw / pitch, in hundredths of a degree |
| `d` | Keyframes `[dx,dy,dz,dyaw,dpitch,flags]`: deltas from the previous keyframe, in thousandths of a block and hundredths of a degree. `flags`: `1` sneaking, `2` swimming, `4` gliding |
| `e` | Equipment events `{k:<keyframe index>,v:{<equipment>}}` |
| `s` | Ticks at which an arm swing happened |
| `a` | Actions `{t:<tick>,k:<kind>}`. `k`: `1` hit, `2` use, `3` place, `4` break. Except hits, `x` `y` `z` give the block relative to the start block; a place also has `b` (the block with its state) and, for a door or a bed, `p` (the other half) |

Then play it with `#survirec:v1/play {with:{name:"walk"}}`.

# 🧩 Conventions

- **Namespacing**: every function, tag, score, team and storage is prefixed with `survirec`.
- **Versioning**: every function and advancement lives under `survirec:v<version>/` (for example `survirec:v1.2.0/`), so two versions never overwrite each other's files. The public entry points are the `#survirec:v1/...` function tags (major version only): each version adds its own `survirec:v<version>/api/<name>` to them, behind a version guard. A future `v2` can live next to it without breaking `v1` users.
- **Pack ID and loading**: `pack.mcmeta` (with `"id": "survirec"`) and the versioned load ([LanternLoad](https://github.com/LanternMC/load)) are generated by StewBeet from `beet.yml`. When several datapacks embed Survirec, the `enumerate` / `resolve` tags elect the newest version: only that one loads, ticks, answers the `#survirec:v1/...` tags and records the actions (its advancements check the version too).
- **Dependencies**: StewBeet finds the `#bs.block:` calls, checks the Bookshelf Block version at load (with a clickable message when it is missing) and welds the module into `Survirec_datapack_with_libs.zip`.
- **Pack enabled tags** (`#survirec:installed`, `#survirec:major`...): generated by StewBeet from Minecraft 26.3, where the registry they need exists.
- **Data pack menu dialog**: `survirec:about` is listed in `#smithed:data_packs` (pause screen), with `required: false`.
- **Tag specification**: spawned entities carry `smithed.entity` and `smithed.strict`; the stop item carries `{smithed:{ignore:{everything:1b}}}`, the menu item `{smithed:{ignore:{functionality:1b,crafting:1b}}}`.

# ⚡ Performance

Cost of an entity while it plays, per tick: a few scoreboard operations, and one teleport every `move_every` ticks (`2` by default). Entities take turns, so only half of them move on a given tick. Swings, actions and timing stay exact to the tick: only the visible position is updated less often, and the client smooths the movement in between. `move_every:1` is the smoothest, `3` or `4` the lightest.

| Entity state | Cost |
| ------------ | ---- |
| Playing, a player within `range` | Full cost (above) |
| Paused (no player within `range`), frozen (`loop:0`) or waiting for its group | Almost nothing: 3 checks per tick |
| Standing still in its sequence | No teleport |

**How many?** It depends on the server's hardware, so measure it: run `/tick query` (it shows the average milliseconds per tick, `mspt`), add entities, and stay under about 40 mspt (50 = lag). As a rough order of magnitude, a few hundred entities playing near players at the same time, and many more paused far from players. Beyond the server, every mannequin is a player model to draw: the players' frame rate often becomes the limit first when hundreds are on screen.

To go further: lower `range` so that only the entities near players play, raise `move_every`, and prefer `every:4` or more when recording (fewer keyframes to read).

# 🔍 Notes

- **Names** (`name`, `id`, `group`, `tag`): letters, digits and `_` only, 1 to 32 characters. Anything else is refused with a message.
- **One recording per player**: every player has their own recording state, so several players can record at the same time. A player who is already recording or armed is refused (a challenge pressure plate is silently ignored).
- **Leaving during a recording**: the recording is cancelled when the player comes back.
- Equipment names, lore, book contents and custom data are not recorded: they are invisible on a playback entity, and quotes in them would break the copied command.
- A long recording is exported in several commands (300 keyframes each). Equipment and arm swings get their own command when there are many of them, to stay under the command block size limit.

- Skins use a player name, which needs an online-mode server for the name to be resolved.
- Hits and right-clicks on blocks or entities are recorded as swings. Swings in the air cannot be detected by a datapack without blocking the player's real interactions.
- The recording coordinates are stored as integers: stay within about 2 million blocks of the origin.
- `pose`, `profile` and `equipment` use entity fields of the target version: check them if a future version renames them.

# 🛠️ Development

Built with [StewBeet](https://github.com/Stoupy51/StewBeet) (a Beet framework), like the other Smithed-style libraries ([Cinemalya](https://github.com/Stoupy51/Cinemalya), [CommonSignals](https://github.com/Stoupy51/CommonSignals)...).
There is no hand-written datapack file: every function, tag, advancement, dialog and the dimension are generated by the Python code in `user/`, under the version of `beet.yml`.

## Build locally

Requirements: [Python](https://www.python.org/downloads/) **3.14 or newer** and [uv](https://docs.astral.sh/uv/).

```
uv run stewbeet
```

Run it from the project folder (the one containing `beet.yml`). `build/` then holds:

| File | Content |
| ---- | ------- |
| `Survirec_datapack.zip` | Survirec alone (Bookshelf Block must be installed separately) |
| `Survirec_datapack_with_libs.zip` | Survirec with Bookshelf Block merged in (Smithed Weld): the one to ship |

The first build downloads Bookshelf Block from Modrinth (cached in `.beet_cache/`). `uv run stewbeet watch` rebuilds on every change.
To copy the datapack straight into a world after each build, uncomment `build_copy_destinations` in `beet.yml`.

## Project layout

| Path                       | Role                                                                          |
| -------------------------- | ----------------------------------------------------------------------------- |
| `beet.yml`                 | Project configuration: id, author, version, Minecraft version, pipeline       |
| `user/link.py`             | Build entry point: calls every module below                                   |
| `user/api.py`              | Public function tags (defaults, name checks, version guard) and signals       |
| `user/common.py`           | Command fragments shared by the modules (chat text, buttons, per-axis loops...) |
| `user/load.py`             | Objectives, world state, tick and unload                                      |
| `user/record.py`, `playback.py`, `spawn.py`, `challenge.py`, `vault.py`, `core.py` | Recording, playback, spawning, challenges, block copies, management |
| `user/block.py`            | Block reading on top of Bookshelf Block                                       |
| `user/menu.py`, `help_pages.py`, `dialogs.py` | Menu item, help dialogs, other dialogs                     |
| `user/resources.py`        | Dimension, block and item tags, advancements                                  |
| `upload.py`                | Publishes a release (GitHub, Modrinth, Smithed)                               |
| `CHANGELOG.md`             | Changes of every version                                                      |

StewBeet generates `pack.mcmeta`, the versioned load ([LanternLoad](https://github.com/LanternMC/load)), the dependency check, the scoreboard constants (`#<n> survirec.data`), the function headers and the unload function.
The version lives in `beet.yml` only.

## Publish

Run `uv run python upload.py` after a build. It reads the tokens from `~/stewbeet/credentials.yml`.

# 📄 License

[MIT](LICENSE)

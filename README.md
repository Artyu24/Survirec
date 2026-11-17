# 🎬 Survirec

A vanilla datapack library that **records a player's movements and replays them with a mannequin** (or any other living entity).
No mods, no resource pack: only commands.

- 🎥 Records walking, sprinting, jumping, sneaking, swimming, elytra flight, equipment changes and arm swings (hits, right-clicks on blocks and entities).
- 🔁 Replays the movement in a loop, interpolated between keyframes (one keyframe every `N` ticks, so sequences stay small).
- 🧍 Mannequin by default, but any living entity works. Per-playback skin, texture, size, speed, offset, pose and equipment overrides.
- 📋 The sequence is copied into **one command block command** (long ones are split in a command block chain): no file to move around.
- 🏁 **Challenge mode**: a player (even in adventure) is recorded for `X` seconds, then a double with their skin replays the run in a loop. Several recordings can be synchronized in a group.
- ⚡ Cheap playback: scores and one `tp` macro per entity and tick. Stationary entities are not teleported, and entities with no player nearby are paused.
- 🧩 Follows the [Smithed conventions](https://docs.smithed.dev/conventions/).

📦 **Embedded library**: package it inside your datapack rather than shipping it separately.
Developed for Minecraft Java **26.2**. No dependency.

# ⚡ Quick start

## For players and map makers

```
function survirec:start {name:"walk",every:4}
```

You get a stop item (right-click to stop, sneak + right-click to also walk back to the start) and red buttons in the chat.
When the recording ends, click the **yellow button** in the chat to copy the playback command, then paste it in a command block.
Run `function survirec:help` for an in-game, paginated help.

| I want to                              | Command                                                              |
| -------------------------------------- | -------------------------------------------------------------------- |
| Record                                 | `function survirec:start {name:"walk",every:4}`                      |
| Stop / stop and walk back to the start | `function survirec:stop` / `function survirec:stop_loop`             |
| Cancel                                 | `function survirec:abort`                                            |
| Replay a sequence already loaded       | `function survirec:again {...}` (same fields as the copied command)  |
| Run a challenge                        | `execute as @p run function survirec:challenge {id:"epreuve1",time:30}` |
| Run synchronized challenges            | `execute as @p run function survirec:challenge_g {id:"a",time:5,group:"room1"}` |
| Remove entities                        | `survirec:kill {tag:"x"}`, `survirec:kill_name {name:"walk"}`, `survirec:kill_all` |
| Delete stored data                     | `function survirec:forget {name:"walk"}`                             |
| Change the animation range             | `function survirec:range {r:128}`                                    |
| Unblock / diagnose                     | `function survirec:reset`, `function survirec:debug`                 |

### Playback fields

The copied command starts with these fields. Edit them before running the command block.

| Field                                  | Meaning                                                                 |
| -------------------------------------- | ----------------------------------------------------------------------- |
| `pos`                                  | Where the entity appears. Default: where you started recording. `"~ ~ ~"` is the **center** of the command block, `"~ ~-0.5 ~"` the floor it stands on |
| `entity`                               | `minecraft:mannequin` (default) or any living entity                    |
| `size`                                 | Scale. `1` normal, `0.5` half, `2` double                               |
| `loop`                                 | `1` loop, `0` play once and stay, `2` play once and disappear           |
| `speed`                                | Percent. `100` normal                                                   |
| `offset`                               | Start delay in ticks, to desynchronize several entities                 |
| `tag`                                  | Triggering the block again replaces the entity with this tag            |
| `pose`                                 | Empty keeps the recorded poses. Otherwise forced: `standing`, `crouching`, `swimming`, `sleeping`, `fall_flying` |
| `skin`                                 | Player name (mannequin only)                                            |
| `texture`                              | Base64 `textures` property value, used if `skin` is empty               |
| `head` `chest` `legs` `feet` `mainhand` `offhand` | Item overrides. Empty keeps the recorded equipment            |

Do not edit `f`, `n`, `y`, `p`, `d`, `e`, `s`: they are the sequence data.

## Challenge groups

Every double belongs to a group (`main` unless `challenge_g` is used). Doubles of the same player and group start and finish together:
a shorter double stays frozen on its last position until the longest one is done, then all of them walk back to their start point (2 seconds) and start again together.
Triggering a challenge again removes the player's previous double for that `id` and records a new one.
Only one recording can run at a time on the server.

# 🔧 Developer API

Every entry point takes **one `with` compound**, so each field inside stays optional.
Run them as the player where it makes sense (`start`, `challenge`).

| Function tag                | `with` fields (defaults)                                       |
| --------------------------- | -------------------------------------------------------------- |
| `#survirec:v1/start`        | `name` (`"rec"`), `every` (`4`)                                |
| `#survirec:v1/stop`         | none (`with` not needed)                                       |
| `#survirec:v1/stop_loop`    | none                                                           |
| `#survirec:v1/abort`        | none                                                           |
| `#survirec:v1/play`         | `name`, plus every playback field above (`pos:"~ ~ ~"`, `loop:1`, `speed:100`...) |
| `#survirec:v1/challenge`    | `id` (`"default"`), `time` (`30`), `group` (`"main"`)          |
| `#survirec:v1/kill`         | `tag` or `name`. With neither, everything is removed           |
| `#survirec:v1/kill_all`     | none                                                           |
| `#survirec:v1/forget`       | `name`                                                         |
| `#survirec:v1/range`        | `r` (`128`)                                                    |

```
execute as @p run function #survirec:v1/start {with:{name:"walk",every:4}}
execute positioned 10 64 10 run function #survirec:v1/play {with:{name:"walk",loop:1,speed:150,texture:"<base64>"}}
execute as @p run function #survirec:v1/challenge {with:{id:"a",time:5,group:"room1"}}
```

Only the `#survirec:v1/...` function tags are the public API. Other functions are private and may change.

## Signals

Add your own function to these tags.

| Tag                                      | When                                                  | Runs as            |
| ---------------------------------------- | ----------------------------------------------------- | ------------------ |
| `#survirec:v1/signals/on_record_start`   | A recording (or challenge) has just started           | the recorded player |
| `#survirec:v1/signals/on_record_stop`    | A recording has ended                                 | the recorded player |
| `#survirec:v1/signals/on_spawn`          | A playback entity has just been created               | the new entity     |

## Sequence format

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

Then play it with `#survirec:v1/play {with:{name:"walk"}}`.

# 🧩 Conventions

- **Namespacing**: every function, tag, score, team and storage is prefixed with `survirec`.
- **Pack ID**: `"id": "survirec"` in `pack.mcmeta`.
- **Pack enabled tags**: the files are in `extras/pack_enabled` and are not loaded by default: the `context_int_provider` registry they rely on only exists since Minecraft 26.3. On 26.3+, copy that `data` folder into the datapack.
- **Tag specification**: spawned entities carry `smithed.entity` and `smithed.strict`; the stop item carries `{smithed:{ignore:{everything:1b}}}`.
- **Not applicable**: CMD prefixing (no `custom_model_data`), vanilla overrides (none). The optional data pack menu dialog is not implemented.

# 🔍 Notes

- Skins use a player name, which needs an online-mode server for the name to be resolved.
- Hits and right-clicks on blocks or entities are recorded as swings. Swings in the air cannot be detected by a datapack without blocking the player's real interactions.
- The recording coordinates are stored as integers: stay within about 2 million blocks of the origin.
- `pose`, `profile` and `equipment` use entity fields of the target version: check them if a future version renames them.

# 📄 License

[MIT](LICENSE)

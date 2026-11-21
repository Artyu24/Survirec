# Survirec - notes pour Claude

Librairie datapack vanilla **Minecraft Java 26.2** (Smithed + StewBeet, auteur **Artyu24**). Elle enregistre les mouvements et actions d'un joueur et les rejoue avec des mannequins (ou d'autres entités). Le README décrit l'API publique.

## Règles du projet (à respecter)
- **Version 1.0.0 atteinte** : ne jamais casser l'API publique (`#survirec:v1/...`, leurs champs, le format des séquences, les commandes déjà copiées dans des command blocks). Une feature = version mineure (1.x.0), un correctif = patch (1.0.x). Un changement incompatible va dans des tags `#survirec:v2/...` à côté de `v1`.
- À chaque changement : version dans `beet.yml` (et `pyproject.toml`), entrée dans `CHANGELOG.md`, README et aide en jeu (`user/help_pages.py`) à jour.
- Rester en **26.2**. Le passage en 26.3 se fait seulement sur demande (Bookshelf suivra : 4.1.x pour 26.2, 4.2.x pour 26.3).
- **Aucun /trigger**. Un non-op ne doit pouvoir lancer aucune commande du pack lui-même. Seules les épreuves (challenges) servent aux non-op, via un bouton qui active un command block.
- Le menu, l'aide, les boutons copier et le QuickStart n'utilisent **que** les tags publics `#survirec:v1/...`, jamais de fonctions versionnées (`survirec:v1.x.y/...`) : un lien dans le chat ou un dialog doit survivre à une mise à jour.
- Aide en français, seul le mot expliqué en gras, sans fioritures.
- Conventions Smithed, structure StewBeet comme les libs de Stoupy51 (Cinemalya, CommonSignals).

## Conventions de version (multi-versions, LanternLoad)
- Tout le code est **généré** sous `survirec:v{version}/...` avec `write_versioned_function` (version complète de `beet.yml`). Jamais de chemin écrit en dur : toujours `{functions}/...` (`functions = f"{ns}:v{version}"`) dans les f-strings.
- Les tags publics sont `#survirec:v{major}/<nom>` : chaque version y ajoute `survirec:v{version}/api/<nom>`, qui commence par la garde de version (`#survirec.loaded`, `major`, `minor`, `patch` dans `load.status`). Ajouter un point d'entrée = une entrée dans `entry_points()` de `user/api.py`.
- Load / tick / unload : `write_load_file`, `write_tick_file`, `write_unload_file` (`user/load.py`). Le tick n'est lancé que pour la version élue, et ne parcourt les entités que si `#instance_count` > 0.
- Advancements versionnés (`survirec:v{version}/record/trigger/*`) avec la même garde dans leur fonction de récompense.
- Les dialogs, la dimension et les tags de blocs/objets ne sont pas versionnés (contenu partagé, identique entre versions).

## Noms
- Tout nom se lit sans contexte : objectifs (`survirec.keyframe_progress`), tags (`survirec.instance`), fake players (`#sequence_time`), fonctions (verbe : `record/capture_keyframe`), storages et clés. Les constantes `#<n> survirec.data` sont posées par le plugin `auto.scoreboard_constants`.
- Storages persistants : `survirec:data seqs` (public, format des séquences), `survirec:library` (enregistrements gardés), `survirec:instances` (entités de lecture), `survirec:in_progress` (enregistrements en cours), `survirec:config`, `survirec:challenge_groups`. Storages de travail : `playback`, `recording`, `call`, `name_check`, `block`, `recorder`, `challenge`, `challenge_call`, `import` (voir `Storages` dans `user/common.py`).
- Exception voulue : les clés du format de séquence (`n`, `y`, `p`, `d`, `e`, `s`, `a`, et `t`, `k`, `x`, `b`, `p` des actions) restent courtes, elles sont recopiées dans les command blocks (32 500 caractères au plus par bloc).

## Structure (`user/`)
- `link.py` appelle tous les modules. `api.py` : tags publics et signaux. `load.py` : objectifs, état du monde, tick, unload.
- `record.py` (enregistrement), `playback.py` (entités de lecture, actions, groupes, relâchement des boutons, impulsions), `spawn.py` (apparition), `challenge.py` (épreuves), `vault.py` (copies de blocs), `core.py` (noms, séquences, kill, portée, reset, start/stop), `menu.py`, `help_pages.py`.
- `block.py` : lecture des blocs avec **Bookshelf Block** (`#bs.block:get_block`, `#bs.block:replace_properties`, `bs:out block`). StewBeet détecte `#bs.block:` et ajoute la dépendance + le weld.
- `resources.py` : dimension `survirec:vault`, tags de blocs, tags de dégâts (`WEAPON_DAMAGE`), advancements. `dialogs.py` : menu, formulaires, convention Smithed Data Pack Menu Dialog.
- Dimension cachée `survirec:vault` : chunk 0 = blocs seuls (libres dans `survirec:config free_block_slots`), chunk 1 = cubes 3x3x3 d'enregistrement (`free_cube_slots`), chunk 2 = cubes de regard par joueur, case 15 319 15 = case de travail.
- `common.py` : fragments partagés, à utiliser au lieu de les réécrire (`AXES`, `DIMENSIONS`, `Storages`, `wrap_yaw()`, `store_position()`, `kill_tagged()`, `build_sequence()`, `check_group_alive()`, `timer()`, et le texte de chat `text()`, `say()`, `info()`, `run()`, `copy()`, `SEPARATOR`). `copy()` met toujours la commande entre guillemets simples (les macros y injectent des guillemets doubles).
- Un bloc qui se répète se génère par une boucle `content += f"""..."""`, jamais par `"\n".join`. Les champs publics de `play` sont définis une seule fois (`PLAYBACK_FIELDS`).

## Build
Python 3.14 + uv : `uv run stewbeet` (sortie dans `build/`, `Survirec_datapack_with_libs.zip` contient Bookshelf Block). `uv run stewbeet watch` pour reconstruire à chaque modification.
Vérifier la syntaxe des commandes : `uv run python -m mecha -m 26.2 build/Survirec_datapack_with_libs.zip`.

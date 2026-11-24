# pyright: reportUnknownVariableType=false
# Imports
from beet import ProjectConfig
from stewbeet import JsonDict
from stewbeet.continuous_delivery import load_credentials, upload_to_modrinth, upload_to_smithed
from stewbeet.utils import get_project_config
from stouputils.io import read_file

# Get credentials and try to find the beet configuration
credentials: dict[str, str] = load_credentials("~/stewbeet/credentials.yml")
cfg: ProjectConfig = get_project_config()


# The GitHub release is made by hand: the changelog is the section of this version in CHANGELOG.md
changelog: str = read_file(f"{cfg.directory}/CHANGELOG.md").split(f"## {cfg.version}\n", 1)[1].split("\n## ", 1)[0].strip()


## Uploads

# Upload to Modrinth
modrinth_config: JsonDict = {
    "slug": cfg.id,
    "project_name": cfg.name.replace(" ", ""),
    "version": cfg.version,
    "authors": cfg.author,
    "summary": "Minecraft datapack library to record a player's movements and replay them with mannequins",
    "description_markdown": read_file(f"{cfg.directory}/README.md"),
    "version_type": "release",
    "build_folder": cfg.output,
}
upload_to_modrinth(credentials, modrinth_config, changelog)

# Upload to Smithed
smithed_config: JsonDict = {
    "project_id": cfg.id,
    "project_name": cfg.name.replace(" ", ""),
    "version": cfg.version,
}
upload_to_smithed(credentials, smithed_config, changelog)

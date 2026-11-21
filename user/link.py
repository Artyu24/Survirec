""" Survirec: every file of the library is generated here, under survirec:v<version>/ (see the README, Development). """
# Imports
from beet import Context

from . import api, block, challenge, core, dialogs, help_pages, load, menu, playback, record, resources, spawn, vault


# Main function is run just before finalyzing the build process (zip, headers, lang, ...)
def beet_default(ctx: Context) -> None:
	# Load, tick and unload, then the public entry points and everything they call into
	load.main()
	api.main()
	core.main()
	record.main()
	playback.main()
	spawn.main()
	challenge.main()
	vault.main()
	block.main()
	menu.main()
	help_pages.main()

	# Non-function resources
	resources.main()
	dialogs.main()

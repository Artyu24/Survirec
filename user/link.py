"""Survirec: hooks the hand-written library (src/) into StewBeet's versioned load and tick."""
from beet import Context
from stewbeet import write_load_file, write_tick_file


def beet_default(ctx: Context) -> None:
    # Runs in <id>:v<version>/load/confirm_load (LanternLoad convention, once the version is resolved)
    write_load_file("""
function survirec:v1/private/load
""")
    # Runs every tick in <id>:v<version>/tick
    write_tick_file("""
function survirec:v1/private/tick
""")

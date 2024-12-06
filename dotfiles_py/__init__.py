"""
file:           __init__.py
package:        dotfiles_py
author:         Ragdata
date:           6/12/2024
license:        MIT License
repository:     https://github.com/Ragdata/dotfiles-py
copyright:      Copyright © 2024 Redeyed Technologies
"""

""" ============================================================ """
""" DEPENDENCIES                                                 """
""" ============================================================ """

import os

from pathlib import Path

""" ============================================================ """
""" VARIABLES                                                    """
""" ============================================================ """

HOME = Path.home()
REPO = Path(__file__).parents[1]

CFG_FILES: list = [".env", ".secrets.yml", "defaults.py", "defaults.yml", "settings.py", "settings.yml"]

CFG_DIRS: list = [
    REPO,
    Path(f"{str(REPO)}/src/cfg/.dotfiles"),
    Path(f"{str(HOME)}/.dotfiles/cfg/.dotfiles")
]

""" ============================================================ """
""" MODULE                                                       """
""" ============================================================ """

def get_config_files() -> list:
    """Searches configured directories for config files"""
    files: list = []

    for path in CFG_DIRS:
        for file in CFG_FILES:
            if (path == REPO and file != ".env") or (path != REPO and file == ".env"):
                continue
            p = Path("/".join([str(path), file]))
            if p.exists():
                files.append(p)

    return files

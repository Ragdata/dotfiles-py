####################################################################
# dotfiles_py.__init__.py
####################################################################
"""
file:           __init__.py
package:        dotfiles_py
author:         Ragdata
date:           10/11/2024
license:        MIT License
repository:     https://github.com/Ragdata/dotfiles-py
copyright:      Copyright © 2024 Redeyed Technologies
"""
####################################################################
# DEPENDENCIES
####################################################################
from fnmatch import fnmatch
from pathlib import Path

#from dotfiles_py.config import settings
####################################################################
# ATTRIBUTES
####################################################################
#__all__ = ["HOME","CFG_FILES","CFG_DIRS","get_config_files","get_settings_files","settings"]
__pkg_name__ = "dotfiles_py"
__pkg_version__ = "0.1.0"
####################################################################
# VARS
####################################################################
HOME = Path.home()

CFG_FILES: list = [".env", ".secrets.yml", "defaults.py", "defaults.yml", "settings.py", "settings.yml"]

CFG_DIRS: list = [
    Path(f"{str(HOME)}/.local/dotfiles-py/src/cfg/.dotfiles"),
    Path(f"{str(HOME)}/.dotfiles/cfg/.dotfiles"),
    Path(f"{str(HOME)}/.dotfiles/cfg")
]
####################################################################
# MODULES
####################################################################
def get_config_files() -> list:
    """Searches configured directories for configuration files"""
    files: list = []
    match: bool = False

    for path in CFG_DIRS:
        for file in CFG_FILES:
            p = Path("/".join([str(path), file]))
            if p.exists():
                files.append(p)
    # check that at least one 'defaults' file is available
    for i in files:
        if fnmatch(str(i), '*defaults*'):
            match = True
            break
    if not match:
        raise FileNotFoundError("Config default settings not found!")

    return files

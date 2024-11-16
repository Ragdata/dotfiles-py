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
####################################################################
# VARS
####################################################################
HOME = Path.home()

CFG_FILES: list = [".env", ".secrets.yml", "defaults.py", "defaults.yml", "settings.py", "settings.yml"]

CFG_DIRS: list = [
    HOME.joinpath(".local/dotfiles-py/src/cfg/.dotfiles"),
    HOME.joinpath(".dotfiles/cfg/.dotfiles"),
    HOME.joinpath(".dotfiles/cfg"),
]
####################################################################
# MODULES
####################################################################
def get_config_files() -> list:
    """Searches configured directories for configuration files"""
    files: list = []
    match: bool = False
    for pathname in CFG_DIRS:
        for filename in CFG_FILES:
            p: Path = pathname.joinpath(filename)
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

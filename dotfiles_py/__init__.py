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
from pathlib import Path
####################################################################
# ATTRIBUTES
####################################################################
HOME = Path.home()

CFG_FILES: list = [".env", ".secrets.toml", "defaults.toml", "settings.toml"]

CFG_DIRS: list = [
    HOME.joinpath(".dotfiles/cfg"), 
    HOME.joinpath(".dotfiles/cfg/.dotfiles"), 
    HOME.joinpath(".local/dotfiles-py/src/cfg/.dotfiles")
]
####################################################################
# MODULES
####################################################################

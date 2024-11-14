####################################################################
# dotfiles_py.config.py
####################################################################
"""
file:           config.py
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
from typing import Any

from dynaconf import Dynaconf

from dotfiles_py import CFG_FILES, CFG_DIRS
####################################################################
# ATTRIBUTES
####################################################################

####################################################################
# MODULES
####################################################################
# Find config files
for filename in CFG_FILES:
    match filename:
        case ".env":
            varname = "dotenv"
        case ".secrets.toml":
            varname = "secrets"
        case "defaults.toml":
            varname = "defaults"
        case "settings.toml":
            varname = "settings"
        case _:
            raise ValueError(f"Unrecognized config file '{filename}'")
    for path in CFG_DIRS:
        filepath = path.join(filename)
        if filepath.exists():
            globals()[varname] = filepath
            break

if "defaults" not in globals():
    raise FileNotFoundError(f"Config default settings not found!")

settings_files: list = []

settings_files.append(str(globals()["defaults"]))

if "settings" in globals():
    settings_files.append(str(globals()["settings"]))
if "secrets" in globals():
    settings_files.append(str(globals()["secrets"]))

dynaconf_args: dict[str, Any] = {}

if "dotenv" in globals():
    dynaconf_args["load_dotenv"] = True
    dynaconf_args["dotenv_path"] = str(globals()["dotenv"])

dynaconf_args["settings_files"] = settings_files
dynaconf_args["root_path"] = str(Path.home())

settings = Dynaconf( dynaconf_args )

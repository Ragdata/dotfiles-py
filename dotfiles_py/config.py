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

from dynaconf import Dynaconf, add_converter

from dotfiles_py import get_config_files, get_settings_files
####################################################################
# ATTRIBUTES
####################################################################

####################################################################
# MODULES
####################################################################
# Custom Casting Token
add_converter("path", Path)
# Find config files
get_config_files()
# Get settings files
file_list = get_settings_files()
# Assemble Dynaconf args
dynaconf_args: dict[str, Any] = {}

if "dotenv" in globals():
    dynaconf_args["load_dotenv"] = True
    dynaconf_args["dotenv_path"] = str(globals()["dotenv"])

if len(file_list) == 1:
    dynaconf_args["settings_file"] = file_list[0]
elif len(file_list) > 1:
    dynaconf_args["settings_files"] = file_list
else:
    raise ValueError("No settings files found")

dynaconf_args["root_path"] = str(Path.home())

settings = Dynaconf( dynaconf_args )

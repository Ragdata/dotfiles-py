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
import os.path

from pathlib import Path

from dynaconf import Dynaconf, add_converter

from dotfiles_py import get_config_files
####################################################################
# MODULE
####################################################################
# Custom Casting Token
add_converter("path", Path)
# Find config files
paths = get_config_files()
# Setup the env_loader
loaders = ["dynaconf.loaders.env_loader"]
# Get settings files
files: list = []
for p in paths:
    if os.path.basename(p) == ".env":
        os.environ["LOAD_DOTENV_FOR_DYNACONF"] = "@bool true"
        os.environ["DOTENV_PATH_FOR_DYNACONF"] = str(p)
    else:
        files.append(str(p))
if len(files) == 1:
    os.environ["SETTINGS_FILE_FOR_DYNACONF"] = files[0]
elif len(files) > 1:
    os.environ["SETTINGS_FILES_FOR_DYNACONF"] = files
else:
    raise ValueError("No settings files found")

# dynaconf_args["root_path"] = str(Path.home())

settings = Dynaconf(
    LOADERS_FOR_DYNACONF=loaders,
    ROOT_PATH_FOR_DYNACONF=Path.home()
)

settings.configure()

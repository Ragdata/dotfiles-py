"""
file:           config.py
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

from dynaconf import Dynaconf, add_converter

from dotfiles_py import REPO, get_config_files

""" ============================================================ """
""" MODULE                                                       """
""" ============================================================ """

# add repo path to env
os.environ["REPO"] = str(REPO)

# custom casting token
add_converter("path", Path)

# find config files
paths = get_config_files()
# setup the env_loader
loaders = ["dynaconf.loaders.env_loader"]
# load settings files
files: list = []

# set environment
os.environ["ENV_FOR_DYNACONF"] = os.environ.get("ENV_FOR_DYNACONF", "prod")

for p in paths:
    if p.name == ".env":
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

settings = Dynaconf(LOADERS_FOR_DYNACONF=loaders, ENVIRONMENTS_FOR_DYNACONF=True, ENVVAR_PREFIX_FOR_DYNACONF="DOT")

settings.configure()

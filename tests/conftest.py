####################################################################
# tests.conftest.py
####################################################################
"""
file:           conftest.py
package:        tests
author:         Ragdata
date:           10/11/2024
license:        MIT License
repository:     https://github.com/Ragdata/dotfiles-py
copyright:      Copyright © 2024 Redeyed Technologies
"""
####################################################################
# DEPENDENCIES
####################################################################
import os
import copy
import pytest

from pathlib import Path
from typing import Any

from dynaconf import Dynaconf
from dynaconf.utils import DynaconfDict

from dotfiles_py import get_config_files
####################################################################
# SETUP
####################################################################
@pytest.fixture(scope="module")
def settings():
    """Settings fixture with some defaults"""
    mode = "TEST"
    # find config files
    paths = get_config_files()
    # Get settings files
    files: list = []

    for p in paths:
        if os.path.basename(p) != ".env":
            files.append(str(p))

    if len(files) == 1:
        os.environ["SETTINGS_FILE_FOR_DYNACONF"] = files[0]
    elif len(files) > 1:
        os.environ["SETTINGS_FILES_FOR_DYNACONF"] = files
    else:
        raise ValueError("No settings files found!")

    loaders = ["dynaconf.loaders.env_loader"]

    os.environ[f"DYNA{mode}_PORT"] = "@int 5000"
    os.environ[f"DYNA{mode}_VALUE"] = "@float 42.1"
    os.environ[f"DYNA{mode}_ALIST"] = '@json ["item1", "item2", "item3"]'
    os.environ[f"DYNA{mode}_ADICT"] = '@json {"key": "value"}'
    os.environ[f"DYNA{mode}_DEBUG"] = "@bool true"

    sets = Dynaconf(
        LOADERS_FOR_DYNACONF=loaders,
        ENVVAR_PREFIX_FOR_DYNACONF=f"DYNA{mode}",
        ROOT_PATH_FOR_DYNACONF=Path.home(),
    )

    sets.configure()
    return sets

@pytest.fixture(scope="module")
def testdir():
    return os.path.dirname(os.path.abspath(__file__))

@pytest.fixture(scope="module")
def clean_env():
    backup = copy.deepcopy(os.environ)
    for key in os.environ.keys():
        if key.startswith(("DYNACONF_", "FLASK_", "DJANGO_")):
            del os.environ[key]
    yield
    os.environ.update(backup)


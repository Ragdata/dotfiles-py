####################################################################
# tests.test_config.py
####################################################################
"""
file:           test_config.py
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

from pathlib import Path

from dotfiles_py import HOME, CFG_FILES, CFG_DIRS
####################################################################
# ATTRIBUTES
####################################################################

####################################################################
# MODULES
####################################################################
def test_settings(settings):
    """`settings` is a fixture defined in conftest.py"""
    assert HOME == str(Path.home())
    assert CFG_FILES[0] == ".env"
    assert CFG_DIRS[2] == str(Path.home().joinpath(".dotfiles/cfg"))
    assert settings.PORT == 5000
    assert isinstance(settings.PORT, int)
    assert settings.get("dir.home") == str(Path.home())

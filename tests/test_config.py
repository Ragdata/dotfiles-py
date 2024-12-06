"""
file:           test_config.py
package:        tests
author:         Ragdata
date:           10/11/2024
license:        MIT License
repository:     https://github.com/Ragdata/dotfiles-py
copyright:      Copyright © 2024 Redeyed Technologies
"""

""" ============================================================ """
""" DEPENDENCIES                                                 """
""" ============================================================ """

from pathlib import Path

""" ============================================================ """
""" MODULE                                                       """
""" ============================================================ """

def test_settings(settings):
    """`settings` is a fixture defined in conftest.py"""
    assert settings.current_env == "test"
    assert settings.dir.home == Path.home()
    assert settings.PORT == 5000
    assert settings.file.subtrees == Path.joinpath(settings.dir.conf.test, ".subtrees.yml")


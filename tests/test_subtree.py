"""
file:           test_subtree.py
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

from typer.testing import CliRunner

from dotfiles_py.subtree.cli import app
from dotfiles_py.config import get_config

""" ============================================================ """
""" MODULE                                                       """
""" ============================================================ """

config = get_config()

runner = CliRunner()

def test_callback():
    result = runner.invoke(app)
    assert result.exit_code == 0

def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0

####################################################################
# tests.test_subtree.py
####################################################################
"""
file:           test_subtree.py
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
from typer.testing import CliRunner
from dotfiles_py.subtree.cli import app
from dotfiles_py.subtree.models import Subtree
####################################################################
# ATTRIBUTES
####################################################################

####################################################################
# MODULES
####################################################################
runner = CliRunner()

def test_callback():
    result = runner.invoke(app)
    assert result.exit_code == 0

def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0

def test_add(settings):

    treefile = Path(settings.get('dir.repo'))
    treefile = treefile.joinpath('tests/data/.subtrees.yml')

    subtree = Subtree(treefile)

    assert treefile.exists() == True


def test_list():
    pass

def test_fetch():
    pass

def test_pull():
    pass

def test_remove():
    pass

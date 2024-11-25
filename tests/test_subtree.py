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
subdata = {
    "test-repo": {
        "path": "vendor/github.com/ragdata/test-repo",
        "url": "https://github.com/ragdata/test-repo.git",
        "branch": "master"
    }
}
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

    treepath = settings.get('dir.repo')
    treepath = "/".join([treepath, 'tests/data/.subtrees.yml'])
    treefile = Path(treepath)

    label = "test-repo"
    path = subdata.get(f"{label}.path")
    url = subdata.get(f"{label}.url")
    branch = subdata.get(f"{label}.branch")

    

    # result = runner.invoke(app, [f"add '{label}' '{path}' '{url}' '{branch}'"])

    assert path == subdata.get(f"{label}.path")
    assert url == subdata.get(f"{label}.url")
    assert branch == subdata.get(f"{label}.branch")
    assert treefile.exists() == True
    # assert result.exit_code == 0


def test_list():
    pass

def test_fetch():
    pass

def test_pull():
    pass

def test_remove():
    pass

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
from dynaconf import Dynaconf
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
home = Path.home()
label = "test-repo"
testtree = ".local/dotfiles-py/tests/data/.subtrees.yml"
tree = "/".join([str(home), testtree])
treepath = Path(tree)
subtree = Subtree(treepath)
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

def test_add(settings: Dynaconf):
    """Test cast for Subtree.add()"""
    path = subdata[label]['path']
    url = subdata[label]['url']
    branch = subdata[label]['branch']

    result = subtree.add(label, path, url, branch)

    assert path and path == subdata.get(f"{label}.path")
    assert url and url == subdata.get(f"{label}.url")
    assert branch and branch == subdata.get(f"{label}.branch")
    assert treepath.exists() == True
    assert result == True

def test_list():
    pass

def test_fetch():
    pass

def test_pull():
    pass

def test_remove(settings: Dynaconf):
    """Test case for Subtree.remove()"""
    print(subtree.store.items())

    # result = subtree.remove(label)

    # assert result == True

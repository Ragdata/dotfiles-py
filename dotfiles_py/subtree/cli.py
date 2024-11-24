####################################################################
# dotfiles_py.subtree.cli.py
####################################################################
"""
file:           cli.py
package:        dotfiles_py.subtree
author:         Ragdata
date:           10/11/2024
license:        MIT License
repository:     https://github.com/Ragdata/dotfiles-py
copyright:      Copyright © 2024 Redeyed Technologies
"""
####################################################################
# DEPENDENCIES
####################################################################
import typer

from typing import Annotated

from dotfiles_py.subtree import models
####################################################################
# ATTRIBUTES
####################################################################

####################################################################
# MODULES
####################################################################
app = typer.Typer()

@app.callback()
def callback():
    """
    Dotfiles-PY :: Git Subtrees Submodule
    """

@app.command()
def add():
    """Add a subtree to the current repository"""

@app.command()
def fetch():
    """Perform a `git fetch` for the named subtree"""

@app.command(name='list')
def show():
    """List all currently installed subtrees"""
    models.Subtree().show()

@app.command()
def pull():
    """Perform a `git pull` for the named subtree"""

@app.command()
def remove():
    """Remove the named subtree from the current repository"""

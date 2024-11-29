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
import sys
import typer

from rich import print
from typing import Annotated, Optional


from dotfiles_py.subtree import __app_name__, __app_version__
from dotfiles_py.subtree.models import Subtree
####################################################################
# ATTRIBUTES
####################################################################

####################################################################
# MODULES
####################################################################
app = typer.Typer(rich_markup_mode="rich", context_settings={'help_option_names': ['-h', '--help']}, no_args_is_help=True)
subtree = Subtree()

@app.callback(invoke_without_command=True)
def callback(version: bool = typer.Option(False, '-V', '--version', help="Display the submodule version and exit", is_eager=True)) -> int:
    """
    [yellow]Dotfiles-PY[/yellow] :: Git Subtrees Submodule
    """
    if version:
        print(f"{__app_name__.capitalize()} [yellow]v{__app_version__}[/yellow]")
        raise typer.Exit(1)

    return 0

@app.command('add')
def add(label: str, path: str, url: str,
    branch: Annotated[Optional[str], typer.Option()] = "master",
    squash: Annotated[Optional[bool], typer.Option()] = True,
    message: Annotated[Optional[str], typer.Option()] = None
) -> int:
    """Add a subtree to the current repository"""
    subtree.add(label, path, url, branch, squash, message)
    return 0

@app.command('fetch')
def fetch(label: str) -> int:
    """Perform a `git fetch` for the named subtree"""
    return 0

@app.command('list')
def show() -> int:
    """List all currently installed subtrees"""
    subtree.show()
    return 0

@app.command('pull')
def pull(label: str) -> int:
    """Perform a `git pull` for the named subtree"""
    return 0

@app.command('remove')
def remove(label: str) -> int:
    """Remove the named subtree from the current repository"""
    subtree.remove(label)
    return 0

@app.command('version')
def module_version() -> int:
    """Display the submodule version and exit"""
    return callback(True)

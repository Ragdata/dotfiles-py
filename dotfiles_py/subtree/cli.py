"""
file:           cli.py
package:        dotfiles_py.subtree
author:         Ragdata
date:           10/11/2024
license:        MIT License
repository:     https://github.com/Ragdata/dotfiles-py
copyright:      Copyright © 2024 Redeyed Technologies
"""

""" ============================================================ """
""" DEPENDENCIES                                                 """
""" ============================================================ """

import typer

from rich import print
from typing import Annotated, Optional

from dotfiles_py import subtree
from dotfiles_py.config import get_config
from dotfiles_py.subtree.models import Subtree

""" ============================================================ """
""" MODULE                                                       """
""" ============================================================ """

app = typer.Typer(rich_markup_mode="rich", context_settings={'help_option_names': ['-h', '--help']}, no_args_is_help=True)

config = get_config()

subtree = Subtree()

@app.callback(invoke_without_command=True)
def callback(version: bool = typer.Option(False, '-V', '--version', help="Display the submodule version and exit", is_eager=True)) -> typer.Exit:
    """
    [yellow]Dotfiles-PY[/yellow] :: Git Subtrees Submodule
    """
    if version:
        print(f"")
        print(config.dir.repo)
        return typer.Exit()
    return typer.Exit(1)


@app.command('version')
def module_version() -> typer.Exit:
    """Display the submodule version and exit"""
    return callback(True)

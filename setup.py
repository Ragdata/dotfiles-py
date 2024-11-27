####################################################################
# setup.py
####################################################################
"""
file:           setup.py
package:        dotfiles_py
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

from setuptools import setup
from dotfiles_py import __pkg_version__
####################################################################
# ATTRIBUTES
####################################################################

####################################################################
# MODULES
####################################################################
setup(
    name="dotfiles-py",
    version=__pkg_version__,
    py_modules=["dotfiles_py"],
    packages=["dotfiles_py"],
    extras_require={
        "all": [
            "dynaconf~=3.2",
            "multipledispatch~=1",
            "python-box[all]~=7.0",
            "shellingham==1.4.0",
            "typer~=0.13",
            "mkdocs~=1.6",
            "termynal~=0.12",
            "mkdocs-material~=9.5",
            "pytest~=8.3"
        ],
        "docs": ["mkdocs~=1.6", "termynal~=0.12", "mkdocs-material~=9.5"],
        "tests": ["pytest~=8.3"]
    }
)

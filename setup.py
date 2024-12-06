"""
file:           setup.py
package:        dotfiles_py
author:         Ragdata
date:           6/12/2024
license:        MIT License
repository:     https://github.com/Ragdata/dotfiles-py
copyright:      Copyright © 2024 Redeyed Technologies
"""

""" ============================================================ """
""" DEPENDENCIES                                                 """
""" ============================================================ """

import tomllib

from setuptools import setup

""" ============================================================ """
""" FUNCTIONS                                                    """
""" ============================================================ """

def _version():
    with open("pyproject.toml", "rb") as f:
        config = tomllib.load(f)
    return config['project']['version']

""" ============================================================ """
""" MODULES                                                      """
""" ============================================================ """

setup(
    name="dotfiles-py",
    version=_version(),
    py_modules=["dotfiles_py"],
    packages=["dotfiles_py"],
    extras_require={
        "all": [
            "dynaconf~=3.2",
            "multipledispatch~=1.0",
            "python-box[all]~=7.0",
            "typer~=0.15",
            "mkdocs~=1.6",
            "termynal~=0.12",
            "mkdocs-material~=9.5",
            "pytest~=8.3",
            "setuptools~=66.1",
            "wheel~=0.45"
        ],
        "dev": ["setuptools~=66.1", "wheel~=0.45"],
        "docs": ["mkdocs~=1.6", "termynal~=0.12", "mkdocs-material~=9.5"],
        "tests": ["pytest~=8.3"]
    }
)

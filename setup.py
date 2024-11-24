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
####################################################################
# ATTRIBUTES
####################################################################

####################################################################
# MODULES
####################################################################
def version(*names, **kwargs):
    content = ""
    with open(os.path.join(os.path.dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")) as f:
        content = f.read().strip()
    return content

setup(
    name="dotfiles-py",
    version=version("dotfiles_py", "VERSION"),
    py_modules=["dotfiles_py"],
    packages=["dotfiles_py"],
    extras_require={
        "all": [
            "PyGithub~=2.4",
            "colorama==0.4.4",
            "dynaconf~=3.2",
            "python-box[all]~=7.0",
            "shellingham==1.4.0",
            "typer~=0.13",
            "yaspin~=3.1",
            "mkdocs~=1.6",
            "termynal~=0.12",
            "mkdocs-material~=9.5",
            "pytest~=8.3"
        ],
        "docs": ["mkdocs~=1.6", "termynal~=0.12", "mkdocs-material~=9.5"],
        "tests": ["pytest~=8.3"]
    }
)

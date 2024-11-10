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

setup(version=version("dotfiles_py", "VERSION"))

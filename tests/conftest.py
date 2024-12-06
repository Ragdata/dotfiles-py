"""
file:           conftest.py
package:        tests
author:         Ragdata
date:           6/12/2024
license:        MIT License
repository:     https://github.com/Ragdata/dotfiles-py
copyright:      Copyright © 2024 Redeyed Technologies
"""

""" ============================================================ """
""" DEPENDENCIES                                                 """
""" ============================================================ """

import os
import copy
import pytest

from pathlib import Path

from dotfiles_py.config import get_config

""" ============================================================ """
""" MODULE                                                       """
""" ============================================================ """

@pytest.fixture(scope="module")
def settings():
    """Settings Fixture"""
    os.environ["ENV_FOR_DYNACONF"] = "test"

    # test values
    os.environ["DOT_PORT"] = "@int 5000"
    os.environ["DOT_VALUE"] = "@float 42.1"
    os.environ["DOT_ALIST"] = '@json ["item1", "item2", "item3"]'
    os.environ["DOT_ADICT"] = '@json {"key": "value"}'
    os.environ["DOT_DEBUG"] = "@bool true"

    return get_config()

@pytest.fixture(scope="module")
def testdir():
    return Path(__file__).parent

@pytest.fixture(scope="module")
def clean_env():
    backup = copy.deepcopy(os.environ)
    for key in os.environ.keys():
        if key.startswith(("DOT_", "FLASK_", "DJANGO_")):
            del os.environ[key]
    yield
    os.environ.update(backup)

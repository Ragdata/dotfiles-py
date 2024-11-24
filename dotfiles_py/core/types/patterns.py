####################################################################
# dotfiles_py.core.types.patterns.py
####################################################################
"""
file:           patterns.py
package:        dotfiles_py.core.types
author:         Ragdata
date:           10/11/2024
license:        MIT License
repository:     https://github.com/Ragdata/dotfiles-py
copyright:      Copyright © 2024 Redeyed Technologies
"""
####################################################################
# DEPENDENCIES
####################################################################
import threading
####################################################################
# ATTRIBUTES
####################################################################

####################################################################
# MODULES
####################################################################
def singleton(cls):
    """
    A thread-safe decorator for creating Singletons

    This decorator allows a class to exist as only a single instance
    throughout an application.  If the instance does not exist, one
    will be created; otherwise, the existing instance will be returned.

    This implementation is thread-safe, ensuring that only a single
    instance is created even in multithreaded environments.
    """
    _instances = {}
    _lock = threading.Lock()

    def get_instance(*args, **kwargs) -> object:

        with _lock:
            if cls not in _instances:
                _instances[cls] = cls(*args, **kwargs)
            return _instances[cls]

    return get_instance

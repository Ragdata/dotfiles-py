"""
file:           models.py
package:        dotfiles_py.subtree
author:         Ragdata
date:           6/12/2024
license:        MIT License
repository:     https://github.com/Ragdata/dotfiles-py
copyright:      Copyright © 2024 Redeyed Technologies
"""

""" ============================================================ """
""" DEPENDENCIES                                                 """
""" ============================================================ """

from box import Box
from pathlib import Path
from typing import Union
from ruamel.yaml import YAML
from dataclasses import dataclass
from subprocess import run, CompletedProcess
from multipledispatch import dispatch as overloaded

from dotfiles_py.config import get_config

""" ============================================================ """
""" ATTRIBUTES                                                   """
""" ============================================================ """

__all__ = ["SubtreeStore", "Subtree"]

config = get_config()

NoneType = type(None)

INDENTATION = config.indent

""" ============================================================ """
""" MODULE                                                       """
""" ============================================================ """

@dataclass(eq=False, order=False, match_args=False, kw_only=True)
class SubtreeStore(Box):

    def __init__(self, *args, **kwargs):
        """Initialise storage box"""
        # enable dot notation
        kwargs['box_dots'] = True

        super().__init__(*args, **kwargs)

class Subtree(object):

    _store = SubtreeStore()
    _treefile = Path(config.file.subtrees)

    @overloaded(dict, (str, Path))
    def __init__(self, data, filepath) -> None:
        """Instantiates a new Subtree object from raw data and with a filepath"""
        if isinstance(filepath, str):
            filepath = Path(filepath)
        self.treefile = filepath
        if not self.treefile.exists():
            self.treefile.touch(mode=0o644)
        self.store.update(data)
    @overloaded((str, Path))
    def __init__(self, filepath) -> None:
        """Instantiates a new Subtree object from a file"""
        if isinstance(filepath, str):
            filepath = Path(filepath)
        self.treefile = filepath

        if self.treefile.exists():
            data = self._load()
        else:
            self.treefile.touch(mode=0o644)
            data = None

        if data is not None:
            self.store.update(data)
    @overloaded(dict)
    def __init__(self, data) -> None:
        """Instantiates a new Subtree object from raw data"""
        if not self.treefile.exists():
            self.treefile.touch(mode=0o644)
            self.store.update(data)
    @overloaded()
    def __init__(self):
        """Instantiates a new Subtree object from default parameters"""
        if self.treefile.exists():
            data = self._load()
        else:
            self.treefile.touch(mode=0o644)
            data = None

        if data is not None:
            self.store.update(data)

    @property
    def treefile(self) -> Union[Path, None]:
        return self._treefile
    @treefile.setter
    def treefile(self, filepath: str | Path) -> None:
        if isinstance(filepath, str):
            filepath = Path(filepath)
        self._treefile = filepath

    @property
    def store(self) -> Union[SubtreeStore, None]:
        return self._store
    @store.setter
    def store(self, obj: SubtreeStore) -> None:
        self._store = obj

    @staticmethod
    def _get_cmd(cmd: str) -> list[str]:
        """Split a command string into usable parts"""
        return cmd.split()

    def _load(self) -> dict:
        """Load YAML data from treefile"""
        return YAML(typ='safe').load(self.treefile)

    def _run(self, cmd: str, **kwargs) -> CompletedProcess[bytes]:
        """Execute command using subprocess"""
        if 'cwd' not in kwargs.keys():
            kwargs["cwd"] = config.dir.repo
        return run(cmd, **kwargs)

    def _write(self):
        """Write the contents of the store to the designated treefile"""
        yaml = YAML(typ='safe')
        yaml.indent(mapping=INDENTATION, sequence=INDENTATION, offset=INDENTATION)
        yaml.dump(self.store.to_dict(), self.treefile)



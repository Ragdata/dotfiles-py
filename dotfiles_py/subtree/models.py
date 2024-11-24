####################################################################
# dotfiles_py.subtree.models.py
####################################################################
"""
file:           models.py
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
import json
import shlex
import subprocess

from box import Box
from dataclasses import dataclass
from dynaconf import Dynaconf
from pathlib import Path
from ruamel.yaml import YAML
from typing import Any, overload
from rich import print

from dotfiles_py.config import settings as config
####################################################################
# ATTRIBUTES
####################################################################
__all__ = ["SubtreeStore", "Subtree"]
####################################################################
# MODULES
####################################################################

# @dataclass(eq=False, order=False, match_args=False, kw_only=True)
# class SubtreeItem:

#     label:  str  = None
#     path:   Path = None
#     url:    str  = None
#     branch: str  = None

#     @overload
#     def __init__(self) -> None:
#         pass
#     @overload
#     def __init__(self, data: dict) -> None:
#         if not isinstance(data, dict):
#             raise ValueError("'data' must be of type `dict`")
#         self.fmDict(data)
#     @overload
#     def __init__(self, label: str = None, path: Path | str = None, url: str = None, branch: str = None) -> None:
#         self.label = label
#         self.url = url
#         self.branch = branch
#         if isinstance(path, Path):
#             self.path = path
#         elif isinstance(path, str):
#             self.path = Path(path)
#         else:
#             raise ValueError("Value of 'path' must be of type `str` or `Path`")

#     def __repr__(self) -> str:
#         return f"{self.__class__.__name__}(label={self.label!r}, path={str(self.path)!r}, url={self.url!r}, branch={self.branch!r})"

#     def __str__(self) -> str:
#         return f"{self.label}(path={str(self.path)}, url={self.url}, branch={self.branch})"

#     def fmDict(self, data: dict):
#         if len(data) == 0:
#             raise ValueError("Data structure is empty")
#         if len(data) == 1:
#             for k in data.keys(): self.label = k
#             for k, v in data.values():
#                 if k == "path":
#                     if isinstance(v, Path):
#                         self[k] = v
#                     if isinstance(v, str):
#                         self[k] = Path(k)
#                 else:
#                     self[k] = v
#         if len(data) > 1:
#             for k, v in data:
#                 if k == "path":
#                     if isinstance(v, Path):
#                         self[k] = v
#                     if isinstance(v, str):
#                         self[k] = Path(k)
#                 else:
#                     self[k] = v

#     def toDict(self):
#         return {self.label: {"path": str(self.path), "url": self.url, "branch": self.branch}}

#     def toJson(self, path: str):
#         return json.dumps(self.toDict(), indent=4)

#     def toYaml(self, path: str):
#         return yaml.dump(self.toDict(), indent=4)

@dataclass(eq=False, order=False, match_args=False, kw_only=True)
class SubtreeStore(Box):

    @overload
    def __init__(self) -> None:
        super().__init__(box_dots=True)
    @overload
    def __init__(self, obj: dict) -> None:
        super().__init__(obj)

class Subtree(object):

    _store: SubtreeStore
    _treefile: Path

    @overload
    def __init__(self, filepath: str | Path) -> None:
        if isinstance(filepath, str):
            filepath = Path(filepath)

        self._treefile = filepath

        data = self._load()

        self._store = SubtreeStore(data)

    def __init__(self) -> None:
        if not isinstance(config, Dynaconf):
            raise TypeError("Config object not available")

        self._treefile = Path(config.get("file.subtrees"))

        if not self._treefile.exists():
            self._treefile.touch(mode=0o644)
            data = {}
        else:
            data = self._load()

        self._store = SubtreeStore(data)

    def _erase(self):
        pass

    def _items(self):
        return self._store.items()

    def _keys(self):
        return self._store.keys()

    def _load(self) -> Any:
        return YAML(typ='safe').load(self._treefile)

    def _run(self, cmd: str, **kwargs):
        return subprocess.run(cmd, cwd=config.get("dir.repo"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def _values(self):
        return self._store.values()

    def _write(self):
        YAML.dump(self._store.to_dict(), self._treefile)

    def add(self, label: str, path: str, url: str, branch: str, squash: bool = True, message: str = None):

        if self._store.contains(label):
            raise ValueError(f"Subtree '{label}' already exists")
        if self._store.contains(path):
            raise ValueError(f"A subtree already exists at '{path}'")

        self._run(f"git remote add -f '{label}' '{url}'")

        if not squash:
            self._run(f"git subtree add --prefix '{path}' '{label}' '{branch}'")
        else:
            self._run(f"git subtree add --prefix '{path}' '{label}' '{branch}' --squash")

        self._store[label] = {'path': path, 'url': url, 'branch': branch}

        self._write()

    def fetch(self, label: str):

        if not self._store.contains(label):
            raise ValueError(f"Subtree '{label}' not found")
        branch = self._store.get(label.join(['.branch']))
        self._run(f"git fetch '{label}' '{branch}'")

    def merge(self):
        pass

    def pull(self, label: str):
        pass

    def remove(self, label: str):
        pass

    def show(self):
        print(self._store.to_yaml())

    def split(self):
        pass




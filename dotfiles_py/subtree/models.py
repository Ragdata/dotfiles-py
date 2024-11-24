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
from box import Box
from dataclasses import dataclass
from dynaconf import Dynaconf
from pathlib import Path
from ruamel.yaml import YAML
from typing import Any, overload
from collections.abc import Mapping
from subprocess import run as exec_, PIPE, CompletedProcess
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
    def __init__(self, obj: Mapping[Any, Any]) -> None:
        super().__init__(obj, box_dots=True)

    def __init__(self) -> None:
        super().__init__(box_dots=True)

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
            data = None
        else:
            data = self._load()

        if data:
            self._store = SubtreeStore(data)
        else:
            self._store = SubtreeStore()

    # def _erase(self):
    #     pass

    def _items(self):
        return self._store.items()

    def _keys(self):
        return self._store.keys()

    def _load(self):
        """Load YAML data from treefile"""
        return YAML(typ='safe').load(self._treefile)

    def _run(self, cmd: str, **kwargs) -> CompletedProcess[bytes]:
        """Execute command using subprocess"""
        return exec_(cmd, cwd=config.get("dir.repo"), stdout=PIPE, stderr=PIPE, check=True)

    def _values(self):
        return self._store.values()

    def _write(self):
        YAML.dump(self._store.to_dict(), self._treefile)

    def add(self, label: str, path: str, url: str, branch: str, squash: bool = True, message: str = None):
        """Add a subtree to the current repository"""
        if self._store.contains(label):
            raise ValueError(f"Subtree '{label}' already exists")
        if self._store.contains(path):
            raise ValueError(f"A subtree already exists at '{path}'")

        self._run(f"git remote add -f '{label}' '{url}'")

        suffix = ""
        if squash:
            suffix = " --squash"

        self._run(f"git subtree add --prefix '{path}' '{label}' '{branch}'{suffix}")

        self._store[label] = {'path': path, 'url': url, 'branch': branch}

        self._write()

    def fetch(self, label: str):
        """Perform a `git fetch` for the named subtree"""
        if not self._store.contains(label):
            raise ValueError(f"Subtree '{label}' not found")
        branch = self._store.get(label.join(['.branch']))
        self._run(f"git fetch '{label}' '{branch}'")

    # def merge(self):
    #     pass

    def pull(self, label: str, squash: bool = True):
        """Perform a `git pull` for the named subtree"""
        if not self._store.contains(label):
            raise ValueError(f"Subtree '{label}' not found")
        path = self._store.get(label.join(['.path']))
        branch = self._store.get(label.join(['.branch']))
        suffix = ""
        if squash:
            suffix = " --squash"

        self._run(f"git subtree pull --prefix '{path}' '{label}' '{branch}'{suffix}")

    def remove(self, label: str):
        """Delete specified subtree"""
        if not self._store.contains(label):
            raise ValueError(f"Subtree '{label}' not found")
        path = self._store.get(label.join(['.path']))
        url = self._store.get(label.join(['.url']))
        branch = self._store.get(label.join(['.branch']))

        root_path = Path(config.get('dir.repo'))
        tree_path = root_path.joinpath(path)

        if not tree_path.exists():
            raise FileNotFoundError(f"Directory '{str(tree_path)}' not found")

        self._run(f"git remote remove '{label}'")
        self._run(f"git rm -r '{str(tree_path)}'")

        del self._store[label]


    def show(self):
        """List all currently installed subtrees"""
        print(self._store.to_yaml())

    # def split(self):
    #     pass




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
from typing import Any, Union
#from collections.abc import Mapping
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
@dataclass(eq=False, order=False, match_args=False, kw_only=True)
class SubtreeStore(Box):

    def __init__(self, data: dict = None) -> None:

        if data:
            super().__init__(data, box_dots=True)
        else:
            super().__init__(box_dots=True)

class Subtree(object):

    _store: SubtreeStore | None = None
    _treefile: Path = Path(config.get('file.subtrees'))

    def __init__(self, filepath: str | Path = None) -> None:
        """Instantiates a new Subtree object"""
        self.treefile = filepath

        if self.treefile.exists():
            data = self._load()
        else:
            self.treefile.touch(mode=0o644)
            data = None

        if data is not None:
            self.store = SubtreeStore(data)
        else:
            self.store = SubtreeStore()

    @property
    def treefile(self) -> Union[Path, None]:
        """Getter for self._treefile"""
        return self._treefile
    @treefile.setter
    def treefile(self, filepath: str | Path) -> None:
        """Setter for self._treefile"""
        if isinstance(filepath, str):
            filepath = Path(filepath)
        self._treefile = filepath

    @property
    def store(self) -> Union[SubtreeStore, None]:
        """Getter for self._store"""
        return self._store
    @store.setter
    def store(self, obj: SubtreeStore) -> None:
        """Setter for self._store"""
        self._store = obj

    # def _erase(self):
    #     pass

    def _load(self) -> dict:
        """Load YAML data from treefile"""
        return YAML(typ='safe').load(self.treefile)

    def _run(self, cmd: str, **kwargs) -> CompletedProcess[bytes]:
        """Execute command using subprocess"""
        return exec_(cmd, cwd=config.get("dir.repo"), stdout=PIPE, stderr=PIPE, check=True)

    def _write(self):
        YAML.dump(self.store.to_dict(), self.treefile)

    def add(self, label: str, path: str, url: str, branch: str, squash: bool = True, message: str = None):
        """Add a subtree to the current repository"""
        suffix = ""
        paths = []
        labels = self.store.keys(False)

        if label in labels:
            raise ValueError(f"Subtree '{label}' already exists")
        if len(labels) > 0:
            for l in labels:
                paths.append(self.store.get(f"{l}.path"))
        if path in paths:
            raise ValueError(f"Subtree already exists at '{path}'")

        if squash:
            suffix = " --squash"

        self._run(f"git remote add -f '{label}' '{url}'")
        self._run(f"git subtree add --prefix '{path}' '{label}' '{branch}'{suffix}")

        self.store[label] = {'path': path, 'url': url, 'branch': branch}

        self._write()

    def fetch(self, label: str):
        """Perform a `git fetch` for the named subtree"""
        if not self.store.contains(label):
            raise ValueError(f"Subtree '{label}' not found")
        branch = self.store.get(label.join(['.branch']))
        self._run(f"git fetch '{label}' '{branch}'")

    # def merge(self):
    #     pass

    def pull(self, label: str, squash: bool = True):
        """Perform a `git pull` for the named subtree"""
        if not self.store.contains(label):
            raise ValueError(f"Subtree '{label}' not found")
        path = self.store.get(label.join(['.path']))
        branch = self.store.get(label.join(['.branch']))
        suffix = ""
        if squash:
            suffix = " --squash"

        self._run(f"git subtree pull --prefix '{path}' '{label}' '{branch}'{suffix}")

    def remove(self, label: str):
        """Delete specified subtree"""
        if not self.store.contains(label):
            raise ValueError(f"Subtree '{label}' not found")
        path = self.store.get(label.join(['.path']))
        url = self.store.get(label.join(['.url']))
        branch = self.store.get(label.join(['.branch']))

        root_path = Path(config.get('dir.repo'))
        tree_path = root_path.joinpath(path)

        if not tree_path.exists():
            raise FileNotFoundError(f"Directory '{str(tree_path)}' not found")

        self._run(f"git remote remove '{label}'")
        self._run(f"git rm -r '{str(tree_path)}'")

        del self.store[label]

    def show(self):
        """List all currently installed subtrees"""
        print(self.store.to_yaml())

    # def split(self):
    #     pass




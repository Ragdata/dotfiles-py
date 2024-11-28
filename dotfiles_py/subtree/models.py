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
from typing import Union
#from collections.abc import Mapping
from subprocess import run as exec_, CompletedProcess, Popen, PIPE
from multipledispatch import dispatch as overload_
from rich import print

from dotfiles_py.config import settings as config
####################################################################
# ATTRIBUTES
####################################################################
__all__ = ["SubtreeStore", "Subtree"]
NoneType = type(None)
INDENTATION = config.get('yaml.indent')
####################################################################
# MODULES
####################################################################
@dataclass(eq=False, order=False, match_args=False, kw_only=True)
class SubtreeStore(Box):

    @overload_(dict)
    def __init__(self, data: dict, *args, **kwargs):

        if 'box_dots' in kwargs.keys():
            kwargs.update({"box_dots": True})
        else:
            kwargs["box_dots"] = True

        super().__init__(data, *args, **kwargs)

    @overload_()
    def __init__(self, *args, **kwargs):

        if 'box_dots' in kwargs.keys():
            kwargs.update({"box_dots": True})
        else:
            kwargs["box_dots"] = True

        super().__init__(*args, **kwargs)

class Subtree(object):

    _store: SubtreeStore | None = None
    _treefile: Path = Path(config.get('file.subtrees'))

    @overload_(dict)
    def __init__(self, data: dict) -> None:
        """Instantiates a new Subtree object from data"""
        if not self.treefile.exists():
            self.treefile.touch(mode=0o644)
        self.store = SubtreeStore(data)

    @overload_(dict, (str, Path))
    def __init__(self, data: dict, filepath: str | Path = None) -> None:
        """Instantiates a new Subtree object from data with filename"""
        if isinstance(filepath, str):
            filepath = Path(filepath)
        self.treefile = filepath
        if not self.treefile.exists():
            self.treefile.touch(mode=0o644)
        self.store = SubtreeStore(data)

    @overload_((str, Path))
    def __init__(self, filepath: str | Path = None) -> None:
        """Instantiates a new Subtree object from file"""
        if filepath is not None:
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

    @staticmethod
    def _get_cmd(cmd: str):
        """Split a command string into usable parts"""
        return cmd.split()

    def _load(self) -> dict:
        """Load YAML data from treefile"""
        return YAML(typ='safe').load(self.treefile)

    def _run(self, cmd: str, **kwargs) -> CompletedProcess[bytes]:
        """Execute command using subprocess"""
        if 'cwd' in kwargs.keys():
            kwargs.update({"cwd": config.get("dir.repo")})
        else:
            kwargs["cwd"] = config.get("dir.repo")
        if 'check' in kwargs.keys():
            ckval = kwargs["check"]
            kwargs.update({"check": ckval})
        else:
            kwargs["check"] = True

        return exec_(cmd, **kwargs)

    def _write(self):
        """Write the contents of the store to the designated treefile"""
        yaml = YAML(typ='safe')
        yaml.indent(mapping=INDENTATION, sequence=INDENTATION, offset=INDENTATION)
        yaml.dump(self.store.to_dict(), self.treefile)

    def add(self, label: str, path: str, url: str, branch: str, squash: bool = True, message: str = None) -> bool:
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

        cmd = f"git remote add {label} {url}"
        parts = cmd.split()
        self._run(parts)

        cmd = f"git subtree add --prefix {path} {label} {branch}{suffix}"
        parts = cmd.split()
        self._run(parts)

        self.store[label]['path'] = path
        self.store[label]['url'] = url
        self.store[label]['branch'] = branch
        # rewrite treefile
        self._write()

        return True

    def fetch(self, label: str):
        """Perform a `git fetch` for the named subtree"""
        if not self.store.contains(label):
            raise ValueError(f"Subtree '{label}' not found")
        branch = self.store.get(label.join(['.branch']))
        self._run(f"git fetch {label} {branch}")

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

        self._run(f"git subtree pull --prefix {path} {label} {branch}{suffix}")

    def remove(self, label: str) -> bool:
        """Delete specified subtree"""
        root = config.get('dir.repo')
        if not label in self.store.keys():
            return True
        # get subtree path
        path = self.store[f"{label}.path"]
        tree = "/".join([str(root), str(path)])
        # remove remote
        self._run(self._get_cmd(f"git remote remove {label}"), check=False)
        # remove files
        self._run(self._get_cmd(f"git rm -r {tree}"), check=False)
        # remove data
        if label in self.store.keys():
            del self.store[label]
        # rewrite treefile
        self._write()

        return True

    def show(self):
        """List all currently installed subtrees"""
        print(self.store.to_yaml())

    # def split(self):
    #     pass




####################################################################
# dotfiles_py.core.ansi.types.py
####################################################################
"""
file:           types.py
package:        dotfiles_py.core.ansi
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
import sys
from io import UnsupportedOperation
from collections.abc import Iterable
from dotfiles_py.core.ansi import ANSI, Foreground, FOREGROUND, Style
####################################################################
# ATTRIBUTES
####################################################################

####################################################################
# MODULES
####################################################################
def _check_color(*, no_color: bool | None = None, force_color: bool | None = None) -> bool:
    """Check env vars and system for tty/dumb terminal"""
    if no_color is not None and no_color:
        return False
    if force_color is not None and force_color:
        return True
    
    # check env vars
    if "ANSI_COLORS_DISABLED" in os.environ:
        return False
    if "NO_COLOR" in os.environ:
        return False
    if "FORCE_COLOR" in os.environ:
        return True
    
    # then check system
    if os.environ.get("TERM") == "dumb":
        return False
    if not hasattr(sys.stdout, "fileno"):
        return False
    
    try:
        return os.isatty(sys.stdout.fileno())
    except UnsupportedOperation:
        return sys.stdout.isatty()

def ansi_text(text: str, color: Foreground):
    _format = "%s%dm%s%s"
    return _format % (ANSI['CSI'], FOREGROUND[color], text, ANSI['RESET'])

class AnsiText(object):
    
    _format: str = "%s%sm%s%s"
    _codes: list = ()
    _text: str = ""
    _fmt_txt: str = ""
    
    def __init__(self, text: str, *, fg: int | None = None, bg: int | None = None, style: Iterable[Style] | None = None, auto: bool = False) -> None:

        if fg is None and bg is None and style is None:
            raise ValueError("No parameters included")
        if not text:
            raise ValueError("Must include text")
        else:
            self._text = text
        if style is not None:
            for code in style:
                self._codes.append(code)
        if fg is not None:
            self._codes.append(fg)
        if bg is not None:
            self._codes.append(bg)
        if auto:
            self.format()
            self.print()
    
    def format(self):
        if len(self._codes) == 0:
            raise ValueError("No codes present")
        _string = ";".join(self._codes)
        self._fmt_txt = self._format % (ANSI['CSI'], _string, self._text, ANSI['RESET'])
    
    def print(self):
        print(self._fmt_txt)

class AnsiCursor(object):
    pass

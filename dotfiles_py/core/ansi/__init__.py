####################################################################
# dotfiles_py.core.ansi.__init__.py
####################################################################
"""
file:           __init__.py
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
from typing import Literal

from dotfiles_py.core.ansi.types import AnsiText
####################################################################
# ATTRIBUTES
####################################################################
ANSI_ESC = "\033"
ANSI_CSI = f"{ANSI_ESC}["
ANSI_OSC = f"{ANSI_ESC}]"
ANSI_ST  = f"{ANSI_ESC}\\"
ANSI_BEL = "\a"
ANSI_BS  = "\b"
ANSI_HT  = "\t"
ANSI_LF  = "\n"
ANSI_VT  = "\v"
ANSI_FF  = "\f"
RESET    = f"{ANSI_CSI}0m"
####################################################################
# MODULES
####################################################################
Foreground = Literal[ "black", "red", "green", "yellow", "blue", "magenta", "cyan", "lt_grey", "dk_grey", "lt_red", "lt_green", "lt_yellow", "lt_blue", "lt_magenta", "lt_cyan", "white", "default" ]

Background = Literal[ "on_black", "on_red", "on_green", "on_yellow", "on_blue", "on_magenta", "on_cyan", "on_lt_grey", "on_dk_grey", "on_lt_red", "on_lt_green", "on_lt_yellow", "on_lt_blue", "on_lt_magenta", "on_lt_cyan", "on_white", "on_default" ]

Style = Literal[ "bold", "faint", "italic", "underline", "blink", "invert", "hide", "strike", "dbl_underline", "overline" ]

UnStyle = Literal[ "normal", "no_italic", "no_underline", "no_blink", "no_invert", "no_hide", "no_strike", "no_overline" ]

FOREGROUND: dict[Foreground, int] = {
    "black":            30,
    "red":              31,
    "green":            32,
    "yellow":           33,
    "blue":             34,
    "magenta":          35,
    "cyan":             36,
    "lt_grey":          37,
    "dk_grey":          90,
    "lt_red":           91,
    "lt_green":         92,
    "lt_yellow":        93,
    "lt_blue":          94,
    "lt_magenta":       95,
    "lt_cyan":          96,
    "white":            97,
    "default":          39
}

BACKGROUND: dict[Background, int] = {
    "on_black":         40,
    "on_red":           41,
    "on_green":         42,
    "on_yellow":        43,
    "on_blue":          44,
    "on_magenta":       45,
    "on_cyan":          46,
    "on_lt_grey":       47,
    "on_dk_grey":       100,
    "on_lt_red":        101,
    "on_lt_green":      102,
    "on_lt_yellow":     103,
    "on_lt_blue":       104,
    "on_lt_magenta":    105,
    "on_lt_cyan":       106,
    "on_white":         107,
    "on_default":       49
}

STYLE: dict[Style, list[int, int]] = {
    "bold":             (1, 22),
    "faint":            (2, 22),
    "italic":           (3, 23),
    "underline":        (4, 24),
    "blink":            (5, 25),
    "invert":           (7, 27),
    "hide":             (8, 28),
    "strike":           (9, 29),
    "dbl_underline":    (21, 24),
    "overline":         (53, 55)
}

UNSTYLE: dict[Style, int] = {
    "normal":           22,
    "no_italic":        23,
    "no_underline":     24,
    "no_blink":         25,
    "no_invert":        27,
    "no_hide":          28,
    "no_strike":        29,
    "no_overline":      55
}

ANSI: dict[str, str] = {
    "ESC":      ANSI_ESC,
    "CSI":      ANSI_CSI,
    "OSC":      ANSI_OSC,
    "ST":       ANSI_ST,
    "BEL":      ANSI_BEL,
    "BS":       ANSI_BS,
    "HT":       ANSI_HT,
    "LF":       ANSI_LF,
    "VT":       ANSI_VT,
    "FF":       ANSI_FF,
    "RESET":    RESET
}

__all__ = [
    "ANSI",
    "Foreground",
    "FOREGROUND",
    "Background",
    "BACKGROUND",
    "Style",
    "STYLE",
    "UnStyle",
    "UNSTYLE",
    "AnsiText",
    "AnsiCursor"
]

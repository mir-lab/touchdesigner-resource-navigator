"""Pane Controls
"""

# allows all type hints to be imported as strings by default
from __future__ import annotations

# allows for type checking without circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import navigatorEXT

# global op shortcut to TouchDesigner Curriculum Navigator
Navigator = op.TDCN

#####################################################
## PANE CONTROLS
#####################################################

def Save_tox_copy(par):
    ...

def Set_view(state, view_type):
    ... 

def _copy_current_example(example):
    ...

def Win_close():
    ...

def Open_floating():
    ...

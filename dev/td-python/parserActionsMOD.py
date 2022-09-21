"""Actions Parser
"""

# allows all type hints to be imported as strings by default
from __future__ import annotations

# allows for type checking without circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import navigatorEXT

# global op shortcut to TouchDesigner Curriculum Navigator
Navigator:navigatorEXT.NavController = op.TDCN

def _web_action_map(action:navigatrEXT.action):
    '''
    Dictionary map of fucntions that corespond to web actions


    Args
    ---------------
    action (str)
    > String name of coresponding NavController method


    Returns
    ---------------
    action_map_func (method)
    > matching method from NavController
    '''
    action_map = {
        "load_tox" : Navigator.ext.NavController.load_tox,
        "open_floating_network" : Navigator.ext.NavController.open_floating_network,
        "open_in_browser" : Navigator.ext.NavController.open_in_browser,
        "update_td_pars" : Navigator.ext.NavController.update_td_pars
    }
    action_map_func = action_map.get(action)
    return action_map_func

def Web_action(qs_result):
    '''
    Action Runner - tries to run the requested web-action

    Args
    ---------------
    qs_result (query string obj):
    > the resulting query string from a URL

    '''

    try:
        func = _web_action_map(qs_result.get('action')[0])
        func(qs_result)
    
    except Exception as e:
        if debug:
            debug(e)
        else:
            pass       
    return 
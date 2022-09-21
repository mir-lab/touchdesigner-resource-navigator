"""Web Actions

#################################
##### Action Specifications #####
#################################

query string formated commands that can be interpreted by TouchDesigner
to drive scripts and actions in TD.

Query strings require the following args:

* actionable:bool
* action:string (function name)
* keyWordArgsDefinedByFunction:value

examples:
?actionable=1&action=load_tox&remotePath=someUrl

?actionable=1&action=open_floating_network

?actionable=1&action=open_in_browser

?actionable=1&action=update_td_pars&somePar=someVal
"""

Navigator = op.TDCN

def load_tox(qs_results:dict):
    """
    Load TOX from URL

    Args
    ---------------
    qs_results (query_string obj)
    > query string from ULR, contains all necessary args and vals
    """

    if Navigator.nav_debug.eval():
        debug("loading remote")

    remote_tox = qs_results.get('remotePath')
    self.selected_remote_tox = remote_tox[0]
    self.load_new_selection()
    self.remove_qs_from_path() 
    pass

def open_floating_network(qs_results:dict):
    """
    Opens Floating Network Window
    
    Args
    ---------------
    qs_results (query_string obj)
    > query string from ULR, contains all necessary args and vals
    """

    if Navigator.nav_debug.eval():
        debug("Open Floating Window")
    floating_pane = ui.panes.createFloating(name="Example")
    current_example = Navigator.ext.NavController.get_current_example()
    floating_pane.owner = current_example
    floating_pane.home()

    Navigator.ext.NavController.remove_qs_from_path()
    pass

def open_in_browser(qs_results:dict):
    """
    Open URL in web browser
    
    Args
    ---------------
    qs_results (query_string obj)
    > query string from ULR, contains all necessary args and vals

    """

    address = Navigator.web_browser.par.Address.eval()
    ui.viewFile(address)
    Navigator.ext.NavController.remove_qs_from_path()

def update_td_pars(qs_results:dict):
    """
    Update TD parameters
    
    Args
    ---------------
    qs_results (query_string obj)
    > query string from ULR, contains all necessary args and vals
    """

    target_op = Navigator.ext.NavController.get_current_example()
    exempt_keys = ['action', 'actionable']
    for each_par, each_val in qs_results.items():
        if each_par in exempt_keys:
            pass
        else:
            try:
                target_op.par[each_par] = each_val[0]
            except Exception as e:
                pass
        
        if Navigator.nav_debug.eval():
            debug(each_par, each_val)

    Navigator.ext.NavController.remove_qs_from_path()
    pass


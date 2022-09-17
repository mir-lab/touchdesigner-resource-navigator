#####################################################
## ACTIONS Parser
#####################################################

def _web_action_map(self, action):
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
        "load_tox" : self.load_tox,
        "open_floating_network" : self.open_floating_network,
        "open_in_browser" : self.open_in_browser,
        "update_td_pars" : self.update_td_pars
    }
    action_map_func = action_map.get(action)
    return action_map_func

def _web_action(self, qs_result):
    '''
    Action Runner - tries to run the requested web-action

    Args
    ---------------
    qs_result (query string obj):
    > the resulting query string from a URL

    '''

    try:
        func = self._web_action_map(qs_result.get('action')[0])
        func(qs_result)
    except Exception as e:
        if debug:
            debug(e)
        else:
            pass       
    return 

#####################################################
## ACTIONS 
#####################################################

def open_floating_network(self, qs_results):
    '''
    Opens Floating Network Window
    
    Args
    ---------------
    qs_results (query_string obj)
    > query string from ULR, contains all necessary args and vals
    '''

    if NavController.nav_debug.eval():
        debug("Open Floating Window")
    floating_pane = ui.panes.createFloating(name="Example")
    current_example = self.get_current_example()
    floating_pane.owner = current_example
    floating_pane.home()

    self.remove_qs_from_path()
    pass

def update_td_pars(self, qs_results):
    '''
    Update TD parameters
    
    Args
    ---------------
    qs_results (query_string obj)
    > query string from ULR, contains all necessary args and vals
    '''

    target_op = self.get_current_example()
    exempt_keys = ['action', 'actionable']
    for each_par, each_val in qs_results.items():
        if each_par in exempt_keys:
            pass
        else:
            try:
                target_op.par[each_par] = each_val[0]
            except Exception as e:
                pass
        if NavController.nav_debug.eval():
            debug(each_par, each_val)

    self.remove_qs_from_path()
    pass

def load_tox(self, qs_results):
    '''
    Load TOX from URL

    Args
    ---------------
    qs_results (query_string obj)
    > query string from ULR, contains all necessary args and vals
    '''

    if NavController.nav_debug.eval():
        debug("loading remote")

    remote_tox = qs_results.get('remotePath')
    self.selected_remote_tox = remote_tox[0]
    self.load_new_selection()
    self.remove_qs_from_path() 
    pass

def open_in_browser(self, qs_results):
    '''
    Open URL in web browser
    
    Args
    ---------------
    qs_results (query_string obj)
    > query string from ULR, contains all necessary args and vals

    '''

    address = NavController.web_browser.par.Address.eval()
    ui.viewFile(address)
    self.remove_qs_from_path()


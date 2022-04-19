import urllib.request

#####################################################
# action spec
#####################################################
'''
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
'''

class NavController:
    '''
    Extension for managing the Curriculum Navigator

    Notes
    ---------------

    TD Palette Dependencies
    - webBrowser==1.1

    The NavController uses the webBrowser palette component to render
    a rich text experience alongside a TouchDesigner example. The Navigator component
    loads and fetches a TOX from a remote source, and loads it dynamically into
    a lightweight shell experience. This keeps all TOX elements outside of the 
    component context, ensuring that fetched examples are always the 
    most recently updated.

    debug() is largely preferred over print() in this extension, relyling on the 
    Navigator COMP's Debug parmaeter to control outputting messages to the 
    text-port. 

    Navigator loading and web-interaction is driven by a query string model 
    for providing data to the webBrowser context to be interpreted by TouchDesigner.
    Query string parsing is handled by the Python built-in library urllib to provide
    for simplified support across platforms.

    This extension is organized into blocks with respective areas of focus:
    - ACTIONS Parser
        Parsing mechanics and function-lookup map for handling incoming 
        query string requests.

    - ACTIONS
        Supported actions parsable from query strings
        Currently all actions accept a singe arg - query string (qs_string) - 
        passing responsibility for handing the qs_string object to the called
        function. This matches a similar pattern found in lister, where a single
        info object is reliably passed to functions.

    - Timer Functions
        Consolidated location for handling timer callbacks, reducing the number of 
        places where python code may need to be updated.
    '''

    NavigatorCOMP   = parent.Navigator
    NavigatorCOMP = parent.Navigator
    view = parent.Navigator.op('container_ui/container_view')
    web_browser = parent.Navigator.op('container_ui/container_nav_and_text/webBrowser')
    loading_view = parent.Navigator.op('container_ui/container_view/container_loading')
    settings_view = parent.Navigator.op('container_ui/container_view/container_settings')
    disp_buffer = parent.Navigator.op('container_ui/container_view/container_display_buffer')
    trans_timer = parent.Navigator.op('container_ui/container_view/container_loading/timer1')

    nav_debug = parent.Navigator.par.Debug

    def __init__(self, ownerOp):
        '''
        EXT Init 


        Args
        ---------------
        ownerOp (TD_operator)
        > The TouchDesigner operator initialzing this ext, usually `me`
        
        '''
        
        self.Owner_op = ownerOp
        self.selected_remote_tox = None

    def Url_update(self, url):
        '''
        Updates webrender TOP URL

        Args
        ---------------
        url (str)
        > The URL from the webBrowser COMP

        '''

        qs_result = self.query_string_parse(url)
        key_list = [key for key in qs_result.keys()]

        # check for the actionable arg
        if qs_result.get('actionable', [0])[0] == '1':
            self._web_action(qs_result)
        else:
            pass

        pass

    def Zoom_update(self, zoom_level):
        '''
        Update web render zoom level

        Args
        ---------------
        zoom_level (int)
        > The target zoom level for the webrender TOP
        '''
        print(f"document.body.style.zoom = '{zoom_level}%'")
        NavController.web_browser.op('webrender1').executeJavaScript(f"document.body.style.zoom = '{zoom_level}%'")

    def Zoom_increment(self, increment_val):
        prev_val = NavController.NavigatorCOMP.par.Webrenderzoom.eval()
        NavController.NavigatorCOMP.par.Webrenderzoom = increment_val + prev_val
    
    def Zoom_reset(self, val):
        print("zoom reset")
        NavController.NavigatorCOMP.par.Webrenderzoom = val

    def get_current_example(self):
        '''
        Get current example

        Returns
        ---------------
        current_example (TD_operator)
        > The current component loaded in the Navigator's display buffer COMP
        '''

        current_example = parent.Navigator.op('container_ui/container_view/container_display_buffer').findChildren(depth=1)[0]
        return current_example

    def remove_qs_from_path(self):
        '''
        Remove query string from URL path

        '''

        if NavController.nav_debug.eval():
            debug("remove QS from Path")

        address = NavController.web_browser.par.Address.eval()
        cleanAddress = self.clean_url(address)
        NavController.web_browser.par.Address = cleanAddress
    
    def clean_url(self, url):
        '''
        Clean up a URL

        Removes dangling query strings from path.

        Args
        ---------------
        url (str)
        > The URL from the webBrowser COMP


        Returns
        ---------------
        url (str)
        > URL with all query strings removed
        '''
        return urllib.parse.urljoin(url, urllib.parse.urlparse(url).path)

    def load_new_selection(self):
        '''
        Load selection

        '''

        if NavController.nav_debug.eval():
            debug("loading new selection")

        NavController.loading_view.par['display'] = True
        self.display_loading_screen()

    def display_loading_screen(self):
        '''
        Display loading screen during load

        '''

        if NavController.nav_debug.eval():
            debug("starting timer")

        NavController.trans_timer.par.active = True
        NavController.trans_timer.par.start.pulse()

    def load_remote_tox(self):
        '''
        Load Remote TOX

        '''

        remoteTox = self.selected_remote_tox

        try:

            asset = urllib.request.urlopen(remoteTox)
            tox = asset.read()
            loadedTox = NavController.disp_buffer.loadByteArray(tox)
            loadedTox.par['display'] = True
            loadedTox.nodeX = 0
            loadedTox.nodeY = 0
            loadedTox.par.hmode = 1
            loadedTox.par.vmode = 1
            self.update_browser()

        except Exception as e:
            if NavController.nav_debug.eval():
                debug(e)
            else:
                pass

    def clear_view(self):
        '''
        Clear display buffer of any ops

        '''

        for each in NavController.disp_buffer.findChildren(depth=1):
            each.destroy()

    def set_timer_play(self, playVal):
        '''
        Start timer's play

        Args
        ---------------
        playVal (bool)
        > The play parameter value to be passed to the timer CHOP

        '''
        NavController.trans_timer.par['play'] = playVal

    def toggle_settings(self):
        '''
        Toggle display par for settings
        '''
        NavController.settings_view.par.display = (0 if NavController.settings_view.par.display else 1)

    def query_string_parse(self, url):
        '''
        Parse query string

        Args
        ---------------
        url (str)
        > The URL from the webBrowser COMP

        Returns
        ---------------
        qs_result (query string obj)
        > the resulting query string from a URL
        '''

        parse_result = urllib.parse.urlparse(url).query
        qs_result = urllib.parse.parse_qs(parse_result)
        return qs_result

    def update_browser(self):
        '''
        Update webrender TOP / Web Browser  
        '''
        url = self.selected_remote_tox
        NavController.web_browser.par['Address'] = url

    def Navigator_reset(self):
        '''
        Reset Navigator to default state
        '''

        self.clear_view()
        default = parent.Navigator.op('container_ui/container_view/container_loading/container_start')
        copy_op = NavController.disp_buffer.copy(default)
        copy_op.nodeX = 0
        copy_op.nodeY = 0
        copy_op.par.display = True
        copy_op.par.opacity = 1
        copy_op.par.Text = "Navigator"

    def On_page_load(self):
        '''
        Send JS command to browser on load
        '''
        NavController.web_browser.par.Javascript = "document.getElementsByClassName('td-navigator-shown')[0].classList.remove('td-navigator-shown')"
        run('parent.Navigator.op("container_ui/container_nav_and_text").op("webBrowser").par.Sendjavascript.pulse()')
        pass

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

    #####################################################
    ## Timer Functions
    #####################################################

    def Timer_segment_enter(self, **kwargs):
        '''
        timer onSegmentEnter callback       

        Args
        ---------------
        **kwargs (keyword args)
        > Timer op key word args


        '''
        timerOp = kwargs.get('timerOp')
        segment = kwargs.get('segment')
        interrupt = kwargs.get('interrupt')

        if segment > 0:
            timerOp.par.play = False
            self.clear_view()
            run(self.load_remote_tox(), delayFrames = 1)
            timerOp.par.play = True

    def Timer_on_done(self, **kwargs):
        '''
        timer onDone callback

        Args
        ---------------
        **kwargs (keyword args)
        > Timer op key word args

        '''
        NavController.loading_view.par['display'] = False
        kwargs.get('timerOp').par.active = False
        pass


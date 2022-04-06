#####################################################
# imports
#####################################################

import urllib
import requests

#####################################################
# action spec
#####################################################
'''
actionable:bool
action:function
keyWordArgsDefinedByFunction:value


examples:
?actionable=1&action=load_tox&remotePath=someUrl

?actionable=1&action=open_floating_network

?actionable=1&action=open_in_browser

?actionable=1&action=update_td_pars&somePar=someVal
'''

class NavController:

    #####################################################
    # class variables
    #####################################################

    NavigatorCOMP   = parent.Navigator
    NavigatorCOMP = parent.Navigator
    navAndText = parent.Navigator.op('container_ui/container_nav_and_text')
    view = parent.Navigator.op('container_ui/container_view')
    linkManifest = parent.Navigator.op('table_manifestBuffer')
    lister = parent.Navigator.op('container_ui/container_nav_and_text/container_nav/lister')
    webBrowser = parent.Navigator.op('container_ui/container_nav_and_text/webBrowser')
    loadingView = parent.Navigator.op('container_ui/container_view/container_loading')
    settingsView = parent.Navigator.op('container_ui/container_view/container_settings')
    dispBuffer = parent.Navigator.op('container_ui/container_view/container_display_buffer')
    transTimer = parent.Navigator.op('container_ui/container_view/container_loading/timer1')

    nav_debug = parent.Navigator.par.Debug


    #####################################################
    # functions
    #####################################################

    def __init__(self, ownerOp):
        '''Updates webrender TOP URL
        '''
        self.Owner_op = ownerOp

    def Url_update(self, url, debug=True):
        '''Updates webrender TOP URL
        '''
        qs_result = self.querry_string_parse(url)
        key_list = [key for key in qs_result.keys()]

        # check for the actionable arg
        if qs_result.get('actionable', [0])[0] == '1':
            self._web_action(qs_result)
        else:
            pass

        pass

    def get_current_example(self):
        '''Get current example
        '''
        current_example = parent.Navigator.op('container_ui/container_view/container_display_buffer').findChildren(depth=1)[0]
        return current_example

    def remove_qs_from_path(self):
        '''Remove query string from URL path
        '''
        if NavController.nav_debug.eval():
            debug("remove QS from Path")

        address = NavController.webBrowser.par.Address.eval()
        cleanAddress = self.clean_url(address)
        NavController.webBrowser.par.Address = cleanAddress
    
    def clean_url(self, url):
        '''Clean up a URL
        '''
        return urllib.parse.urljoin(url, urllib.parse.urlparse(url).path)

    def load_new_selection(self):
        '''Load selection
        '''
        if NavController.nav_debug.eval():
            debug("loading new selection")

        NavController.loadingView.par['display'] = True
        self.display_loading_screen()

    def display_loading_screen(self):
        '''Display loading screen during load
        '''
        if NavController.nav_debug.eval():
            debug("starting timer")

        NavController.transTimer.par.active = True
        NavController.transTimer.par.start.pulse()

    def load_remote_tox(self):
        '''Load Remoate TOX
        '''
        remoteTox = NavController.NavigatorCOMP.fetch('selectedRemoteTox')

        try:

            asset = urllib.request.urlopen(remoteTox)
            tox = asset.read()
            loadedTox = NavController.dispBuffer.loadByteArray(tox)
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
        '''Clear display buffer of any ops
        '''
        for each in NavController.dispBuffer.findChildren(depth=1):
            each.destroy()

    def set_timer_play(self, playVal):
        '''Start timer's play 
        '''
        NavController.transTimer.par['play'] = playVal

    def toggle_settings(self):
        '''Toggle display par for settings
        '''
        NavController.settingsView.par.display = (0 if settingsView.par.display else 1)

    def querry_string_parse(self, url):
        '''Parse querry string
        '''
        parse_result = urllib.parse.urlparse(url).query
        qs_result = urllib.parse.parse_qs(parse_result)
        return qs_result

    def update_browser(self):
        '''Update webrender TOP / Web Browser
        '''
        url = NavController.NavigatorCOMP.fetch('selectedWebPage')
        NavController.webBrowser.par['Address'] = url

    def Navigator_reset(self):
        self.clear_view()
        default = parent.Navigator.op('container_ui/container_view/container_loading/container_start')
        copy_op = NavController.dispBuffer.copy(default)
        copy_op.nodeX = 0
        copy_op.nodeY = 0
        copy_op.par.display = True
        copy_op.par.opacity = 1
        copy_op.par.Text = "Navigator"

    def On_page_load(self):
        NavController.webBrowser.par.Javascript = "document.getElementsByClassName('td-navigator-shown')[0].classList.remove('td-navigator-shown')"
        run('parent.Navigator.op("container_ui/container_nav_and_text").op("webBrowser").par.Sendjavascript.pulse()')
        pass

    #####################################################
    ## ACTIONS Parser
    #####################################################

    def _web_action_map(self, action):
        print(action)
        action_map = {
            "load_tox" : self.load_tox,
            "open_floating_network" : self.open_floating_network,
            "open_in_browser" : self.open_in_browser,
            "update_td_pars" : self.update_td_pars
        }
        return action_map.get(action)

    def _web_action(self, qs_result):
        try:
            func = self._web_action_map(qs_result.get('action')[0])
            debug(func)
            func(qs_result)
        except Exception as e:
            if debug:
                print(e)
            else:
                pass       
        return 

    #####################################################
    ## ACTIONS 
    #####################################################

    def open_floating_network(self, qs_results):
        '''Opens Floating Network Window
        '''
        if NavController.nav_debug.eval():
            print("Open Floating Window")
        debug("running ope_floating")
        floating_pane = ui.panes.createFloating(name="Example")
        current_example = self.get_current_example()
        floating_pane.owner = current_example
        floating_pane.home()

        self.remove_qs_from_path()
        pass

    def update_td_pars(self, qs_results):
        '''Update TD parameters
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
        '''Load TOX from URL
        '''
        if NavController.nav_debug.eval():
            debug("loading remote")

        remote_tox = qs_results.get('remotePath')
        NavController.NavigatorCOMP.store('selectedRemoteTox', remote_tox[0])
        self.load_new_selection()
        self.remove_qs_from_path() 
        pass

    def open_in_browser(self, qs_results):
        '''Open URL in web browser
        '''
        address = NavController.webBrowser.par.Address.eval()
        ui.viewFile(address)
        self.remove_qs_from_path()

    #####################################################
    ## Timer Functions
    #####################################################

    def Timer_segment_enter(self, **kwargs):
        '''timer onSegmentEnter callback
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
        '''timer onDone callback
        '''
        NavController.loadingView.par['display'] = False
        kwargs.get('timerOp').par.active = False
        pass


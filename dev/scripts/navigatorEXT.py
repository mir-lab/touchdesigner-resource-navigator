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

class Navigator:

    #####################################################
    # class variables
    #####################################################

    NavigatorCOMP   = parent.Navigator
    navAndText      = NavigatorCOMP.op('container_ui/container_nav_and_text')
    view 		    = NavigatorCOMP.op('container_ui/container_view')
    linkManifest    = NavigatorCOMP.op('table_manifestBuffer')

    lister          = navAndText.op('container_nav/lister')
    webBrowser  	= navAndText.op('webBrowser')

    loadingView     = view.op('container_loading')
    settingsView    = view.op('container_settings')
    dispBuffer      = view.op('container_display_buffer')

    transTimer      = loadingView.op('timer1')

    nav_debug       = NavigatorCOMP.par.Debug

    #####################################################
    # functions
    #####################################################

    def url_update(self, url, debug=True):
        '''Updates webrender TOP URL
        '''
        qs_result = querry_string_parse(url)
        key_list = [key for key in qs_result.keys()]

        # check for the actionable arg
        if qs_result.get('actionable', [0])[0] == '1':

            # try our action as a function
            try:
                func = eval(qs_result.get('action')[0])
                func(qs_result)

            except Exception as e:
                if debug:
                    print(e)
                pass

        else:
            pass

        pass

    def open_floating_network(self, qs_results):
        '''Opens Floating Network Window
        '''
        if nav_debug.eval():
            print("Open Floating Window")

        floating_pane = ui.panes.createFloating(name="Example")
        current_example = get_current_example()
        floating_pane.owner = current_example
        floating_pane.home()

        remove_qs_from_path()
        pass

    def update_td_pars(self, qs_results):
        '''Update TD parameters
        '''
        target_op = get_current_example()
        exempt_keys = ['action', 'actionable']
        for each_par, each_val in qs_results.items():
            if each_par in exempt_keys:
                pass
            else:
                try:
                    target_op.par[each_par] = each_val[0]
                except Exception as e:
                    pass
            if nav_debug.eval():
                debug(each_par, each_val)

        remove_qs_from_path()
        pass

    def get_current_example(self):
        '''Get current example
        '''
        current_example = parent.Navigator.op('container_ui/container_view/container_display_buffer').findChildren(depth=1)[0]
        return current_example

    def open_in_browser(self, qs_results):
        '''Open URL in web browser
        '''
        address = webBrowser.par.Address.eval()
        ui.viewFile(address)
        remove_qs_from_path()

    def remove_qs_from_path(self):
        '''Remove query string from URL path
        '''
        if nav_debug.eval():
            debug("remove QS from Path")

        address = webBrowser.par.Address.eval()
        cleanAddress = clean_url(address)
        webBrowser.par.Address = cleanAddress
    
    def clean_url(self, url):
        '''Clean up a URL
        '''
        return urllib.parse.urljoin(url, urllib.parse.urlparse(url).path)

    def load_tox(self, qs_results):
        '''Load TOX from URL
        '''
        if nav_debug.eval():
            debug("loading remote")

        remote_tox = qs_results.get('remotePath')
        NavigatorCOMP.store('selectedRemoteTox', remote_tox[0])
        load_new_selection()
        remove_qs_from_path() 
        pass

    def load_new_selection(self):
        '''Load selection
        '''
        if nav_debug.eval():
            debug("loading new selection")

        loadingView.par['display'] = True
        display_loading_screen()

    def display_loading_screen(self):
        '''Display loading screen during load
        '''
        if nav_debug.eval():
            debug("starting timer")

        transTimer.par.active = True
        transTimer.par.start.pulse()

    def update_browser(self):
        '''Update webrender TOP / Web Browser
        '''
        url = NavigatorCOMP.fetch('selectedWebPage')
        webBrowser.par['Address'] = url

    def load_remote_tox(self):
        '''Load Remoate TOX
        '''
        remoteTox = NavigatorCOMP.fetch('selectedRemoteTox')

        try:

            asset = urllib.request.urlopen(remoteTox)
            tox = asset.read()
            loadedTox = dispBuffer.loadByteArray(tox)
            loadedTox.par['display'] = True
            loadedTox.nodeX = 0
            loadedTox.nodeY = 0
            loadedTox.par.hmode = 1
            loadedTox.par.vmode = 1
            update_browser()

        except Exception as e:
            if nav_debug.eval():
                debug(e)
            else:
                pass

    def clear_view(self):
        '''Clear display buffer of any ops
        '''
        for each in dispBuffer.findChildren(depth=1):
            each.destroy()

    def set_timer_play(self, playVal):
        '''Start timer's play 
        '''
        transTimer.par['play'] = playVal

    def toggle_settings(self):
        '''Toggle display par for settings
        '''
        settingsView.par.display = (0 if settingsView.par.display else 1)

    def querry_string_parse(self, url):
        '''Parse querry string
        '''
        parse_result = urllib.parse.urlparse(url).query
        qs_result = urllib.parse.parse_qs(parse_result)
        return qs_result

    def navigator_reset(self):
        clear_view()
        default = parent.Navigator.op('container_ui/container_view/container_loading/container_start')
        copy_op = dispBuffer.copy(default)
        copy_op.nodeX = 0
        copy_op.nodeY = 0
        copy_op.par.display = True
        copy_op.par.opacity = 1
        copy_op.par.Text = "Navigator"

    #####################################################
    ## Timer Functions
    #####################################################

    def timer_segment_enter(self, **kwargs):
        '''timer onSegmentEnter callback
        '''
        timerOp = kwargs.get('timerOp')
        segment = kwargs.get('segment')
        interrupt = kwargs.get('interrupt')

        if segment > 0:
            timerOp.par.play = False
            clear_view()
            run(load_remote_tox(), delayFrames = 1)
            timerOp.par.play = True

    def on_timer_done(self, **kwargs):
        '''timer onDone callback
        '''
        loadingView.par['display'] = False
        kwargs.get('timerOp').par.active = False
        pass


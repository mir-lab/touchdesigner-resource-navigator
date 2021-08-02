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

#####################################################
# module variables
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

#####################################################
# functions
#####################################################

def url_update(url, debug=True):
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

def open_floating_network(qs_results):
    print("Open Floating Window")

    floating_pane = ui.panes.createFloating(name="Example")
    current_example = get_current_example()
    floating_pane.owner = current_example
    floating_pane.home()

    remove_qs_from_path()
    pass

def update_td_pars(qs_results):
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
        print(each_par, each_val)
    remove_qs_from_path()
    pass

def get_current_example():
    current_example = parent.Navigator.op('container_ui/container_view/container_display_buffer').findChildren(depth=1)[0]
    return current_example

def open_in_browser(qs_results):
    address = webBrowser.par.Address.eval()
    ui.viewFile(address)

def remove_qs_from_path():
    print("remove QS from Path")

    address = webBrowser.par.Address.eval()
    cleanAddress = clean_url(address)
    webBrowser.par.Address = cleanAddress
 
def clean_url(url):
    return urllib.parse.urljoin(url, urllib.parse.urlparse(url).path)

def load_tox(qs_results):
    print("loading remote")

    remote_tox = qs_results.get('remotePath')
    NavigatorCOMP.store('selectedRemoteTox', remote_tox[0])
    load_new_selection()
    remove_qs_from_path() 
    pass

def load_new_selection():
    print("loading new selection")

    loadingView.par['display'] = True
    display_loading_screen()

def display_loading_screen():
    print("starting timer")

    transTimer.par.start.pulse()

def update_browser():
    url = NavigatorCOMP.fetch('selectedWebPage')
    webBrowser.par['Address'] = url

def load_remote_tox():
    remoteTox = NavigatorCOMP.fetch('selectedRemoteTox')

    try:

        asset 	    = urllib.request.urlopen(remoteTox)
        tox 	    = asset.read()
        loadedTox   = dispBuffer.loadByteArray(tox)
        loadedTox.par['display'] = True
        loadedTox.nodeX = 0
        loadedTox.nodeY = 0
        loadedTox.par.hmode = 1
        loadedTox.par.vmode = 1
        update_browser()

    except Exception as e:
        print(e)

def clear_view():
    for each in dispBuffer.findChildren(depth=1):
        each.destroy()

def set_timer_play(playVal):
    transTimer.par['play'] = playVal

def toggle_settings():
    settingsView.par.display = (0 if settingsView.par.display else 1)

def querry_string_parse(url):
    parse_result = urllib.parse.urlparse(url).query
    qs_result = urllib.parse.parse_qs(parse_result)
    return qs_result

#####################################################
## Timer Functions
#####################################################

def timer_segment_enter(**kwargs):
    timerOp = kwargs.get('timerOp')
    segment = kwargs.get('segment')
    interrupt = kwargs.get('interrupt')

    if segment > 0:
        timerOp.par.play = False
        clear_view()
        run(load_remote_tox(), delayFrames = 1)
        timerOp.par.play = True

def on_timer_done(**kwargs):
    loadingView.par['display'] = False
    pass


"""Web Browser COMP helpers
"""

Navigator = op.TDCN

def Zoom_update(zoom_level) -> None:
    """
    Update web render zoom level

    Args
    ---------------
    zoom_level (int)
    > The target zoom level for the webrender TOP
    """
    print(f"document.body.style.zoom = '{zoom_level}%'")
    Navigator.ext.NavController.web_browser.op('webrender1').executeJavaScript(f"document.body.style.zoom = '{zoom_level}%'")

def Zoom_increment(increment_val) -> None:
    """Increments zoom value"""
    prev_val = Navigator.NavigatorCOMP.par.Webrenderzoom.eval()
    Navigator.NavigatorCOMP.par.Webrenderzoom = increment_val + prev_val

def Zoom_reset(val) -> None:
    """Resets webbrowser soom"""
    Navigator.NavigatorCOMP.par.Webrenderzoom = val

def Resetnavigator(par):
    parent.Navigator.Navigator_reset()

def Webrenderzoom(par):
    parent.Navigator.Zoom_update(par.eval())

def Winopen(par):
    print(par)
    parent.Navigator.Floating_window(par)

def Winclose(par):
    print(par)
#####################################################
## PANE CONTROLS
#####################################################

def Save_tox_copy(self, par):
    if par.eval():
        print("Save TOX copy")

        disp_buffer = NavController.disp_buffer
        current_example = disp_buffer.findChildren(type=containerCOMP)[0]
        save_ready_tox = self._copy_current_example(current_example)

        tox_path = ui.chooseFile(
            load=False, 
            start=f"{current_example}.tox", 
            fileTypes=['tox'], 
            title='Save Current TOX')
        

        # set hmode, vmode, width, and height for containers
        if save_ready_tox.type == 'container':
            save_ready_tox.par.hmode = 0
            save_ready_tox.par.vmode = 0
            save_ready_tox.par.w = 1080
            save_ready_tox.par.h = 1080
        else:
            pass

        save_ready_tox.save(tox_path)
        save_ready_tox.destroy()

def Set_view(self, state, view_type):
    if state:
        example_pane = ui.panes['NavigatorExample']

        if view_type == 'panel':
            example_pane.owner = NavController.view
            example_pane.changeType(PaneType.PANEL)

        elif view_type == 'network':
            current_example = NavController.disp_buffer.findChildren(type=containerCOMP)[0]
            example_pane.owner = current_example
            example_pane.changeType(PaneType.NETWORKEDITOR)
            ui.panes['NavigatorExample'].home()
        
        elif view_type == 'floating':
            # TODO - complete floating window call
            debug("SET FLOATING")

        else:
            pass        

def _copy_current_example(self, example):
    copied_tox = op('/sys/quiet').copy(example)
    copied_tox.nodeX = 0
    copied_tox.nodeY = 200
    return copied_tox

def Win_close(self):
    ui.panes['Navigator'].close()
    ui.panes['NavigatorExample'].close()

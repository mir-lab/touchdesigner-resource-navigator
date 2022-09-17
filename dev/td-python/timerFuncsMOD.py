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


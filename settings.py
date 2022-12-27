class settings:
    def __init__(self, path, debug):
        ''' Settings initialization
        path : Application sub-domain
        debug: boolean, indicates whether debug-mode is on or not
        '''
        self.path = path
        self.debug = debug

# Sinlge object paradigm
settings = settings(path="/", debug=True)



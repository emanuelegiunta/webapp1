class settings:
    def __init__(self, path, debug):
        ''' Settings initialization
        path : Application sub-domain
        debug: boolean, indicates whether debug-mode is on or not
        '''
        self.path = path
        self.debug = debug

    def formatted_path(self):
        ''' Not very clean thing to let Jinja have a path without leading /
        '''
        return self.path[1:]

# Sinlge object paradigm
# `path` should end with a "/", eg: "/test/", "/mysite/app/"
settings = settings(path="/", debug=True)



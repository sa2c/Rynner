class RunManager:
    '''
    Run manager is a container for application hosts and run types
    '''

    def __init__(self, hosts=None, plugins=None):
        self.hosts = hosts
        self.plugins = plugins

        # hosts and plugins should not be None
        if self.hosts is None:
            self.hosts = []
        if self.plugins is None:
            self.plugins = []

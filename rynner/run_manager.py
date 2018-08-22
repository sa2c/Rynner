class RunManager:
    '''
    Run manager is a container for application hosts and run types
    '''

    def __init__(self, hosts=None, run_types=None):
        self.hosts = hosts
        self.run_types = run_types

        # hosts and run_types should not be None
        if self.hosts is None:
            self.hosts = []
        if self.run_types is None:
            self.run_types = []

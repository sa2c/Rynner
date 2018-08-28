class Datastore:
    def __init__(self, connection):
        self.connection = connection

    def store(self, plugin_id, run_id, **kwargs):
        raise NotImplementedError()

    def jobs(self, plugin_id):
        raise NotImplementedError()

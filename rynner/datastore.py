import os
import yaml


class Datastore:
    store_name = 'datastore.yaml'

    def __init__(self, connection):
        self.connection = connection

    def write(self, basedir, data):
        path = os.path.join(basedir, self.store_name)
        content = yaml.dump(data)
        self.connection.put_file_content(content, path)

    def read(self, basedir):
        path = os.path.join(basedir, self.store_name)
        content = self.connection.get_file_content(path)
        return yaml.load(content)

    def jobs(self, plugin_id):
        raise NotImplementedError()

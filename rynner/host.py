import fabric
from rynner.behaviour import InvalidContextOption


class Connection():
    def __init__(self, host, user):
        self.conn = fabric.Connection(host=host, user=user)

    def run_command(self, cmd, pwd=None):
        if pwd is not None:
            self.conn.cd(pwd)
        self.conn.run(cmd)

    def put_file(self, local_path, remote_path):
        self.conn.put(local_path, remote_path)

    def get_file(self, remote_path, local_path):
        self.conn.get(remote_path, local_path)

    def put_file_content(self, remote_path, content):
        raise NotImplementedError()


class Host:
    def __init__(self, behaviour, connection, datastore):
        self.connection = connection
        self.behaviour = behaviour
        self.datastore = datastore

    def upload(self, id, uploads):
        for upload in uploads:
            if len(upload) != 2:
                raise InvalidContextOption(
                    'invalid format for uploads options: {uploads}')
            self.connection.put_file(upload[0], upload[1])

    def parse(self, id, options):
        context = self.behaviour.parse(options)
        self.datastore.store(id, options)
        return context

    def run(self, id, context):
        isrunning = self.behaviour.run(self.connection, context)
        self.datastore.isrunning(id, isrunning)

    def type(self, string):
        return self.behaviour.type(string)

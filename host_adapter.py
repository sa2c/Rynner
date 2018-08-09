import fabric

# TODO HostAdapter.create_directory(string) => creates directory relative to base
# TODO init should take host,user, BASEDIR (i.e. directory every relative path is translated to)
# TODO connect should be deferred until required...
# TODO all paths should be relative to BASEDIR
# TODO put_file should have a relative=True default...and be absolute if specified


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


# TODO implement download. API: def download(id, uploads):
# TODO behaviour should check that upload completed before end
class HostAdapter:
    def __init__(self, behaviour, connection, datastore):
        self.connection = connection
        self.behaviour = behaviour
        self.datastore = datastore

    def upload(self, id, uploads):
        for upload in uploads:
            self.connection.put_file(upload[0], upload[1])

    def parse(self, options):
        return self.behaviour.parse(options)

    def run(self, id, options):
        self.datastore.store(id, options)
        isrunning = self.behaviour.run(self.connection, options)
        self.datastore.isrunning(id, isrunning)

    def type(self, string):
        return self.behaviour.type(string)

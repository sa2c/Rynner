import fabric
import io
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
        self.conn.put(io.StringIO(content), remote_path)


class Host:
    '''
    Host is initialized with
    - a Connection object (1 to 1 to ssh connection/remote server)
    - a 'behaviour': 1 to 1 to 'scheduler' (slurm, pbs...)
    - a datastore object which is used to store status

    It basically connects 'behaviour' and 'connection'
    '''

    def __init__(self, behaviour, connection, datastore):
        self.connection = connection
        self.behaviour = behaviour
        datastore.set_connection(connection)
        self.datastore = datastore

    def upload(self, id, uploads):
        '''
        Uploads files through the connection.
        '''
        for upload in uploads:
            if len(upload) != 2:
                raise InvalidContextOption(
                    'invalid format for uploads options: {uploads}')
            self.connection.put_file(upload[0], upload[1])

    def parse(self, id, options):
        '''
        Gets context from behaviour, which takes 'run options' as argument.
        Context is to be passed to the run method
        '''
        context = self.behaviour.parse(options)
        self.datastore.store(id, options)
        return context

    def run(self, id, context):
        isrunning = self.behaviour.run(self.connection, context,
                                       self._remote_path(id))
        self.datastore.isrunning(id, isrunning)

    def _remote_path(self, id):
        return str(id)

    def type(self, string):
        '''
        Gets type from behaviour and returns it.
        '''
        return self.behaviour.type(string)

    def jobs(self, run_type_id=None):
        return self.datastore.jobs(run_type_id)

    def update(self, run_type_id=None):
        self.datastore.update(run_type_id)

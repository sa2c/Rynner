import paramiko
import io
from rynner.behaviour import InvalidContextOption


class Connection():
    def __init__(self, logger, host, user=None, key_filename=None):
        self.logger = logger
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        #key = paramiko.RSAKey.from_private_key_file(rsa_file)
        self.log(
            f'connecting: host={host}, username={user}, key_filename={key_filename}'
        )
        self.log(f'connected {self.ssh}')
        self.ssh.connect(host, username=user, key_filename=key_filename)
        self.log('opening sftp')
        self.sftp = self.ssh.open_sftp()

    def run_command(self, cmd, pwd=None):
        if pwd is not None:
            cd_cmd = 'cd {pwd}'
            cmd = '; '.join([cd_cmd, cmd])

        self.log(f'running command ({self.ssh}): {cmd}')

        stdin, stdout, stderr = self.ssh.exec_command(cmd)

        exit_status = stdout.channel.recv_exit_status()
        out = stdout.read().decode().split('\n')
        err = stderr.read().decode().split('\n')

        self.log(f'Standard Output:\n{out}')
        self.log(f'Standard Error:\n{err}')

        return (exit_status, out, err)

    def put_file(self, local_path, remote_path):
        self.log(f'transferring file: {local_path} -> {remote_path}')
        self.sftp.put(local_path, remote_path)

    def put_file_content(self, content, remote_path):
        self.log(f'''
Creating remote file:
* File path:
{remote_path}
* File content:
{content}
        ''')

        file = self.sftp.file(remote_path, mode='w')
        file.write(content)
        file.flush()

        self.log(f'File {remote_path} written')

    def get_file(self, remote_path, local_path):
        self.log(f'Transfer remote file: {remote_path} -> {local_path}')
        self.sftp.get(remote_path, local_path)
        self.log(f'File {remote_path} transferred')

    def _ensure_dir(self, remote_path):
        parts = remote_path.split('/')
        if (len(parts) > 1):
            dir = '/'.join(parts[0:-1])
            self.sftp.mkdir(dir)

    def log(self, message):
        self.logger.info(message)


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

    def jobs(self, plugin_id=None):
        return self.datastore.jobs(plugin_id)

    def update(self, plugin_id=None):
        self.datastore.update(plugin_id)

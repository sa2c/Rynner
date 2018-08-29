import paramiko
import os
from rynner.behaviour import InvalidContextOption


class Connection():
    def __init__(self, logger, host, user=None, rsa_file=None):
        self.logger = logger
        self.host = host
        self.user = user
        self.rsa_file = rsa_file
        self.ssh = None
        self.log(f'created connection object')

    def run_command(self, cmd, pwd=None):
        self._ensure_connected()
        if pwd is not None:
            self._ensure_dir(pwd)
            cd_cmd = f'cd {pwd}'
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
        self._ensure_connected()
        self._ensure_dir(remote_path)
        self.log(f'transferring file: {local_path} -> {remote_path}')
        self.sftp.put(local_path, remote_path)

    def get_file_content(self, remote_path):
        self._ensure_connected()
        file = self.sftp.file(remote_path, mode='r')
        try:
            contents = file.read()
        except:
            pass
        file.close()

        return contents

    def put_file_content(self, content, remote_path):
        self._ensure_connected()
        self._ensure_dir(remote_path)
        self.log(
            f' Creating remote file:\n* File path:\n{remote_path}\n* File content:\n{content}'
        )

        file = self.sftp.file(remote_path, mode='w')
        file.write(content)
        file.flush()

        self.log(f'File {remote_path} written')

    def get_file(self, remote_path, local_path):
        self._ensure_connected()
        self.log(f'Transfer remote file: {remote_path} -> {local_path}')
        self.sftp.get(remote_path, local_path)
        self.log(f'File {remote_path} transferred')

    def _ensure_connected(self):
        if self.ssh is None:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            key = paramiko.RSAKey.from_private_key_file(self.rsa_file)
            self.log(
                f'connecting: host={self.host}, username={self.user}, key={self.rsa_file}'
            )
            self.ssh.connect(self.host, username=self.user, pkey=key)
            self.log(f'connected {self.ssh}')
            self.log('opening sftp')
            self.sftp = self.ssh.open_sftp()

    def _ensure_dir(self, remote_path, is_directory=False):
        """
        recursively create directories if they don't exist
        remote_path - remote path to create.
        is_directory - specifies if remote path is a directory
        """

        dirs_ = []

        if is_directory:
            dir_ = remote_path
        else:
            dir_, basename = os.path.split(remote_path)

        while len(dir_) > 1:
            dirs_.append(dir_)
            dir_, _ = os.path.split(dir_)

        if len(dir_) == 1 and not dir_.startswith("/"):
            dirs_.append(dir_)  # For a remote_path path like y/x.txt

        while len(dirs_):
            dir_ = dirs_.pop()
            try:
                self.sftp.stat(dir_)
            except:
                self.log(f'creating directory {dir_}')
                self.sftp.mkdir(dir_)

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
        self.datastore = datastore

    def upload(self, plugin_id, run_id, uploads):
        '''
        Uploads files through the connection.
        '''
        for upload in uploads:
            if len(upload) != 2:
                raise InvalidContextOption(
                    'invalid format for uploads options: {uploads}')
            local, remote = upload

            basedir = self._remote_basedir(plugin_id, run_id)
            basedir = os.path.join(basedir, remote)
            self.connection.put_file(local, remote)

    def parse(self, plugin_id, run_id, options):
        '''
        Gets context from behaviour, which takes 'run options' as argument.
        Context is to be passed to the run method
        '''
        context = self.behaviour.parse(options)

        # set data to store in context['datastore']
        options['plugin_id'] = plugin_id
        options['run_id'] = run_id
        context['datastore'] = options

        return context

    def run(self, plugin_id, run_id, context):
        exit_status = self.behaviour.run(
            self.connection, context, self._remote_basedir(plugin_id, run_id))

        basedir = self._remote_basedir(plugin_id, run_id)
        self.datastore.store(basedir, context)

    def _remote_basedir(self, plugin_id, run_id):
        return os.path.join("rynner", plugin_id, run_id)

    def type(self, string):
        '''
        Gets type from behaviour and returns it.
        '''
        return self.behaviour.type(string)

    def jobs(self, plugin_id=None):
        return self.datastore.jobs(plugin_id)

    def update(self, plugin_id=None):
        self.datastore.update(plugin_id)

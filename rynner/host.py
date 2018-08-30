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

        self.log(f'run command ({self.ssh}):\n{cmd}')

        stdin, stdout, stderr = self.ssh.exec_command(cmd)

        exit_status = stdout.channel.recv_exit_status()
        out = stdout.read().decode()
        err = stderr.read().decode()

        self.log(f'Standard Output:\n{out}')
        self.log(f'Standard Error:\n{err}')

        return (exit_status, out, err)

    def put_file(self, local_path, remote_path):
        self._ensure_connected()
        self._ensure_dir(remote_path)
        self.log(f'transferring file:\n{local_path} -> {remote_path}')
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

    def list_dir(self, remote_path):
        self._ensure_connected()
        return self.sftp.listdir(remote_path)

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
    Host object abstracts the interface between the plugin
    and a remote machine.
    '''

    def __init__(self, behaviour, connection, datastore):
        '''
        arguments:
            connection : a rynner Connection object
            behaviour : a rynner Behaviour object
            datastore : a rynner Datastore object
        '''
        self.connection = connection
        self.behaviour = behaviour
        self.datastore = datastore
        self._cached_runs = {}  #NoUT

    def upload(self, plugin_id, run_id, uploads):
        '''
        Uploads files using connection.
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
        Ask behaviour to build a context object from the options supplied by
        calls to RunManager.
        '''
        context = self.behaviour.parse(options)

        return context

    def run(self, plugin_id, run_id, context):
        '''
        Run a job for a context, which was returned previously from a call to
        self.parse. Details of creating a job on a remote machine according to
        the context object is delegated to behaviour object.
        '''
        exit_status = self.behaviour.run(
            self.connection, context, self._remote_basedir(plugin_id, run_id))

    def store(self, plugin_id, run_id, data):
        '''
        Persists data for a run using the datastore object
        '''
        basedir = self._remote_basedir(plugin_id, run_id)
        self.datastore.write(basedir, data)

    def _remote_basedir(self, plugin_id, run_id=''):
        '''
        Returns the remote base directory. Typically a working
        directory of a run on the remote filesystem.
        '''
        return os.path.join("rynner", plugin_id, run_id)

    def type(self, string):
        '''
        Gets type from this behaviour and returns it.
        '''
        return self.behaviour.type(string)

    def jobs(self, plugin_id=None):
        '''
        Uses the datastore to return a list of all data for jobs
        for a given plugin.
        '''
        return self._cached_runs

    def update(self, plugin_id):
        '''
        Triggers an update of job data from datastore
        '''
        basedir = self._remote_basedir(plugin_id)
        all_ids = self.datastore.all_job_ids(basedir)
        new_ids = {
            i: self._remote_basedir(plugin_id, i)
            for i in all_ids if i not in self._cached_runs.keys()
        }

        new_runs = self.datastore.read_multiple(new_ids)

        self._cached_runs.update(new_runs)

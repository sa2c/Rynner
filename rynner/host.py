import paramiko, os, yaml
from rynner.host_patterns import host_patterns
from rynner.pattern_parser import PatternParser, InvalidContextOption
from rynner.datastore import Datastore
from PySide2.QtCore import QObject, Signal
from logging import Logger


class Connection():
    '''A class representing the connection to a cluster frontend.

    Contains methods to run commands on the remote machine, move files to and
    from the remote machine, query the remote filesystem.

    '''

    def __init__(self, logger, host, user=None, rsa_file=None):
        '''
        Parameters
        ----------
        `logger` : 
           A :class:`Logger object<rynner.log.Logger>`.
        `host` : string
           A string containing the name of the host.
        `user` : string
           User name for the SSH connection.
        `rsa_file` : string
           Name of the file of the private SSH key.

        '''
        self.logger = logger
        self.host = host
        self.user = user
        self.rsa_file = rsa_file
        self.ssh = None
        self.log(f'created connection object')

    def run_command(self, cmd, pwd=None):
        '''
        Parameters
        ----------
        `cmd` : string
           The command to execute.
        `pwd` : string, optional
           The working directory for the command.
        '''
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
        '''Transfer file from `local_path` to `remote_path`'''
        self._ensure_connected()
        self._ensure_dir(remote_path)
        self.log(f'transferring file:\n{local_path} -> {remote_path}')
        self.sftp.put(local_path, remote_path)

    def get_file_content(self, remote_path):
        '''Read remote file and return its content.'''
        self._ensure_connected()
        file = self.sftp.file(remote_path, mode='r')
        try:
            contents = file.read()
        except:
            pass
        file.close()

        return contents

    def put_file_content(self, content, remote_path):
        '''Write content to remote file.'''
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
        '''Transfer file from `remote_path` to `local_path`.'''
        self._ensure_connected()
        self.log(f'Transfer remote file: {remote_path} -> {local_path}')
        self.sftp.get(remote_path, local_path)
        self.log(f'File {remote_path} transferred')

    def dir_exists(self, remote_path):
        '''Returns True if `remote_path` exists, False otherwise.'''
        try:
            self.sftp.stat(remote_path)
            return True
        except IOError:
            return False

    def list_dir(self, remote_path):
        '''Returns a list of directories at the `remote_path`.'''

        self._ensure_connected()
        self.log(f'listing directory: {remote_path}')
        if self.dir_exists(remote_path):
            return self.sftp.listdir(remote_path)
        else:
            return []

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


class Host(QObject):
    '''A representation of a remote host and a connection to it.

    '''

    runs_updated = Signal(dict)

    def __init__(self, pattern_parser, connection, datastore):
        '''
        Parameters
        ----------
            `pattern_parser` : rynner PatternParser
                See :class:`PatternParser<rynner.pattern_parser.PatternParser>`.
            `connection` : rynner Connection
                See :class:`Connection <rynner.host.Connection>`.
            `datastore` : rynner Datastore
                See :class:`Datastore<rynner.datastore.Datastore>`.
        '''
        self.connection = connection
        self.pattern_parser = pattern_parser
        self.datastore = datastore
        self._cached_runs = {}  #NoUT

        super().__init__(parent=None)

    def upload(self, plugin_id, run_id, uploads):
        '''
        Uploads files using the connection to the remote host.

        Parameters
        ----------
        `plugin_id` :
           Plugin identifier (see :func:`Plugin constructor<rynner.plugin.Plugin.__init__>`)
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
        Ask pattern_parser to build a context object from the options supplied by
        calls to :class:`~rynner.run.RunManager`.
        '''
        context = self.pattern_parser.parse(options)

        return context

    def run(self, plugin_id, run_id, context):
        '''
        Run a job for a context, which was returned previously from a call to
        self.parse. Details of creating a job on a remote machine according to
        the context object is delegated to pattern_parser object.
        '''
        exit_status = self.pattern_parser.run(
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
        Gets type from this pattern_parser and returns it.
        '''
        return self.pattern_parser.type(string)

    def runs(self, plugin_id):
        '''
        Uses the datastore to return a list of all data for jobs
        for a given plugin.
        '''
        if plugin_id in self._cached_runs.keys():
            return self._cached_runs[plugin_id]
        else:
            return []

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

        # update cache with new runs
        if plugin_id not in self._cached_runs.keys():
            self._cached_runs[plugin_id] = {}

        self._cached_runs[plugin_id].update(new_runs)

        # get queue
        qids = [data['qid'] for data in self._cached_runs[plugin_id].values()]
        queue = self.get_queue(qids)

        # merge queue info into all cached run data
        for run_data in self._cached_runs[plugin_id].values():
            qid = run_data['qid']
            if qid in queue.keys():
                run_data['queue'] = queue[qid]

        self.runs_updated.emit(self._cached_runs)

    def get_queue(self, jids):
        raise NotImplementedError(
            "method get_queue should be implemented in subclass")


class GenericClusterHost(Host):
    ''' A representation of a cluster frontend.

    '''
    def __init__(self,
                 host,
                 username,
                 rsa_file,
                 host_pattern,
                 submit_cmd,
                 defaults=[]):

        self.logger = Logger('host-logger')

        pattern_parser = PatternParser(host_pattern, submit_cmd, defaults)

        connection = Connection(
            self.logger, host, user=username, rsa_file=rsa_file)

        datastore = Datastore(connection)

        super().__init__(pattern_parser, connection, datastore)


class SlurmHost(GenericClusterHost):
    ''' A convenient subclass of :class:`~rynner.host.GenericClusterHost`
    for a Slurm-managed cluster frontend.'''

    def __init__(self, domain, username, rsa_file):

        submit_cmd = 'sbatch jobcard | sed "s/Submitted batch job//" > qid'
        host_pattern = host_patterns['slurm']

        super().__init__(domain, username, rsa_file, host_pattern, submit_cmd)

    def get_queue(self, jids):
        fields = ['JobID', 'NCPUS', 'NNodes', 'State', 'TimeLimit', 'Elapsed']
        delim = '|&|'

        cmd = f"sacct -j {','.join(jids)} -n -o {','.join(fields)} -p --delimiter='{delim}'"
        exitstatus, stdout, stderr = self.connection.run_command(cmd)

        data = {}

        for line in stdout.split('\n'):
            # skip empty lines
            if len(line) == 0:
                continue

            field_values = line.split(delim)
            jid = field_values[0]

            if 'batch' not in jid and 'extern' not in jid:
                data[jid] = {}
                for index in range(1, len(fields)):
                    data[jid][fields[index]] = field_values[index]

        return data


class PBSHost(GenericClusterHost):
    ''' A convenient subclass of :class:`~rynner.host.GenericClusterHost`
    for a PBS-managed cluster frontend.'''

    def __init__(self, domain, username, rsa_file):

        submit_cmd = 'qsub jobcard > qid'
        host_pattern = host_patterns['pbs']

        super().__init__(domain, username, rsa_file, host_pattern, submit_cmd)

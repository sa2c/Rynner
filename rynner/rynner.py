import uuid
import os


class Rynner:

    StatusRunning = 'RUNNING'
    StatusCreated = 'CREATED'
    StatusSubmitted = 'SUBMITTED'
    StatusCancelled = 'CANCELLED'

    def __init__(self, provider, datastore):
        self.provider = provider
        self.datastore = datastore
        self._runs = []

    def create_run(self, script, uploads=None, downloads=None, namespace=None):
        if not uploads:
            uploads = []

        if not downloads:
            downloads = []

        uid = str(uuid.uuid1())

        run = {
            'id': uid,
            'remote-dir': self._remote_dir(namespace, uid),
            'uploads': uploads,
            'downloads': downloads,
            'script': script,
            'status': Rynner.StatusSubmitted
        }

        self._runs.append(run)

        return run

    def _remote_dir(self, namespace, uid):
        if namespace:
            path = os.path.join(namespace, uid)
        else:
            path = str(uid)

        return path

    def _parse_paths(self, file_transfers):
        for file_transfer in file_transfers:
            if type(file_transfer) == str:
                src = file_transfer
                dest, _ = os.path.split(file_transfer)

            elif len(file_transfer):
                src, dest = file_transfer
            else:
                raise InvalidContextOption(
                    'invalid format for uploads options: {uploads}')

        if dest == '':
            dest = '.'

        return src, dest

    def upload(self, run):
        '''
        Uploads files using connection.
        '''

        uploads = run['uploads']

        if len(uploads) > 0:
            src, dest = self._parse_paths(uploads)

            self.provider.channel.push_file(src, dest)

    def download(self, run):
        '''
        Uploads files using connection.
        '''

        downloads = run['downloads']

        if len(downloads) > 0:
            src, dest = self._parse_paths(downloads)

            self.provider.channel.pull_file(src, dest)

    def submit(self, run):
        run['qid'] = self.provider.submit(run['script'], 1)
        run['status'] = Rynner.StatusSubmitted

    def cancel(self, run):
        run['qid'] = self.provider.cancel(run['script'], 1)
        run['status'] = Rynner.StatusCancelled

    def _finished_since_last_update(self):

        qids = [r['qid'] for r in self._runs]
        status = self.provider.status(qids)

        return [
            run for index, run in enumerate(self._runs)
            if run['status'] == Rynner.StatusRunning
            and status[index] == Rynner.StatusRunning
        ]

    def runs(self):
        self.update_runs(self._runs)
        return self._runs

    def update_runs(self, runs):
        '''
        Triggers an update of job data from datastore
        '''

        runs = self._finished_since_last_update()
        #infos = self.provider.info(runs)
        infos = runs

        for index, run in enumerate(runs):
            run['info'] = infos[index]


#def get_info_slurm(self, jids):
#    fields = ['JobID', 'NCPUS', 'NNodes', 'State', 'TimeLimit', 'Elapsed']
#    delim = '|&|'
#
#    cmd = f"sacct -j {','.join(jids)} -n -o {','.join(fields)} -p --delimiter='{delim}'"
#    exitstatus, stdout, stderr = self.connection.run_command(cmd)
#
#    data = {}
#
#    for line in stdout.split('\n'):
#        # skip empty lines
#        if len(line) == 0:
#            continue
#
#        field_values = line.split(delim)
#        jid = field_values[0]
#
#        if 'batch' not in jid and 'extern' not in jid:
#            data[jid] = {}
#            for index in range(1, len(fields)):
#                data[jid][fields[index]] = field_values[index]
#
#    return data

from libsubmit import SSHChannel
from libsubmit.providers.slurm.slurm import SlurmProvider
from rynner.rynner import Rynner


class MySlurmProvider(SlurmProvider):
    def info(self, jids):
        fields = ['JobID', 'NCPUS', 'NNodes', 'State', 'TimeLimit', 'Elapsed']
        delim = '|&libsubmit&|'

        cmd = f"sacct -j {','.join(jids)} -n -o {','.join(fields)} -p --delimiter='{delim}'"
        exitstatus, stdout, stderr = self.channel.execute_wait(cmd)

        data = []

        for line in stdout.split('\n'):
            # skip empty lines
            if len(line) == 0:
                continue

            field_values = line.split(delim)
            jid = field_values[0]

            if 'batch' not in jid and 'extern' not in jid:
                data.append({
                    fields[index]: field_values[index]
                    for index in range(1, len(fields))
                })

        return data


provider = MySlurmProvider(
    'compute',
    channel=SSHChannel(
        hostname='sunbird.swansea.ac.uk',
        username='s.mark.dawson',
        script_dir='/tmp',
    ),
    nodes_per_block=1,
    tasks_per_node=1,
    init_blocks=1,
    max_blocks=1,
)

datastore = None
rynner = Rynner(provider)
run = rynner.create_run(
    script='cat Makefile > tmps', uploads=['Makefile'], downloads=['tmps'])
rynner.upload(run)
print('upload')
print(run)
rynner.submit(run)
print('submit')
print(run)

runs = [run]
rynner.update(runs)
print('runs')
print(runs)

rynner.download(run)

from libsubmit import SSHChannel
from libsubmit.providers.slurm.slurm import SlurmProvider
from rynner.rynner import Rynner

provider = SlurmProvider(
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
rynner = Rynner(provider, datastore)
run = rynner.create_run(
    script='cat Makefile > tmps', uploads=['Makefile'], downloads=['tmps'])
rynner.upload(run)
print('upload')
print(run)
rynner.submit(run)
print('submit')
print(run)

runs = rynner.runs()
print('runs')
print(runs)

rynner.download(run)

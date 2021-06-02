from parsl.channels import SSHChannel
from parsl.providers.slurm.slurm import SlurmProvider
from rynner.rynner import Rynner

provider = SlurmProvider(
    'compute',
    channel=SSHChannel(
        hostname='sunbird.swansea.ac.uk',
        username='s.user.name',
        script_dir='/tmp'
    ),
    nodes_per_block=1,
    # tasks_per_node=1,  # fixme doesnt exist anymore?
    init_blocks=1,
    max_blocks=1,
)

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

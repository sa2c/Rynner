from parsl.channels import SSHChannel
from parsl.providers.slurm.slurm import SlurmProvider
from rynner.rynner import Rynner


username = input("Enter your username: ")
domain = input("Enter the domain: ")

connect_ = input(f'Connect as {username} at {domain}? [Yy/Yes/No/Nn]:')
if connect_.lower() not in ('y', 'yes', ''):
    print('No connection established, exiting.')
    exit(1)
else:
    provider = SlurmProvider(
        'compute',
        channel=SSHChannel(
            hostname=domain,
            username=username,
            script_dir='/tmp'
        ),
        nodes_per_block=1,
        # tasks_per_node=1,  # fixme doesn't exist anymore?
        init_blocks=1,
        max_blocks=1
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


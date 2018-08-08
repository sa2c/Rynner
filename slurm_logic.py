slurm_options = {
    'walltime': '#SBATCH --time={}',
    'memory': '#SBATCH --memory={}',
    'num_nodes': '#SBATCH --nodes={}',
    'runner_args': '#SBATCH --runner_args={}'
}

# TODO - things like bandwidth are options which are left out at this stage, should i seperate them in the run object? or in the runner? or handle them here.


def submit(self, path, scheduler_options, host_adapter):
    ''' creates and runs the jobcard '''

    jc = ''
    for option, value in options.items():
        method = getattr(self, option)
        jc += slurm_options[value].format(*value)

    for argument, value in scheduler_options.items():
        jc += f'#SLURM {argument} : {value}'

    host_adapter.put_file_contents(directory / jobcard, jc)
    id = host_adapter.run_command(submit_cmd)

    return id


# def submit(self, jobcard, options):
#     pass

# Run
#    * calls get_context on behaviour
#    * maps all options onto behaviour (rather than options)
#    * passes the same context every time
#    * submits the job using behaviour.submit

# => from data['runner'] or passed in manually? Needs a string representation of host_adapter to serialize (should be easy, create a UUID and store it on the cluster => combine with something in case duplicate ).

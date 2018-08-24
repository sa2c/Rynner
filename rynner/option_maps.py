#!/usr/bin/env python3
'''
In this file, various 'option_map' objects for the different schedulers are
written.

NOTES:
In many cases, there are conflicting/redundant ways to require resources.
1. --nodes/--ntasks-per-node/--ntasks : there are some nuances here, but we assume 
   cases nnodes = ceil(ntasks/ntasks-per-node)
2. --mem/--mem-per-cpu : these are mutually exclusive. We assume 1 task per core.
'''

slurm1711_option_map = [
    ('#SBATCH --job-name={}', 'name'),
    # this is 'share' in older versions of slurm
    ('#SBATCH --oversubscribe', 'oversubscribe'),
    ('#SBATCH --output={}', 'output_file'),
    ('#SBATCH --mem-per-cpu={}', 'memory_per_task_MB'),  # MB
    ('#SBATCH --ntasks={}', 'ntasks'),
    ('#SBATCH --ntasks-per-node={}', 'ntasks_per_node'),
    ('#SBATCH --gres=gpu:{}', 'ngpus'),
    # slurm accepts either this format or minutes
    ('#SBATCH --time={}', 'runtime_HMS'),
    ('#SBATCH --partition={}', 'queue'),
    ('#SBATCH --account={}', 'account')
]

# obtained from here
# https://hpcc.usc.edu/support/documentation/pbs-to-slurm/
# and from the pbs and pbs_resources man pages.
pbs_option_map = [
    ('#PBS -N={}', 'name'),
    ('#PBS -l placement=shared ', 'oversubscribe'),
    ('#PBS -o {}', 'output_file'),
    ('#PBS -l pmem={}mb', 'memory_per_task_MB'),  # MB
    ('#PBS -l procs={}', 'ntasks'),
    ('#PBS -l ppn={}', 'ntasks_per_node'),
    ('#PBS -l ngpus={}', 'ngpus'),
    # pbs accepts either this format or seconds
    ('#PBS -l walltime={}', 'runtime_HMS'),
    ('#PBS -q {}', 'queue'),
    ('#PBS -A {}', 'account')
]

#!/usr/bin/env python3
'''In this file, various patterns for matching host options for the different
schedulers are written. The following "pattern dictionaries" consist of fixed
numbers of key-value pair that are needed to convert the from an intermediate
representation used in the Rynner framework to the language used by a particular
version of a scheduler. The intermediate representation cannot be as expressive
and flexible as the specific scheduler languages, but it should be convenient.

The system is flexible enough to allow callables as values in the pattern
dictionary, in case it is not possible to ha a one-to-one correspondence
between the Rynner framework "intermediate representation" and the language of
a scheduling system.

These sets of patterns are collected in the :data:`host_patterns` dictionary,
the keys of which are the scheduling system names.

Here is the list of keys that are allowed in each of the pattern dictionaries:

   #. `account` : for accounting purposes.
   #. `memory_per_task_MB` : memory needed by each task in MB
   #. `name` : The name for the job that will be used by the scheduler.
   #. `ngpus` : the number of gpus needed by the job
   #. `ntasks_per_node` : the number of tasks to launch on each node. This will
       of course depend on the hardware of the cluster used.
   #. `ntasks` : the total number of MPI tasks that need to be launched.
   #. `output_file` : the file where the standard output (and error) of the job
       will be written.
   #. `oversubscribe` : In case the job does not need to fully use one node, if
       the cluster setup supports it, it is possible to allow your job to share
       the node with another job. This can be beneficial to reduce queue
       waiting time.
   #. `queue` : The queue/partition to run thr job on.
   #. `runtime_HMS` : the requested walltime in the HH:MM:SS format. H can be
       any positive number.

In many cases, there are conflicting/redundant ways to require resources.
   1. --nodes/--ntasks-per-node/--ntasks : there are some nuances here, but we assume 
      nnodes = ceil(ntasks/ntasks-per-node)
   2. --mem/--mem-per-cpu : these are mutually exclusive. We assume 1 task per core.

'''

slurm1711_patterns = [
    ('#SBATCH --job-name={}', 'name'),
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

# in older versions of SLURM '--share' was used instead of '--oversubscribe'
slurm1509_patterns = [
    ('#SBATCH --job-name={}', 'name'),
    ('#SBATCH --share', 'oversubscribe'),
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
pbs_patterns = [
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

host_patterns = {'slurm': slurm1711_patterns, 'pbs': pbs_patterns}

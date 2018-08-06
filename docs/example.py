'''
A possible use of the API
'''
from RESET.InputTypes import *
from RESET import Job, JobType, SlurmRunner
import RESET
from my_app_library import lib

git_repo_url = 'github.com/M4rkD/test'
# could be possible to support some interesting abstractions of the software?
executable = RESET.GitRepo(
    git_repo_url, build='make parallel', exe='bin/parallel')
# alternatively
executable = RESET.GitRepo(
    git_repo_url, build='make parallel', exe='bin/parallel')

# UI stuff for job configuration
interface = {
    'JobName': TextField(),
    'PlotType': OptionField({
        # How to serialise arbitrary objects as options? Option name? Pickle?
        'Line': lib.plot_line,
        'Bar': lib.plot_bar,
        'Pie': lib.plot_pie
    }).set_label('Plot Type'),
    'Velocity': NumericField(10),
    'WorkingDir': Directory(),  # maybe camel case in directory is auto-parsed?
    'localDataFile': File(default=lib.local_data_default),
    'localConfigFile': File(default='path/to/local/file'),
    'config_date': HiddenField(datetime.datetime.now, on=HiddenField.ACCEPT),
    'commitID': GitCommitField(git_repo_url),
    'runner' : SelectRunnable([SlurmRunner,ClusterRunner])
}

# Should config remember the last state or each option?

#defaults setup is: lambda (data, runner): runner.job().config(data)
# Sets up the job object
def setup(data):
    # set up some filesystem behaviour

    job = data['runner'].run()
    job.download([(remote, local), (remote, local)])
    job.download(remote=remote, local=local, interval=1000)   # interval in minutes
    job.upload([(local, remote)])
    job.walltime('12:24:13')                                 # can I do anything clever on AWS here?
    job.num_nodes(1)                                         # used for provisioning on AWS
    job.memory(1)                                            # used for selecting nodes on AWS
    job.bandwidth(1000)

    job.from_template({
        'dimensions': 2,
        'cmd': executable.path(commit=data['commitID'])
    })

    if runner.is(SlurmRunner):
        job.options('time', '23432', 'dependents', 1)
    if runner.is(PBSRunner):
        job.options('time', '23432', 'dependents', 1)
    if runner.is(AWSRunner):
        job.options('time', '23432', 'dependents', 1)

    return job # return job, so that parent can do the running


def plot_results(data):
    x, y = app_lib.import_data(data['localDataFile'])
    plot(x, y)


def do_postprocess(data):
    app_lib.expensive_data_operation(data['localDataFile'], data['mode'])


job_type = JobType(setup, config_interface)

job_type.register_templates({
    SlurmRunner: 'template_path',
    PBSRunner: 'template_path'
})

# add a postprocessing
job_type.add_action('Plot Results', plot_results)

# add a postprocessing action with dependency
plot_action = job_type.add_action('Plot Results', plot_results)
job_type.add_action('Run postprocessing', do_postprocess, depends=plot_action)
job_type.supported_runners(SlurmRunner, ClusterRunner, AWSRunner)

register_job_type('My Job Type', job_type)

if __name__ == '__main__':
    # initialise job_type
    init_app(concurrent=True, api='1.2')

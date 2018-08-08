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
    'JobName':
    TextField(),
    'PlotType':
    OptionField({
        # How to serialise arbitrary objects as options? Option name? Pickle?
        'Line': lib.plot_line,
        'Bar': lib.plot_bar,
        'Pie': lib.plot_pie
    }).set_label('Plot Type'),
    'Velocity':
    NumericField(10),
    'WorkingDir':
    Directory(),  # maybe camel case in directory is auto-parsed?
    'localDataFile':
    File(default=lib.local_data_default),
    'localConfigFile':
    File(default='path/to/local/file'),
    'config_date':
    HiddenField(datetime.datetime.now, on=HiddenField.ACCEPT),
    'commitID':
    GitCommitField(git_repo_url),
    'cluster':
    SelectRunner(
    )  # specifies types of runners...but the ACTUAL list is elsewhere...
}

# Should config remember the last state or each option?


#defaults setup is: lambda (data, runner): runner.job().config(data)
# Sets up the job object
def setup(data):
    # set up some filesystem behaviour

    # data['runner'] is a SPECIFIC RUNNER INSTANCE, which is associated with the cluster we specify...

    run = Run(data['cluster'])  # or Run(HostAdapter(scheduler='slurm'))
    # job interface is FIXED for everyone
    # runner is a string key for data, or an object instance with a run method
    # runner can be an instance of anything on which we can call run with the job for submission

    store = run.id  # use this to "connect" to later if you need to, shouldn't need to...ignore for now

    run.download([('remote', 'local'),
                  ('remote', 'local')])  # <= adds to Runner under job
    run.download(
        remote='remote', local='local', interval=1000)  # interval in minutes
    run.upload([('local', 'remote')])
    run.walltime('12:24:13')  # can I do anything clever on AWS here?
    run.num_nodes(1)  # used for provisioning on AWS
    run.memory(1)  # used for selecting nodes on AWS
    run.bandwidth(1000)

    run.from_template({
        'dimensions': 2,
        'cmd': executable.path(commit=data['commitID'])
    })

    # equivalent....
    run.data['new_data'] = 'new value'
    data['new_data'] = 'new value'

    # additional cluster-specific examples
    if run.slurm:
        run.options('time', '23432', 'dependents', 1)
    if run.pbs:
        run.options('time', '23432', 'dependents', 1)
    if run.aws:
        run.options('time', '23432', 'dependents', 1)

    return run  # return run, so that parent can do the running


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

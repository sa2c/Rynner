'''
A possible use of the API
'''
from RESET.InputTypes import *
from RESET import Job, JobType
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
_interface = {
    JobName:
    TextField(),
    PlotType:
    OptionField({
        # How to serialise arbitrary objects as options? Option name? Pickle?
        'Line': lib.plot_line,
        'Bar': lib.plot_bar,
        'Pie': lib.plot_pie
    }).set_label('Plot Type'),
    Velocity:
    NumericField(10),
    WorkingDir:
    Directory(),  # maybe camel case in directory is auto-parsed?
    localDataFile:
    File(default=lib.local_data_default),
    localConfigFile:
    File(default='path/to/local/file'),
    config_date:
    HiddenField(datetime.datetime.now, on=HiddenField.ACCEPT),
    commitID:
    GitCommitField(git_repo_url),
    mode:
    54  # add some any serialisable, constant data here
}

# Should config remember the last state or each option?

template_files = {'SlurmTypes': 'template_path', 'PBSTypes': 'template_path'}
JobType.register_templates(template_files)


#defaults setup is: lambda (data, runner): runner.job().config(data)
# Sets up the job object
def setup(data, runner):

    job = runner.job()

    # set up some filesystem behaviour
    job.download(local=data['WorkingDir'])
    job.upload(local=data['WorkingDir'], remote=[])
    job.download(
        remote=['/some/remote/path'],
        local=[data['localDataFile']],
        interval=1000)  # follow/sync file

    job.bandwidth(1000)

    jobcard_variables = {
        'dimensions': 2,
        'cmd': executable.path(commit=data['commitID'])
    }

    job.config(jobcard_variables)

    return job


def plot_results(data):
    x, y = app_lib.import_data(data['localDataFile'])
    plot(x, y)


def do_postprocess(data):
    app_lib.expensive_data_operation(data['localDataFile'], data['mode'])


job_type = JobType(
    setup, config_interface,
    executable)  # executable is optional? can be set on Job object

# add a postprocessing
job_type.add_action('Plot Results', plot_results)

# add a postprocessing action with dependency
plot_action = job_type.add_action('Plot Results', plot_results)
job_type.add_action('Run postprocessing', do_postprocess, depends=plot_action)

register_job_type('My Job Type', job_type)

if __name__ == '__main__':
    # initialise job_type
    init_app(concurrent=True, api='1.2')

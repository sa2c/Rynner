-> Application Main Window UI
-> UI is indeed, and calls actions on another object (controller?)

Views =>
GUI job list window => StandardModel (for current jobs) => easy-peasy
GUI job creation dialog => JobModel (i.e. wrapper for config containing logic for validations etc)

JobModel -> wrapper for job type??? Are there reasons for job model to change without jobtype

class JobType:
    def __init__(self, setup_function, config_interface, executable=None):
        self.job_setup = setup_function
        self.config = config_interface
        self.actions = {}
        if self.executable is not None:
            # what makes sense to do here?

        # maintain dict of all instantiated job types in module variable registered_job_types??
        # or explicitly register jobs?
        types.append(self)

    def add_action(self, label, func, auto=False, depends=None):
        self.actions[label] = func


class Job:
    def __init__(self, name):
        self.name = name
        self.jc_opts = JobCardOptions()
        # set some defaults job options from cluster default config

    def transfer_file(self, name):
        # register a file transfer handler? a callable that is called at specific times (e.g. on a timer)
        # this has to be serialisable!!!!

    def set_options(self, **kwargs):
        # add an option to option list
        self.jc_opts = kwargs
        # not a big fan of this...

    # same pattern for all jobcard options...but what is the pattern?

    def set_job_template(self, template, variables):
        # need to make sure that later additions/settings do not conflict - always rewrite self.jobcard
        # not convinced by this...?
        self.jobcard = parser(template, variables)

    def get_jobcard(self, option_map):
        # returns the jobfile for a given cluster
        options_string = jc_opts.option_map(self.jobcard_options)
        # quite tightly couples with cluster here....!!
        return options_string + self.jobcard

class SerialJob(Job):
    # subclasses Job with some default behaviour - think about this...
    def from_exec(self, exec):
        self.jobcard = ...

class ClusterList(List):
    self.clusters = [...]

    def add(self, datafile):
        self.clusters.append(Cluster.from_datafile(datafile))

class Cluster:
    def __init__(scheduler_adapter, options, option_map):
        # reads the cluster data file(s) and configures itself accordingly
        self.data = data
        self.schedule_adapter = scheduler_adapter
        # data file
        # do we need a job here

    def get_options(options):
        options = {**self.option_defaults, **options}

        for option in options:
            str += self.option_map[option]

def initalize_type(job_type):
    # this creates job_type in some global register
    # what happens with duplicate labels

-> contains a pointer 
-> Contain config and logic
JobType.get_data()

…

 view (i.e. generate new job), has a job-specific view

Main GUI generates jobs…

-> Application Main Window UI
-> UI is indeed, and calls actions on another object (controller?)

Views =>
GUI job list window => StandardModel (for current jobs) => easy-peasy
GUI job creation dialog => JobModel (i.e. wrapper for config containing logic for validations etc)

JobModel -> wrapper for job type??? Are there reasons for job model to change without jobtype


class JobType:
    types = []

    def __init__(self, setup_function, config_run_create_view, executable=None):
        self.job_setup = setup_function
        self.config = config_run_create_view
        self.actions = {}
        if self.executable is not None:
            # what makes sense to do here?

        # maintain dict of all instantiated job types in module variable registered_job_types??
        # or explicitly register jobs?
        types.append(self)

    def add_action(self, string, func):
        self.actions['string'] = func

class Job:
    def __init__(self, name):
        self.name = name
        # set some defaults job options from cluster default config

    def transfer_file(self, name):
        # register a file transfer handler

    # same pattern applies to all jobcard options
    def set_number_nodes(self, 10):
        # add an option to option list
        self.cluster_options['number_of_nodes', 10]
        # not a big fan of this...

    def jobfile(self, cluster):
        # returns the jobfile for a given cluster
        options_string = cluster.options(self.cluster_options)
        # quite tightly couples with cluster here....!!

class SerialJob(Job):
    # subclasses Job with some default behaviour

class SlurmCluster(Cluster):
    def __init__(data_file):
        # reads the cluster data file and configures itself accordingly
        # adds itself to package variable
        # do we need a job here



def initalize_type(job_type):
    # this creates job_type in some global register
    # what happens with duplicate labels

-> contains a pointer 
-> Contain config and logic
JobType.get_data()

…

 view (i.e. generate new job), has a job-specific view

Main GUI generates jobs….



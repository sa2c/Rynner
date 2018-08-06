class Runner:
    def __init__(self, logic):
        pass

    def type(self, classname):
        '''Convenience method for determining the type of an object'''
        return isinstance(self, classname)

    def run(self, options, config, downloads, uploads):
        pass
        # actually


##### HOW DOES THE DATA GET INTO HERE???

#        jobID = self.runner_logic.reserve()  # <= instantiated with runner_logic
#
#        # create base dir - different ordering => manages downloads, also manages "remembering" stuff and sync behaviour
#        # needs to be called later to "finish" the job
#        manager = JobManager(jobID, uploads, downloads)
#
#        # store relevant data for later
#        self.database.store(jobID, options, config, uploads, downloads)
#
#        for option, value in options.items:
#            # options are just passed on to the runner_logic => runner_logic + Run are VERY coupled, runner_logic and runner are not
#            self.runner_logic.set_option(option, value)
#
#        self.runner_logic.start(jobID)
#
#        return jobID

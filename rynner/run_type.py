from rynner.run import Run


class RunAction:
    def __init__(self, label, function):
        self.label = label
        self.function = function


class RunType:
    default_params = [("id", "Job ID"), ("name", "Job Name")]

    def __init__(self, domain, name, interface, runner=None, params=None):
        self.name = name
        self.domain = domain
        self.interface = interface
        self.actions = []
        self.runner = runner

        # set params to input, if specified otherwise set to default params
        if params is None:
            self.params = self.default_params
        else:
            self.params = params

    def create(self):
        # display configuration window
        accepted = self.interface.show()

        if accepted and len(self.interface.invalid()) == 0:
            data = self.interface.data()

            if self.runner is None:
                run = Run(**data)
            else:
                self.runner(data)

    def add_action(self, label, function):
        action = RunAction(label, function)
        self.actions.append(action)
        return action

    def list_jobs(self, hosts):
        jobs = []
        for host in hosts:
            for job in host.jobs(self.domain):
                jobs.append(job)
        return jobs


class RunTypeCollection:
    '''
    This class allows a collection of RunType objects to be used with the same API as a single object.
    '''

    def __init__(self, name, run_types, params=None):
        self.name = name
        self.run_types = run_types
        if params is None:
            self.params = RunType.default_params
        else:
            self.params = params

        self.actions = []

    def list_jobs(self, hosts):
        jobs = [
            job for host in hosts for run_type in self.run_types
            for job in host.jobs(run_type.domain)
        ]
        return jobs

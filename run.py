class Run:
    '''mostly holds the context and delegates settings and behaviour to either runner or runner.behaviour, passing the context.'''

    # TODO support additional options for runners (via a call to behaviour?)

    def __init__(self, data, runner=None, options={}, template=None):
        self.__downloads = []
        self.__uploads = []
        self.runner = runner
        self.template = template
        self.data = data

        if self.runner is None:
            raise RunnerNotSpecifiedException

        self.__behaviour_context = runner.behaviour.get_context()
        self.__runner_context = runner.get_context()

        for key, value in options.items():
            method = getattr(self, key)
            method(value)

    ########################### File Upload/Download lists ############################

    def download(self, remote, local, **kwargs):
        self.runner.download(self.__runner_context, remote, local, **kwargs)

    def upload(self, local, remote, **kwargs):
        self.runner.upload(self.__runner_context, local, remote, **kwargs)

    ########################## Runner Option Setters ##########################

    def bandwidth(self, bandwidth):
        # TODO - this is passed to runner, not behaviour
        self.runner.bandwidth(self.__runner_context, bandwidth)

    ######################## Behaviour Option Setters #########################

    def walltime(self, seconds=0, minutes=0, hours=0):
        self.runner.behaviour.walltime(
            self.__behaviour_context, seconds + minutes * 60 + hours * 60 * 60)

    def memory(self, mb=0, kb=0, gb=0):
        self.runner.behaviour.memory(self.__behaviour_context,
                                     kb + mb * 1024 + gb * 1024**2)

    def num_cores(self, num_cores):
        self.runner.behaviour.num_cores(self.__behaviour_context, num_cores)

    def script(self, script):
        self.runner.behaviour.script(self.__behaviour_context, script)

    ############################# Utility Methods #############################

    def from_template(self, args, template=None):
        if template is None:
            template = self.template
        self.script(template.render(args))

    ################################# Actions #################################

    def run(self):
        return self.runner.run(self.__runner_context, self.__behaviour_context)


class InvalidDownloadOptionException(ValueError):
    pass


class InvalidUploadOptionException(ValueError):
    pass


class RunnerNotSpecifiedException(AttributeError):
    pass

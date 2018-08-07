class Run:

    # TODO support additional options for runners (via a call to behaviour?)

    __valid_download_arguments = ['interval']
    __valid_upload_arguments = []

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
        self.__add_to_file_list(local, remote, self.__downloads,
                                self.__valid_download_arguments,
                                InvalidDownloadOptionException, **kwargs)

    def upload(self, local, remote, **kwargs):
        self.__add_to_file_list(local, remote, self.__uploads,
                                self.__valid_upload_arguments,
                                InvalidUploadOptionException, **kwargs)

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

    def num_nodes(self, num_nodes):
        self.runner.behaviour.num_nodes(self.__behaviour_context, num_nodes)

    def script(self, script):
        self.runner.behaviour.script(self.__behaviour_context, script)

    ############################# Utility Methods #############################

    def from_template(self, args, template=None):
        if template is None:
            template = self.template
        self.script(template.render(args))

    ############################# Private methods #############################

    def __add_to_file_list(self, first, second, filelist, valid_args,
                           exception, **kwargs):
        if type(first) is str and type(second) is str:
            first = [first]
            second = [second]

        downloads = list(zip(first, second))

        # raise an exception if not a valid keyword
        for key in kwargs.keys():
            if not key in valid_args:
                raise exception()

        # append kwargs as dict to each relevant file
        if len(kwargs) > 0:
            downloads = [(*d, kwargs) for d in downloads]

        # add downloads to downloads list
        filelist.extend(downloads)

    ################################# Actions #################################

    def run(self):
        return self.runner.run(self.__runner_context, self.__behaviour_context)

    ############################# Property Lists ##############################

    @property
    def downloads(self):
        return self.__downloads

    @property
    def uploads(self):
        return self.__uploads


class InvalidDownloadOptionException(ValueError):
    pass


class InvalidUploadOptionException(ValueError):
    pass


class RunnerNotSpecifiedException(AttributeError):
    pass

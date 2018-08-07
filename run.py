class Run:
    '''mostly holds the context and delegates settings and behaviour to either host or host.behaviour, passing the context.'''

    # TODO support additional options for hosts (via a call to behaviour?)

    def __init__(self, data, host=None, options={}, template=None):
        self.__downloads = []
        self.__uploads = []
        self.host = host
        self.template = template
        self.data = data

        if self.host is None:
            raise HostNotSpecifiedException

        self.__behaviour_context = host.behaviour.get_context()
        self.__host_context = host.get_context()

        for key, value in options.items():
            method = getattr(self, key)
            method(value)

    ########################### File Upload/Download lists ############################

    def download(self, remote, local, **kwargs):
        self.host.download(self.__host_context, remote, local, **kwargs)

    def upload(self, local, remote, **kwargs):
        self.host.upload(self.__host_context, local, remote, **kwargs)

    ########################## Host Option Setters ##########################

    def bandwidth(self, bandwidth):
        # TODO - this is passed to host, not behaviour
        self.host.bandwidth(self.__host_context, bandwidth)

    ######################## Behaviour Option Setters #########################

    def walltime(self, seconds=0, minutes=0, hours=0):
        self.host.behaviour.walltime(self.__behaviour_context,
                                     seconds + minutes * 60 + hours * 60 * 60)

    def memory(self, mb=0, kb=0, gb=0):
        self.host.behaviour.memory(self.__behaviour_context,
                                   kb + mb * 1024 + gb * 1024**2)

    def num_cores(self, num_cores):
        self.host.behaviour.num_cores(self.__behaviour_context, num_cores)

    def script(self, script):
        self.host.behaviour.script(self.__behaviour_context, script)

    ############################# Utility Methods #############################

    def from_template(self, args, template=None):
        if template is None:
            template = self.template
        self.script(template.render(args))

    ################################# Actions #################################

    def run(self):
        return self.host.run(self.__host_context, self.__behaviour_context)


class InvalidDownloadOptionException(ValueError):
    pass


class InvalidUploadOptionException(ValueError):
    pass


class HostNotSpecifiedException(AttributeError):
    pass

from restricted_dict import RestrictedDict


class InvalidDownloadOptionException(ValueError):
    pass


class InvalidUploadOptionException(ValueError):
    pass


class RunnerNotSpecifiedException(AttributeError):
    pass


class Run:
    __valid_download_arguments = ['interval']
    __valid_upload_arguments = []
    __allowed_options = {'walltime', 'jobcard'}

    def __init__(self, options=None, runner=None, template=None):
        '''options should be None or an object of type dict, these options are intended to be used to configure the runner'''
        self.__downloads = []
        self.__uploads = []
        self.options = RestrictedDict(options, allowed=self.__allowed_options)
        self.runner = runner
        self.template = template

    ########################### File Upload/Download lists ############################

    def download(self, remote, local, **kwargs):
        self.__add_to_file_list(local, remote, self.__downloads,
                                self.__valid_download_arguments,
                                InvalidDownloadOptionException, **kwargs)

    def upload(self, local, remote, **kwargs):
        self.__add_to_file_list(local, remote, self.__uploads,
                                self.__valid_upload_arguments,
                                InvalidUploadOptionException, **kwargs)

    ############################# Option Setters ##############################

    def walltime(self, seconds=0, minutes=0, hours=0):
        self.options['walltime'] = seconds + minutes * 60 + hours * 60 * 60

    def from_template(self, args):
        self.options['jobcard'] = self.template.parse(args)

    def jobcard(self, string):
        self.options['jobcard'] = self.jobcard

    ############################# Private methods #############################

    def __get_option(self, option_name):
        return self.options[option_name]

    def __add_to_file_list(self, first, second, filelist, valid_args,
                           exception, **kwargs):
        '''add a download, with a gien set of options'''
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
        if self.runner is None:
            raise RunnerNotSpecifiedException
        self.runner.run(self.options, self.downloads, self.uploads)

    ############################# Property Lists ##############################

    @property
    def downloads(self):
        return self.__downloads

    @property
    def uploads(self):
        return self.__uploads

class InvalidDownloadOptionException(ValueError):
    pass


class InvalidUploadOptionException(ValueError):
    pass


class InvalidOptionException(ValueError):
    pass


class Run:
    __valid_download_arguments = ['interval']
    __valid_upload_arguments = []
    __valid_options = ['walltime', 'num_nodes']

    def __init__(self, options=None):
        '''options should be None or an object of type dict, these options are intended to be used to configure the runner'''
        self.__downloads = []
        self.__uploads = []
        self.options = {}

        # validate and set options
        if options is not None:
            if not isinstance(options, dict):
                raise TypeError('options argument should be a dict')
            else:
                for option, value in options.items():
                    self.__add_option(option, value)

    ############################### Set Methods ###############################

    def walltime(self, seconds, minutes=0, hours=0):
        self.__add_option('walltime', seconds)

    ########################### File Upload/Download lists ############################

    def download(self, remote, local, **kwargs):
        self.__add_to_file_list(local, remote, self.__downloads,
                                self.__valid_download_arguments,
                                InvalidDownloadOptionException, **kwargs)

    def upload(self, local, remote, **kwargs):
        self.__add_to_file_list(local, remote, self.__uploads,
                                self.__valid_upload_arguments,
                                InvalidUploadOptionException, **kwargs)

    ############################# Private methods #############################

    def __add_option(self, option_name, value):
        self.options[option_name] = value
        if option_name not in self.__valid_options:
            m = f'{option_name} is not a valid option'
            raise InvalidOptionException(m)

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

    ############################# Property Lists ##############################

    @property
    def downloads(self):
        return self.__downloads

    @property
    def uploads(self):
        return self.__uploads
